from datetime import timedelta
from random import choice, randint
from time import sleep
from typing import List

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler
)
from telegram.constants import ChatAction, ParseMode

from bot.constants.enemy import (
    AMBUSH_TEXTS,
    CALLBACK_TEXT_DEFEND,
    DEFEND_BUTTON_TEXT,
    MAX_MINUTES_FOR_ATTACK,
    MIN_MINUTES_FOR_ATTACK,
    PATTERN_DEFEND,
    SECTION_END_DICT,
    SECTION_START_DICT,
    SECTION_TEXT_AMBUSH,
    SECTION_TEXT_AMBUSH_ATTACK,
    SECTION_TEXT_AMBUSH_DEFENSE,
    SECTION_TEXT_AMBUSH_XP,
    SECTION_TEXT_FAIL
)
from bot.constants.rest import COMMANDS as REST_COMMANDS
from bot.conversations.bag import send_drop_message
from bot.decorators.battle import need_not_in_battle
from bot.decorators.char import (
    confusion,
    skip_if_dead_char,
    skip_if_immobilized,
    skip_if_no_have_char
)
from bot.decorators.player import skip_if_no_singup_player
from bot.decorators.print import print_basic_infos
from bot.functions.bag import drop_random_items_from_bag
from bot.functions.chat import callback_data_to_dict, callback_data_to_string
from constant.text import (
    SECTION_HEAD_ATTACK_END,
    SECTION_HEAD_ATTACK_START,
    SECTION_HEAD_ENEMY_END,
    SECTION_HEAD_ENEMY_START,
    SECTION_HEAD_FAIL_END,
    SECTION_HEAD_FAIL_START,
    SECTION_HEAD_XP_END,
    SECTION_HEAD_XP_START
)
from bot.decorators.job import skip_if_spawn_timeout
from bot.functions.char import (
    add_xp,
    choice_char,
    get_base_xp_from_enemy_attack,
    get_player_chars_from_group,
    save_char
)
from bot.functions.date_time import is_boosted_day
from bot.functions.general import get_attribute_group_or_player

from function.date_time import get_brazil_time_now
from function.text import create_text_in_box


from repository.mongo import CharacterModel
from repository.mongo.populate.enemy import create_random_enemies

from rpgram import Dice
from rpgram.characters import BaseCharacter, NPCharacter, PlayerCharacter


async def job_create_ambush(context: ContextTypes.DEFAULT_TYPE):
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
            f'JOB_CREATE_AMBUSH() - {now}: '
            f'Evento de item inicia em {minutes_in_seconds // 60} minutos.'
        )
        context.job_queue.run_once(
            callback=job_start_ambush,
            when=minutes_in_seconds,
            name=f'JOB_CREATE_AMBUSH_{i}',
            chat_id=chat_id,
        )


@skip_if_spawn_timeout
async def job_start_ambush(context: ContextTypes.DEFAULT_TYPE):
    '''Um grupo de inimigos irá atacar os jogadores de maneira aleatória.
    '''

    print('JOB_START_AMBUSH()')
    job = context.job
    chat_id = job.chat_id
    group_level = get_attribute_group_or_player(chat_id, 'group_level')
    silent = get_attribute_group_or_player(chat_id, 'silent')
    enemy_list = create_random_enemies(group_level)
    message_id = None
    context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    for enemy_char in enemy_list:
        try:
            defenser_char = choice_char(chat_id=chat_id, is_alive=True)
            user_id = defenser_char.player_id
            player_name = defenser_char.player_name
        except ValueError as error:
            print(f'JOB_ENEMY_ATTACK(): {error}')
            if message_id:
                break
            return ConversationHandler.END

        if not message_id:
            message_id = await send_ambush_message(
                chat_id=chat_id,
                context=context,
                silent=silent,
            )
            sleep(1)

        text = (
            f'*{enemy_char.full_name_with_level}* iniciou um *ATAQUE* contra '
            f'{player_name}.'
        )
        text = create_text_in_box(
            text=text,
            section_name=SECTION_TEXT_AMBUSH_ATTACK,
            section_start=SECTION_HEAD_ATTACK_START,
            section_end=SECTION_HEAD_ATTACK_END
        )

        defend_button = get_defend_button(
            user_id=user_id,
            enemy=enemy_char
        )
        reply_markup = InlineKeyboardMarkup([defend_button])
        response = await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            # disable_notification=silent,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_to_message_id=message_id,
            allow_sending_without_reply=True,
            reply_markup=reply_markup,
        )
        sleep(2)

        minutes = randint(MIN_MINUTES_FOR_ATTACK, MAX_MINUTES_FOR_ATTACK)
        job_name = get_enemy_attack_jobname(
            user_id=user_id,
            enemy_char=enemy_char
        )
        job_data = {
            'enemy_id': str(enemy_char.player_id),
            'message_id': response.message_id
        }
        context.job_queue.run_once(
            callback=job_enemy_attack,
            when=timedelta(minutes=minutes),
            data=job_data,
            name=job_name,
            chat_id=chat_id,
            user_id=user_id,
        )
        put_ambush_dict(context=context, enemy=enemy_char)
        print(
            f'{enemy_char.full_name_with_level} ira atacar '
            f'{defenser_char.player_name} em {minutes} minutos.'
        )

    # ---------- END FOR ---------- #

    await add_xp_group(
        chat_id=chat_id,
        enemy_list=enemy_list,
        context=context,
        silent=silent,
        message_id=message_id,
    )


