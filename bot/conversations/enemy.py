from random import choice, randint

from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from bot.constants.enemy import AMBUSH_TEXTS
from bot.constants.rest import COMMANDS as REST_COMMANDS
from bot.decorators.job import skip_if_spawn_timeout
from bot.functions.char import choice_char, save_char
from bot.functions.date_time import is_boosted_day
from bot.functions.general import get_attribute_group_or_player

from constant.text import SECTION_HEAD_2, SECTION_HEAD_2_END, TEXT_SEPARATOR

from function.date_time import get_brazil_time_now
from function.text import escape_basic_markdown_v2

from repository.mongo.populate.enemy import create_random_enemies

from rpgram import Dice


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


@skip_if_spawn_timeout
async def job_enemy_attack(context: ContextTypes.DEFAULT_TYPE):
    '''Um grupo de inimigos ataca os jogadores de maneira aleatória.
    '''
    job = context.job
    chat_id = int(job.chat_id)  # chat_id vem como string
    group_level = get_attribute_group_or_player(chat_id, 'group_level')
    silent = get_attribute_group_or_player(chat_id, 'silent')
    enemy_list = create_random_enemies(group_level)
    texts = [escape_basic_markdown_v2(
        f'{SECTION_HEAD_2.format("EMBOSCADA")}'
        f'\n\n'
        f'{choice(AMBUSH_TEXTS)}'
        f'\n\n'
    )]

    for enemy_char in enemy_list:
        try:
            defenser_char = choice_char(chat_id=chat_id, is_alive=True)
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

        if not damage_report['defense']['is_miss']:
            save_char(defenser_char)
        texts.append(damage_report['text'])

    full_text = f'{TEXT_SEPARATOR}\n'.join(texts)
    full_text += escape_basic_markdown_v2(
        f'Os inimigos fugiram!'
        if len(enemy_list) > 1
        else f'O inimigo fugiu!'
    )
    full_text += escape_basic_markdown_v2(
        f'\n\n{SECTION_HEAD_2_END.format("EMBOSCADA")}'
    )
    await context.bot.send_message(
        chat_id=chat_id,
        text=full_text,
        disable_notification=silent,
        parse_mode=ParseMode.MARKDOWN_V2,
    )
