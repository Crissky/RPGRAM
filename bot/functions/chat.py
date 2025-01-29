from datetime import timedelta
from random import choice, randint
from time import sleep
from typing import Any, Callable, List, Union
from bson import ObjectId
from telegram import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    Update
)

from telegram.constants import ChatAction, ChatType, ParseMode
from telegram.error import BadRequest, Forbidden, RetryAfter, TimedOut
from telegram.ext import ContextTypes, ConversationHandler

from bot.constants.close import CALLBACK_CLOSE
from bot.constants.job import BASE_JOB_KWARGS
from bot.functions.general import get_attribute_group_or_player
from bot.functions.job import job_exists, remove_job_by_name
from bot.functions.player import get_player_attribute_by_id
from function.text import escape_basic_markdown_v2
from rpgram.boosters.equipment import Equipment
from rpgram.consumables.consumable import Consumable
from rpgram.consumables.other import GemstoneConsumable, TrocadoPouchConsumable
from rpgram.enums import EmojiEnum, FaceEmojiEnum
from rpgram.item import Item
from random import randint


HOURS_DELETE_MESSAGE_FROM_CONTEXT = 4
CHAT_TYPE_GROUPS = (ChatType.GROUP, ChatType.SUPERGROUP)
MIN_AUTODELETE_TIME = timedelta(minutes=15)
HALF_AUTODELETE_TIME = timedelta(minutes=30)


# TEXTS
REPLY_MARKUP_DEFAULT = 'DEFAULT'
LEFT_CLOSE_BUTTON_TEXT = f'{EmojiEnum.CLOSE.value}Fechar'
RIGHT_CLOSE_BUTTON_TEXT = f'Fechar{EmojiEnum.CLOSE.value}'
REFRESH_BUTTON_TEXT = f'{EmojiEnum.REFRESH.value}Atualizar'
DETAIL_BUTTON_TEXT = f'{EmojiEnum.DETAIL.value}Detalhar'


CALLBACK_KEY_LIST = [
    'act',
    'buy',
    'command',
    'drop',
    'hand',
    'identify',
    'equip_info',
    'item',
    'item_id',
    'page',
    'retry_state',
    'sell',
    'sell_item',
    'sell_item_id',
    'sell_page',
    'sort',
    'use',
    '_id',
    'user_id',
    'target_id',
    'enemy_id',
    'item_quest_job_name',
    '_all',
    'classe_name',
    'classe_index',
    'race_name',
    'row',
    'col',
    'skill',
    'skill_back',
    'list_use_skill',
    'list_learn_skill',
    'list_upgrade_skill',
    'check_use_skill',
    'check_learn_skill',
    'check_upgrade_skill',
    'use_skill',
    'learn_skill',
    'action_use_skill',
    'action_learn_skill',
    'action_upgrade_skill',
    'action_use_target',
    'help_skill',
    'list_all_skill',
    'list_classe_skill',
    'list_way_skill',
    'check_way_skill',
    'way_name',
]
VERBOSE_ARGS = ['verbose', 'v']
REPLY_CHAT_ACTION_KWARGS = dict(action=ChatAction.TYPING)


