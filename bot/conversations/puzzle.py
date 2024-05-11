from datetime import timedelta
from random import choice, randint
from typing import List

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
)

from bot.constants.puzzle import (
    GOD_GREETINGS_TEXTS,
    GOD_START_NARRATION_TEXTS,
    SECTION_TEXT_PUZZLE
)
from bot.decorators.job import skip_if_spawn_timeout
from bot.functions.chat import (
    call_telegram_message_function,
    callback_data_to_string
)
from bot.functions.config import get_attribute_group
from bot.functions.date_time import is_boosted_day

from bot.functions.keyboard import reshape_row_buttons
from constant.text import SECTION_HEAD_PUZZLE_END, SECTION_HEAD_PUZZLE_START

from function.date_time import get_brazil_time_now
from function.text import create_text_in_box, escape_for_citation_markdown_v2

from repository.mongo.populate.tools import choice_rarity

from rpgram import GridGame


async def job_create_puzzle(context: ContextTypes.DEFAULT_TYPE):
    '''Cria job do Puzzle de Thoth & Seshat.

    Thoth: Deus Egípcios da sabedoria, escrita e magia. 
    Acredita-se que tenha inventado os jogos de tabuleiro e enigmas.

    Seshat: Deusa Egípcios da escrita, conhecimento e medidas.
    Associada a jogos de estratégia e desafios mentais.
    '''

    job = context.job
    chat_id = job.chat_id
    now = get_brazil_time_now()
    times = randint(1, 2) if is_boosted_day(now) else 1
    for i in range(times):
        minutes = randint(1, 2)
        print(
            f'JOB_CREATE_PUZZLE() - {now}: '
            f'Evento de item inicia em {minutes} minutos.'
        )
        context.job_queue.run_once(
            callback=job_start_puzzle,
            when=timedelta(minutes=minutes),
            name=f'JOB_CREATE_PUZZLE_{i}',
            chat_id=chat_id,
        )


@skip_if_spawn_timeout
async def job_start_puzzle(context: ContextTypes.DEFAULT_TYPE):
    '''Envia a mensagem com o Puzzle de Thoth & Seshat.
    '''

    job = context.job
    chat_id = job.chat_id
    group_level = get_attribute_group(chat_id, 'group_level')
    rarity = choice_rarity(group_level)
    new_grid = GridGame(rarity=rarity)
    start_text = choice(GOD_START_NARRATION_TEXTS)
    god_greetings = f'>{choice(GOD_GREETINGS_TEXTS)}'
    text = f'{start_text}\n\n{god_greetings}'
    grid_buttons = get_grid_buttons(new_grid)
    reply_markup = InlineKeyboardMarkup(grid_buttons)

    text = create_text_in_box(
        text=text,
        section_name=SECTION_TEXT_PUZZLE,
        section_start=SECTION_HEAD_PUZZLE_START,
        section_end=SECTION_HEAD_PUZZLE_END,
        clean_func=escape_for_citation_markdown_v2,
    )
    reply_text_kwargs = dict(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN_V2,
        allow_sending_without_reply=True,
        reply_markup=reply_markup,
    )
    response = await call_telegram_message_function(
        function_caller='JOB_START_PUZZLE()',
        function=context.bot.send_message,
        **reply_text_kwargs
    )


def get_grid_buttons(grid: GridGame) -> List[InlineKeyboardButton]:
    n_rows = grid.n_rows
    buttons = []
    for coor in grid:
        button = InlineKeyboardButton(
            text=f'{coor.text}',
            callback_data=callback_data_to_string({
                'row': coor.row,
                'col': coor.col,
            }),
        )
        buttons.append(button)

    return reshape_row_buttons(
        buttons=buttons,
        buttons_per_row=n_rows,
    )
