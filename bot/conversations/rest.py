from datetime import timedelta
from random import choice, randint
from typing import List

from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    PrefixHandler,
)

from bot.constants.filters import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.constants.job import BASE_JOB_KWARGS
from bot.constants.rest import (
    COMMANDS,
    MINUTES_TO_RECOVERY_ACTION_POINTS,
    MINUTES_TO_RECOVERY_HIT_POINTS,
    REPLY_TEXT_REST_INDAY,
    REPLY_TEXT_REST_MIDDAY,
    REPLY_TEXT_REST_MIDNIGHT,
    REPLY_TEXTS_ALREADY_RESTING,
    REPLY_TEXTS_NO_NEED_REST,
    REPLY_TEXTS_STARTING_REST,
    SECTION_TEXT_ACTION_PONTOS,
    SECTION_TEXT_REST,
    SECTION_TEXT_REST_MIDNIGHT,
    SECTION_TEXT_WAKEUP
)
from bot.decorators import (
    print_basic_infos,
    skip_if_no_have_char,
    skip_if_no_singup_player,
)
from bot.functions.bag import TENT, have_tent, sub_tent_from_bag
from bot.functions.char import save_char
from bot.functions.chat import (
    MIN_AUTODELETE_TIME,
    call_telegram_message_function,
    get_close_keyboard,
    send_private_message
)
from bot.functions.config import get_attribute_group
from bot.functions.general import get_attribute_group_or_player
from bot.functions.player import get_players_id_by_chat_id
from constant.text import (
    SECTION_HEAD_ACTION_POINTS_END,
    SECTION_HEAD_ACTION_POINTS_START,
    SECTION_HEAD_REST_END,
    SECTION_HEAD_REST_INDAY_END,
    SECTION_HEAD_REST_INDAY_START,
    SECTION_HEAD_REST_MIDDAY_END,
    SECTION_HEAD_REST_MIDDAY_START,
    SECTION_HEAD_REST_MIDNIGHT_END,
    SECTION_HEAD_REST_MIDNIGHT_START,
    SECTION_HEAD_REST_START,
    SECTION_HEAD_WAKEUP_END,
    SECTION_HEAD_WAKEUP_START
)
from function.date_time import get_brazil_time_now
from function.text import create_text_in_box

from repository.mongo import CharacterModel, PlayerModel
from rpgram import Player
from rpgram.characters import BaseCharacter


