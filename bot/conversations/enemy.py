from random import choice, randint
from typing import List

from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from bot.constants.enemy import AMBUSH_TEXTS
from bot.constants.rest import COMMANDS as REST_COMMANDS
from bot.conversations.bag import send_drop_message
from bot.functions.bag import drop_random_items_from_bag
from constant.text import (
    SECTION_HEAD_ENEMY_END,
    SECTION_HEAD_ENEMY_START,
    SECTION_HEAD_MAGICAL_ATTACK_END,
    SECTION_HEAD_MAGICAL_ATTACK_START,
    SECTION_HEAD_PHYSICAL_ATTACK_END,
    SECTION_HEAD_PHYSICAL_ATTACK_START,
    SECTION_HEAD_PRECISION_ATTACK_END,
    SECTION_HEAD_PRECISION_ATTACK_START,
    SECTION_HEAD_XP_END,
    SECTION_HEAD_XP_START
)
from bot.decorators.job import skip_if_spawn_timeout
from bot.functions.char import add_xp, choice_char, get_player_chars_from_group, save_char
from bot.functions.date_time import is_boosted_day
from function.date_time import get_brazil_time_now
from bot.functions.general import get_attribute_group_or_player
from function.text import create_text_in_box

from repository.mongo.populate.enemy import create_random_enemies

from rpgram import Dice
from rpgram.characters import BaseCharacter


SECTION_TEXT_AMBUSH = 'EMBOSCADA'
SECTION_TEXT_AMBUSH_ATTACK = 'ATAQUE EMBOSCADA'
SECTION_TEXT_AMBUSH_XP = 'XP EMBOSCADA'


async def job_create_enemy_attack(context: ContextTypes.DEFAULT_TYPE):
    '''Cria um evento de ataque de inimigo que ocorrerá entre 1 e 299 minutos.
    Está função é chamada em cada 3 horas.
    '''
    job = context.job
    chat_id = job.chat_id
    now = get_brazil_time_now()

    times = randint(1, 2) if is_boosted_day(now) else 1
    for i in range(times):
        minutes_in_seconds = randint(1, 179) * 60
        print(
            f'JOB_CREATE_ENEMY_ATTACK() - {now}: '
            f'Evento de item inicia em {minutes_in_seconds // 60} minutos.'
        )
        context.job_queue.run_once(
            callback=job_enemy_attack,
            when=minutes_in_seconds,
            name=f'JOB_CREATE_ENEMY_ATTACK_{i}',
            chat_id=chat_id,
        )


