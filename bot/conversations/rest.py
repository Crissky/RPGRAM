from datetime import timedelta
from random import choice

from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    PrefixHandler,
)

from bot.constants.filters import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.constants.rest import (
    COMMANDS,
    REPLY_TEXTS_ALREADY_RESTING,
    REPLY_TEXTS_NO_NEED_REST,
    REPLY_TEXTS_STARTING_REST,
    SECTION_TEXT_REST
)
from bot.decorators import (
    need_not_in_battle,
    print_basic_infos,
    skip_if_no_have_char,
    skip_if_no_singup_player,
)
from bot.functions.chat import send_private_message
from bot.functions.general import get_attribute_group_or_player
from constant.text import SECTION_HEAD_REST_END, SECTION_HEAD_REST_START
from function.text import create_text_in_box

from repository.mongo import BattleModel, CharacterModel, PlayerModel


@skip_if_no_singup_player
@skip_if_no_have_char
@need_not_in_battle
@print_basic_infos
async def rest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    char_model = CharacterModel()
    battle_model = BattleModel()
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    job_name = get_rest_jobname(user_id)
    current_jobs = context.job_queue.get_jobs_by_name(job_name)
    silent = get_attribute_group_or_player(chat_id, 'silent')
    player_character = char_model.get(user_id)
    character_id = player_character._id
    current_hp = player_character.cs.show_hit_points
    battle = battle_model.get(query={
        '$or': [{'blue_team': character_id}, {'red_team': character_id}]
    })

    if battle:
        text = 'Você não pode descansar, pois está em batalha.'
    elif current_jobs:
        reply_text_already_resting = choice(REPLY_TEXTS_ALREADY_RESTING)
        text = (
            f'{reply_text_already_resting}\n\n'
            f'HP: {current_hp}'
        )
    elif player_character.is_healed:
        reply_text_no_need_rest = choice(REPLY_TEXTS_NO_NEED_REST)
        text = (
            f'{reply_text_no_need_rest}\n\n'
            f'HP: {current_hp}'
        )
    else:
        context.job_queue.run_repeating(
            callback=job_rest_cure,
            interval=timedelta(hours=1),
            chat_id=chat_id,
            user_id=user_id,
            name=job_name,
            data=user_id
        )
        reply_text_starting_rest = choice(REPLY_TEXTS_STARTING_REST)
        text = (
            f'{reply_text_starting_rest}\n\n'
            f'HP: {current_hp}\n\n'
            f'Seu personagem irá recuperar HP a cada hora.'
        )
    await update.message.reply_text(
        text=text,
        disable_notification=silent
    )


async def job_rest_cure(context: ContextTypes.DEFAULT_TYPE):
    char_model = CharacterModel()
    player_model = PlayerModel()
    job = context.job
    chat_id = job.chat_id
    user_id = job.user_id
    player_character = char_model.get(user_id)
    player = player_model.get(user_id)
    revive_reporting = ''
    if player_character.is_dead:
        report = player_character.cs.revive()
        revive_reporting = '🧚‍♂️REVIVEU🧚‍♀️\n\n'
    else:
        max_hp = player_character.cs.hp
        heal = int(max_hp * 0.18)
        report = player_character.cs.cure_hit_points(heal)
    char_model.save(player_character)
    report_text = report['text']
    hp_reporting = (
        f'{revive_reporting}'
        f'Seu personagem curou HP❤️‍🩹 descansando!\n\n'
        f'{report_text}\n\n'
    )

    if player_character.is_healed:
        job.schedule_removal()
        text = (
            f'{hp_reporting}'
            f'O HP do seu personagem está completamente recuperado. '
            f'O descanso foi finalizado.'
        )

    else:
        text = f'{hp_reporting} Seu personagem continua descansando…'

    text = create_text_in_box(
        text=text,
        section_name=SECTION_TEXT_REST,
        section_start=SECTION_HEAD_REST_START,
        section_end=SECTION_HEAD_REST_END,
    )

    if player.verbose:
        await send_private_message(
            function_caller='JOB_REST_CURE()',
            context=context,
            text=text,
            user_id=job.user_id,
        )


def stop_resting(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    job_name = get_rest_jobname(user_id)
    current_jobs = context.job_queue.get_jobs_by_name(job_name)
    print('current_jobs', current_jobs)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def get_rest_jobname(user_id):
    return f'REST-{user_id}'


REST_HANDLERS = [
    PrefixHandler(
        PREFIX_COMMANDS,
        COMMANDS,
        rest,
        BASIC_COMMAND_FILTER
    ),
    CommandHandler(
        COMMANDS,
        rest,
        BASIC_COMMAND_FILTER
    )
]