async def send_private_message(
    function_caller: str,
    context: ContextTypes.DEFAULT_TYPE,
    text: str,
    user_id: int,
    chat_id: int = None,
    markdown: bool = False,
    reply_markup: InlineKeyboardMarkup = REPLY_MARKUP_DEFAULT,
    close_by_owner: bool = True,
    auto_delete_message: Union[bool, int, timedelta] = True,
):
    ''' Tenta enviar mensagem privada, caso não consiga pelo erro "Forbidden" 
    envia mensagem para o grupo marcando o nome do jogador.
    '''

    markdown = ParseMode.MARKDOWN_V2 if markdown else None
    owner_id = user_id if close_by_owner is True else None
    reply_markup = (
        reply_markup
        if reply_markup != REPLY_MARKUP_DEFAULT
        else get_close_keyboard(user_id=owner_id)
    )

    try:
        silent = get_player_attribute_by_id(user_id, 'silent')
        call_telegram_kwargs = dict(
            chat_id=user_id,
            text=text,
            parse_mode=markdown,
            disable_notification=silent,
            reply_markup=reply_markup,
        )

        await call_telegram_message_function(
            function_caller='SEND_PRIVATE_MESSAGE()',
            function=context.bot.send_message,
            context=context,
            need_response=False,
            auto_delete_message=auto_delete_message,
            **call_telegram_kwargs
        )
    except Forbidden as error:
        if isinstance(chat_id, int):
            print(
                f'SEND_PRIVATE_MESSAGE(): Usuário {user_id} não pode '
                f'receber mensagens privadas. '
                f'Enviando mensagem para o grupo de ID {chat_id}.\n'
                f'Function Caller: {function_caller}\n'
                f'Message: {text}\n'
                f'(ERROR: {error})'
            )
            silent = get_attribute_group_or_player(chat_id, 'silent')
            member = await context.bot.get_chat_member(
                chat_id=chat_id,
                user_id=user_id
            )
            user_name = escape_basic_markdown_v2(member.user.name)
            text = f'{user_name}\n{text}'
            send_text_kwargs = dict(
                chat_id=chat_id,
                text=text,
                parse_mode=markdown,
                disable_notification=silent,
                reply_markup=reply_markup,
            )
            await call_telegram_message_function(
                function_caller='SEND_PRIVATE_MESSAGE()',
                function=context.bot.send_message,
                context=context,
                need_response=False,
                auto_delete_message=auto_delete_message,
                **send_text_kwargs
            )
        else:
            print(
                f'SEND_PRIVATE_MESSAGE(): Usuário {user_id} não pode '
                f'receber mensagens privadas e um "chat_id" não foi passado. '
                f'Ele precisa iniciar uma conversa com o bot.\n'
                f'Function Caller: {function_caller}\n'
                f'(ERROR: {error})'
            )


async def send_alert_or_message(
    function_caller: str,
    context: ContextTypes.DEFAULT_TYPE,
    query: CallbackQuery,
    text: str,
    user_id: int,
    chat_id: int = None,
    markdown: bool = False,
    reply_markup: InlineKeyboardMarkup = REPLY_MARKUP_DEFAULT,
    show_alert: bool = False,
):
    '''Envia um alert se uma query for passado, caso contrário, enviará 
    uma mensagem privada.
    '''

    if query:
        return await answer(query=query, text=text, show_alert=show_alert)
    else:
        return await send_private_message(
            function_caller=function_caller,
            context=context,
            text=text,
            user_id=user_id,
            chat_id=chat_id,
            markdown=markdown,
            reply_markup=reply_markup,
            close_by_owner=False,
        )


async def forward_message(
    function_caller: str,
    user_ids: Union[int, List[int]],
    message: Message = None,
    context: ContextTypes.DEFAULT_TYPE = None,
    chat_id: int = None,
    message_id: int = None,
    silent: bool = None,
):
    '''Encaminha uma mensagem usando um Message ou um ContextTypes
    '''
    if context and not chat_id:
        raise ValueError('chat_id é necessário quando passado um context.')
    if context and not message_id:
        raise ValueError('message_id é necessário quando passado um context.')
    if not message and not context:
        raise ValueError('message ou context deve ser passado.')

    message_chat_id = message.chat_id if hasattr(message, 'chat_id') else None
    if isinstance(user_ids, int):
        user_ids = [user_ids]
    user_ids = list(set(user_ids))

    for user_id in user_ids:
        if silent is None:
            user_silent = get_player_attribute_by_id(user_id, 'silent')
        else:
            user_silent = silent
        if message_chat_id == user_id:
            continue  # Evita encaminhamento para o próprio chat privado
        try:
            if hasattr(message, 'forward'):
                call_telegram_kwargs = dict(
                    chat_id=user_id,
                    disable_notification=user_silent
                )

                await call_telegram_message_function(
                    function_caller='FORWARD_MESSAGE()',
                    function=message.forward,
                    context=context,
                    need_response=False,
                    **call_telegram_kwargs
                )
            elif context:
                call_telegram_kwargs = dict(
                    chat_id=user_id,
                    from_chat_id=chat_id,
                    message_id=message_id,
                    disable_notification=user_silent
                )

                await call_telegram_message_function(
                    function_caller='FORWARD_MESSAGE()',
                    function=context.bot.forward_message,
                    context=context,
                    need_response=False,
                    **call_telegram_kwargs
                )
            else:
                print(
                    f'FORWARD_MESSAGE(): Não foi possível encaminhar a '
                    f'mensagem de {message_chat_id} para {user_id}.\n'
                    f'Function Caller: {function_caller}\n'
                    f'message: {type(message)}\n'
                    f'context: {type(context)}\n'
                )
        except Exception as error:
            print(f'{function_caller}: {error}')