@skip_if_spawn_timeout
async def job_enemy_attack(context: ContextTypes.DEFAULT_TYPE):
    '''Um grupo de inimigos ataca os jogadores de maneira aleatória.
    '''

    job = context.job
    chat_id = job.chat_id
    group_level = get_attribute_group_or_player(chat_id, 'group_level')
    silent = get_attribute_group_or_player(chat_id, 'silent')
    enemy_list = create_random_enemies(group_level)
    dead_player_list = []
    message_id = None
    section_start_dict = {
        'Physical Attack': SECTION_HEAD_PHYSICAL_ATTACK_START,
        'Precision Attack': SECTION_HEAD_PRECISION_ATTACK_START,
        'Magical Attack': SECTION_HEAD_MAGICAL_ATTACK_START,
    }
    section_end_dict = {
        'Physical Attack': SECTION_HEAD_PHYSICAL_ATTACK_END,
        'Precision Attack': SECTION_HEAD_PRECISION_ATTACK_END,
        'Magical Attack': SECTION_HEAD_MAGICAL_ATTACK_END,
    }

    for enemy_char in enemy_list:
        try:
            defenser_char = choice_char(chat_id=chat_id, is_alive=True)
            user_id = defenser_char.player_id
            player_name = defenser_char.player_name
        except ValueError as error:
            print(f'JOB_ENEMY_ATTACK(): {error}')
            if message_id:
                break
            return

        if not message_id:
            message_id = await send_ambush_message(
                chat_id=chat_id,
                context=context,
                silent=silent,
            )

        attack_report = enemy_char.to_attack(
            defenser_char=defenser_char,
            attacker_dice=Dice(20),
            defenser_dice=Dice(20),
            to_dodge=True,
            to_defend=True,
            rest_command=REST_COMMANDS[0],
            verbose=True,
            markdown=True
        )
        text_report = attack_report['text']
        attacker_action_name = attack_report['attack']['action']

        if not attack_report['dead']:
            base_xp = int(
                enemy_char.points_multiplier *
                max(enemy_char.level - defenser_char.level, 10)
            )
            report_xp = add_xp(
                chat_id=chat_id,
                char=defenser_char,
                base_xp=base_xp,
            )
            text_report += f'{report_xp["text"]}\n\n'
        else:
            save_char(defenser_char)

        text_report = create_text_in_box(
            text=text_report,
            section_name=SECTION_TEXT_AMBUSH_ATTACK,
            section_start=section_start_dict[attacker_action_name],
            section_end=section_end_dict[attacker_action_name]
        )
        response = await context.bot.send_message(
            chat_id=chat_id,
            text=text_report,
            disable_notification=silent,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_to_message_id=message_id,
            allow_sending_without_reply=True,
        )

        if attack_report['dead']:
            dead_player_list.append({
                'user_id': user_id,
                'player_name': player_name,
                'message_id': response.message_id,
            })

    await add_xp_group(
        chat_id=chat_id,
        enemy_list=enemy_list,
        context=context,
        silent=silent,
        message_id=message_id,
    )

    for dead_player_dict in dead_player_list:
        user_id = dead_player_dict['user_id']
        player_name = dead_player_dict['player_name']
        message_id = dead_player_dict['message_id']
        drop_items = drop_random_items_from_bag(user_id=user_id)
        await send_drop_message(
            context=context,
            items=drop_items,
            text=f'{player_name} morreu e dropou o item',
            chat_id=chat_id,
            message_id=message_id,
            silent=True,
        )


async def send_ambush_message(
    chat_id: int,
    context: ContextTypes.DEFAULT_TYPE,
    silent: bool = None,
) -> int:
    '''Envia a primeira mensagem da Emboscada
    '''

    ambush_text = choice(AMBUSH_TEXTS)
    ambush_text = create_text_in_box(
        text=ambush_text,
        section_name=SECTION_TEXT_AMBUSH,
        section_start=SECTION_HEAD_ENEMY_START,
        section_end=SECTION_HEAD_ENEMY_END
    )
    response = await context.bot.send_message(
        chat_id=chat_id,
        text=ambush_text,
        disable_notification=silent,
        parse_mode=ParseMode.MARKDOWN_V2,
    )
    message_id = response.message_id

    return message_id


async def add_xp_group(
    chat_id: int,
    enemy_list: List[BaseCharacter],
    context: ContextTypes.DEFAULT_TYPE,
    silent: bool,
    message_id: int = None,
):
    char_list = get_player_chars_from_group(chat_id=chat_id, is_alive=True)

    total_allies = len(char_list)

    sum_level = sum([enemy.level for enemy in enemy_list])
    sum_multiplier = sum([enemy.points_multiplier for enemy in enemy_list])

    avg_level = sum_level // len(enemy_list)

    multiplied_level = (avg_level * sum_multiplier)

    full_text = ''
    for char in char_list:
        level_diff = multiplied_level - (char.level * 2)
        base_xp = int(max(level_diff, 10) / total_allies)
        report_xp = add_xp(
            chat_id=chat_id,
            char=char,
            base_xp=base_xp,
        )
        full_text += f'{report_xp["text"]}\n'

    full_text += '\n' + (
        f'Os inimigos fugiram!'
        if len(enemy_list) > 1
        else f'O inimigo fugiu!'
    )
    full_text = create_text_in_box(
        text=full_text,
        section_name=SECTION_TEXT_AMBUSH_XP,
        section_start=SECTION_HEAD_XP_START,
        section_end=SECTION_HEAD_XP_END
    )
    await context.bot.send_message(
        chat_id=chat_id,
        text=full_text,
        disable_notification=silent,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_to_message_id=message_id,
        allow_sending_without_reply=True,
    )
