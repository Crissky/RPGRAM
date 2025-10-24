from datetime import timedelta
from random import choice, randint
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ContextTypes,
    MessageHandler
)
from telegram.constants import ParseMode

from bot.constants.filters import (
    ALLOW_WORDGAME_BUTTON_FILTER,
    ALLOW_WORDGAME_FILTER
)
from bot.constants.job import BASE_JOB_KWARGS
from bot.constants.word_game import (
    SECTION_TEXT_WORDGAME,
    WORD_GOD_GREETINGS_TEXTS,
    WORD_GOD_LOSES_FEEDBACK_TEXTS,
    WORD_GOD_NAME,
    WORD_GOD_TIMEOUT_FEEDBACK_TEXTS,
    WORD_GOD_WINS_FEEDBACK_TEXTS,
    WORD_START_NARRATION_TEXTS
)
from bot.constants.word_game import WORDGAME_COMMAND
from bot.decorators.job import skip_if_spawn_timeout
from bot.functions.char import (
    add_xp_group,
    char_is_alive,
    punishment,
    bad_move_damage
)
from bot.functions.chat import (
    call_telegram_message_function,
    delete_message_from_context,
    edit_message_text,
    get_close_button
)
from bot.functions.config import get_attribute_group, is_group_spawn_time
from bot.functions.item import drop_random_prize
from bot.functions.job import remove_job_by_name
from constant.text import (
    SECTION_HEAD_PUZZLE_END,
    SECTION_HEAD_PUZZLE_START,
    SECTION_HEAD_TIMEOUT_PUNISHMENT_PUZZLE_END,
    SECTION_HEAD_TIMEOUT_PUNISHMENT_PUZZLE_START,
    SECTION_HEAD_TIMEOUT_PUZZLE_END,
    SECTION_HEAD_TIMEOUT_PUZZLE_START
)
from function.text import create_text_in_box, escape_for_citation_markdown_v2
from repository.mongo.populate.tools import choice_rarity
from rpgram.errors import InvalidWordError
from rpgram.minigames.secret_word.secret_word import SecretWordGame


DICT_GAMES_KEY = 'games'
GAME_OBJECT_KEY = 'game'
DELETE_MESSAGE_ID_KEY = 'delete_message_id_list'


@skip_if_spawn_timeout
async def job_start_wordgame(context: ContextTypes.DEFAULT_TYPE):
    '''Envia a mensagem com o Desafio de Palavra de Hermes.
    '''

    print('JOB_START_WORDGAME()')
    job = context.job
    chat_id = job.chat_id
    group_level = get_attribute_group(chat_id, 'group_level')
    silent = get_attribute_group(chat_id, 'silent')
    rarity = choice_rarity(group_level)
    game = SecretWordGame(rarity=rarity)
    start_text = choice(WORD_START_NARRATION_TEXTS)
    god_greetings = f'>{WORD_GOD_NAME}: {choice(WORD_GOD_GREETINGS_TEXTS)}'
    text = (
        f'{start_text}\n\n'
        f'{god_greetings}\n\n'
        f'Responda com a *Palavra Secreta* de {game.size} letras!!!'
    )
    minutes = randint(120, 180)

    text = create_text_in_box(
        text=text,
        section_name=f'{SECTION_TEXT_WORDGAME} {game.rarity.value}'.upper(),
        section_start=SECTION_HEAD_PUZZLE_START,
        section_end=SECTION_HEAD_PUZZLE_END,
        clean_func=escape_for_citation_markdown_v2,
    )
    send_message_kwargs = dict(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN_V2,
        disable_notification=silent,
        allow_sending_without_reply=True,
    )
    response = await call_telegram_message_function(
        function_caller='JOB_START_WORDGAME()',
        function=context.bot.send_message,
        context=context,
        **send_message_kwargs
    )
    message_id = response.message_id
    job_name = get_wordgame_job_name(message_id)
    put_wordgame_in_dict(context=context, message_id=message_id, game=game)
    context.job_queue.run_once(
        callback=job_timeout_wordgame,
        when=timedelta(minutes=minutes),
        data=dict(message_id=message_id),
        chat_id=chat_id,
        name=job_name,
        job_kwargs=BASE_JOB_KWARGS,
    )


