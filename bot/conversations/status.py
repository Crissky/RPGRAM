from telegram.error import Forbidden
from telegram.ext import ContextTypes
from bot.decorators.job import skip_if_spawn_timeout

from bot.functions.char import activate_conditions
from bot.functions.general import get_attribute_group_or_player
from constant.text import TEXT_SEPARATOR
from function.date_time import get_brazil_time_now

from repository.mongo import GroupModel, StatusModel
from rpgram.enums import EmojiEnum


@skip_if_spawn_timeout
async def job_activate_conditions(context: ContextTypes.DEFAULT_TYPE):
    status_model = StatusModel()
    job = context.job
    chat_id = int(job.chat_id)  # chat_id vem como string
    now = get_brazil_time_now()

    print(f'JOB_ACTIVATE_CONDITIONS() - {now}')
    player_id_list = status_model.get_all(
        query={
            'condition_args': {
                '$exists': True, '$not': {'$size': 0}
            }
        },
        fields=['player_id']
    )

    for player_id in player_id_list:
        print('player_id:', player_id)
        report = activate_conditions(user_id=player_id)
        print('report:', report)
        text = report['text']
        if text:
            text = f'{EmojiEnum.STATUS.value}STATUS REPORT:\n\n' + text
            text += f'{TEXT_SEPARATOR}\n\n'
            text += report['all_status_verbose']
            try:
                silent = get_attribute_group_or_player(player_id, 'silent')
                await context.bot.send_message(
                    chat_id=player_id,
                    text=text,
                )
            except Forbidden as error:
                silent = get_attribute_group_or_player(chat_id, 'silent')
                member = await context.bot.get_chat_member(
                    chat_id=chat_id,
                    user_id=player_id
                )
                user_name = member.user.name
                text = f'{user_name}\n{text}'
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    disable_notification=silent,
                )
