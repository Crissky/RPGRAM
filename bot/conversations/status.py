from telegram.error import BadRequest
from telegram.ext import ContextTypes
from bot.decorators.job import skip_if_spawn_timeout

from bot.functions.char import activate_conditions
from bot.functions.chat import MIN_AUTODELETE_TIME, send_private_message
from bot.functions.player import get_player_verbose, get_players_id_by_chat_id
from constant.text import (
    SECTION_HEAD_STATUS_END,
    SECTION_HEAD_STATUS_START,
    TEXT_SEPARATOR
)
from function.date_time import get_brazil_time_now
from function.text import create_text_in_box

from repository.mongo import CharacterModel
from rpgram.characters import BaseCharacter


@skip_if_spawn_timeout
async def job_activate_conditions(context: ContextTypes.DEFAULT_TYPE):
    char_model = CharacterModel()
    job = context.job
    chat_id = job.chat_id
    now = get_brazil_time_now()

    print(f'JOB_ACTIVATE_CONDITIONS() - {now}')
    player_id_list = get_players_id_by_chat_id(chat_id=chat_id)
    player_id_list = char_model.get_all(
        query={
            'status.condition_args': {
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
        verbose = get_player_verbose(player_id)

        if not player_char or player_char.is_dead:
            continue

        report = activate_conditions(char=player_char)
        text = report['text']
        have_debuff = report.get('have_debuff')
        if text and (have_debuff or verbose):
            if not player_char.status.is_empty:
                text += f'{TEXT_SEPARATOR}\n\n'
                text += player_char.status.get_condition_full_names()
            text = create_text_in_box(
                text=text,
                section_name='STATUS REPORT',
                section_start=SECTION_HEAD_STATUS_START,
                section_end=SECTION_HEAD_STATUS_END,
            )
            try:
                await send_private_message(
                    function_caller='JOB_ACTIVATE_CONDITIONS()',
                    context=context,
                    text=text,
                    user_id=player_id,
                    chat_id=chat_id,
                    markdown=True,
                    close_by_owner=False,
                    auto_delete_message=MIN_AUTODELETE_TIME,
                )
            except BadRequest as e:
                if  str(e).startswith("Can't parse entities"):
                    await send_private_message(
                        function_caller='JOB_ACTIVATE_CONDITIONS()',
                        context=context,
                        text=text,
                        user_id=player_id,
                        chat_id=chat_id,
                        markdown=False,
                        close_by_owner=False,
                        auto_delete_message=MIN_AUTODELETE_TIME,
                    )
                else:
                    raise
        else:
            print(
                f'REPORT DE JOB_ACTIVATE_CONDITIONS SKIPPADO PARA '
                f'{player_char.player_name}({player_id}), '
                f'have_debuff: {have_debuff}, '
                f'verbose: {verbose}, '
                f'text: "{text}"'
            )
