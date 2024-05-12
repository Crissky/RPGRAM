from datetime import timedelta
from random import choice, randint
from typing import List

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
)

from bot.constants.puzzle import (
    GOD_BAD_MOVE_FEEDBACK_TEXTS,
    GOD_GOOD_MOVE_FEEDBACK_TEXTS,
    GOD_GREETINGS_TEXTS,
    GOD_START_NARRATION_TEXTS,
    GOD_WINS_FEEDBACK_TEXTS,
    GODS_LOSES_FEEDBACK_TEXTS,
    PATTERN_PUZZLE,
    SECTION_TEXT_PUZZLE
)
from bot.decorators.job import skip_if_spawn_timeout
from bot.functions.chat import (
    call_telegram_message_function,
    callback_data_to_dict,
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
    times = randint(1, 1) if is_boosted_day(now) else 1
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
    grid = GridGame(rarity=rarity)
    start_text = choice(GOD_START_NARRATION_TEXTS)
    god_greetings = f'>{choice(GOD_GREETINGS_TEXTS)}'
    text = f'{start_text}\n\n{god_greetings}\n\n{grid.full_colors_text}'
    grid_buttons = get_grid_buttons(grid)
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
    message_id = response.message_id
    put_grid_in_dict(message_id, context, grid)


async def switch_puzzle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('SWITCH_PUZZLE()')
    query = update.callback_query
    message_id = query.message.message_id
    grid = get_grid_from_dict(message_id, context)
    data = callback_data_to_dict(query.data)
    row = data['row']
    col = data['col']

    if grid is None:
        await query.edit_message_text('Esse desafio não existe mais.')
        return ConversationHandler.END

    is_good_move = grid.switch(row=row, col=col)
    grid_buttons = get_grid_buttons(grid)
    reply_markup = InlineKeyboardMarkup(grid_buttons)

    if grid.is_solved:
        text = choice(GOD_WINS_FEEDBACK_TEXTS)
    elif grid.is_failed:
        text = choice(GODS_LOSES_FEEDBACK_TEXTS)
    elif is_good_move is True:
        text = choice(GOD_GOOD_MOVE_FEEDBACK_TEXTS)
    else:
        text = choice(GOD_BAD_MOVE_FEEDBACK_TEXTS)

    text = create_text_in_box(
        text=f'>{text}\n\n{grid.full_colors_text}',
        section_name=SECTION_TEXT_PUZZLE,
        section_start=SECTION_HEAD_PUZZLE_START,
        section_end=SECTION_HEAD_PUZZLE_END,
        clean_func=escape_for_citation_markdown_v2,
    )
    reply_text_kwargs = dict(
        text=text,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=reply_markup,
    )
    response = await call_telegram_message_function(
        function_caller='SWITCH_PUZZLE()',
        function=query.edit_message_text,
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


def put_grid_in_dict(
    message_id: int,
    context: ContextTypes.DEFAULT_TYPE,
    grid: GridGame,
):
    '''Adiciona o grid ao dicionário de Grids, em que a chave é a 
    message_id.
    '''

    grids = context.chat_data.get('grids', {})
    grids[message_id] = {'grid': grid}
    if not 'grids' in context.chat_data:
        context.chat_data['grids'] = grids


def get_grid_from_dict(
    message_id: int,
    context: ContextTypes.DEFAULT_TYPE
) -> GridGame:
    grids = context.chat_data.get('grids', {})
    grid_dict = grids.get(message_id, {})
    grid = grid_dict.get('grid', None)

    return grid


def remove_grid_from_dict(
    message_id: int,
    context: ContextTypes.DEFAULT_TYPE
):
    grids = context.chat_data.get('grids', {})
    grids.pop(message_id, None)
    context.chat_data['grids'] = grids


PUZZLE_HANDLERS = [
    CallbackQueryHandler(switch_puzzle, pattern=PATTERN_PUZZLE),
]
