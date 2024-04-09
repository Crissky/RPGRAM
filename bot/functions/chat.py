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

from telegram.constants import ChatAction, ParseMode
from telegram.error import Forbidden, RetryAfter, TimedOut
from telegram.ext import ContextTypes

from bot.constants.close import CALLBACK_CLOSE
from bot.functions.general import get_attribute_group_or_player
from bot.functions.player import get_player_attribute_by_id
from rpgram.enums import EmojiEnum, FaceEmojiEnum


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
    'race_name',
]


async def send_private_message(
    function_caller: str,
    context: ContextTypes.DEFAULT_TYPE,
    text: str,
    user_id: int,
    chat_id: int = None,
    markdown: bool = False,
    reply_markup: InlineKeyboardMarkup = REPLY_MARKUP_DEFAULT,
    close_by_owner: bool = False,
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
        await context.bot.send_message(
            chat_id=user_id,
            text=text,
            parse_mode=markdown,
            disable_notification=silent,
            reply_markup=reply_markup,
        )
    except Forbidden as error:
        if isinstance(chat_id, int):
            silent = get_attribute_group_or_player(chat_id, 'silent')
            member = await context.bot.get_chat_member(
                chat_id=chat_id,
                user_id=user_id
            )
            user_name = member.user.name
            text = f'{user_name}\n{text}'
            await context.bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=markdown,
                disable_notification=silent,
                reply_markup=reply_markup,
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
        return await query.answer(text=text, show_alert=show_alert)
    else:
        return await send_private_message(
            function_caller=function_caller,
            context=context,
            text=text,
            user_id=user_id,
            chat_id=chat_id,
            markdown=markdown,
            reply_markup=reply_markup
        )


async def forward_message(
    function_caller: str,
    user_ids: Union[int, List[int]],
    message: Message = None,
    context: ContextTypes.DEFAULT_TYPE = None,
    chat_id: int = None,
    message_id: int = None,
):
    '''Encaminha uma mensagem usando um Message ou um ContextTypes
    '''
    if context and not chat_id:
        raise ValueError('chat_id é necessário quando passado um context.')
    if context and not message_id:
        raise ValueError('message_id é necessário quando passado um context.')
    if not message and not context:
        raise ValueError('message ou context deve ser passado.')

    message_chat_id = message.chat_id if message else None
    if isinstance(user_ids, int):
        user_ids = [user_ids]
    user_ids = list(set(user_ids))

    for user_id in user_ids:
        user_silent = get_player_attribute_by_id(user_id, 'silent')
        if message_chat_id == user_id:
            continue  # Evita encaminhamento para o próprio chat privado
        try:
            if message:
                await message.forward(
                    chat_id=user_id,
                    disable_notification=user_silent
                )
            elif context:
                await context.bot.forward_message(
                    chat_id=user_id,
                    from_chat_id=chat_id,
                    message_id=message_id,
                    disable_notification=user_silent
                )
        except Exception as error:
            print(f'{function_caller}: {error}')


async def edit_message_text(
    function_caller: str,
    new_text: str,
    user_id: int = None,
    context: ContextTypes.DEFAULT_TYPE = None,
    chat_id: int = None,
    message_id: int = None,
    query: CallbackQuery = None,
    markdown: bool = False,
    reply_markup: InlineKeyboardMarkup = REPLY_MARKUP_DEFAULT,
) -> Union[Message, bool]:
    '''Edita uma mensagem usando um Message ou um ContextTypes.
    '''

    if context and not chat_id:
        raise ValueError('chat_id é necessário quando passado um context.')
    if context and not message_id:
        raise ValueError('message_id é necessário quando passado um context.')
    if not query and not context:
        raise ValueError('query ou context deve ser passado.')

    markdown = ParseMode.MARKDOWN_V2 if markdown else None
    reply_markup = (
        reply_markup
        if reply_markup != REPLY_MARKUP_DEFAULT
        else get_close_keyboard(user_id=user_id)
    )

    for _ in range(3):
        try:
            if query:
                response = await query.edit_message_text(
                    text=new_text,
                    parse_mode=markdown,
                    reply_markup=reply_markup,
                )
            elif context:
                response = await context.bot.edit_message_text(
                    text=new_text,
                    chat_id=chat_id,
                    message_id=message_id,
                    parse_mode=markdown,
                    reply_markup=reply_markup,
                )
            else:
                raise ValueError(
                    'Mensagem não foi editada. '
                    'query ou context deve ser passado.'
                )
            break
        except RetryAfter as error:
            sleep_time = error.retry_after + randint(1, 3)
            print(
                f'RetryAfter: retrying EDIT_MESSAGE_TEXT_AND_FORWARD from '
                f'{function_caller} in {sleep_time} seconds.'
            )
            await context.bot.send_chat_action(
                chat_id=chat_id,
                action=ChatAction.TYPING
            )
            sleep(sleep_time)
            continue
        except TimedOut as error:
            sleep_time = 3
            print(
                f'TimedOut: retrying EDIT_MESSAGE_TEXT_AND_FORWARD from '
                f'{function_caller} in {sleep_time} seconds.'
            )
            sleep(sleep_time)
            continue

    return response


async def edit_message_text_and_forward(
    function_caller: str,
    new_text: str,
    user_ids: Union[int, List[int]],
    context: ContextTypes.DEFAULT_TYPE = None,
    chat_id: int = None,
    message_id: int = None,
    query: CallbackQuery = None,
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

    response = await edit_message_text(
        function_caller=function_caller,
        new_text=new_text,
        user_id=owner_id,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        query=query,
        markdown=markdown,
        reply_markup=reply_markup
    )

    await forward_message(
        function_caller=function_caller,
        user_ids=user_ids,
        message=response
    )

    return response


async def reply_text_and_forward(
    function_caller: str,
    new_text: str,
    user_ids: Union[int, List[int]],
    update: Update = None,
    context: ContextTypes = None,
    chat_id: int = None,
    message_id: int = None,
    allow_sending_without_reply=True,
    markdown: bool = False,
    reply_markup: InlineKeyboardMarkup = REPLY_MARKUP_DEFAULT,
    close_by_owner: bool = False,
):
    '''Responde uma mensagem e a encaminha para o usuário.
    '''

    if update is None and context is None:
        raise ValueError('update ou context deve ser passado.')
    if update and context:
        raise ValueError(
            'update ou context não podem ser passados ao mesmo tempo.'
        )
    if context and not isinstance(chat_id, int):
        raise ValueError('Quando usar context, chat_id deve ser um inteiro.')
    if context and not isinstance(message_id, int):
        raise ValueError(
            'Quando usar context, message_id deve ser um inteiro.'
        )

    if isinstance(user_ids, int):
        user_ids = [user_ids]

    markdown = ParseMode.MARKDOWN_V2 if markdown else None
    owner_id = user_ids[0] if close_by_owner is True else None
    both_function_caller = f'{function_caller} and REPLY_TEXT_AND_FORWARD()'
    reply_markup = (
        reply_markup
        if reply_markup != REPLY_MARKUP_DEFAULT
        else get_close_keyboard(user_id=owner_id)
    )
    reply_text_kwargs = dict(
        text=new_text,
        parse_mode=markdown,
        reply_markup=reply_markup,
        allow_sending_without_reply=allow_sending_without_reply,
    )

    if update:
        function = update.effective_message.reply_text
    elif context:
        function = context.bot.send_message
        reply_text_kwargs['chat_id'] = chat_id
        reply_text_kwargs['reply_to_message_id'] = message_id

    response = await call_telegram_message_function(
        function_caller=both_function_caller,
        function=function,
        **reply_text_kwargs
    )

    await forward_message(
        function_caller=function_caller,
        user_ids=user_ids,
        message=response
    )


async def call_telegram_message_function(
    function_caller: str,
    function: Callable,
    *args,
    **kwargs
) -> Union[Any, Message]:
    '''Função que chama qualquer função de mensagem do telegram. 
    Caso ocorra um erro do tipo RetryAfter ou TimedOut, a função agurdará 
    alguns segundos tentará novamente com um número máximo de 3 tentativas.
    '''

    for i in range(3):
        try:
            response = await function(*args, **kwargs)
            break
        except RetryAfter as error:
            sleep_time = error.retry_after + randint(1, 3)
            print(
                f'RetryAfter({i}): retrying activate "{function.__name__}" '
                f'from {function_caller} in {sleep_time} seconds.'
            )
            sleep(sleep_time)
            continue
        except TimedOut as error:
            sleep_time = 3
            print(
                f'TimedOut({i}): retrying activate "{function.__name__}" '
                f'from {function_caller} in {sleep_time} seconds.'
            )
            sleep(sleep_time)
            continue

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
    return InlineKeyboardMarkup([[
        get_close_button(user_id=user_id)
    ]])


def get_refresh_close_keyboard(
    user_id: int,
    refresh_data: str = 'refresh',
    to_detail: bool = False,
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        get_refresh_close_button(
            user_id=user_id,
            refresh_data=refresh_data,
            to_detail=to_detail
        )
    ])


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
