from datetime import timedelta
from typing import Callable, Optional
from bson import ObjectId
from telegram import Update
from telegram.ext import ContextTypes, PrefixHandler, CommandHandler

from bot.constants.game_debug import COMMANDS
from bot.constants.filters import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.constants.job import BASE_JOB_KWARGS
from bot.conversations.picross import job_start_picross
from bot.conversations.puzzle import job_start_puzzle
from bot.conversations.word_game import job_start_wordgame
from bot.functions.chat import call_telegram_message_function
from bot.functions.config import get_attribute_group


async def create_game_event(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    chat_id = context._chat_id
    args = context.args
    job_start_name = args[0] if args else None
    job_callback = select_job_start_game(job_start_name)
    silent = get_attribute_group(chat_id, 'silent')
    reply_text_kwargs = dict(
        chat_id=chat_id,
        disable_notification=silent,
        allow_sending_without_reply=True,
    )

    if job_callback:
        job_callback_name = job_callback.__name__.upper()
        job_name = f'{job_callback_name}_{ObjectId()}'
        text = f'UM {job_callback_name} FOI CRIADO! 5 SEGUNDOS PARA COMEÇAR'
        reply_text_kwargs['text'] = text.upper()
        context.job_queue.run_once(
            callback=job_callback,
            when=timedelta(seconds=5),
            chat_id=chat_id,
            name=job_name,
            job_kwargs=BASE_JOB_KWARGS,
        )
    else:
        text = f'JOGO NÃO ENCONTRADO. USE UM ARG VÁLIDO ({args}).'
        reply_text_kwargs['text'] = text

    await call_telegram_message_function(
        function_caller='CREATE_GAME_EVENT()',
        function=context.bot.send_message,
        context=context,
        **reply_text_kwargs
    )


def select_job_start_game(job_start_name: str) -> Optional[Callable]:
    if not isinstance(job_start_name, str):
        return None

    job_callback = None
    event_name = job_start_name.lower()

    if event_name == 'puzzle':
        job_callback = job_start_puzzle
    elif event_name == 'wordgame':
        job_callback = job_start_wordgame
    elif event_name == 'picross':
        job_callback = job_start_picross

    return job_callback


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
