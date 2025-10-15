from datetime import timedelta
from random import choice, randint
from typing import List

from bson import ObjectId
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    PrefixHandler
)

from bot.constants.filters import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.constants.job import BASE_JOB_KWARGS
from bot.constants.picross import (
    GOD_BAD_MOVE_FEEDBACK_TEXTS,
    GOD_GREETINGS_TEXTS,
    GOD_START_NARRATION_TEXTS,
    GOD_WINS_FEEDBACK_TEXTS,
    GODS_LOSES_FEEDBACK_TEXTS,
    GODS_NAME,
    GODS_TIMEOUT_FEEDBACK_TEXTS,
    PATTERN_PICROSS,
    PATTERN_TOGGLE_PICROSS,
    SECTION_TEXT_PICROSS
)
from bot.decorators.job import skip_if_spawn_timeout
from bot.functions.char import add_xp_group, bad_move_damage, punishment
from bot.functions.chat import (
    REPLY_MARKUP_DEFAULT,
    call_telegram_message_function,
    callback_data_to_dict,
    callback_data_to_string,
    edit_message_text
)
from bot.functions.config import get_attribute_group, is_group_spawn_time

from bot.functions.item import drop_random_prize
from bot.functions.job import remove_job_by_name
from bot.functions.keyboard import reshape_row_buttons
from constant.text import (
    SECTION_HEAD_PUZZLE_BADMOVE_END,
    SECTION_HEAD_PUZZLE_BADMOVE_START,
    SECTION_HEAD_PUZZLE_COMPLETE_END,
    SECTION_HEAD_PUZZLE_COMPLETE_START,
    SECTION_HEAD_PUZZLE_END,
    SECTION_HEAD_PUZZLE_START,
    SECTION_HEAD_TIMEOUT_PUNISHMENT_PUZZLE_END,
    SECTION_HEAD_TIMEOUT_PUNISHMENT_PUZZLE_START,
    SECTION_HEAD_TIMEOUT_PUZZLE_END,
    SECTION_HEAD_TIMEOUT_PUZZLE_START
)
from function.text import create_text_in_box, escape_for_citation_markdown_v2
from repository.mongo.populate.tools import choice_rarity

from rpgram.enums.rarity import RarityEnum
from rpgram.minigames.picross.picross import PicrossGame


@skip_if_spawn_timeout
async def job_start_picross(context: ContextTypes.DEFAULT_TYPE):
    '''Envia a mensagem com o Picross de Xochipilli.

    Xochipilli: Deus Asteca das flores, arte, música e dança.
    '''

    print('JOB_START_PICROSS()')
    job = context.job
    chat_id = job.chat_id
    group_level = get_attribute_group(chat_id, 'group_level')
    silent = get_attribute_group(chat_id, 'silent')
    rarity = choice_rarity(group_level)
    picross = PicrossGame(rarity=rarity)
    picross.generate_random_picross()
    start_text = choice(GOD_START_NARRATION_TEXTS)
    god_greetings = f'>{GODS_NAME}: {choice(GOD_GREETINGS_TEXTS)}'
    text = f'{start_text}\n\n{god_greetings}\n\n```{picross.text}```'
    section_name = (
        f'{SECTION_TEXT_PICROSS} {picross.rarity.value.upper()} '
        f'{picross.width}✖{picross.height}'
    )
    picross_buttons = get_picross_buttons(picross)
    reply_markup = InlineKeyboardMarkup(picross_buttons)
    minutes = randint(120, 180)
    text = create_text_in_box(
        text=text,
        section_name=section_name,
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
        function_caller='JOB_START_PICROSS()',
        function=context.bot.send_message,
        context=context,
        **reply_text_kwargs
    )
    message_id = response.message_id
    job_name = get_picross_job_name(message_id)
    put_picross_in_dict(
        context=context,
        message_id=message_id,
        picross=picross
    )
    context.job_queue.run_once(
        callback=job_timeout_picross,
        when=timedelta(minutes=minutes),
        data=dict(message_id=message_id),
        chat_id=chat_id,
        name=job_name,
        job_kwargs=BASE_JOB_KWARGS,
    )