async def edit_message_text(
    function_caller: str,
    new_text: str,
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    message_id: int,
    user_id: int = None,
    need_response: bool = True,
    markdown: bool = False,
    reply_markup: InlineKeyboardMarkup = REPLY_MARKUP_DEFAULT,
    close_by_owner: bool = True,
) -> Union[Message, bool]:
    '''Edita uma mensagem usando um Message ou um ContextTypes.
    '''

    markdown = ParseMode.MARKDOWN_V2 if markdown is True else None
    owner_id = user_id if close_by_owner is True else None
    reply_markup = (
        reply_markup
        if reply_markup != REPLY_MARKUP_DEFAULT
        else get_close_keyboard(user_id=owner_id)
    )
    edit_text_kwargs = dict(
        text=new_text,
        chat_id=chat_id,
        message_id=message_id,
        parse_mode=markdown,
        reply_markup=reply_markup,
    )
    response = await call_telegram_message_function(
        function_caller=f'{function_caller} -> EDIT_MESSAGE_EDIT()',
        function=context.bot.edit_message_text,
        context=context,
        need_response=need_response,
        **edit_text_kwargs
    )

    return response


async def edit_message_text_and_forward(
    function_caller: str,
    new_text: str,
    user_ids: Union[int, List[int]],
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    message_id: int,
    need_response: bool = True,
    markdown: bool = False,
    reply_markup: InlineKeyboardMarkup = REPLY_MARKUP_DEFAULT,
    close_by_owner: bool = False,
) -> Union[Message, bool]:
    '''Edita uma mensagem usando um Message ou um ContextTypes e encaminha 
    a mesma para o usuário.
    '''

    if isinstance(user_ids, int):
        user_ids = [user_ids]

    owner_id = user_ids[0] if close_by_owner is True else None
    both_function_caller = (
        f'{function_caller} and EDIT_MESSAGE_TEXT_AND_FORWARD()'
    )

    response = await edit_message_text(
        function_caller=both_function_caller,
        new_text=new_text,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        user_id=owner_id,
        need_response=need_response,
        markdown=markdown,
        reply_markup=reply_markup
    )

    await forward_message(
        function_caller=both_function_caller,
        user_ids=user_ids,
        message=response
    )

    return response


