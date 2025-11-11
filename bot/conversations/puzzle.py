from datetime import timedelta
from random import choice, randint
from typing import List

from telegram import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update
)
from telegram.constants import ParseMode
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
)

from bot.constants.job import BASE_JOB_KWARGS
from bot.constants.puzzle import (
    GOD_BAD_MOVE_FEEDBACK_TEXTS,
    GOD_GOOD_MOVE_FEEDBACK_TEXTS,
    GOD_GREETINGS_TEXTS,
    GOD_START_NARRATION_TEXTS,
    GOD_WINS_FEEDBACK_TEXTS,
    GODS_LOSES_FEEDBACK_TEXTS,
    GODS_NAME,
    GODS_TIMEOUT_FEEDBACK_TEXTS,
    PATTERN_PUZZLE,
    SECTION_TEXT_PUZZLE
)
from bot.decorators import (
    skip_if_spawn_timeout,
    skip_if_no_singup_player,
    print_basic_infos,
    retry_after
)
from bot.functions.char import punishment
from bot.functions.char import add_xp_group
from bot.functions.chat import (
    REPLY_MARKUP_DEFAULT,
    call_telegram_message_function,
    callback_data_to_dict,
    callback_data_to_string,
    edit_message_text,
    get_close_keyboard
)
from bot.functions.config import get_attribute_group, is_group_spawn_time
from bot.functions.item import drop_random_prize
from bot.functions.job import remove_job_by_name
from bot.functions.keyboard import reshape_row_buttons

from constant.text import (
    SECTION_HEAD_TIMEOUT_PUNISHMENT_PUZZLE_END,
    SECTION_HEAD_TIMEOUT_PUNISHMENT_PUZZLE_START,
    SECTION_HEAD_PUZZLE_BADMOVE_END,
    SECTION_HEAD_PUZZLE_BADMOVE_START,
    SECTION_HEAD_PUZZLE_COMPLETE_END,
    SECTION_HEAD_PUZZLE_COMPLETE_START,
    SECTION_HEAD_PUZZLE_END,
    SECTION_HEAD_PUZZLE_FAIL_END,
    SECTION_HEAD_PUZZLE_FAIL_START,
    SECTION_HEAD_PUZZLE_GOODMOVE_END,
    SECTION_HEAD_PUZZLE_GOODMOVE_START,
    SECTION_HEAD_PUZZLE_START,
    SECTION_HEAD_TIMEOUT_PUZZLE_END,
    SECTION_HEAD_TIMEOUT_PUZZLE_START
)

from function.text import create_text_in_box, escape_for_citation_markdown_v2

from repository.mongo.populate.tools import choice_rarity

from rpgram import GridGame


# ROUTES
(
    START_ROUTES,
) = range(1)


@skip_if_spawn_timeout
async def job_start_puzzle(context: ContextTypes.DEFAULT_TYPE):
    '''Envia a mensagem com o Puzzle de Thoth & Seshat.

    Thoth: Deus Egípcios da sabedoria, escrita e magia.
    Acredita-se que tenha inventado os jogos de tabuleiro e enigmas.

    Seshat: Deusa Egípcios da escrita, conhecimento e medidas.
    Associada a jogos de estratégia e desafios mentais.
    '''

    print('JOB_START_PUZZLE()')
    job = context.job
    chat_id = job.chat_id
    group_level = get_attribute_group(chat_id, 'group_level')
    silent = get_attribute_group(chat_id, 'silent')
    rarity = choice_rarity(group_level)
    grid = GridGame(rarity=rarity)
    start_text = choice(GOD_START_NARRATION_TEXTS)
    god_greetings = f'>{GODS_NAME}: {choice(GOD_GREETINGS_TEXTS)}'
    text = f'{start_text}\n\n{god_greetings}\n\n{grid.full_colors_text}'
    grid_buttons = get_grid_buttons(grid)
    minutes = randint(120, 180)
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
        disable_notification=silent,
        allow_sending_without_reply=True,
        reply_markup=reply_markup,
    )
    response = await call_telegram_message_function(
        function_caller='JOB_START_PUZZLE()',
        function=context.bot.send_message,
        context=context,
        **reply_text_kwargs
    )
    message_id = response.message_id
    job_name = get_puzzle_job_name(message_id)
    put_grid_in_dict(context=context, message_id=message_id, grid=grid)
    context.job_queue.run_once(
        callback=job_timeout_puzzle,
        when=timedelta(minutes=minutes),
        data=dict(message_id=message_id),
        chat_id=chat_id,
        name=job_name,
        job_kwargs=BASE_JOB_KWARGS,
    )


