from telegram.ext import ContextTypes
from bot.decorators.job import skip_if_spawn_timeout

from bot.functions.char import activate_conditions
from bot.functions.chat import send_private_message
from bot.functions.player import get_players_id_by_chat_id
from constant.text import (
    SECTION_HEAD_STATUS_END,
    SECTION_HEAD_STATUS_START,
    TEXT_SEPARATOR
)
from function.date_time import get_brazil_time_now
from function.text import create_text_in_box

from repository.mongo import CharacterModel, StatusModel
from rpgram.characters import BaseCharacter


@skip_if_spawn_timeout
async def job_activate_conditions(context: ContextTypes.DEFAULT_TYPE):
    status_model = StatusModel()
    job = context.job
    chat_id = job.chat_id
    now = get_brazil_time_now()

    print(f'JOB_ACTIVATE_CONDITIONS() - {now}')
    player_id_list = get_players_id_by_chat_id(chat_id=chat_id)
    player_id_list = status_model.get_all(
        query={
            'condition_args': {
                '$exists': True, '$not': {'$size': 0}
            },
            'player_id': {'$in': player_id_list}
        },
        fields=['player_id']
    )

    for player_id in player_id_list:
        print('player_id:', player_id)
        char_model = CharacterModel()
        player_char: BaseCharacter = char_model.get(player_id)

        if not player_char or player_char.is_dead:
            continue

        report = activate_conditions(char=player_char)
        text = report['text']
        if text:
            text += f'{TEXT_SEPARATOR}\n\n'
            text += report['all_status_verbose']
            text = create_text_in_box(
                text=text,
                section_name='STATUS REPORT',
                section_start=SECTION_HEAD_STATUS_START,
                section_end=SECTION_HEAD_STATUS_END,
            )
            await send_private_message(
                function_caller='JOB_ACTIVATE_CONDITIONS()',
                context=context,
                text=text,
                user_id=player_id,
                chat_id=chat_id,
                markdown=True
            )