async def job_timeout_wordgame(context: ContextTypes.DEFAULT_TYPE):
    ''' Causa dano e Status aos jogadores caso o tempo para concluir o
    puzzle encerre. Mas se já estiver forma do horário de spawn, os
    deuses irão embora.
    '''

    print('JOB_TIMEOUT_WORDGAME()')
    job = context.job
    chat_id = job.chat_id
    data = job.data
    message_id = data['message_id']
    is_spawn_time = is_group_spawn_time(chat_id)
    game = get_wordgame_from_dict(context=context, message_id=message_id)
    section_name = f'{SECTION_TEXT_WORDGAME} {game.rarity.value}'.upper()

    if not is_spawn_time:
        text = (
            'Ah, mortais, o crepúsculo já dança no horizonte, '
            'e mesmo o deus da luz deve ceder ao ciclo eterno. '
            'O tempo, meu eterno aliado, me chama para repousar '
            'atrás das montanhas douradas. '
            'Embora seus corações tenham vacilado, '
            'deixo para trás não a ira, mas o perdão. '
            'Que minha ausência seja uma nova chance, '
            'e que a aurora os encontre mais sábios. '
            'Sigam, livres da maldição, pois até mesmo o sol, '
            'em sua glória infinita, sabe quando é hora de partir.'
        )
        section_start = SECTION_HEAD_TIMEOUT_PUZZLE_START
        section_end = SECTION_HEAD_TIMEOUT_PUZZLE_END
    else:
        text = choice(WORD_GOD_TIMEOUT_FEEDBACK_TEXTS)
        text += ' '
        text += choice(WORD_GOD_LOSES_FEEDBACK_TEXTS)
        section_start = SECTION_HEAD_TIMEOUT_PUNISHMENT_PUZZLE_START
        section_end = SECTION_HEAD_TIMEOUT_PUNISHMENT_PUZZLE_END
        await punishment(
            context=context,
            message_id=message_id,
        )

    text = create_text_in_box(
        text=f'>{WORD_GOD_NAME}: {text}',
        section_name=section_name,
        section_start=section_start,
        section_end=section_end,
        clean_func=escape_for_citation_markdown_v2,
    )
    await edit_message_text(
        function_caller='JOB_TIMEOUT_WORDGAME()',
        new_text=text,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        need_response=False,
        markdown=True
    )
    remove_wordgame_from_dict(context=context, message_id=message_id)


