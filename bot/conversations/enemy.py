from random import choice, randint, random

from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from bot.constants.enemy import AMBUSH_TEXTS
from bot.constants.rest import COMMANDS as REST_COMMANDS
from bot.decorators.job import skip_if_spawn_timeout
from bot.functions.char import choice_char, save_char
from bot.functions.date_time import is_boosted_day
from bot.functions.general import get_attribute_group_or_player

from constant.text import TEXT_SEPARATOR

from function.date_time import get_brazil_time_now
from function.text import escape_basic_markdown_v2

from repository.mongo.populate.enemy import create_random_enemies

from rpgram import Dice
from rpgram.battle import Battle


@skip_if_spawn_timeout
async def job_create_enemy_attack(context: ContextTypes.DEFAULT_TYPE):
    '''Cria um evento de ataque de inimigo que ocorrerá entre 1 e 299 minutos.
    Está função é chamada em cada 3 horas.
    '''
    job = context.job
    chat_id = int(job.chat_id)  # chat_id vem como string
    now = get_brazil_time_now()

    times = randint(1, 2) if is_boosted_day(now) else 1
    for i in range(times):
        minutes_in_seconds = randint(1, 299) * 60
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


async def job_enemy_attack(context: ContextTypes.DEFAULT_TYPE):
    '''Um grupo de inimigos ataca os jogadores de maneira aleatória.
    '''
    job = context.job
    chat_id = int(job.chat_id)  # chat_id vem como string
    group_level = get_attribute_group_or_player(chat_id, 'group_level')
    silent = get_attribute_group_or_player(chat_id, 'silent')
    battle = Battle([], [], None)
    enemy_list = create_random_enemies(group_level)
    texts = [choice(AMBUSH_TEXTS) + '\n\n']

    for enemy_char in enemy_list:
        text = ''
        target_char = choice_char(chat_id=chat_id, is_alive=True)
        target_player_name = target_char.player_name
        enemy_dice = Dice(20)
        target_dice = Dice(20)
        enemy_dice.throw()
        target_dice.throw()

        accuracy = battle.get_accuracy(
            enemy_char.cs.hit,
            target_char.cs.evasion,
            enemy_dice,
            target_dice,
        )
        dodge_score = random()
        if dodge_score >= accuracy:
            text += (
                f'{target_player_name} *ESQUIVOU DO ATAQUE* de '
                f'*{enemy_char.full_name_with_level}*.\n\n'
            )
        else:
            text += (
                f'*{enemy_char.full_name_with_level}* *ATACOU* '
                f'{target_player_name}\n\n'
            )
            action = enemy_char.get_best_action_attack()
            attack_value = enemy_char.get_action_attack(action)
            attack_value_boosted = battle.get_total_value(
                attack_value,
                enemy_dice
            )
            (
                defense_value,
                defense_action
            ) = target_char.get_action_defense(action)
            defense_value_boosted = battle.get_total_value(
                defense_value,
                target_dice
            )
            damage = attack_value_boosted - defense_value_boosted
            damage = max(damage, 0)
            damage_report = target_char.cs.damage_hit_points(damage)
            action = action.replace('_', ' ').title()
            defense_action = defense_action.replace('_', ' ').title()
            text += (
                f'*{action}*: {attack_value_boosted}({attack_value}), '
                f'{enemy_dice.text}\n'
            )
            text += (
                f'*{defense_action}*: '
                f'{defense_value_boosted}({defense_value}), '
                f'{target_dice.text}\n'
            )
            text += damage_report['text']
            if damage_report['dead']:
                text += (
                    f'\n\n{target_player_name} morreu! '
                    f'Use o comando /{REST_COMMANDS[0]} para descansar.'
                )
            text += '\n\n'
            save_char(target_char)
        texts.append(text)

    full_text = f'{TEXT_SEPARATOR}\n'.join(texts)
    full_text += (
        f'Os inimigos fugiram!'
        if len(enemy_list) > 1
        else f'O inimigo fugiu!'
    )
    full_text = escape_basic_markdown_v2(full_text)
    await context.bot.send_message(
        chat_id=chat_id,
        text=full_text,
        disable_notification=silent,
        parse_mode=ParseMode.MARKDOWN_V2,
    )
