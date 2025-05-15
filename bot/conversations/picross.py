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
    PrefixHandler
)

from bot.constants.filters import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.constants.job import BASE_JOB_KWARGS
from bot.constants.picross import (
    GOD_GREETINGS_TEXTS,
    GOD_START_NARRATION_TEXTS,
    GODS_LOSES_FEEDBACK_TEXTS,
    GODS_NAME,
    GODS_TIMEOUT_FEEDBACK_TEXTS,
    PATTERN_PICROSS,
    SECTION_TEXT_PICROSS
)
from bot.decorators.job import skip_if_spawn_timeout
from bot.functions.char import punishment
from bot.functions.chat import (
    call_telegram_message_function,
    callback_data_to_string,
    edit_message_text
)
from bot.functions.config import get_attribute_group, is_group_spawn_time

from bot.functions.keyboard import reshape_row_buttons
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
    # rarity = choice_rarity(group_level)
    rarity = RarityEnum.MYTHIC
    picross = PicrossGame(rarity=rarity)
    picross.generate_random_puzzle()
    start_text = choice(GOD_START_NARRATION_TEXTS)
    # god_greetings = f'>{GODS_NAME}: {choice(GOD_GREETINGS_TEXTS)}'
    god_greetings = f'>{choice(GOD_GREETINGS_TEXTS)}'
    text = f'{start_text}\n\n{god_greetings}\n\n```{picross.text}```'
    picross_buttons = get_picross_buttons(picross)
    minutes = randint(120, 180)
    reply_markup = InlineKeyboardMarkup(picross_buttons)

    text = create_text_in_box(
        text=text,
        section_name=SECTION_TEXT_PICROSS,
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
        callback=job_timeout_puzzle,
        when=timedelta(minutes=minutes),
        data=dict(message_id=message_id),
        chat_id=chat_id,
        name=job_name,
        job_kwargs=BASE_JOB_KWARGS,
    )


