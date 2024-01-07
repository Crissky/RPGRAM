from random import choice, randint

from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from bot.constants.enemy import AMBUSH_TEXTS
from bot.constants.rest import COMMANDS as REST_COMMANDS
from bot.conversations.bag import send_drop_message
from bot.functions.bag import drop_random_items_from_bag
from constant.text import (
    SECTION_HEAD_ENEMY_END,
    SECTION_HEAD_ENEMY_START,
    TEXT_SEPARATOR
)
from bot.decorators.job import skip_if_spawn_timeout
from bot.functions.char import add_xp, choice_char, save_char
from bot.functions.date_time import is_boosted_day
from function.date_time import get_brazil_time_now
from bot.functions.general import get_attribute_group_or_player
from function.text import create_text_in_box, escape_basic_markdown_v2

from repository.mongo.populate.enemy import create_random_enemies

from rpgram import Dice


async def job_create_enemy_attack(context: ContextTypes.DEFAULT_TYPE):
    '''Cria um evento de ataque de inimigo que ocorrerá entre 1 e 299 minutos.
    Está função é chamada em cada 3 horas.
    '''
    job = context.job
    chat_id = int(job.chat_id)  # chat_id vem como string
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
    chat_id = int(job.chat_id)  # chat_id vem como string
    group_level = get_attribute_group_or_player(chat_id, 'group_level')
    silent = get_attribute_group_or_player(chat_id, 'silent')
    enemy_list = create_random_enemies(group_level)
    texts = [escape_basic_markdown_v2(f'{choice(AMBUSH_TEXTS)}\n\n')]

    for enemy_char in enemy_list:
        try:
            defenser_char = choice_char(chat_id=chat_id, is_alive=True)
            user_id = defenser_char.player_id
            player_name = defenser_char.player_name
        except ValueError as error:
            print(f'JOB_ENEMY_ATTACK(): {error}')
            if len(texts) > 1:
                break
            return
        damage_report = enemy_char.to_attack(
            defenser_char=defenser_char,
            attacker_dice=Dice(20),
            defenser_dice=Dice(20),
            to_dodge=True,
            to_defend=True,
            rest_command=REST_COMMANDS[0],
            verbose=True,
            markdown=True
        )

        text_report = damage_report['text']

        if not damage_report['defense']['is_miss']:
            save_char(defenser_char)
        if damage_report['dead']:
            drop_items = drop_random_items_from_bag(user_id=user_id)
            await send_drop_message(
                chat_id=chat_id,
                context=context,
                items=drop_items,
                text=f'{player_name} morreu e dropou o item',
                silent=True,
            )
        else:
            base_xp = int(
                enemy_char.points_multiplier *
                max(enemy_char.level - defenser_char.level, 10)
            )
            report_xp = add_xp(
                chat_id=chat_id,
                user_id=user_id,
                base_xp=base_xp,
            )
            text_report += escape_basic_markdown_v2(f'{report_xp["text"]}\n\n')

        texts.append(text_report)

    full_text = f'{TEXT_SEPARATOR}\n'.join(texts)
    full_text += escape_basic_markdown_v2(
        f'Os inimigos fugiram!'
        if len(enemy_list) > 1
        else f'O inimigo fugiu!'
    )
    full_text = create_text_in_box(
        text=full_text,
        section_name='EMBOSCADA',
        section_start=SECTION_HEAD_ENEMY_START,
        section_end=SECTION_HEAD_ENEMY_END
    )
    await context.bot.send_message(
        chat_id=chat_id,
        text=full_text,
        disable_notification=silent,
        parse_mode=ParseMode.MARKDOWN_V2,
    )