async def job_enemy_attack(context: ContextTypes.DEFAULT_TYPE):
    '''Após um breve tempo aleatório, o inimigo atacara um aliado.
    '''

    print('JOB_ENEMY_ATTACK()')
    char_model = CharacterModel()
    job = context.job
    chat_id = job.chat_id
    user_id = job.user_id
    job_data = job.data
    enemy_id = job_data['enemy_id']
    message_id = job_data['message_id']
    enemy_char = get_enemy_from_ambush_dict(context=context, enemy_id=enemy_id)
    defenser_char = char_model.get(user_id)

    if enemy_char and defenser_char and defenser_char.is_alive:
        await enemy_attack(
            context=context,
            chat_id=chat_id,
            message_id=message_id,
            enemy_char=enemy_char,
            defenser_char=defenser_char,
            to_dodge=True
        )
    elif defenser_char and defenser_char.is_dead:
        text = f'{defenser_char.player_name} está morto.'
        print(text)
        text = create_text_in_box(
            text=text,
            section_name=SECTION_TEXT_FAIL,
            section_start=SECTION_HEAD_FAIL_START,
            section_end=SECTION_HEAD_FAIL_END,
        )
        await context.bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id=message_id,
            parse_mode=ParseMode.MARKDOWN_V2,
        )