async def reply_text(
    function_caller: str,
    text: str,
    context: ContextTypes.DEFAULT_TYPE,
    user_id: int = None,
    update: Update = None,
    chat_id: int = None,
    message_id: int = None,
    need_response: bool = True,
    allow_sending_without_reply=True,
    markdown: bool = False,
    reply_markup: InlineKeyboardMarkup = REPLY_MARKUP_DEFAULT,
    silent: bool = None,
    close_by_owner: bool = True,
    auto_delete_message: Union[bool, int, timedelta] = True,
) -> Message:
    '''Responde uma mensagem.

    Se update e context forem passados simultaneamente, a mensagem será 
    respondida usando update.effective_message.reply_text
    '''

    if update is None:
        if context is None:
            raise ValueError('update ou context deve ser passado.')
        if not isinstance(chat_id, int):
            raise ValueError(
                'Quando usar context, chat_id deve ser um inteiro.'
            )
        if not isinstance(message_id, int):
            raise ValueError(
                'Quando usar context, message_id deve ser um inteiro.'
            )

    if update and user_id is None:
        user_id = update.effective_user.id

    if silent is None:
        if isinstance(chat_id, int):
            silent = get_attribute_group_or_player(chat_id, 'silent')
        elif isinstance(user_id, int):
            silent = get_player_attribute_by_id(user_id, 'silent')

    markdown = ParseMode.MARKDOWN_V2 if markdown else None
    owner_id = user_id if close_by_owner is True else None
    reply_markup = (
        reply_markup
        if reply_markup != REPLY_MARKUP_DEFAULT
        else get_close_keyboard(user_id=owner_id)
    )
    reply_text_kwargs = dict(
        text=text,
        parse_mode=markdown,
        disable_notification=silent,
        reply_markup=reply_markup,
        allow_sending_without_reply=allow_sending_without_reply,
    )

    if update:
        reply_text_kwargs['function'] = update.effective_message.reply_text
    elif context:
        reply_text_kwargs['function'] = context.bot.send_message
        reply_text_kwargs['chat_id'] = chat_id
        reply_text_kwargs['reply_to_message_id'] = message_id

    response = await call_telegram_message_function(
        function_caller=function_caller,
        context=context,
        need_response=need_response,
        auto_delete_message=auto_delete_message,
        **reply_text_kwargs
    )

    return response


async def reply_text_and_forward(
    function_caller: str,
    text: str,
    context: ContextTypes.DEFAULT_TYPE,
    user_ids: Union[int, List[int]],
    update: Update = None,
    chat_id: int = None,
    message_id: int = None,
    need_response: bool = True,
    allow_sending_without_reply=True,
    markdown: bool = False,
    reply_markup: InlineKeyboardMarkup = REPLY_MARKUP_DEFAULT,
    close_by_owner: bool = False,
    silent_reply: bool = None,
    silent_forward: bool = None,
) -> Message:
    '''Responde uma mensagem e a encaminha para o usuário.
    '''

    if isinstance(user_ids, int):
        user_ids = [user_ids]

    owner_id = user_ids[0] if close_by_owner is True else None
    both_function_caller = f'{function_caller} and REPLY_TEXT_AND_FORWARD()'

    response = await reply_text(
        function_caller=both_function_caller,
        text=text,
        user_id=owner_id,
        update=update,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        need_response=need_response,
        allow_sending_without_reply=allow_sending_without_reply,
        markdown=markdown,
        reply_markup=reply_markup,
        silent=silent_reply,
    )

    await forward_message(
        function_caller=both_function_caller,
        user_ids=user_ids,
        message=response,
        silent=silent_forward,
    )

    return response


# QUERY FUNCTIONS
async def delete_message_from_context(
    function_caller: str,
    context: ContextTypes.DEFAULT_TYPE,
    message_id: int,
):
    '''Deleta a mensagem usando context, 
    caso ocorra um erro BadRequest (Mensagem não encontrada), ignora ação.
    '''

    chat_id = context._chat_id
    try:
        print('CONTEXT_DELETE_MESSAGE() TRYING DELETE_MESSAGE')
        delete_message_kwargs = dict(
            chat_id=chat_id,
            message_id=message_id
        )
        await call_telegram_message_function(
            function_caller=function_caller,
            function=context.bot.delete_message,
            context=context,
            need_response=False,
            **delete_message_kwargs
        )
    except BadRequest as e:
        print('CONTEXT_DELETE_MESSAGE() BADREQUEST EXCEPT')
        if 'Message to delete not found' in e.message:
            print(f'\tError Message: "{e.message}"')
        elif "Message can't be deleted" in e.message:
            print(f'\tError Message: "{e.message}" (Sem Permissão)')
        else:
            raise e