@skip_if_no_singup_player
@skip_if_no_have_char
@print_basic_infos
async def rest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Comando que inicia o descanso do personagem.
    O descanso faz com que o personagem recupere HP a cada 
    "MINUTES_TO_RECOVERY_HIT_POINTS" minutos.
    Se o personagem estiver morto, ele reviverá e recuperará 1 de HP 
    em "MINUTES_TO_RECOVERY_HIT_POINTS" minutos.'''

    char_model = CharacterModel()
    player_model = PlayerModel()
    chat_id = update.effective_chat.id
    caller_user_id = update.effective_user.id
    silent = get_attribute_group_or_player(chat_id, 'silent')
    caller_have_tent = have_tent(caller_user_id)
    args = context.args or []
    user_id_list = [caller_user_id]
    player_name_list = [name for name in args if name.startswith('@')]

    if player_name_list and caller_have_tent:
        player_name = args[0]
        user_id_list = []
        m_query = {'name': {'$in': player_name_list}}
        player_list: List[Player] = player_model.get_all(query=m_query)
        for player in player_list:
            caller_have_tent = have_tent(caller_user_id)
            if not caller_have_tent:
                break
            if player:
                user_id_list.append(player.player_id)
                sub_tent_from_bag(user_id=caller_user_id)
            else:
                text = create_text_in_box(
                    text=f'{player_name} não foi encontrado.',
                    section_name=SECTION_TEXT_REST,
                    section_start=SECTION_HEAD_REST_START,
                    section_end=SECTION_HEAD_REST_END,
                    clean_func=None,
                )
                reply_text_kwargs = dict(
                    text=text,
                    disable_notification=silent,
                    allow_sending_without_reply=True,
                    reply_markup=get_close_keyboard(user_id=caller_user_id)
                )

                await call_telegram_message_function(
                    function_caller='REST.REST()',
                    function=update.effective_message.reply_text,
                    context=context,
                    need_response=False,
                    skip_retry=False,
                    auto_delete_message=MIN_AUTODELETE_TIME,
                    **reply_text_kwargs,
                )
    elif player_name_list and not caller_have_tent:
        player_name = args[0]
        text = (
            f'Você não tem um "{TENT}" para ajudar o descanso de '
            f'{player_name}.'
        )
        text = create_text_in_box(
            text=text,
            section_name=SECTION_TEXT_REST,
            section_start=SECTION_HEAD_REST_START,
            section_end=SECTION_HEAD_REST_END,
            clean_func=None,
        )
        reply_text_kwargs = dict(
            text=text,
            disable_notification=silent,
            allow_sending_without_reply=True,
            reply_markup=get_close_keyboard(user_id=caller_user_id)
        )

        return await call_telegram_message_function(
            function_caller='REST.REST()',
            function=update.effective_message.reply_text,
            context=context,
            need_response=False,
            skip_retry=False,
            auto_delete_message=MIN_AUTODELETE_TIME,
            **reply_text_kwargs,
        )

    for user_id in user_id_list:
        job_name = get_rest_jobname(user_id=user_id)
        current_jobs = context.job_queue.get_jobs_by_name(job_name)
        player_character: BaseCharacter = char_model.get(user_id)
        current_hp = player_character.cs.show_hit_points
        debuffs_text = player_character.status.debuffs_text
        char_name = (
            f'{player_character.name}, '
            f'O {player_character.race_name} {player_character.classe_name}'
        )

        if current_jobs:
            reply_text_already_resting = choice(REPLY_TEXTS_ALREADY_RESTING)
            reply_text_already_resting = reply_text_already_resting.format(
                char_name=char_name
            )
            text = (
                f'{reply_text_already_resting}\n\n'
                f'HP: {current_hp}\n'
                f'Status: {debuffs_text}.'
            )
        elif player_character.is_healed and not player_character.is_debuffed:
            reply_text_no_need_rest = choice(REPLY_TEXTS_NO_NEED_REST)
            reply_text_no_need_rest = reply_text_no_need_rest.format(
                char_name=char_name
            )
            text = (
                f'{reply_text_no_need_rest}\n\n'
                f'HP: {current_hp}\n'
                f'Status: {debuffs_text}.'
            )
        else:
            create_job_rest_cure(
                context=context,
                chat_id=chat_id,
                user_id=user_id,
            )
            reply_text_starting_rest = choice(REPLY_TEXTS_STARTING_REST)
            reply_text_starting_rest = reply_text_starting_rest.format(
                char_name=char_name
            )
            text = (
                f'{reply_text_starting_rest}\n\n'
                f'HP: {current_hp}\n'
                f'Status: {debuffs_text}\n\n'
                f'{player_character.player_name} '
                f'irá recuperar HP e Status a cada '
                f'{MINUTES_TO_RECOVERY_HIT_POINTS} minutos.'
            )

        create_job_rest_action_point(
            context=context,
            chat_id=chat_id,
            user_id=user_id,
        )
        text = create_text_in_box(
            text=text,
            section_name=SECTION_TEXT_REST,
            section_start=SECTION_HEAD_REST_START,
            section_end=SECTION_HEAD_REST_END,
            clean_func=None,
        )
        reply_text_kwargs = dict(
            text=text,
            disable_notification=silent,
            allow_sending_without_reply=True,
            reply_markup=get_close_keyboard(user_id=caller_user_id)
        )

        await call_telegram_message_function(
            function_caller='REST.REST()',
            function=update.effective_message.reply_text,
            context=context,
            need_response=False,
            skip_retry=False,
            auto_delete_message=MIN_AUTODELETE_TIME,
            **reply_text_kwargs,
        )


def create_job_rest_cure(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    user_id: int,
):
    job_name = get_rest_jobname(user_id)
    context.job_queue.run_repeating(
        callback=job_rest_cure,
        interval=timedelta(minutes=MINUTES_TO_RECOVERY_HIT_POINTS),
        chat_id=chat_id,
        user_id=user_id,
        data=user_id,
        name=job_name,
        job_kwargs=BASE_JOB_KWARGS,
    )


def create_job_rest_action_point(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    user_id: int,
    char: BaseCharacter = None,
):
    if not isinstance(char, BaseCharacter):
        char_model = CharacterModel()
        char: BaseCharacter = char_model.get(user_id)

    job_name = get_rest_action_points_jobname(user_id=user_id)
    current_jobs = context.job_queue.get_jobs_by_name(job_name)
    if not current_jobs and not char.is_full_action_points:
        context.job_queue.run_repeating(
            callback=job_rest_action_point,
            interval=timedelta(minutes=MINUTES_TO_RECOVERY_ACTION_POINTS),
            user_id=user_id,
            chat_id=chat_id,
            name=job_name,
            job_kwargs=BASE_JOB_KWARGS,
        )


async def job_rest_cure(context: ContextTypes.DEFAULT_TYPE):
    char_model = CharacterModel()
    player_model = PlayerModel()
    job = context.job
    chat_id = job.chat_id
    user_id = job.user_id
    player_character: BaseCharacter = char_model.get(user_id)
    player: Player = player_model.get(user_id)
    revive_reporting = ''
    level = (
        get_attribute_group(chat_id, 'group_level') or
        player_character.level
    )
    min_level = max(1, int(level / 20 * 0.90))
    max_level = max(2, int(level / 20 * 1.10))
    heal_low_hp_bonus = 1 + player_character.cs.irate_hp
    status_debuff_bonus = player_character.status.total_level_debuff // 5
    condition_quantity = randint(min_level, max_level)
    condition_quantity = int(
        (condition_quantity + status_debuff_bonus) * heal_low_hp_bonus
    )

    old_show_hp = player_character.cs.show_hit_points
    if player_character.is_dead:
        report = player_character.cs.revive()
        revive_reporting = '🧚‍♂️REVIVEU🧚‍♀️\n\n'
    else:
        max_hp = player_character.cs.hp
        heal = int(max_hp * 0.10) * heal_low_hp_bonus
        report = player_character.cs.cure_hit_points(heal)
    status_report = player_character.status.remove_random_debuff_conditions(
        condition_quantity
    )
    new_show_hp = player_character.cs.show_hit_points
    true_cure = report['true_cure']
    save_char(char=player_character)
    report_text = f'*HP*: {old_show_hp} ››› {new_show_hp} (*{true_cure}*).'
    hp_reporting = (
        f'{revive_reporting}'
        f'Seu personagem curou HP❤️‍🩹 descansando!\n\n'
        f'{report_text}\n\n'
    )

    if status_report['text']:
        hp_reporting += (
            f'*STATUS*({condition_quantity}):\n'
            f'{status_report["text"]}\n\n'
        )

    if player_character.is_healed and not player_character.is_debuffed:
        job.schedule_removal()
        text = (
            f'{hp_reporting}'
            f'O HP do seu personagem está completamente recuperado. '
            f'O descanso foi finalizado.'
        )
        section_name = SECTION_TEXT_WAKEUP
        section_start = SECTION_HEAD_WAKEUP_START
        section_end = SECTION_HEAD_WAKEUP_END
    else:
        text = f'{hp_reporting} Seu personagem continua descansando…'
        section_name = SECTION_TEXT_REST
        section_start = SECTION_HEAD_REST_START
        section_end = SECTION_HEAD_REST_END

    text = create_text_in_box(
        text=text,
        section_name=section_name,
        section_start=section_start,
        section_end=section_end,
    )

    if player.verbose:
        await send_private_message(
            function_caller='JOB_REST_CURE()',
            context=context,
            text=text,
            user_id=job.user_id,
            markdown=True,
            close_by_owner=False,
        )


async def job_rest_action_point(context: ContextTypes.DEFAULT_TYPE):
    print('JOB_REST_ACTION()')
    char_model = CharacterModel()
    player_model = PlayerModel()
    job = context.job
    user_id = job.user_id
    chat_id = job.chat_id
    char: BaseCharacter = char_model.get(user_id)
    player: Player = player_model.get(user_id)
    report = char.add_action_points(1)
    save_char(char=char)

    text = report['text']
    text = create_text_in_box(
        text=text,
        section_name=SECTION_TEXT_ACTION_PONTOS,
        section_start=SECTION_HEAD_ACTION_POINTS_START,
        section_end=SECTION_HEAD_ACTION_POINTS_END,
    )

    if char.is_full_action_points:
        job.schedule_removal()

    if player.verbose or char.is_full_action_points:
        await send_private_message(
            function_caller='JOB_REST_ACTION_POINT()',
            context=context,
            text=text,
            user_id=user_id,
            chat_id=chat_id,
            markdown=True,
            close_by_owner=False,
        )


async def autorest_midnight(context: ContextTypes.DEFAULT_TYPE):
    '''Comando que inicia o descanso de todos os personagens do grupo que 
    não estão com o HP cheio.
    O descanso faz com que o personagem recupere HP e Stauts a cada 
    "MINUTES_TO_RECOVERY_HIT_POINTS" minutos.
    Se o personagem estiver morto, ele reviverá, recuperando 1 de HP 
    em "MINUTES_TO_RECOVERY_HIT_POINTS" minutos.'''

    print('JOB_AUTOREST_MIDNIGHT()')
    char_model = CharacterModel()
    job = context.job
    chat_id = job.chat_id
    user_ids = get_players_id_by_chat_id(chat_id=chat_id)
    silent = get_attribute_group_or_player(chat_id, 'silent')
    texts = []
    for user_id in user_ids:
        job_name = get_rest_jobname(user_id)
        current_jobs = context.job_queue.get_jobs_by_name(job_name)
        player_character: BaseCharacter = char_model.get(user_id)
        player_name = player_character.player_name
        character_id = player_character._id
        current_hp = player_character.cs.show_hit_points
        player_need_rest = (
            player_character.is_damaged or player_character.is_debuffed
        )

        create_job_rest_action_point(
            context=context,
            chat_id=chat_id,
            user_id=user_id,
        )
        if current_jobs or not player_need_rest:
            continue
        else:
            create_job_rest_cure(
                context=context,
                chat_id=chat_id,
                user_id=user_id,
            )
            texts.append(f'{player_name} - HP: {current_hp}')

    if texts:
        players_hp = '\n'.join(texts)
        now = get_brazil_time_now()
        if now.hour in [11, 12, 13]:
            reply_text_rest = choice(REPLY_TEXT_REST_MIDDAY)
            section_start = SECTION_HEAD_REST_MIDDAY_START
            section_end = SECTION_HEAD_REST_MIDDAY_END
        elif now.hour in range(6, 18):
            reply_text_rest = choice(REPLY_TEXT_REST_INDAY)
            section_start = SECTION_HEAD_REST_INDAY_START
            section_end = SECTION_HEAD_REST_INDAY_END
        else:
            reply_text_rest = choice(REPLY_TEXT_REST_MIDNIGHT)
            section_start = SECTION_HEAD_REST_MIDNIGHT_START
            section_end = SECTION_HEAD_REST_MIDNIGHT_END
        text = (
            f'{reply_text_rest}\n\n'
            f'{players_hp}\n\n'
            f'Os personagens irão recuperar HP e Status a cada '
            f'{MINUTES_TO_RECOVERY_HIT_POINTS} minutos.'
        )

        text = create_text_in_box(
            text=text,
            section_name=SECTION_TEXT_REST_MIDNIGHT,
            section_start=section_start,
            section_end=section_end,
            clean_func=None,
        )

        call_telegram_kwargs = dict(
            chat_id=chat_id,
            text=text,
            disable_notification=silent
        )

        await call_telegram_message_function(
            function_caller='JOB_AUTOREST_MIDNIGHT()',
            function=context.bot.send_message,
            context=context,
            need_response=False,
            **call_telegram_kwargs
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


def get_rest_action_points_jobname(user_id):
    return f'REST-ACTIONPOINTS-{user_id}'


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