async def answer_wordgame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Responde ao Desafio de Palavra de Hermes.
    '''

    print('ANSWER_WORDGAME()')
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    message_id = update.effective_message.message_id
    message_text = update.effective_message.text
    reply_message = update.effective_message.reply_to_message
    args = message_text.split()
    is_correct = None
    put_message_id_in_delete_list(context=context, message_id=message_id)

    if reply_message:
        reply_message_id = reply_message.message_id
    elif len(args) >= 4 and WORDGAME_COMMAND in args:
        bot_name = args[0]
        command = args[1]
        reply_message_id = int(args[2])
        message_text = args[3]
    else:
        print(f'Sem reply_message e sem 4 args.')
        return None

    game = get_wordgame_from_dict(context=context, message_id=reply_message_id)
    if not game:
        print(f'Jogo da mensagem "{reply_message_id}" não foi encontrado.')
        return None

    is_alive = char_is_alive(user_id=user_id)
    silent = get_attribute_group(chat_id, 'silent')
    if not is_alive:
        text = 'Você não pode jogar, pois não está morto.'
        section_name = f'{SECTION_TEXT_WORDGAME} {game.rarity.value}'.upper()
        text = create_text_in_box(
            text=text,
            section_name=section_name,
            section_start=SECTION_HEAD_PUZZLE_START,
            section_end=SECTION_HEAD_PUZZLE_END,
            clean_func=escape_for_citation_markdown_v2,
        )
        inline_query_text = f'{WORDGAME_COMMAND} {reply_message_id} '
        reply_button = InlineKeyboardButton(
            text='Responder',
            switch_inline_query_current_chat=inline_query_text
        )
        close_button = get_close_button(user_id=None, right_icon=True)
        reply_markup = InlineKeyboardMarkup([[reply_button, close_button]])
        reply_text_kwargs = dict(
            chat_id=chat_id,
            text=text,
            parse_mode=ParseMode.MARKDOWN_V2,
            disable_notification=silent,
            reply_to_message_id=reply_message_id,
            allow_sending_without_reply=True,
            reply_markup=reply_markup,
        )

        response = await call_telegram_message_function(
            function_caller='ANSWER_WORDGAME()',
            function=context.bot.send_message,
            context=context,
            **reply_text_kwargs
        )

        response_message_id = response.message_id
        put_message_id_in_delete_list(
            context=context,
            message_id=response_message_id,
        )

        return None

    try:
        game_response = game.check_word(message_text)
        is_correct = game_response['is_correct']
        text = game_response['text']
        text += '\n'
        if is_correct:
            prize_text = f'{WORD_GOD_NAME} deixou como recompensa'
            text += '✅PALAVRA CORRETA!\n\n'
            god_congrats = (
                f'>{WORD_GOD_NAME}: {choice(WORD_GOD_WINS_FEEDBACK_TEXTS)}'
            )
            text += f'{god_congrats}'
            delete_kwargs = dict(
                chat_id=chat_id,
                message_id=reply_message_id
            )

            remove_timeout_wordgame_job(
                context=context,
                message_id=reply_message_id
            )
            remove_wordgame_from_dict(
                context=context,
                message_id=reply_message_id
            )
            await call_telegram_message_function(
                function_caller='ANSWER_WORDGAME()',
                function=context.bot.delete_message,
                context=context,
                need_response=False,
                **delete_kwargs
            )
            await add_xp_group(
                chat_id=chat_id,
                context=context,
                silent=silent,
                message_id=message_id,
            )
            await drop_random_prize(
                context=context,
                silent=silent,
                rarity=game.rarity,
                update=update,
                text=prize_text,
            )
        else:
            damage_text = bad_move_damage(
                user_id=user_id,
                multiplier=game.num_try
            )
            text += f'❌Palavra incorreta!\n\n{damage_text}'
        await delete_old_wordgame_answer_messages(context=context)
    except InvalidWordError as error:
        text = str(error)
        print(f'ERROR: "{error}"')

    text = create_text_in_box(
        text=text,
        section_name=f'{SECTION_TEXT_WORDGAME} {game.rarity.value}'.upper(),
        section_start=SECTION_HEAD_PUZZLE_START,
        section_end=SECTION_HEAD_PUZZLE_END,
        clean_func=escape_for_citation_markdown_v2,
    )
    buttons = []
    if not is_correct:
        inline_query_text = f'{WORDGAME_COMMAND} {reply_message_id} '
        reply_button = InlineKeyboardButton(
            text='Responder',
            switch_inline_query_current_chat=inline_query_text
        )
        buttons.append(reply_button)
    close_button = get_close_button(user_id=None, right_icon=True)
    buttons.append(close_button)
    reply_markup = InlineKeyboardMarkup([buttons])

    reply_text_kwargs = dict(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN_V2,
        disable_notification=silent,
        reply_to_message_id=reply_message_id,
        allow_sending_without_reply=True,
        reply_markup=reply_markup,
    )

    response = await call_telegram_message_function(
        function_caller='ANSWER_WORDGAME()',
        function=context.bot.send_message,
        context=context,
        **reply_text_kwargs
    )

    if not is_correct:
        response_message_id = response.message_id
        put_message_id_in_delete_list(
            context=context,
            message_id=response_message_id,
        )


def get_wordgame_job_name(message_id):
    return f'JOB_TIMEOUT_WORDGAME_{message_id}'


def remove_timeout_wordgame_job(
    context: ContextTypes.DEFAULT_TYPE,
    message_id: int,
) -> bool:
    '''Remove o job de Timeout do WordGame.
    '''

    job_name = get_wordgame_job_name(message_id=message_id)
    return remove_job_by_name(context=context, job_name=job_name)


def put_wordgame_in_dict(
    context: ContextTypes.DEFAULT_TYPE,
    message_id: int,
    game: SecretWordGame,
):
    '''Adiciona o Word Game ao dicionário de Games, em que a chave é a
    message_id.
    '''

    print('WORDGAME.PUT_WORDGAME_IN_DICT()')
    games = context.chat_data.get(DICT_GAMES_KEY, {})
    games[message_id] = {GAME_OBJECT_KEY: game}
    if not DICT_GAMES_KEY in context.chat_data:
        context.chat_data[DICT_GAMES_KEY] = games


def get_wordgame_from_dict(
    context: ContextTypes.DEFAULT_TYPE,
    message_id: int,
) -> SecretWordGame:
    '''Retorna um Word Game do dicionário de Games de acordo com o
    message_id passado.
    '''

    print('WORDGAME.GET_WORDGAME_FROM_DICT()')
    wordgames = context.chat_data.get(DICT_GAMES_KEY, {})
    wordgame_dict = wordgames.get(message_id, {})
    wordgame = wordgame_dict.get(GAME_OBJECT_KEY, None)
    print('Word Game:', wordgame)

    return wordgame


def remove_wordgame_from_dict(
    context: ContextTypes.DEFAULT_TYPE,
    message_id: int,
):
    '''Remove um Word Game do dicionário de Games de acordo com o
    message_id passado.
    '''

    print('WORDGAME.REMOVE_WORDGAME_FROM_DICT()')
    wordgames = context.chat_data.get(DICT_GAMES_KEY, {})
    wordgames.pop(message_id, None)
    context.chat_data[DICT_GAMES_KEY] = wordgames


def put_message_id_in_delete_list(
    context: ContextTypes.DEFAULT_TYPE,
    message_id: int,
):
    '''Adiciona um message_id a lista de message_ids das mensagens que
    serão deletadas
    '''

    print('WORDGAME.PUT_WORDGAME_MESSAGE_ID_IN_DICT()')
    delete_message_id_list = context.chat_data.get(DELETE_MESSAGE_ID_KEY, [])
    delete_message_id_list.append(message_id)
    if DELETE_MESSAGE_ID_KEY not in context.chat_data:
        context.chat_data[DELETE_MESSAGE_ID_KEY] = delete_message_id_list


def get_delete_message_id_list(context: ContextTypes.DEFAULT_TYPE) -> list:
    return context.chat_data.get(DELETE_MESSAGE_ID_KEY, [])


async def delete_old_wordgame_answer_messages(
    context: ContextTypes.DEFAULT_TYPE
):
    '''Apaga todas as mensagens que estão na lista de message_ids
    '''

    print('WORDGAME.DELETE_OLD_WORDGAME_ANSWER_MESSAGES()')
    delete_message_id_list = get_delete_message_id_list(context=context)
    for message_id in delete_message_id_list:
        await delete_message_from_context(
            function_caller='DELETE_OLD_WORDGAME_ANSWER_MESSAGES()',
            context=context,
            message_id=message_id
        )

    context.chat_data[DELETE_MESSAGE_ID_KEY] = []


WORDGAME_HANDLERS = [
    MessageHandler(
        filters=ALLOW_WORDGAME_FILTER,
        callback=answer_wordgame
    ),
    MessageHandler(
        filters=ALLOW_WORDGAME_BUTTON_FILTER,
        callback=answer_wordgame
    ),
]