async def call_telegram_message_function(
    function_caller: str,
    function: Callable,
    context: ContextTypes.DEFAULT_TYPE,
    need_response: bool = True,
    skip_retry: bool = False,
    auto_delete_message: Union[bool, int, timedelta] = True,
    **kwargs
) -> Union[Any, Message]:
    '''Função que chama qualquer função de mensagem do telegram. 
    Caso ocorra um erro do tipo RetryAfter ou TimedOut, a função agurdará 
    alguns segundos tentará novamente com um número máximo de 3 tentativas. 
    Caso a função retorne um objeto do tipo Message, a mensagem será excluída 
    em "HOURS_DELETE_MESSAGE_FROM_CONTEXT" horas.

    Se need_response for True, a função aguardará para realizar uma nova 
    tentativa, caso contrário, a função será agendada em um job para ser 
    executada posteriormente.

    Se skip_retry for True, a função não tentará novamente e nem agendará uma 
    nova tentativa.

    Se auto_delete_message for igual a False, a exclusão automática da 
    mensagem será ignorada. Caso seja igual a True, a mensagem será excluída 
    em "HOURS_DELETE_MESSAGE_FROM_CONTEXT" horas. 
    Mas se for um valor inteiro positivo, a mensagem será excluída em uma 
    quantidade de horas igual ao valor passado.
    E se for um timedelta, a mensagem será excluída de acordo com o tempo 
    passado no timedelta.
    '''

    print(f'{function_caller}->CALL_TELEGRAM_MESSAGE_FUNCTION()')
    job_call_telegram_kwargs = dict(
        function_caller=function_caller,
        function=function,
        context=context,
        **kwargs
    )
    response = None
    is_error = True
    catched_error = None
    for i in range(3):
        try:
            response = await function(**kwargs)
            is_error = False
            break
        except (RetryAfter, TimedOut) as error:
            catched_error = error
            if skip_retry is True:
                break

            if isinstance(error, RetryAfter):
                sleep_time = error.retry_after + randint(1, 3)
            elif isinstance(error, TimedOut):
                sleep_time = 5

            error_name = error.__class__.__name__
            if need_response is False:
                print(
                    f'{error_name}{i}({sleep_time}): '
                    f'creating JOB "{function.__name__}" '
                )
                job_name = (
                    f'{function_caller}->'
                    f'CALL_TELEGRAM_MESSAGE_FUNCTION->'
                    f'JOB_CALL_TELEGRAM-{ObjectId()}'
                )
                context.job_queue.run_once(
                    callback=job_call_telegram,
                    when=timedelta(seconds=sleep_time),
                    data=job_call_telegram_kwargs,
                    name=job_name,
                    job_kwargs=BASE_JOB_KWARGS,
                )
                return ConversationHandler.END

            print(
                f'{error_name}{i}: RETRYING activate "{function.__name__}" '
                f'from {function_caller} in {sleep_time} seconds.'
            )
            sleep(sleep_time)
            continue

    if is_error is True:
        print(f'ERROR: {function_caller}')
        if catched_error:
            raise catched_error
        raise Exception(f'Error in {function_caller}')

    if (
        isinstance(response, Message)
        and is_chat_group(message=response)
        and auto_delete_message
    ):
        complete_function_caller = (
            f'{function_caller}->'
            f'CALL_TELEGRAM_MESSAGE_FUNCTION()'
        )
        create_job_delete_message_from_context(
            function_caller=complete_function_caller,
            context=context,
            message=response,
            when=auto_delete_message
        )

    return response


