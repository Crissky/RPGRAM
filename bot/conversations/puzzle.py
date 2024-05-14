from datetime import timedelta
from operator import attrgetter
from random import choice, randint, shuffle
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
    GODS_NAME,
    PATTERN_PUZZLE,
    SECTION_TEXT_PUZZLE,
    SECTION_TEXT_PUZZLE_PUNISHMENT,
    SECTION_TEXT_PUZZLE_XP
)
from bot.conversations.bag import send_drop_message
from bot.decorators import (
    need_not_in_battle,
    confusion,
    skip_if_dead_char,
    skip_if_immobilized,
    skip_if_spawn_timeout,
    skip_if_no_singup_player,
    print_basic_infos,
    retry_after
)
from bot.functions.char import (
    add_conditions,
    add_trap_damage,
    add_xp,
    get_chars_level_from_group,
    get_player_chars_from_group
)
from bot.functions.chat import (
    call_telegram_message_function,
    callback_data_to_dict,
    callback_data_to_string,
    get_close_keyboard
)
from bot.functions.config import get_attribute_group
from bot.functions.date_time import is_boosted_day

from bot.functions.keyboard import reshape_row_buttons
from constant.text import (
    SECTION_HEAD_PUNISHMENT_END,
    SECTION_HEAD_PUNISHMENT_START,
    SECTION_HEAD_PUZZLE_END,
    SECTION_HEAD_PUZZLE_START,
    SECTION_HEAD_XP_END,
    SECTION_HEAD_XP_START,
    TEXT_SEPARATOR_2
)

from function.date_time import get_brazil_time_now
from function.text import create_text_in_box, escape_for_citation_markdown_v2

from repository.mongo.populate.item import (
    create_random_consumable,
    create_random_equipment
)
from repository.mongo.populate.tools import choice_rarity

from rpgram import GridGame
from rpgram.conditions.factory import factory_condition
from rpgram.enums.debuff import DEBUFF_FULL_NAMES
from rpgram.enums.rarity import RarityEnum
from random import sample


# ROUTES
(
    START_ROUTES,
) = range(1)


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
        minutes = randint(1, 59)
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
    silent = get_attribute_group(chat_id, 'silent')
    rarity = choice_rarity(group_level)
    grid = GridGame(rarity=rarity)
    start_text = choice(GOD_START_NARRATION_TEXTS)
    god_greetings = f'>{GODS_NAME}: {choice(GOD_GREETINGS_TEXTS)}'
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
        disable_notification=silent,
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


@skip_if_no_singup_player
@skip_if_dead_char
@need_not_in_battle
@skip_if_immobilized
@confusion(START_ROUTES)
@print_basic_infos
@retry_after
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

    if grid.is_solved:
        await solved(grid=grid, query=query, context=context)
    elif grid.is_failed:
        await failed(grid=grid, query=query, context=context)
    elif is_good_move is True:
        await good_move(grid=grid, query=query)
    else:
        await bad_move(grid=grid, query=query)


async def solved(
    grid: GridGame,
    query: CallbackQueryHandler,
    context: ContextTypes.DEFAULT_TYPE
):
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    silent = get_attribute_group(chat_id, 'silent')
    text = choice(GOD_WINS_FEEDBACK_TEXTS)
    reply_text_kwargs = dict(
        text=text,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=get_close_keyboard(None),
    )
    remove_grid_from_dict(message_id, context)
    await edit_message_text(grid, query, reply_text_kwargs)
    await add_xp_group(
        chat_id=chat_id,
        context=context,
        silent=silent,
        message_id=message_id,
    )
    await puzzle_drop_random_prize(
        chat_id=chat_id,
        context=context,
        silent=silent,
        rarity=grid.rarity,
    )


async def failed(
    grid: GridGame,
    query: CallbackQueryHandler,
    context: ContextTypes.DEFAULT_TYPE
):
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    silent = get_attribute_group(chat_id, 'silent')
    text = choice(GODS_LOSES_FEEDBACK_TEXTS)
    reply_text_kwargs = dict(
        text=text,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=get_close_keyboard(None),
    )
    await edit_message_text(grid, query, reply_text_kwargs)
    remove_grid_from_dict(message_id, context)
    await punishment(
        chat_id=chat_id,
        context=context,
        silent=silent,
        message_id=message_id,
    )


async def good_move(grid: GridGame, query: CallbackQueryHandler):
    text = choice(GOD_GOOD_MOVE_FEEDBACK_TEXTS)
    grid_buttons = get_grid_buttons(grid)
    reply_markup = InlineKeyboardMarkup(grid_buttons)
    reply_text_kwargs = dict(
        text=text,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=reply_markup,
    )
    await edit_message_text(grid, query, reply_text_kwargs)


async def bad_move(grid: GridGame, query: CallbackQueryHandler):
    text = choice(GOD_BAD_MOVE_FEEDBACK_TEXTS)
    grid_buttons = get_grid_buttons(grid)
    reply_markup = InlineKeyboardMarkup(grid_buttons)
    reply_text_kwargs = dict(
        text=text,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=reply_markup,
    )
    await edit_message_text(grid, query, reply_text_kwargs)


