from datetime import timedelta
from random import choice, randint
from bson import ObjectId
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from bot.constants.job import BASE_JOB_KWARGS
from bot.constants.word_game import (
    SECTION_TEXT_WORDGAME,
    WORD_GOD_GREETINGS_TEXTS,
    WORD_GOD_LOSES_FEEDBACK_TEXTS,
    WORD_GOD_NAME,
    WORD_GOD_TIMEOUT_FEEDBACK_TEXTS,
    WORD_START_NARRATION_TEXTS
)
from bot.decorators.job import skip_if_spawn_timeout
from bot.functions.chat import (
    call_telegram_message_function,
    edit_message_text
)
from bot.functions.config import get_attribute_group, is_group_spawn_time
from bot.functions.date_time import is_boosted_day
from constant.text import (
    SECTION_HEAD_PUZZLE_END,
    SECTION_HEAD_PUZZLE_START,
    SECTION_HEAD_TIMEOUT_PUNISHMENT_PUZZLE_END,
    SECTION_HEAD_TIMEOUT_PUNISHMENT_PUZZLE_START,
    SECTION_HEAD_TIMEOUT_PUZZLE_END,
    SECTION_HEAD_TIMEOUT_PUZZLE_START
)
from function.date_time import get_brazil_time_now
from function.text import create_text_in_box, escape_for_citation_markdown_v2
from repository.mongo.populate.tools import choice_rarity
from rpgram.minigames.secret_word.secret_word import SecretWordGame


async def create_wordgame_event(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    '''Cria job do Desafio de Palavra de Hermes.
    '''

    chat_id = update.effective_chat.id
    now = get_brazil_time_now()
    times = randint(1, 2) if is_boosted_day(now) else 1
    for i in range(times):
        minutes = randint(1 + (i*20), 10 + (i*20))
        print(
            f'CREATE_WORDGAME_EVENT() - {now}: '
            f'Evento de item inicia em {minutes} minutos.'
        )
        context.job_queue.run_once(
            callback=job_start_wordgame,
            when=timedelta(minutes=minutes),
            chat_id=chat_id,
            name=f'JOB_CREATE_WORDGAME_{ObjectId()}',
            job_kwargs=BASE_JOB_KWARGS,
        )


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
        f'Qual a *Palavra Secreta* de {game.size} letras.'
    )
    minutes = randint(120, 180)

    text = create_text_in_box(
        text=text,
        section_name=SECTION_TEXT_WORDGAME,
        section_start=SECTION_HEAD_PUZZLE_START,
        section_end=SECTION_HEAD_PUZZLE_END,
        clean_func=escape_for_citation_markdown_v2,
    )
    reply_text_kwargs = dict(
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
        **reply_text_kwargs
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
    section_name = f'{SECTION_TEXT_WORDGAME} {game.rarity.value.upper()}'

    if not is_spawn_time:
        text = (
            'Pois, é chegada a hora tardia em que necessitamos nos retirar '
            'para os nossos augustos domínios, e por isso, em nossa '
            'magnanimidade, concedemos-lhes o perdão. Assim, '
            'não lhes lançaremos nossa maldição.'
        )
        section_start = SECTION_HEAD_TIMEOUT_PUZZLE_START
        section_end = SECTION_HEAD_TIMEOUT_PUZZLE_END
    else:
        text = choice(WORD_GOD_TIMEOUT_FEEDBACK_TEXTS)
        text += ' '
        text += choice(WORD_GOD_LOSES_FEEDBACK_TEXTS)
        section_start = SECTION_HEAD_TIMEOUT_PUNISHMENT_PUZZLE_START
        section_end = SECTION_HEAD_TIMEOUT_PUNISHMENT_PUZZLE_END
        await wordgame_punishment(
            chat_id=chat_id,
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


async def wordgame_punishment(
    chat_id: int,
    context: ContextTypes.DEFAULT_TYPE,
    message_id: int,
):
    '''Punição: adiciona dano e Status a todos os jogadores por falharem no 
    desafio.
    '''

    ...


def get_wordgame_job_name(message_id):
    return f'JOB_TIMEOUT_WORDGAME_{message_id}'


def put_wordgame_in_dict(
    context: ContextTypes.DEFAULT_TYPE,
    message_id: int,
    game: SecretWordGame,
):
    '''Adiciona o Word Game ao dicionário de Games, em que a chave é a 
    message_id.
    '''

    print('WORDGAME.PUT_WORDGAME_IN_DICT()')
    games = context.chat_data.get('games', {})
    games[message_id] = {'game': game}
    if not 'games' in context.chat_data:
        context.chat_data['games'] = games


def get_wordgame_from_dict(
    context: ContextTypes.DEFAULT_TYPE,
    message_id: int,
) -> SecretWordGame:

    print('WORDGAME.GET_WORDGAME_FROM_DICT()')
    grids = context.chat_data.get('games', {})
    grid_dict = grids.get(message_id, {})
    grid = grid_dict.get('game', None)

    return grid


def remove_wordgame_from_dict(
    context: ContextTypes.DEFAULT_TYPE,
    message_id: int,
):

    print('WORDGAME.REMOVE_WORDGAME_FROM_DICT()')
    grids = context.chat_data.get('games', {})
    grids.pop(message_id, None)
    context.chat_data['games'] = grids