def create_job_delete_message_from_context(
    function_caller: str,
    context: ContextTypes.DEFAULT_TYPE,
    message: Message,
    when: Union[bool, int, timedelta] = True,
):
    '''Cria o job que excluirá a mensagem após o tempo passado em `when`.
    '''

    chat_id = message.chat_id
    message_id = message.message_id
    job_name = get_job_delete_message_from_context_name(
        chat_id=chat_id,
        message_id=message_id
    )
    data = {
        'message_id': message_id,
        'function_caller': function_caller,
    }
    when = get_hours_delete_message_from_context(when)
    print(
        f'Mensagem de ID {message_id} do chat de ID {chat_id} '
        f'será excluida em {when} horas.'
    )
    if not job_exists(context=context, job_name=job_name):
        context.job_queue.run_once(
            callback=job_delete_message_from_context,
            when=when,
            data=data,
            name=job_name,
            chat_id=chat_id,
            job_kwargs=BASE_JOB_KWARGS,
        )
    else:
        print(f'Job "{job_name}" já existe.')


def remove_job_delete_message_from_context(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    message_id: int
):
    job_name = get_job_delete_message_from_context_name(
        chat_id=chat_id,
        message_id=message_id
    )
    remove_job_by_name(context=context, job_name=job_name)


async def job_call_telegram(context: ContextTypes.DEFAULT_TYPE):
    '''Agenda uma função call_telegram_message_function caso ocorra um erro 
    do tipo RetryAfter, TimedOut e o need_response seja False
    '''

    print('JOB_CALL_TELEGRAM()')
    job = context.job
    call_telegram_kwargs = job.data
    call_telegram_kwargs['function_caller'] += ' and JOB_CALL_TELEGRAM()'
    print(call_telegram_kwargs['function_caller'])

    await call_telegram_message_function(**call_telegram_kwargs)


async def job_delete_message_from_context(context: ContextTypes.DEFAULT_TYPE):
    '''Job que exclui a mensagem após um tempo pré determinado.
    '''

    print('JOB_DELETE_MESSAGE_FROM_CONTEXT()')
    job = context.job
    data = job.data
    message_id = data['message_id']
    function_caller = data['function_caller']

    await delete_message_from_context(
        function_caller=function_caller,
        context=context,
        message_id=message_id
    )


# QUERY FUNCTIONS
async def delete_message(
    function_caller: str,
    context: ContextTypes.DEFAULT_TYPE,
    query: CallbackQuery,
):
    '''Deleta a mensagem usando query, 
    caso ocorra um erro BadRequest tenta deletar a mensagem usando o context.
    '''

    chat_id = query.message.chat_id
    message_id = query.message.message_id
    try:
        print('DELETE_MESSAGE() TRYING QUERY.DELETE_MESSAGE')
        await call_telegram_message_function(
            function_caller=function_caller + ' and DELETE_MESSAGE()',
            function=query.delete_message,
            context=context,
            need_response=False,
        )
    except BadRequest as e:
        print('DELETE_MESSAGE() BADREQUEST EXCEPT')
        if 'Query is too old' in e.message:
            delete_message_kwargs = dict(
                chat_id=chat_id,
                message_id=message_id
            )
            await call_telegram_message_function(
                function_caller=function_caller,
                function=context.bot.delete_message,
                context=context,
                need_response=False,
                **delete_message_kwargs
            )
        elif 'Message to delete not found' in e.message:
            print(f'\tError Message: "{e.message}"')
        else:
            raise e


async def answer(query: CallbackQuery, text: str, **kwargs):
    '''Tenta enviar um answer, caso ocorra um erro, print o erro e o text
    '''

    try:
        await query.answer(text=text, **kwargs)
    except BadRequest as e:
        print('ANSWER() BADREQUEST EXCEPT.')
        print(f'  text: {text}')