async def job_timeout_picross(context: ContextTypes.DEFAULT_TYPE):
    ''' Causa dano e Status aos jogadores caso o tempo para concluir o 
    picross encerre. Mas se já estiver fora do horário de spawn, o 
    deus irá embora.
    '''

    print('JOB_TIMEOUT_PICROSS()')
    job = context.job
    chat_id = job.chat_id
    data = job.data
    message_id = data['message_id']
    is_spawn_time = is_group_spawn_time(chat_id)
    picross = get_picross_from_dict(context=context, message_id=message_id)
    section_name = f'{SECTION_TEXT_PICROSS} {picross.rarity.value.upper()}'

    if not is_spawn_time:
        text = (
            'Pois, é chegada a hora tardia em que necessito me retirar '
            'para o meu augusto domínio, e por isso, em minha '
            'magnanimidade, concedo-lhes o perdão. Assim, '
            'não lhes lançarei minha maldição.'
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
        text=f'>{GODS_NAME}: {text}\n\n{picross.text}',
        section_name=section_name,
        section_start=section_start,
        section_end=section_end,
        clean_func=escape_for_citation_markdown_v2,
    )
    await edit_message_text(
        function_caller='JOB_TIMEOUT_PICROSS()',
        new_text=text,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        need_response=False,
        markdown=True
    )
    remove_picross_from_dict(context=context, message_id=message_id)