async def edit_message_text(
    grid: GridGame,
    query: CallbackQueryHandler,
    reply_text_kwargs: dict
):
    text = reply_text_kwargs['text']
    section_name = f'{SECTION_TEXT_PUZZLE} {grid.rarity.value.upper()}'
    reply_text_kwargs['text'] = create_text_in_box(
        text=f'>{GODS_NAME}: {text}\n\n{grid.full_colors_text}',
        section_name=section_name,
        section_start=SECTION_HEAD_PUZZLE_START,
        section_end=SECTION_HEAD_PUZZLE_END,
        clean_func=escape_for_citation_markdown_v2,
    )
    await call_telegram_message_function(
        function_caller='SWITCH_PUZZLE_EDIT_MESSAGE_TEXT()',
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


async def add_xp_group(
    chat_id: int,
    context: ContextTypes.DEFAULT_TYPE,
    silent: bool,
    message_id: int = None,
):
    '''Adiciona XP aos jogadores vivos durante a emboscada.
    '''

    full_text = ''
    char_list = get_player_chars_from_group(chat_id=chat_id, is_alive=True)
    sorted_char_list = sorted(
        char_list,
        key=attrgetter('level', 'xp'),
        reverse=True
    )
    for char in sorted_char_list:
        level = (char.level * 2)
        base_xp = int(max(level, 10))
        report_xp = add_xp(
            chat_id=chat_id,
            char=char,
            base_xp=base_xp,
        )
        full_text += f'{report_xp["text"]}\n'

    full_text = create_text_in_box(
        text=full_text,
        section_name=SECTION_TEXT_PUZZLE_XP,
        section_start=SECTION_HEAD_XP_START,
        section_end=SECTION_HEAD_XP_END
    )
    send_message_kwargs = dict(
        chat_id=chat_id,
        text=full_text,
        disable_notification=silent,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_to_message_id=message_id,
        allow_sending_without_reply=True,
        reply_markup=get_close_keyboard(None),
    )

    await call_telegram_message_function(
        function_caller='ADD_XP_GROUP()',
        function=context.bot.send_message,
        **send_message_kwargs
    )


async def puzzle_drop_random_prize(
    chat_id: int,
    context: ContextTypes.DEFAULT_TYPE,
    silent: bool,
    rarity: RarityEnum,
):
    '''Envia uma mensagens de drops de itens quando um aliado defende outro.
    '''

    group_level = get_attribute_group(chat_id, 'group_level')
    char_level_list = get_chars_level_from_group(chat_id=chat_id)
    total_chars = len(char_level_list)
    min_quantity = max(1, total_chars)
    max_quantity = max(2, int(total_chars * 2))
    total_consumables = randint(min_quantity, max_quantity)
    total_equipments = randint(min_quantity, max_quantity)

    consumable_list = list(create_random_consumable(
        group_level=group_level,
        random_level=True,
        total_items=total_consumables
    ))
    all_equipment_list = [
        create_random_equipment(
            equip_type=None,
            group_level=choice(char_level_list),
            rarity=rarity.name,
            random_level=True,
            save_in_database=True,
        )
        for _ in range(total_equipments)
    ]
    drops = [
        item
        for item in (consumable_list + all_equipment_list)
        if item is not None
    ]

    shuffle(drops)
    text = f'{GODS_NAME} deixaram como recompensa'
    await send_drop_message(
        context=context,
        items=drops,
        text=text,
        chat_id=chat_id,
        silent=silent,
    )


async def punishment(
    chat_id: int,
    context: ContextTypes.DEFAULT_TYPE,
    silent: bool,
    message_id: int,
):
    text_list = []
    group_level = get_attribute_group(chat_id, 'group_level')
    char_list = get_player_chars_from_group(chat_id=chat_id, is_alive=True)
    min_ratio_damage = 0.50
    sorted_char_list = sorted(
        char_list,
        key=attrgetter('level', 'xp'),
        reverse=True
    )
    debuff_list = [
        debuff_name.title()
        for debuff_name in DEBUFF_FULL_NAMES.keys()
    ]
    min_debuff_quantity = 0
    max_debuff_quantity = len(debuff_list)
    min_condition_level = int(group_level // 10) + 1
    max_condition_level = min_condition_level * 2
    for char in sorted_char_list:
        report_damage = add_trap_damage(
            min_ratio=min_ratio_damage,
            char=char,
        )
        text = f'{char.player_name} - {report_damage["text"]}\n'

        quantity_sample = randint(min_debuff_quantity, max_debuff_quantity)
        debuff_sample = sample(debuff_list, quantity_sample)
        debuff_sample = [
            factory_condition(
                name=debuff_name,
                level=randint(min_condition_level, max_condition_level)
            )
            for debuff_name in debuff_sample
        ]
        report_condition = add_conditions(
            *debuff_sample,
            char=char,
        )
        text += f'{report_condition["text"]}\n'
        text_list.append(text)

    full_text = f'{TEXT_SEPARATOR_2}\n'.join(text_list)
    full_text = create_text_in_box(
        text=full_text,
        section_name=SECTION_TEXT_PUZZLE_PUNISHMENT,
        section_start=SECTION_HEAD_PUNISHMENT_START,
        section_end=SECTION_HEAD_PUNISHMENT_END
    )
    send_message_kwargs = dict(
        chat_id=chat_id,
        text=full_text,
        disable_notification=silent,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_to_message_id=message_id,
        allow_sending_without_reply=True,
        reply_markup=get_close_keyboard(None),
    )

    await call_telegram_message_function(
        function_caller='PUNISHMENT()',
        function=context.bot.send_message,
        **send_message_kwargs
    )


PUZZLE_HANDLERS = [
    CallbackQueryHandler(switch_puzzle, pattern=PATTERN_PUZZLE),
]
