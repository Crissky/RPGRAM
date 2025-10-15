from datetime import timedelta
from bson import ObjectId
from telegram import Update
from telegram.ext import ContextTypes, PrefixHandler, CommandHandler

from bot.constants.game_debug import COMMANDS
from bot.constants.filters import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.constants.job import BASE_JOB_KWARGS
from bot.conversations.picross import job_start_picross
from bot.functions.chat import call_telegram_message_function
from bot.functions.config import get_attribute_group


async def create_game_event(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    chat_id = context._chat_id
    args = context.args
    job_callback = job_start_picross
    job_callback_name = job_callback.__name__.upper()
    job_name = f'{job_callback_name}_{ObjectId()}'
    context.job_queue.run_once(
        callback=job_callback,
        when=timedelta(seconds=5),
        chat_id=chat_id,
        name=job_name,
        job_kwargs=BASE_JOB_KWARGS,
    )

    text = 'UM PICROSS FOI CRIADO! 5 SEGUNDOS PARA COMEÇAR'
    silent = get_attribute_group(chat_id, 'silent')
    reply_text_kwargs = dict(
        chat_id=chat_id,
        text=text,
        disable_notification=silent,
        allow_sending_without_reply=True,
    )
    response = await call_telegram_message_function(
        function_caller='JOB_START_PICROSS()',
        function=context.bot.send_message,
        context=context,
        **reply_text_kwargs
    )


GAME_DEBUG_HANDLERS = [
    PrefixHandler(
        PREFIX_COMMANDS,
        COMMANDS,
        create_game_event,
        BASIC_COMMAND_FILTER
    ),
    CommandHandler(
        COMMANDS,
        create_game_event,
        BASIC_COMMAND_FILTER
    )
]