async def switch_picross(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('SWITCH_PICROSS()')
    query = update.callback_query
    chat_id = query.message.chat_id
    user_id = query.from_user.id
    message_id = query.message.message_id
    player_name = query.from_user.name
    silent = get_attribute_group(chat_id, 'silent')
    picross = get_picross_from_dict(context=context, message_id=message_id)
    data = callback_data_to_dict(query.data)
    picross_row = data['picross_row']
    picross_col = data['picross_col']

    if picross is None:
        new_text = 'Esse desafio não existe mais.'
        await edit_message_text(
            function_caller='PICROSS.TOGGLE_PICROSS()',
            new_text=new_text,
            context=context,
            chat_id=chat_id,
            message_id=message_id,
            need_response=False,
            markdown=False,
        )

        return ConversationHandler.END

    move = picross.make_move(n_row=picross_row, n_col=picross_col)
    picross_buttons = get_picross_buttons(picross)
    reply_markup = InlineKeyboardMarkup(picross_buttons)
    if picross.check_win():  # Ganhou
        text = choice(GOD_WINS_FEEDBACK_TEXTS)
        prize_text = f'{GODS_NAME} deixou como recompensa'
        remove_timeout_puzzle_job(context=context, message_id=message_id)
        remove_picross_from_dict(context=context, message_id=message_id)
        await picross_edit_message_text(
            picross=picross,
            text=text,
            player_name=player_name,
            context=context,
            message_id=message_id,
            section_start=SECTION_HEAD_PUZZLE_COMPLETE_START,
            section_end=SECTION_HEAD_PUZZLE_COMPLETE_END,
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
            rarity=picross.rarity,
            message_id=message_id,
            text=prize_text,
        )
    elif move is False:  # Movimento errado
        text = choice(GOD_BAD_MOVE_FEEDBACK_TEXTS)
        damage_text = bad_move_damage(
            user_id=user_id,
            multiplier=2.0
        )
        text += f'\n\n{damage_text}'
        await picross_edit_message_text(
            picross=picross,
            text=text,
            player_name=player_name,
            context=context,
            message_id=message_id,
            section_start=SECTION_HEAD_PUZZLE_BADMOVE_START,
            section_end=SECTION_HEAD_PUZZLE_BADMOVE_END,
            reply_markup=reply_markup
        )
    else:  # Ação válida
        mark_text = picross.current_mark_text
        text = (
            f'Ação {mark_text} na '
            f'Linha **{picross_row+1}** e Coluna: **{picross_col+1}**'
        )
        await picross_edit_message_text(
            picross=picross,
            text=text,
            player_name=player_name,
            context=context,
            message_id=message_id,
            reply_markup=reply_markup
        )


async def toggle_picross(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('TOGGLE_PICROSS()')
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    player_name = query.from_user.name
    picross = get_picross_from_dict(context=context, message_id=message_id)
    data = callback_data_to_dict(query.data)
    action_picross_toggle = data['action_picross_toggle']

    if picross is None:
        new_text = 'Esse desafio não existe mais.'
        await edit_message_text(
            function_caller='PICROSS.TOGGLE_PICROSS()',
            new_text=new_text,
            context=context,
            chat_id=chat_id,
            message_id=message_id,
            need_response=False,
            markdown=False,
        )

        return ConversationHandler.END

    picross.toggle_mark()
    picross_buttons = get_picross_buttons(picross)
    reply_markup = InlineKeyboardMarkup(picross_buttons)
    await picross_edit_message_text(
        picross=picross,
        text=f'A marca foi mudada para {picross.current_mark_text}',
        player_name=player_name,
        context=context,
        message_id=message_id,
        reply_markup=reply_markup
    )


async def picross_edit_message_text(
    picross: PicrossGame,
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
        section_name = (
            f'{SECTION_TEXT_PICROSS} {picross.rarity.value.upper()} '
            f'{picross.width}✖{picross.height}'
        )
    if not isinstance(section_start, str):
        section_start = SECTION_HEAD_PUZZLE_START
    if not isinstance(section_end, str):
        section_end = SECTION_HEAD_PUZZLE_END

    text = (
        f'>{GODS_NAME}: {text}\n\n'
        f'Jogada: {player_name}\n\n'
        f'```{picross.text}```\n'
    )
    text = create_text_in_box(
        text=text,
        section_name=section_name,
        section_start=section_start,
        section_end=section_end,
        clean_func=escape_for_citation_markdown_v2,
    )
    await edit_message_text(
        function_caller='PICROSS_EDIT_MESSAGE_TEXT()',
        new_text=text,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        need_response=True,
        markdown=True,
        reply_markup=reply_markup
    )


def get_picross_buttons(
    picross: PicrossGame
) -> List[List[InlineKeyboardButton]]:
    n_cols = picross.width
    buttons = []
    for coor in picross:
        button = InlineKeyboardButton(
            text=f'{coor["text"]}',
            callback_data=callback_data_to_string({
                'picross_row': coor["row"],
                'picross_col': coor["col"],
            }),
        )
        buttons.append(button)

    toggle_button = InlineKeyboardButton(
        text=f'ALTERNAR ({picross.current_mark_text})',
        callback_data=callback_data_to_string({
            'action_picross_toggle': 1,
        }),
    )
    buttons = reshape_row_buttons(
        buttons=buttons,
        buttons_per_row=n_cols,
    )
    buttons.append([toggle_button])

    return buttons


def get_picross_job_name(message_id):
    return f'JOB_TIMEOUT_PICROSS_{message_id}'


def remove_timeout_puzzle_job(
    context: ContextTypes.DEFAULT_TYPE,
    message_id: int,
) -> bool:
    '''Remove o job de Timeout do Puzzle.
    '''

    job_name = get_picross_job_name(message_id=message_id)
    return remove_job_by_name(context=context, job_name=job_name)


def put_picross_in_dict(
    context: ContextTypes.DEFAULT_TYPE,
    message_id: int,
    picross: PicrossGame,
):
    '''Adiciona o picross ao dicionário de Picrosses, em que a chave é a 
    message_id.
    '''

    print('PICROSS.PUT_PICROSS_IN_DICT()')
    picrosses = context.chat_data.get('picrosses', {})
    picrosses[message_id] = {'picross': picross}
    if not 'picrosses' in context.chat_data:
        context.chat_data['picrosses'] = picrosses


def get_picross_from_dict(
    context: ContextTypes.DEFAULT_TYPE,
    message_id: int,
) -> PicrossGame:

    print('PICROSS.GET_PICROSS_FROM_DICT()')
    picrosses = context.chat_data.get('picrosses', {})
    picross_dict = picrosses.get(message_id, {})
    picross = picross_dict.get('picross', None)

    return picross


def remove_picross_from_dict(
    context: ContextTypes.DEFAULT_TYPE,
    message_id: int,
):

    print('PICROSS.REMOVE_PICROSS_FROM_DICT()')
    picrosses = context.chat_data.get('picrosses', {})
    picrosses.pop(message_id, None)
    context.chat_data['picrosses'] = picrosses


PICROSS_HANDLERS = [
    CallbackQueryHandler(switch_picross, pattern=PATTERN_PICROSS),
    CallbackQueryHandler(toggle_picross, pattern=PATTERN_TOGGLE_PICROSS),
]