async def reply_typing(
    function_caller: str,
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await call_telegram_message_function(
        function_caller=function_caller,
        function=update.effective_message.reply_chat_action,
        context=context,
        need_response=False,
        skip_retry=True,
        **REPLY_CHAT_ACTION_KWARGS
    )


# MESSAGE FUNCTIONS
async def message_edit_reply_markup(
    function_caller: str,
    message: Message,
    context: ContextTypes.DEFAULT_TYPE,
    need_response: bool = True,
    reply_markup: InlineKeyboardMarkup = None,
    **kwargs
) -> Message:
    '''Edita a reply_markup de uma mensagem usando a função de edição na 
    Mensagem.
    '''

    edit_reply_markup_kwargs = dict(
        reply_markup=reply_markup,
        **kwargs
    )
    response = await call_telegram_message_function(
        function_caller=f'{function_caller} and MESSAGE_EDIT_REPLY_MARKUP()',
        function=message.edit_reply_markup,
        context=context,
        need_response=need_response,
        **edit_reply_markup_kwargs
    )

    return response


# CALLBACK FUNCTIONS
def callback_data_to_string(callback_data: dict) -> str:
    '''Transforma um dicionário em uma string compactada usada no campo data 
    de um botão.
    '''

    items = []
    for key, value in callback_data.items():
        key_int = CALLBACK_KEY_LIST.index(key)
        if isinstance(value, (str, ObjectId)):
            items.append(f'{key_int}:"{value}"')
        else:
            items.append(f'{key_int}:{value}')
    text = ','.join(items)
    text = f'{{{text}}}'

    return text


def callback_data_to_dict(callback_data_str: str) -> dict:
    '''Transforma de volta uma string compactada usada no campo data 
    de um botão em um dicionário.
    '''

    callback_data = eval(callback_data_str)
    callback_data = {
        CALLBACK_KEY_LIST[key]: value
        for key, value in callback_data.items()
    }
    return callback_data


# BUTTONS FUNCTIONS
def get_close_button(
    user_id: int,
    text: str = None,
    right_icon: bool = False,
) -> InlineKeyboardButton:
    '''Se user_id for None, qualquer um pode fechar a mensagem, 
    caso contrário, somente o usuário com o mesmo user_id poderar fechar 
    a mensagem.
    '''

    if text is None:
        text = LEFT_CLOSE_BUTTON_TEXT
        if right_icon:
            text = RIGHT_CLOSE_BUTTON_TEXT

    return InlineKeyboardButton(
        text=text,
        callback_data=(
            f'{{"command":"{CALLBACK_CLOSE}",'
            f'"user_id":{user_id}}}'
        )
    )


def get_refresh_close_button(
    user_id: int,
    refresh_data: str = 'refresh',
    to_detail: bool = False,
) -> List[InlineKeyboardButton]:
    '''Se user_id for None, qualquer um pode fechar a mensagem, 
    caso contrário, somente o usuário com o mesmo user_id poderar fechar 
    a mensagem.
    '''

    button_list = []
    button_list.append(
        InlineKeyboardButton(
            REFRESH_BUTTON_TEXT,
            callback_data=(
                f'{{"{refresh_data}":1,'
                f'"user_id":{user_id}}}'
            )
        )
    )
    if to_detail:
        button_list.append(
            InlineKeyboardButton(
                DETAIL_BUTTON_TEXT,
                callback_data=(
                    f'{{"{refresh_data}":1,"verbose":"v",'
                    f'"user_id":{user_id}}}'
                )
            )
        )
    button_list.append(get_close_button(user_id=user_id, right_icon=True))

    return button_list


def get_random_refresh_text() -> str:
    emoji = choice(list(FaceEmojiEnum)).value
    return f'Atualizado{emoji}'


def get_close_keyboard(user_id: int) -> InlineKeyboardMarkup:
    '''Se user_id for None, qualquer um pode fechar a mensagem, 
    caso contrário, somente o usuário com o mesmo user_id poderar fechar 
    a mensagem.
    '''

    return InlineKeyboardMarkup([[
        get_close_button(user_id=user_id)
    ]])


def get_refresh_close_keyboard(
    user_id: int,
    refresh_data: str = 'refresh',
    to_detail: bool = False,
) -> InlineKeyboardMarkup:
    '''Se user_id for None, qualquer um pode fechar a mensagem, 
    caso contrário, somente o usuário com o mesmo user_id poderar fechar 
    a mensagem.
    '''

    return InlineKeyboardMarkup([
        get_refresh_close_button(
            user_id=user_id,
            refresh_data=refresh_data,
            to_detail=to_detail
        )
    ])


def get_job_delete_message_from_context_name(chat_id, message_id):
    return f'DELETE_MESSAGE_FROM_CONTEXT_{chat_id}_{message_id}'


def is_verbose(args: list) -> bool:
    if args is None:
        return False

    result = False
    for verbose in VERBOSE_ARGS:
        if verbose in args:
            result = True

    return result


def get_autodelete_time(
    chat_id: int = None,
    minutes: int = 0,
    hours: int = 0
) -> timedelta:
    if minutes < 0 or hours < 0:
        raise ValueError(
            'Os valores de tempo (minutes e hours) '
            'não podem ser menores que zero.'
        )
    elif minutes == hours == 0:
        raise ValueError(
            'minutes e hours não podem ser igual zero simultâneamente. '
        )

    time_multiplier = 1
    if isinstance(chat_id, int):
        # TODO alterar `time_multiplier` para o valor do grupo
        ...

    kwargs = dict(
        minutes=minutes * time_multiplier,
        hours=hours * time_multiplier,
    )

    return timedelta(**kwargs)


def get_autodelete_time_for_drop(
    chat_id: int = None,
    item: Item = None
) -> timedelta:
    min_minutes = 15
    max_minutes = 20

    if item and isinstance(item.item, GemstoneConsumable):
        max_minutes = 40
    elif item and isinstance(item.item, TrocadoPouchConsumable):
        max_minutes = 30
    elif item and isinstance(item.item, Consumable):
        max_minutes = 20
    elif item and isinstance(item.item, Equipment):
        max_minutes = 60

    minutes = randint(min_minutes, max_minutes)

    return get_autodelete_time(chat_id=chat_id, minutes=minutes)


def get_hours_delete_message_from_context(
    chat_id: int = None,
    value: Union[bool, int, timedelta] = HOURS_DELETE_MESSAGE_FROM_CONTEXT
) -> timedelta:
    '''Retorna o tempo para deletar uma mensagem após um tempo
    pré determinado.
    '''

    if value is True:
        value = HOURS_DELETE_MESSAGE_FROM_CONTEXT
    if isinstance(value, int) and value > 0:
        value = get_autodelete_time(chat_id=chat_id, hours=value)
    if isinstance(value, timedelta):
        return value
    else:
        raise TypeError(
            f'value precisa ser do tipo '
            f'"bool", "int" ou "timedelta" ({type(value)}). '
            f'Caso seja do tipo "bool", deve ser True. '
            f'Caso seja do tipo "int", deve ser maior que zero ({value}).'
        )


def is_chat_group(message: Message = None, chat_type: str = None) -> bool:
    if isinstance(message, Message):
        chat_type = message.chat.type
    elif not isinstance(chat_type, str):
        raise TypeError(
            f'message precisa ser do tipo "Message" ({type(message)}) ou '
            f'chat_type precisa ser do tipo "str" ({type(chat_type)})'
        )

    return chat_type in CHAT_TYPE_GROUPS


if __name__ == '__main__':
    d = {
        'drop': 10,
        'item': 10,
        'page': 10,
        'user_id': 123456789,
        'target_id': "123456789"
    }
    print(d1 := callback_data_to_string(d))
    print(d2 := callback_data_to_dict(d1))

    print(is_chat_group(chat_type='group'))

    print('GET_HOURS_DELETE_MESSAGE_FROM_CONTEXT()')
    print(get_hours_delete_message_from_context(value=True))
    print(get_hours_delete_message_from_context(value=5))
    print(get_hours_delete_message_from_context(value=timedelta(minutes=12)))

    print('GET_AUTODELETE_TIME_FOR_DROP()', get_autodelete_time_for_drop())