@skip_if_no_singup_player
@skip_if_no_have_char
@need_not_in_battle
@skip_if_dead_char
@skip_if_immobilized
@confusion()
@print_basic_infos
async def defense_enemy_attack(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    '''Defende aliado de um ataque. Caso sobreviva, ambos receberão XP.
    '''

    char_model = CharacterModel()
    chat_id = update.effective_chat.id
    defenser_user_id = update.effective_user.id
    query = update.callback_query
    message_id = query.message.message_id
    data = callback_data_to_dict(query.data)
    target_user_id = data['user_id']
    enemy_id = data['enemy_id']

    if not 'ambushes' in context.chat_data:
        await query.answer('Essa emboscada já terminou', show_alert=True)
        await query.delete_message()
        return ConversationHandler.END

    if defenser_user_id == target_user_id:
        await query.answer(
            'Você não pode defender a si mesmo.',
            show_alert=True
        )
        return ConversationHandler.END

    enemy_char = get_enemy_from_ambush_dict(context=context, enemy_id=enemy_id)
    defenser_char = char_model.get(defenser_user_id)
    target_char = char_model.get(target_user_id)
    await enemy_attack(
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        enemy_char=enemy_char,
        defenser_char=defenser_char,
        target_char=target_char,
        to_dodge=True
    )
    remove_job_enemy_attack(
        context=context,
        user_id=target_user_id,
        enemy_char=enemy_char
    )


async def enemy_attack(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    message_id: int,
    enemy_char: NPCharacter,
    defenser_char: PlayerCharacter,
    target_char: PlayerCharacter = None,
    to_dodge: bool = False,
):
    '''Função que o Inimigo ataca um jogador
    '''

    text_report = ''
    if target_char and target_char.is_alive:
        section_name = SECTION_TEXT_AMBUSH_DEFENSE
        text_report = (
            f'{defenser_char.player_name} defendeu '
            f'{target_char.player_name}.\n\n'
        )
    else:
        section_name = SECTION_TEXT_AMBUSH_ATTACK

    attack_report = enemy_char.to_attack(
        defenser_char=defenser_char,
        attacker_dice=Dice(20),
        defenser_dice=Dice(20),
        to_dodge=to_dodge,
        to_defend=True,
        rest_command=REST_COMMANDS[0],
        verbose=True,
        markdown=True
    )
    text_report += attack_report['text']
    attacker_action_name = attack_report['attack']['action']

    if not attack_report['dead']:
        base_xp = get_base_xp_from_enemy_attack(enemy_char, defenser_char)
        report_xp = add_xp(
            chat_id=chat_id,
            char=defenser_char,
            base_xp=base_xp,
        )
        if target_char and target_char.is_alive:
            base_xp = get_base_xp_from_enemy_attack(enemy_char, target_char)
            target_report_xp = add_xp(
                chat_id=chat_id,
                char=target_char,
                base_xp=base_xp,
            )
            text_report += f'{target_report_xp["text"]}\n'
        text_report += f'{report_xp["text"]}\n\n'
    else:
        save_char(defenser_char)

    text_report += f'O inimigo fugiu!'
    text_report = create_text_in_box(
        text=text_report,
        section_name=section_name,
        section_start=SECTION_START_DICT[attacker_action_name],
        section_end=SECTION_END_DICT[attacker_action_name]
    )
    await context.bot.edit_message_text(
        text=text_report,
        chat_id=chat_id,
        message_id=message_id,
        parse_mode=ParseMode.MARKDOWN_V2,
    )

    if attack_report['dead']:
        user_id = defenser_char.player_id
        player_name = defenser_char.player_name
        drop_items = drop_random_items_from_bag(user_id=user_id)
        await send_drop_message(
            context=context,
            items=drop_items,
            text=f'{player_name} morreu e dropou o item',
            chat_id=chat_id,
            message_id=message_id,
            silent=True,
        )


def get_defend_button(
    user_id: int,
    enemy: NPCharacter
) -> List[InlineKeyboardButton]:
    '''Retorna o botão para defender um aliado.
    '''

    enemy_id = str(enemy.player_id)
    return [
        InlineKeyboardButton(
            text=DEFEND_BUTTON_TEXT,
            callback_data=callback_data_to_string({
                'command': CALLBACK_TEXT_DEFEND,
                'enemy_id': enemy_id,
                'user_id': user_id,
            })
        )
    ]


def get_enemy_attack_jobname(user_id: int, enemy_char: NPCharacter) -> str:
    '''Nome do job do ataque inimigo
    '''

    enemy_id = str(enemy_char.player_id)
    return f'JOB_ENEMY_ATTACK_{user_id}_{enemy_id}'


def put_ambush_dict(context: ContextTypes.DEFAULT_TYPE, enemy: NPCharacter):
    '''Adiciona o inimigo ao dicionário de ambushes, em que a chave é a 
    enemy_id.
    '''

    enemy_id = str(enemy.player_id)
    ambushes = context.chat_data.get('ambushes', {})
    ambushes[enemy_id] = enemy
    if not 'ambushes' in context.chat_data:
        context.chat_data['ambushes'] = ambushes


def get_enemy_from_ambush_dict(
    context: ContextTypes.DEFAULT_TYPE,
    enemy_id: str
) -> NPCharacter:
    '''Retorna um NPCharacter do dicionário ambushes a partir do enemy_id e o 
    remove do dicionário.
    '''

    return context.chat_data['ambushes'].pop(enemy_id)


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
    '''Adiciona XP aos jogadores vivos durante a emboscada.
    '''

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


def remove_job_enemy_attack(
    context: ContextTypes.DEFAULT_TYPE,
    user_id: int,
    enemy_char: NPCharacter
) -> bool:
    '''Remove o job de ataque do inimigo.
    '''

    job_name = get_enemy_attack_jobname(user_id=user_id, enemy_char=enemy_char)
    current_jobs = context.job_queue.get_jobs_by_name(job_name)
    print('current_jobs', current_jobs)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()

    return True


DEFEND_MSG_HANDLER = CallbackQueryHandler(
    defense_enemy_attack,
    pattern=PATTERN_DEFEND
)
