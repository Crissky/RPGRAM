from datetime import timedelta
from random import choice, randint
from typing import List

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import CallbackQueryHandler, ContextTypes

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

from rpgram.minigames.picross.picross import PicrossGame

@skip_if_spawn_timeout
async def job_start_picross(context: ContextTypes.DEFAULT_TYPE):