async def job_timeout_puzzle(context: ContextTypes.DEFAULT_TYPE):
    ''' Causa dano e Status aos jogadores caso o tempo para concluir o
    puzzle encerre. Mas se já estiver fora do horário de spawn, os
    deuses irão embora.
    '''

    print('JOB_TIMEOUT_PUZZLE()')
    job = context.job
    chat_id = job.chat_id
    data = job.data
    message_id = data['message_id']
    is_spawn_time = is_group_spawn_time(chat_id)
    grid = get_grid_from_dict(context=context, message_id=message_id)
    section_name = f'{SECTION_TEXT_PUZZLE} {grid.rarity.value.upper()}'

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
        text = choice(GODS_TIMEOUT_FEEDBACK_TEXTS)
        text += ' '
        text += choice(GODS_LOSES_FEEDBACK_TEXTS)
        section_start = SECTION_HEAD_TIMEOUT_PUNISHMENT_PUZZLE_START
        section_end = SECTION_HEAD_TIMEOUT_PUNISHMENT_PUZZLE_END
        await punishment(
            context=context,
            message_id=message_id,
        )

    text = create_text_in_box(
        text=f'>{GODS_NAME}: {text}\n\n{grid.full_colors_text}',
        section_name=section_name,
        section_start=section_start,
        section_end=section_end,
        clean_func=escape_for_citation_markdown_v2,
    )
    await edit_message_text(
        function_caller='JOB_TIMEOUT_PUZZLE()',
        new_text=text,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        need_response=False,
        markdown=True
    )
    remove_grid_from_dict(context=context, message_id=message_id)


@skip_if_no_singup_player
# @skip_if_dead_char
# @skip_if_immobilized
# @confusion(START_ROUTES)
@print_basic_infos
@retry_after
async def switch_puzzle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('SWITCH_PUZZLE()')
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    grid = get_grid_from_dict(context=context, message_id=message_id)
    data = callback_data_to_dict(query.data)
    row = data['row']
    col = data['col']

    if grid is None:
        new_text = 'Esse desafio não existe mais.'
        await edit_message_text(
            function_caller='PUZZLE.SWITCH_PUZZLE()',
            new_text=new_text,
            context=context,
            chat_id=chat_id,
            message_id=message_id,
            need_response=False,
            markdown=False,
        )

        return ConversationHandler.END

    is_good_move = grid.switch(row=row, col=col)

    if grid.is_solved:
        await solved(grid=grid, query=query, context=context)
    elif grid.is_failed:
        await failed(grid=grid, query=query, context=context)
    elif is_good_move is True:
        await good_move(grid=grid, query=query, context=context)
    else:
        await bad_move(grid=grid, query=query, context=context)


async def solved(
    grid: GridGame,
    query: CallbackQuery,
    context: ContextTypes.DEFAULT_TYPE
):
    print('PUZZLE.SOLVED()')
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    player_name = query.from_user.name
    silent = get_attribute_group(chat_id, 'silent')
    text = choice(GOD_WINS_FEEDBACK_TEXTS)
    prize_text = f'{GODS_NAME} deixaram como recompensa'
    remove_timeout_puzzle_job(context=context, message_id=message_id)
    remove_grid_from_dict(context=context, message_id=message_id)
    reply_markup = get_close_keyboard(None)
    await puzzle_edit_message_text(
        grid=grid,
        text=text,
        player_name=player_name,
        context=context,
        message_id=message_id,
        section_start=SECTION_HEAD_PUZZLE_COMPLETE_START,
        section_end=SECTION_HEAD_PUZZLE_COMPLETE_END,
        reply_markup=reply_markup,
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
        rarity=grid.rarity,
        message_id=message_id,
        text=prize_text,
    )


async def failed(
    grid: GridGame,
    query: CallbackQuery,
    context: ContextTypes.DEFAULT_TYPE
):
    print('PUZZLE.FAILED()')
    message_id = query.message.message_id
    player_name = query.from_user.name
    text = choice(GODS_LOSES_FEEDBACK_TEXTS)
    reply_markup = get_close_keyboard(None)
    await puzzle_edit_message_text(
        grid=grid,
        text=text,
        player_name=player_name,
        context=context,
        message_id=message_id,
        section_start=SECTION_HEAD_PUZZLE_FAIL_START,
        section_end=SECTION_HEAD_PUZZLE_FAIL_END,
        reply_markup=reply_markup,
    )
    remove_timeout_puzzle_job(context=context, message_id=message_id)
    remove_grid_from_dict(context=context, message_id=message_id)
    await punishment(
        context=context,
        message_id=message_id,
    )


