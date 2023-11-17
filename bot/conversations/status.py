from telegram.error import Forbidden
from telegram.ext import ContextTypes

from bot.functions.char import activate_conditions
from bot.functions.general import get_attribute_group_or_player

from repository.mongo import StatusModel
from rpgram.enums import EmojiEnum


async def job_activate_conditions(context: ContextTypes.DEFAULT_TYPE):
    status_model = StatusModel()
    job = context.job
    chat_id = int(job.chat_id)  # chat_id vem como string
    silent = get_attribute_group_or_player(chat_id, 'silent')

    player_ids = status_model.get_all(
        query={
            'condition_ids': {
                '$exists': True, '$not': {'$size': 0}
            }
        },
        fields=['player_id']
    )

    for player_id in player_ids:
        print('player_id:', player_id)
        report = activate_conditions(user_id=player_id)
        print('report:', report)
        text = report['text']
        if text:
            text = f'{EmojiEnum.STATUS.value}STATUS REPORT:\n\n' + text
            try:
                await context.bot.send_message(
                    chat_id=player_id,
                    text=text,
                )
            except Forbidden as error:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    disable_notification=silent,
                )