async def good_move(
    grid: GridGame,
    query: CallbackQuery,
    context: ContextTypes.DEFAULT_TYPE
):
    print('PUZZLE.GOOD_MOVE()')
    message_id = query.message.message_id
    player_name = query.from_user.name
    text = choice(GOD_GOOD_MOVE_FEEDBACK_TEXTS)
    grid_buttons = get_grid_buttons(grid)
    reply_markup = InlineKeyboardMarkup(grid_buttons)
    await puzzle_edit_message_text(
        grid=grid,
        text=text,
        player_name=player_name,
        context=context,
        message_id=message_id,
        section_start=SECTION_HEAD_PUZZLE_GOODMOVE_START,
        section_end=SECTION_HEAD_PUZZLE_GOODMOVE_END,
        reply_markup=reply_markup,
    )


async def bad_move(
    grid: GridGame,
    query: CallbackQuery,
    context: ContextTypes.DEFAULT_TYPE
):
    print('PUZZLE.BAD_MOVE()')
    message_id = query.message.message_id
    player_name = query.from_user.name
    text = choice(GOD_BAD_MOVE_FEEDBACK_TEXTS)
    grid_buttons = get_grid_buttons(grid)
    reply_markup = InlineKeyboardMarkup(grid_buttons)
    await puzzle_edit_message_text(
        grid=grid,
        text=text,
        player_name=player_name,
        context=context,
        message_id=message_id,
        section_start=SECTION_HEAD_PUZZLE_BADMOVE_START,
        section_end=SECTION_HEAD_PUZZLE_BADMOVE_END,
        reply_markup=reply_markup,
    )


async def puzzle_edit_message_text(
    grid: GridGame,
    text: str,
    player_name: str,
    context: ContextTypes.DEFAULT_TYPE,
    message_id: int,
    section_name: str = None,
    section_start: str = None,
    section_end: str = None,
    reply_markup: InlineKeyboardMarkup = REPLY_MARKUP_DEFAULT,
):
    chat_id = context._chat_id
    if not isinstance(section_name, str):
        section_name = f'{SECTION_TEXT_PUZZLE} {grid.rarity.value.upper()}'
    if not isinstance(section_start, str):
        section_start = SECTION_HEAD_PUZZLE_START
    if not isinstance(section_end, str):
        section_end = SECTION_HEAD_PUZZLE_END

    text = (
        f'>{GODS_NAME}: {text}\n\n'
        f'Jogada: {player_name}\n'
        f'{grid.full_colors_text}\n'
    )
    text = create_text_in_box(
        text=text,
        section_name=section_name,
        section_start=section_start,
        section_end=section_end,
        clean_func=escape_for_citation_markdown_v2,
    )
    await edit_message_text(
        function_caller='SWITCH_PUZZLE_EDIT_MESSAGE_TEXT()',
        new_text=text,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        need_response=True,
        markdown=True,
        reply_markup=reply_markup
    )


def get_grid_buttons(grid: GridGame) -> List[List[InlineKeyboardButton]]:
    n_cols = grid.n_cols
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
        buttons_per_row=n_cols,
    )


def get_puzzle_job_name(message_id):
    return f'JOB_TIMEOUT_PUZZLE_{message_id}'


def remove_timeout_puzzle_job(
    context: ContextTypes.DEFAULT_TYPE,
    message_id: int,
) -> bool:
    '''Remove o job de Timeout do Puzzle.
    '''

    job_name = get_puzzle_job_name(message_id=message_id)
    return remove_job_by_name(context=context, job_name=job_name)


def put_grid_in_dict(
    context: ContextTypes.DEFAULT_TYPE,
    message_id: int,
    grid: GridGame,
):
    '''Adiciona o grid ao dicionário de Grids, em que a chave é a
    message_id.
    '''

    print('PUZZLE.PUT_GRID_IN_DICT()')
    grids = context.chat_data.get('grids', {})
    grids[message_id] = {'grid': grid}
    if 'grids' not in context.chat_data:
        context.chat_data['grids'] = grids


def get_grid_from_dict(
    context: ContextTypes.DEFAULT_TYPE,
    message_id: int,
) -> GridGame:

    print('PUZZLE.GET_GRID_FROM_DICT()')
    grids = context.chat_data.get('grids', {})
    grid_dict = grids.get(message_id, {})
    grid = grid_dict.get('grid', None)

    return grid


def remove_grid_from_dict(
    context: ContextTypes.DEFAULT_TYPE,
    message_id: int,
):

    print('PUZZLE.REMOVE_GRID_FROM_DICT()')
    grids = context.chat_data.get('grids', {})
    grids.pop(message_id, None)
    context.chat_data['grids'] = grids


PUZZLE_HANDLERS = [
    CallbackQueryHandler(switch_puzzle, pattern=PATTERN_PUZZLE),
]
