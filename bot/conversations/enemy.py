from datetime import timedelta
from math import ceil
from operator import attrgetter
from random import choice, randint, shuffle
from time import sleep
from typing import List, Union

from telegram import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    Update
)
from telegram.error import BadRequest
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler
)
from telegram.constants import ChatAction, ParseMode

from bot.constants.enemy import (
    AMBUSH_TEXTS,
    ATTACK_BUTTON_TEXT,
    BASE_ATTRIBUTES_BUTTON_TEXT,
    CALLBACK_TEXT_ATTACK,
    CALLBACK_TEXT_BASE_ATTRIBUTES,
    CALLBACK_TEXT_COMBAT_ATTRIBUTES,
    CALLBACK_TEXT_DEFEND,
    COMBAT_ATTRIBUTES_BUTTON_TEXT,
    COUNTER_LINES,
    DEFEND_BUTTON_TEXT,
    ENEMY_CHANCE_TO_ATTACK_AGAIN_DICT,
    MAX_MINUTES_TO_ATTACK_FROM_RANK_DICT,
    MIN_MINUTES_TO_ATTACK_FROM_RANK_DICT,
    PATTERN_ATTACK,
    PATTERN_ATTRIBUTES,
    PATTERN_DEFEND,
    SECTION_END_DICT,
    SECTION_START_DICT,
    SECTION_TEXT_ALLY_ATTACK,
    SECTION_TEXT_AMBUSH,
    SECTION_TEXT_AMBUSH_ATTACK,
    SECTION_TEXT_AMBUSH_COUNTER,
    SECTION_TEXT_AMBUSH_DEFENSE,
    SECTION_TEXT_AMBUSH_XP,
    SECTION_TEXT_EXCOMMUNICATED,
    SECTION_TEXT_FAIL,
    SECTION_TEXT_FAIL_ALLY_ATTACK,
    SECTION_TEXT_FAIL_AMBUSH_COUNTER,
    SECTION_TEXT_FAIL_AMBUSH_DEFENSE,
    SECTION_TEXT_FLEE
)
from bot.constants.job import BASE_JOB_KWARGS
from bot.constants.rest import COMMANDS as REST_COMMANDS
from bot.conversations.bag import send_drop_message
from bot.conversations.rest import create_job_rest_action_point
from bot.decorators.char import (
    confusion,
    skip_if_dead_char,
    skip_if_immobilized
)
from bot.decorators.player import skip_if_no_singup_player
from bot.decorators.print import print_basic_infos
from bot.functions.bag import drop_random_items_from_bag
from bot.functions.chat import (
    MIN_AUTODELETE_TIME,
    REPLY_MARKUP_DEFAULT,
    answer,
    callback_data_to_dict,
    callback_data_to_string,
    delete_message,
    edit_message_text,
    edit_message_text_and_forward,
    forward_message,
    call_telegram_message_function,
    get_close_keyboard,
    reply_text,
    reply_typing
)
from bot.functions.config import get_attribute_group, is_group_spawn_time
from bot.functions.job import remove_job_by_name
from constant.text import (
    ALERT_SECTION_HEAD,
    SECTION_HEAD,
    SECTION_HEAD_ATTACK_END,
    SECTION_HEAD_ATTACK_START,
    SECTION_HEAD_ENEMY_END,
    SECTION_HEAD_ENEMY_START,
    SECTION_HEAD_FAIL_END,
    SECTION_HEAD_FAIL_START,
    SECTION_HEAD_FLEE_END,
    SECTION_HEAD_FLEE_START,
    SECTION_HEAD_TIMEOUT_SPAWN_END,
    SECTION_HEAD_TIMEOUT_SPAWN_START,
    SECTION_HEAD_XP_END,
    SECTION_HEAD_XP_START,
    TEXT_SEPARATOR
)
from bot.decorators.job import skip_if_spawn_timeout
from bot.functions.char import (
    add_xp,
    choice_char,
    get_base_xp_from_enemy_attack,
    get_base_xp_from_player_attack,
    get_player_chars_from_group,
    save_char
)
from bot.functions.general import (
    get_attribute_group_or_player,
    luck_test
)

from function.text import create_text_in_box, escape_for_citation_markdown_v2

from repository.mongo import CharacterModel, ItemModel, PlayerModel
from repository.mongo.populate.enemy import create_random_enemies
from repository.mongo.populate.item import (
    create_random_consumable,
    create_random_equipment
)

from rpgram import Item, Player
from rpgram.boosters import Equipment
from rpgram.characters import BaseCharacter, NPCharacter, PlayerCharacter
from rpgram.skills.skill_base import BaseSkill


@skip_if_spawn_timeout
async def job_start_ambush(context: ContextTypes.DEFAULT_TYPE):
    '''Um grupo de inimigos irá atacar os jogadores de maneira aleatória.
    '''

    print('JOB_START_AMBUSH()')
    job = context.job
    chat_id = job.chat_id
    message_id = None
    group_level = get_attribute_group(chat_id, 'group_level')
    silent = get_attribute_group_or_player(chat_id, 'silent')
    enemy_list = create_random_enemies(
        group_level=group_level,
        num_min_enemies=2,
        num_max_enemies=4,
    )

    send_chat_action_kwargs = dict(
        chat_id=chat_id,
        action=ChatAction.TYPING
    )
    await call_telegram_message_function(
        function_caller='EMENY.JOB_START_AMBUSH()',
        function=context.bot.send_chat_action,
        context=context,
        need_response=False,
        skip_retry=True,
        **send_chat_action_kwargs
    )

    for enemy_char in enemy_list:
        if not message_id:
            message_id = await send_ambush_message(
                context=context,
                silent=silent,
            )
            sleep(2)

        await create_job_enemy_attack(
            context=context,
            chat_id=chat_id,
            message_id=message_id,
            enemy_char=enemy_char,
            is_first_attack=True,
        )

    # ---------- END FOR ---------- #

    await add_xp_group(
        chat_id=chat_id,
        enemy_list=enemy_list,
        context=context,
        silent=silent,
        message_id=message_id,
    )


async def create_job_enemy_attack(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    message_id: int,
    enemy_char: NPCharacter,
    user_id: int = None,
    is_first_attack: bool = True,
):
    '''Cria um job do ataque de um inimigo.
    O inimigo irá atacar o jogador em um intervalo aleatório definido de
    acordo com o seu rank.
    '''

    print('CREATE_JOB_ENEMY_ATTACK()')
    make_new_attack = False
    enemy_stars_name = enemy_char.stars.name

    if not is_first_attack:
        threshold = ENEMY_CHANCE_TO_ATTACK_AGAIN_DICT[enemy_stars_name]
        make_new_attack = luck_test(threshold)

    # INIMIGO FUGIU
    if is_first_attack is not True and make_new_attack is not True:
        print(f'\t{enemy_char.full_name_with_level} FUGIU!')
        text = f'*{enemy_char.full_name_with_level}* fugiu!'
        text = create_text_in_box(
            text=text,
            section_name=SECTION_TEXT_FLEE,
            section_start=SECTION_HEAD_FLEE_START,
            section_end=SECTION_HEAD_FLEE_END,
        )
        reply_text_kwargs = dict(
            chat_id=chat_id,
            text=text,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_to_message_id=message_id,
            allow_sending_without_reply=True,
            reply_markup=get_close_keyboard(None),
        )
        await call_telegram_message_function(
            function_caller='CREATE_JOB_ENEMY_ATTACK()',
            function=context.bot.send_message,
            context=context,
            need_response=False,
            auto_delete_message=MIN_AUTODELETE_TIME,
            **reply_text_kwargs
        )

        return ConversationHandler.END

    # ESCOLHENDO JOGADOR ALVO DO ATAQUE
    try:
        if not isinstance(user_id, int):
            defender_char = choice_char(chat_id=chat_id, is_alive=True)
        else:
            char_model = CharacterModel()
            defender_char: BaseCharacter = char_model.get(user_id)

        user_id = defender_char.player_id
        player_name = defender_char.player_name
    except ValueError as error:
        print(f'CREATE_JOB_ENEMY_ATTACK(): {error}')
        return ConversationHandler.END

    # ENVIA MENSAGEM DE QUE O INIMIGO VAI ATACAR O JOGADOR
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
    defend_button = get_action_buttons(
        user_id=user_id,
        enemy=enemy_char
    )
    reply_markup = InlineKeyboardMarkup(defend_button)
    send_message_kwargs = dict(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_to_message_id=message_id,
        allow_sending_without_reply=True,
        reply_markup=reply_markup,
    )
    min_minutes = MIN_MINUTES_TO_ATTACK_FROM_RANK_DICT[enemy_stars_name]
    max_minutes = MAX_MINUTES_TO_ATTACK_FROM_RANK_DICT[enemy_stars_name]
    minutes_to_attack = randint(min_minutes, max_minutes)
    response = await call_telegram_message_function(
        function_caller='JOB_START_AMBUSH()',
        function=context.bot.send_message,
        context=context,
        auto_delete_message=timedelta(minutes=(minutes_to_attack + 30)),
        **send_message_kwargs
    )
    sleep(2)
    await forward_message(
        function_caller='JOB_START_AMBUSH()',
        user_ids=user_id,
        message=response
    )

    # CRIA JOB DE ATAQUE DO INIMIGO
    job_data = {
        'enemy_id': str(enemy_char.player_id),
        'message_id': response.message_id
    }
    job_name = get_enemy_attack_job_name(
        user_id=user_id,
        enemy=enemy_char
    )
    context.job_queue.run_once(
        callback=job_enemy_attack,
        when=timedelta(minutes=minutes_to_attack),
        data=job_data,
        chat_id=chat_id,
        user_id=user_id,
        name=job_name,
        job_kwargs=BASE_JOB_KWARGS,
    )
    put_ambush_dict(
        context=context,
        enemy=enemy_char,
        message_id=response.message_id,
        message_text=response.text_markdown_v2,
        reply_markup=response.reply_markup,
        target_id=user_id,
    )

    print(
        f'{enemy_char.full_name_with_level} ira atacar '
        f'{player_name} em {minutes_to_attack} minutos.'
    )


async def job_enemy_attack(context: ContextTypes.DEFAULT_TYPE):
    '''Após um breve tempo aleatório, o inimigo atacara um aliado.
    '''

    print('JOB_ENEMY_ATTACK()')
    char_model = CharacterModel()
    job = context.job
    chat_id = job.chat_id
    is_spawn_time = is_group_spawn_time(chat_id)
    user_id = job.user_id
    job_data = job.data
    enemy_id = job_data['enemy_id']
    message_id = job_data['message_id']
    enemy_char = get_enemy_char_from_ambush_dict(
        context=context,
        enemy_id=enemy_id
    )
    defender_char: BaseCharacter = char_model.get(user_id)
    is_first_attack = False

    send_chat_action_kwargs = dict(
        chat_id=chat_id,
        action=ChatAction.TYPING
    )
    await call_telegram_message_function(
        function_caller='EMENY.JOB_ENEMY_ATTACK()',
        function=context.bot.send_chat_action,
        context=context,
        need_response=False,
        skip_retry=True,
        **send_chat_action_kwargs
    )

    if not is_spawn_time:
        remove_ambush_enemy(context=context, enemy_id=enemy_id)
        text = (
            f'Já está tarde e *{enemy_char.full_name_with_level}* precisa ir '
            f'para casa.\n\n'
            f'O inimigo fugiu!!!'
        )
        text = create_text_in_box(
            text=text,
            section_name=SECTION_TEXT_FLEE,
            section_start=SECTION_HEAD_TIMEOUT_SPAWN_START,
            section_end=SECTION_HEAD_TIMEOUT_SPAWN_END,
        )
        await edit_message_text(
            function_caller='JOB_ENEMY_ATTACK()',
            new_text=text,
            context=context,
            chat_id=chat_id,
            message_id=message_id,
            need_response=False,
            markdown=True
        )

        return ConversationHandler.END

    if (
        enemy_char and not enemy_char.is_immobilized and
        defender_char and defender_char.is_alive
    ):
        await enemy_attack(
            context=context,
            chat_id=chat_id,
            message_id=message_id,
            enemy_char=enemy_char,
            defender_char=defender_char,
            to_dodge=True
        )
    elif defender_char and defender_char.is_dead:
        text = f'*{defender_char.player_name}* está morto.'
        print(text)
        text = create_text_in_box(
            text=text,
            section_name=SECTION_TEXT_FAIL,
            section_start=SECTION_HEAD_FAIL_START,
            section_end=SECTION_HEAD_FAIL_END,
        )
        await edit_message_text_and_forward(
            function_caller='JOB_ENEMY_ATTACK()',
            new_text=text,
            user_ids=user_id,
            context=context,
            chat_id=chat_id,
            message_id=message_id,
            need_response=False,
            markdown=True
        )
    elif not enemy_char:
        text = f'O inimigo "{enemy_id}" não existe mais.'
        print(user_id, text)
        text = create_text_in_box(
            text=text,
            section_name=SECTION_TEXT_FAIL,
            section_start=SECTION_HEAD_FAIL_START,
            section_end=SECTION_HEAD_FAIL_END,
        )
        try:
            await edit_message_text_and_forward(
                function_caller='JOB_ENEMY_ATTACK()',
                new_text=text,
                user_ids=user_id,
                context=context,
                chat_id=chat_id,
                message_id=message_id,
                need_response=False,
                markdown=True
            )
        except BadRequest as e:
            if e.message == 'Message to edit not found':
                remove_ambush_enemy(context=context, enemy_id=enemy_id)
                bad_request_text = (
                    f'A mensagem original da emboscada, de id *{message_id}*, '
                    f'não existe mais e o inimigo não está mais no dicionário '
                    f'de emboscada.'
                )
                bad_request_text = create_text_in_box(
                    text=bad_request_text,
                    section_name=SECTION_TEXT_EXCOMMUNICATED,
                    section_start=SECTION_HEAD_FAIL_START,
                    section_end=SECTION_HEAD_FAIL_END,
                )
                await reply_text(
                    function_caller='JOB_ENEMY_ATTACK()',
                    text=bad_request_text,
                    context=context,
                    chat_id=chat_id,
                    user_id=user_id,
                    message_id=message_id,
                    markdown=True,
                    allow_sending_without_reply=True,
                    need_response=False,
                    auto_delete_message=MIN_AUTODELETE_TIME,
                )
    elif enemy_char.is_immobilized:
        is_first_attack = True
        enemy_name = enemy_char.player_name
        immobilized_names = enemy_char.status.immobilized_names()
        text = (
            f'*{enemy_name}* não pôde atacar, pois está {immobilized_names}.'
        )
        text += enemy_char.activate_status_string()
        print(user_id, text)
        text = create_text_in_box(
            text=text,
            section_name=SECTION_TEXT_FAIL,
            section_start=SECTION_HEAD_FAIL_START,
            section_end=SECTION_HEAD_FAIL_END,
        )
        await edit_message_text_and_forward(
            function_caller='JOB_ENEMY_ATTACK()',
            new_text=text,
            user_ids=user_id,
            context=context,
            chat_id=chat_id,
            message_id=message_id,
            need_response=False,
            markdown=True
        )

    remove_ambush_enemy(context=context, enemy_id=enemy_id)

    if enemy_char and enemy_char.is_alive and message_id:
        await create_job_enemy_attack(
            context=context,
            chat_id=chat_id,
            message_id=message_id,
            enemy_char=enemy_char,
            is_first_attack=is_first_attack,
        )


@skip_if_no_singup_player
@skip_if_dead_char
@skip_if_immobilized
@confusion()
@print_basic_infos
async def defend_enemy_attack(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    '''Defende aliado de um ataque. Caso sobreviva, ambos receberão XP.
    '''

    print('DEFEND_ENEMY_ATTACK()')
    await reply_typing(
        function_caller='ENEMY.DEFEND_ENEMY_ATTACK()',
        update=update,
        context=context,
    )
    char_model = CharacterModel()
    chat_id = update.effective_chat.id
    defender_user_id = update.effective_user.id
    query = update.callback_query
    message_id = query.message.message_id
    data = callback_data_to_dict(query.data)
    target_user_id = data['user_id']
    enemy_id = data['enemy_id']
    enemy_char = get_enemy_char_from_ambush_dict(
        context=context,
        enemy_id=enemy_id
    )
    already_attacked = check_attacker_id_in_ambush_dict(
        context=context,
        enemy_id=enemy_id,
        attacker_id=defender_user_id
    )

    defender_char: BaseCharacter = char_model.get(defender_user_id)
    if not defender_char.can_player_act:
        create_job_rest_action_point(
            context=context,
            chat_id=chat_id,
            user_id=defender_user_id,
        )
        query_text = (
            'Você não possui PONTO(S) DE AÇÃO suficiente(s) '
            'para realizar essa AÇÃO!'
        )
        await answer(query=query, text=query_text, show_alert=True)

        return ConversationHandler.END

    if not enemy_char:
        query_text = 'Essa emboscada já terminou'
        await answer(query=query, text=query_text, show_alert=True)
        await delete_message(
            function_caller='DEFEND_ENEMY_ATTACK()',
            context=context,
            query=query,
        )

        return ConversationHandler.END

    if defender_user_id == target_user_id:
        query_text = 'Você não pode defender a si mesmo.'
        await answer(query=query, text=query_text, show_alert=True)

        return ConversationHandler.END

    if already_attacked:
        query_text = (
            'Você não pode defender este ataque, '
            'pois já atacou este INIMIGO!!!'
        )
        await answer(query=query, text=query_text, show_alert=True)

        return ConversationHandler.END

    target_char: BaseCharacter = char_model.get(target_user_id)
    if target_char.is_alive:
        await enemy_attack(
            context=context,
            chat_id=chat_id,
            message_id=message_id,
            enemy_char=enemy_char,
            defender_char=defender_char,
            target_char=target_char,
            to_dodge=True
        )
    else:
        text = (
            f'Defesa falhou, pois '
            f'*{target_char.player_name}* está morto.'
        )
        print(text)
        text = create_text_in_box(
            text=text,
            section_name=SECTION_TEXT_FAIL_AMBUSH_DEFENSE,
            section_start=SECTION_HEAD_FAIL_START,
            section_end=SECTION_HEAD_FAIL_END,
        )
        await edit_message_text_and_forward(
            function_caller='DEFEND_ENEMY_ATTACK()',
            new_text=text,
            user_ids=[defender_user_id, target_user_id],
            context=context,
            chat_id=chat_id,
            message_id=message_id,
            need_response=False,
            markdown=True,
        )

    remove_enemy_attack_job(
        context=context,
        user_id=target_user_id,
        enemy_char=enemy_char
    )
    remove_ambush_enemy(context=context, enemy_id=enemy_id)
    # if defender_char.is_alive and target_char.is_alive:
    #     await enemy_drop_random_loot(
    #         context=context,
    #         update=update,
    #         enemy_char=enemy_char,
    #         from_attack=False,
    #     )

    await sub_action_point(
        context=context,
        char=defender_char,
        query=query
    )

    if enemy_char and enemy_char.is_alive and message_id:
        await create_job_enemy_attack(
            context=context,
            chat_id=chat_id,
            message_id=message_id,
            enemy_char=enemy_char,
            is_first_attack=False,
        )


@skip_if_no_singup_player
@skip_if_dead_char
@skip_if_immobilized
@confusion()
@print_basic_infos
async def player_attack_enemy(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    '''Função que o jogador ataca um Inimigo
    '''

    print('PLAYER_ATTACK_ENEMY()')
    await reply_typing(
        function_caller='ENEMY.PLAYER_ATTACK_ENEMY()',
        update=update,
        context=context,
    )
    char_model = CharacterModel()
    chat_id = update.effective_chat.id
    attacker_user_id = update.effective_user.id
    query = update.callback_query

    message_id = query.message.message_id
    data = callback_data_to_dict(query.data)
    target_user_id = data['user_id']
    enemy_id = data['enemy_id']
    enemy_char = get_enemy_char_from_ambush_dict(
        context=context,
        enemy_id=enemy_id
    )

    attacker_char: BaseCharacter = char_model.get(attacker_user_id)
    if not attacker_char.can_player_act:
        create_job_rest_action_point(
            context=context,
            chat_id=chat_id,
            user_id=attacker_user_id,
        )
        query_text = (
            'Você não possui PONTO(S) DE AÇÃO suficiente(s) '
            'para realizar essa AÇÃO!'
        )
        await answer(query=query, text=query_text, show_alert=True)

        return ConversationHandler.END

    if not enemy_char:
        query_text = 'Essa emboscada já terminou'
        await answer(query=query, text=query_text, show_alert=True)
        await delete_message(
            function_caller='PLAYER_ATTACK_ENEMY()',
            context=context,
            query=query,
        )

        return ConversationHandler.END

    if attacker_user_id == target_user_id and not enemy_char.is_any_boss:
        query_text = 'Você não tem a habilidade de contra atacar.'
        await answer(query=query, text=query_text, show_alert=True)

        return ConversationHandler.END

    target_char: BaseCharacter = char_model.get(target_user_id)

    await player_attack(
        update=update,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        enemy_char=enemy_char,
        attacker_char=attacker_char,
        target_char=target_char,
        to_dodge=True,
        query=query,
    )

    await sub_action_point(
        context=context,
        char=attacker_char,
        query=query
    )


async def check_enemy_attributes(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    '''Exibe um alerta os Atributos de Base ou de Combate'''

    print('CHECK_ENEMY_ATTRIBUTES()')
    query = update.callback_query
    data = callback_data_to_dict(query.data)
    attr_name = data['command']
    enemy_id = data['enemy_id']
    enemy_char = get_enemy_char_from_ambush_dict(
        context=context,
        enemy_id=enemy_id
    )
    text = f'enemy_char: {enemy_char}'

    if not enemy_char:
        query_text = 'Essa emboscada já terminou'
        await answer(query=query, text=query_text, show_alert=True)
        await delete_message(
            function_caller='CHECK_ENEMY_ATTRIBUTES()',
            context=context,
            query=query,
        )

        return ConversationHandler.END

    if attr_name == CALLBACK_TEXT_BASE_ATTRIBUTES:
        text = enemy_char.base_stats.alert_sheet()
    elif attr_name == CALLBACK_TEXT_COMBAT_ATTRIBUTES:
        text = enemy_char.combat_stats.alert_sheet()

    await answer(query=query, text=text, show_alert=True)


async def enemy_attack(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    message_id: int,
    enemy_char: NPCharacter,
    defender_char: PlayerCharacter,
    target_char: PlayerCharacter = None,
    to_dodge: bool = False,
) -> Union[Message, bool]:
    '''Função que o Inimigo ataca um jogador
    '''

    defender_id = defender_char.player_id
    target_id = defender_char.player_id
    report_text = ''
    if target_char and target_char.is_alive:
        target_id = target_char.player_id
        section_name = SECTION_TEXT_AMBUSH_DEFENSE
        report_text = (
            f'{defender_char.player_name} defendeu '
            f'{target_char.player_name}.\n\n'
        )
    else:
        section_name = SECTION_TEXT_AMBUSH_ATTACK

    attack_report = enemy_char.to_attack(
        defender_char=defender_char,
        defender_dice=None,
        to_dodge=to_dodge,
        to_defend=True,
        rest_command=REST_COMMANDS[0],
        verbose=True,
        markdown=True
    )
    report_text += attack_report['text']
    attacker_action_name = attack_report['attack']['action']
    attacker_skill: BaseSkill = attack_report['attack']['skill']

    if not attack_report['dead']:
        base_xp = get_base_xp_from_enemy_attack(enemy_char, defender_char)
        report_xp = add_xp(
            chat_id=chat_id,
            char=defender_char,
            base_xp=base_xp,
            save_status=True,
        )
        report_text += ALERT_SECTION_HEAD.format('*XP*') + '\n'
        if target_char and target_char.is_alive:
            base_xp = get_base_xp_from_enemy_attack(enemy_char, target_char)
            target_report_xp = add_xp(
                chat_id=chat_id,
                char=target_char,
                base_xp=base_xp,
            )
            report_text += f'{target_report_xp["text"]}\n'
        report_text += f'{report_xp["text"]}\n\n'
    else:
        save_char(char=defender_char)

    skill_defense_type = attacker_skill.skill_defense
    report_text = create_text_in_box(
        text=report_text,
        section_name=section_name,
        section_start=SECTION_START_DICT[skill_defense_type],
        section_end=SECTION_END_DICT[skill_defense_type]
    )

    response = await edit_message_text_and_forward(
        function_caller='ENEMY_ATTACK()',
        new_text=report_text,
        user_ids=[target_id, defender_id],
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        markdown=True,
    )

    if attack_report['dead']:
        user_id = defender_char.player_id
        player_name = defender_char.player_name
        drop_items = drop_random_items_from_bag(user_id=user_id)
        await send_drop_message(
            context=context,
            items=drop_items,
            text=f'{player_name} morreu e dropou o item',
            message_id=message_id,
            silent=True,
        )

    return response


async def player_attack(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    message_id: int,
    enemy_char: NPCharacter,
    attacker_char: PlayerCharacter,
    target_char: PlayerCharacter,
    to_dodge: bool = False,
    attacker_skill: BaseSkill = None,
    query: CallbackQuery = None
) -> dict:
    '''Função que o Jogador ataca um Inimigo
    '''
    attacker_is_target = False
    if target_char and attacker_char.player_id == target_char.player_id:
        target_char = attacker_char
        attacker_is_target = True

    attacker_id = attacker_char.player_id
    target_id = target_char.player_id if target_char else None
    enemy_id = str(enemy_char.player_id)
    reply_markup = get_reply_markup_from_ambush_dict(
        context=context,
        enemy_id=enemy_id,
    )
    report_text = get_message_text_from_ambush_dict(
        context=context,
        enemy_id=enemy_id,
    )
    report_text = report_text.split('\n')
    report_text = '\n'.join(report_text[1:-1])
    report_text = report_text.strip()
    report_text += f'\n\n{TEXT_SEPARATOR}\n\n'
    counter_report = None

    # ATACA se INIMIGO estiver vivo
    if enemy_char.is_alive:
        attack_report = attacker_char.to_attack(
            defender_char=enemy_char,
            defender_dice=None,
            attacker_skill=attacker_skill,
            to_dodge=to_dodge,
            to_defend=True,
            verbose=True,
            markdown=True
        )
        new_report_text = attack_report['text']
        attacker_action_name = attack_report['attack']['action']
        attacker_skill: BaseSkill = attack_report['attack']['skill']
        is_miss = attack_report['defense']['is_miss']

        base_xp = get_base_xp_from_player_attack(
            enemy_char=enemy_char,
            attacker_char=attacker_char,
            is_miss=is_miss
        )
        report_xp = add_xp(
            chat_id=chat_id,
            char=attacker_char,
            base_xp=base_xp,
        )
        new_report_text += ALERT_SECTION_HEAD.format('*XP*') + '\n'
        new_report_text += f'{report_xp["text"]}\n'

        # XP PARA O ALVO SE O INIMIGO MORREU
        if target_char and attack_report['dead'] and not attacker_is_target:
            base_xp = get_base_xp_from_player_attack(
                enemy_char=enemy_char,
                attacker_char=target_char,
                is_miss=is_miss
            )
            target_report_xp = add_xp(
                chat_id=chat_id,
                char=target_char,
                base_xp=base_xp,
            )
            new_report_text += f'{target_report_xp["text"]}\n\n'
            new_report_text += f'O inimigo foi derrotado!!!\n\n'
        # CONTRA-ATAQUE SE O INIMIGO ESQUIVO E O ATACANTE ESTIVER VIVO
        elif is_miss and attacker_char.is_alive:
            section_head = SECTION_HEAD.format('CONTRA-ATAQUE')
            enemy_speech = get_enemy_counter_speech(enemy_char)
            new_report_text += f'\n{section_head}\n>{enemy_speech}\n\n'
            counter_report = enemy_char.to_attack(
                defender_char=attacker_char,
                defender_dice=10,
                to_dodge=True,
                to_defend=True,
                verbose=True,
                markdown=True
            )
            new_report_text += counter_report['text']
            save_char(char=attacker_char)

        if enemy_char.is_alive and target_char and target_char.is_dead:
            new_report_text += (
                f'\n\n'
                f'{target_char.full_name} ({target_char.player_name}) '
                f'está morto, por isso a emboscada será encerrada.'
            )
        if attack_report['dead'] or target_char.is_dead:
            reply_markup = REPLY_MARKUP_DEFAULT

        skill_defense_type = attacker_skill.skill_defense
        report_text = resize_text(report_text + new_report_text)
        report_text = create_text_in_box(
            text=report_text,
            section_name=SECTION_TEXT_AMBUSH_COUNTER,
            section_start=SECTION_START_DICT[skill_defense_type],
            section_end=SECTION_END_DICT[skill_defense_type],
            clean_func=escape_for_citation_markdown_v2,
        )
        add_attacker_id_to_ambush_dict(
            context=context,
            enemy_id=enemy_id,
            attacker_id=attacker_id,
        )
        await add_enemy_counter(
            user_id=attacker_id,
            enemy=enemy_char,
            query=query
        )
    # NÃO ATACA se o INIMIGO estiver morto
    elif enemy_char.is_dead:
        reply_markup = REPLY_MARKUP_DEFAULT
        report_text = (
            f'O ataque falhou, pois '
            f'*{enemy_char.full_name_with_level}* está morto.'
        )
        print(report_text)
        report_text = new_report_text = create_text_in_box(
            text=report_text,
            section_name=SECTION_TEXT_FAIL_AMBUSH_COUNTER,
            section_start=SECTION_HEAD_FAIL_START,
            section_end=SECTION_HEAD_FAIL_END,
        )

    try:
        if message_id is None:
            raise BadRequest('Message to edit not found')
        user_ids = list({
            _id
            for _id in [attacker_id, target_id]
            if _id is not None
        })
        await edit_message_text_and_forward(
            function_caller='PLAYER_ATTACK()',
            new_text=report_text,
            user_ids=user_ids,
            context=context,
            chat_id=chat_id,
            message_id=message_id,
            need_response=False,
            markdown=True,
            reply_markup=reply_markup
        )
    except BadRequest as e:
        if e.message == 'Message to edit not found':
            remove_enemy_attack_job(
                context=context,
                user_id=target_id,
                enemy_char=enemy_char
            )
            remove_ambush_enemy(context=context, enemy_id=enemy_id)
            bad_request_text = (
                f'A mensagem original da emboscada, de id *{message_id}*, '
                f'não existe mais. Por isso, '
                f'*{enemy_char.full_name_with_level}* foi retirado do '
                f'dicionário de emboscada.'
            )
            bad_request_text = create_text_in_box(
                text=bad_request_text,
                section_name=SECTION_TEXT_EXCOMMUNICATED,
                section_start=SECTION_HEAD_FAIL_START,
                section_end=SECTION_HEAD_FAIL_END,
            )
            await reply_text(
                function_caller='PLAYER_ATTACK()',
                text=bad_request_text,
                context=context,
                update=update,
                user_id=target_id,
                markdown=True,
                allow_sending_without_reply=True,
                need_response=False,
                auto_delete_message=MIN_AUTODELETE_TIME,
            )

    set_message_text_from_ambush_dict(
        context=context,
        enemy_id=enemy_id,
        new_message_text=report_text,
    )

    # Dropa itens do ATACANTE se ouve um contra-ataque e ele morreu
    if counter_report and counter_report['dead']:
        user_id = attacker_char.player_id
        player_name = attacker_char.player_name
        drop_items = drop_random_items_from_bag(user_id=user_id)
        await send_drop_message(
            context=context,
            items=drop_items,
            text=f'{player_name} morreu e dropou o item',
            message_id=message_id,
            silent=True,
        )

    if enemy_char.is_dead or (target_char and target_char.is_dead):
        remove_enemy_attack_job(
            context=context,
            user_id=target_id,
            enemy_char=enemy_char
        )
        remove_ambush_enemy(context=context, enemy_id=enemy_id)

    if enemy_char.is_dead and attacker_char.is_alive:
        await enemy_drop_random_loot(
            context=context,
            chat_id=chat_id,
            message_id=message_id,
            enemy_char=enemy_char,
            from_attack=True,
        )

    return {'text': new_report_text}


async def player_attack_player(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    attacker_char: PlayerCharacter,
    defender_char: PlayerCharacter,
    to_dodge: bool = False,
    attacker_skill: BaseSkill = None,
) -> dict:
    '''Função que o Jogador ataca outro Jogador
    '''

    attacker_id = attacker_char.player_id
    defender_id = str(defender_char.player_id)

    # ATACA se INIMIGO estiver vivo
    if defender_char.is_alive:
        attack_report = attacker_char.to_attack(
            defender_char=defender_char,
            defender_dice=None,
            attacker_skill=attacker_skill,
            to_dodge=to_dodge,
            to_defend=True,
            verbose=True,
            markdown=True
        )
        report_text = attack_report['text']
        attacker_skill: BaseSkill = attack_report['attack']['skill']

        skill_defense_type = attacker_skill.skill_defense
        report_text = create_text_in_box(
            text=report_text,
            section_name=SECTION_TEXT_ALLY_ATTACK,
            section_start=SECTION_START_DICT[skill_defense_type],
            section_end=SECTION_END_DICT[skill_defense_type],
            clean_func=escape_for_citation_markdown_v2,
        )
    # NÃO ATACA se o ALVO estiver morto
    elif defender_char.is_dead:
        report_text = (
            f'O ataque falhou, pois '
            f'*{defender_char.full_name_with_level}* está morto.'
        )
        print(report_text)
        report_text = create_text_in_box(
            text=report_text,
            section_name=SECTION_TEXT_FAIL_ALLY_ATTACK,
            section_start=SECTION_HEAD_FAIL_START,
            section_end=SECTION_HEAD_FAIL_END,
        )

    await reply_text(
        function_caller='PLAYER_ATTACK_PLAYER()',
        text=report_text,
        context=context,
        update=update,
        markdown=True,
        allow_sending_without_reply=True,
        need_response=False,
        auto_delete_message=MIN_AUTODELETE_TIME,
    )

    return {'text': report_text}


def resize_text(
    text: str,
    spliter: str = TEXT_SEPARATOR,
) -> str:
    '''Reduz o tamanho do texto para que a mensagem não ultrapasse
    o limite de caracteres.
    '''

    text_list = text.split(spliter)
    final_text_list = text_list
    if len(text_list) > 3:
        start_text_list = [text_list[0]]
        final_text_list = start_text_list + text_list[-2:]

    return spliter.join(final_text_list).strip()


def get_action_buttons(
    user_id: int,
    enemy: NPCharacter
) -> List[InlineKeyboardButton]:
    '''Retorna o botão para defender um aliado.
    '''

    enemy_id = str(enemy.player_id)
    return [
        [
            InlineKeyboardButton(
                text=ATTACK_BUTTON_TEXT,
                callback_data=callback_data_to_string({
                    'command': CALLBACK_TEXT_ATTACK,
                    'enemy_id': enemy_id,
                    'user_id': user_id,
                })
            ),
            InlineKeyboardButton(
                text=DEFEND_BUTTON_TEXT,
                callback_data=callback_data_to_string({
                    'command': CALLBACK_TEXT_DEFEND,
                    'enemy_id': enemy_id,
                    'user_id': user_id,
                })
            )
        ],
        [
            InlineKeyboardButton(
                text=BASE_ATTRIBUTES_BUTTON_TEXT,
                callback_data=callback_data_to_string({
                    'command': CALLBACK_TEXT_BASE_ATTRIBUTES,
                    'enemy_id': enemy_id,
                    'user_id': user_id,
                })
            ),
            InlineKeyboardButton(
                text=COMBAT_ATTRIBUTES_BUTTON_TEXT,
                callback_data=callback_data_to_string({
                    'command': CALLBACK_TEXT_COMBAT_ATTRIBUTES,
                    'enemy_id': enemy_id,
                    'user_id': user_id,
                })
            )
        ]
    ]


def get_enemy_attack_job_name(user_id: int, enemy: NPCharacter) -> str:
    '''Nome do job do ataque inimigo
    '''

    enemy_id = str(enemy.player_id)
    return f'JOB_ENEMY_ATTACK_{user_id}_{enemy_id}'


def get_enemy_counter_speech(enemy: NPCharacter) -> str:
    enemy_alignment = enemy.alignment.name
    text_list = COUNTER_LINES[enemy_alignment]
    text = choice(text_list)

    return f'>{text}'


def put_ambush_dict(
    context: ContextTypes.DEFAULT_TYPE,
    enemy: NPCharacter,
    message_id: int,
    message_text: str,
    reply_markup: InlineKeyboardMarkup,
    target_id: int,
):
    '''Adiciona o inimigo ao dicionário de ambushes, em que a chave é a
    enemy_id.
    '''

    enemy_id = str(enemy.player_id)
    ambushes = context.chat_data.get('ambushes', {})
    ambushes[enemy_id] = {
        'enemy': enemy,
        'attacker_id_list': [],
        'message_id': message_id,
        'message_text': message_text,
        'reply_markup': reply_markup,
        'target_id': target_id,
    }
    if not 'ambushes' in context.chat_data:
        context.chat_data['ambushes'] = ambushes


def add_attacker_id_to_ambush_dict(
    context: ContextTypes.DEFAULT_TYPE,
    enemy_id: str,
    attacker_id: int,
):
    '''Adiciona o attacker_id ao dicionário ambushes.
    '''

    enemy_ambush = get_enemy_dict_from_ambush_dict(
        context=context,
        enemy_id=enemy_id,
    )
    if enemy_ambush:
        attacker_id_list = enemy_ambush['attacker_id_list']
        attacker_id_list.append(attacker_id)


def check_attacker_id_in_ambush_dict(
    context: ContextTypes.DEFAULT_TYPE,
    enemy_id: str,
    attacker_id: int,
) -> bool:
    '''Verifica se o attacker_id está no dicionário de uma emboscada inimiga.
    Retorna True se estiver, False caso contrário.
    '''

    in_ambush = False
    ambushes = context.chat_data.get('ambushes', {})
    enemy_ambush = ambushes.get(enemy_id, {})
    if enemy_ambush:
        attacker_id_list = enemy_ambush['attacker_id_list']
        in_ambush = attacker_id in attacker_id_list

    return in_ambush


def get_all_enemy_id_from_ambush_dict(
    context: ContextTypes.DEFAULT_TYPE
) -> List[str]:
    ambushes = context.chat_data.get('ambushes', {})
    return list(ambushes.keys())


def get_all_enemy_char_from_ambush_dict(
    context: ContextTypes.DEFAULT_TYPE,
    filter_target_id: int = None,
) -> List[NPCharacter]:
    ambushes = context.chat_data.get('ambushes', {})
    return [
        value['enemy']
        for value in ambushes.values()
        if filter_target_id != value['target_id'] or value['enemy'].is_any_boss
    ]


def get_enemy_dict_from_ambush_dict(
    context: ContextTypes.DEFAULT_TYPE,
    enemy_id: str,
) -> dict:
    '''Retorna o dicionário do inimigo a partir do enemy_id.
    '''

    ambushes = context.chat_data.get('ambushes', {})
    return ambushes.get(enemy_id, {})


def get_enemy_char_from_ambush_dict(
    context: ContextTypes.DEFAULT_TYPE,
    enemy_id: str,
) -> NPCharacter:
    '''Retorna um NPCharacter do dicionário ambushes a partir do enemy_id e o
    remove do dicionário.
    '''

    return get_enemy_dict_from_ambush_dict(
        context=context,
        enemy_id=enemy_id,
    ).get('enemy', None)


def get_message_text_from_ambush_dict(
    context: ContextTypes.DEFAULT_TYPE,
    enemy_id: str,
) -> str:
    '''Retorna a mensagem do inimigo a partir do enemy_id.
    '''

    return get_enemy_dict_from_ambush_dict(
        context=context,
        enemy_id=enemy_id,
    ).get('message_text', '')


def get_reply_markup_from_ambush_dict(
    context: ContextTypes.DEFAULT_TYPE,
    enemy_id: str,
) -> str:
    '''Retorna a mensagem do inimigo a partir do enemy_id.
    '''

    return get_enemy_dict_from_ambush_dict(
        context=context,
        enemy_id=enemy_id,
    ).get('reply_markup', '')


def set_message_text_from_ambush_dict(
    context: ContextTypes.DEFAULT_TYPE,
    enemy_id: str,
    new_message_text: str,
):
    '''Retorna a mensagem do inimigo a partir do enemy_id.
    '''

    enemy_dict = get_enemy_dict_from_ambush_dict(
        context=context,
        enemy_id=enemy_id,
    )
    enemy_dict['message_text'] = new_message_text


def remove_ambush_enemy(
    context: ContextTypes.DEFAULT_TYPE,
    enemy_id: str
):
    '''Remove o inimigo do dicionário ambushes.
    '''

    ambushes = context.chat_data.get('ambushes', {})
    ambushes.pop(enemy_id, None)
    context.chat_data['ambushes'] = ambushes


async def sub_action_point(
    context: ContextTypes.DEFAULT_TYPE,
    char: BaseCharacter,
    query: CallbackQuery,
    value: int = 1,
):
    '''Subtrai Pontos de Ação do personagem, salva o personagem no banco,
    cria job de recuperação de Pontos de Ação e
    envia pop-up com os Pontos de Ação atualizados.
    '''

    chat_id = query.message.chat_id
    user_id = char.player_id
    char.sub_action_points(value)
    save_char(char=char)
    create_job_rest_action_point(
        context=context,
        chat_id=chat_id,
        user_id=user_id,
        char=char,
    )

    await answer(query=query, text=char.current_action_points_text)


async def add_enemy_counter(
    user_id: int,
    enemy: NPCharacter,
    query: CallbackQuery,
):
    if enemy.is_dead:
        player_model = PlayerModel()
        player: Player = player_model.get(user_id)
        report = player.add_enemy_counter(enemy=enemy)
        player_model.save(player)

        if query:
            await answer(query=query, text=report['text'])


async def send_ambush_message(
    context: ContextTypes.DEFAULT_TYPE,
    silent: bool = None,
) -> int:
    '''Envia a primeira mensagem da Emboscada
    '''

    chat_id = context._chat_id
    ambush_text = choice(AMBUSH_TEXTS)
    ambush_text = create_text_in_box(
        text=ambush_text,
        section_name=SECTION_TEXT_AMBUSH,
        section_start=SECTION_HEAD_ENEMY_START,
        section_end=SECTION_HEAD_ENEMY_END
    )
    send_message_kwargs = dict(
        chat_id=chat_id,
        text=ambush_text,
        disable_notification=silent,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=get_close_keyboard(user_id=None)
    )

    response = await call_telegram_message_function(
        function_caller='SEND_AMBUSH_MESSAGE()',
        function=context.bot.send_message,
        context=context,
        auto_delete_message=MIN_AUTODELETE_TIME,
        **send_message_kwargs
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

    print('ADD_XP_GROUP()')
    char_list = get_player_chars_from_group(chat_id=chat_id, is_alive=True)
    total_allies = len(char_list)

    sum_level = sum([enemy.level for enemy in enemy_list])
    sum_multiplier = sum([enemy.points_multiplier for enemy in enemy_list])
    avg_level = sum_level // len(enemy_list)
    multiplied_level = (avg_level * sum_multiplier)

    full_text = ''
    sorted_char_list = sorted(
        char_list,
        key=attrgetter('level', 'xp'),
        reverse=True
    )
    for char in sorted_char_list:
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
    send_message_kwargs = dict(
        chat_id=chat_id,
        text=full_text,
        disable_notification=silent,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_to_message_id=message_id,
        allow_sending_without_reply=True,
        reply_markup=get_close_keyboard(None),
    )

    await call_telegram_message_function(
        function_caller='ADD_XP_GROUP()',
        function=context.bot.send_message,
        context=context,
        need_response=False,
        auto_delete_message=MIN_AUTODELETE_TIME,
        **send_message_kwargs
    )


def remove_enemy_attack_job(
    context: ContextTypes.DEFAULT_TYPE,
    user_id: int,
    enemy_char: NPCharacter
) -> bool:
    '''Remove o job de Ataque do Inimigo.
    '''

    job_name = get_enemy_attack_job_name(
        user_id=user_id,
        enemy=enemy_char
    )
    return remove_job_by_name(context=context, job_name=job_name)


async def enemy_drop_random_loot(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    message_id: int,
    enemy_char: NPCharacter,
    from_attack: bool,
):
    '''Envia uma mensagens de drops de itens quando um aliado defende outro.
    '''

    item_model = ItemModel()
    silent = get_attribute_group_or_player(chat_id, 'silent')
    points_multiplier = enemy_char.bs.points_multiplier

    if from_attack:
        group_level = enemy_char.level + (points_multiplier * 5)
        total_consumables = randint(1, int(points_multiplier + 2))
        total_equipments = randint(1, ceil(points_multiplier / 2))
    else:
        group_level = ceil(enemy_char.level * 0.90)
        total_consumables = 1
        total_equipments = randint(0, 1)

    consumable_list = list(create_random_consumable(
        group_level=group_level,
        random_level=True,
        total_items=total_consumables
    ))

    if from_attack:
        equips_list = list(enemy_char.equips)
    else:
        equips_list = [choice(list(enemy_char.equips))]

    equips_list = [
        Item(equipment)
        for equipment in equips_list
        if isinstance(equipment, Equipment)
    ]

    all_equipment_list = [
        create_random_equipment(
            equip_type=None,
            group_level=group_level,
            random_level=True,
        )
        for _ in range(total_equipments)
    ]
    all_equipment_list.extend(equips_list)

    for equipment_item in all_equipment_list:
        if isinstance(equipment_item, Item):
            equipment = equipment_item.item
            item_model.save(equipment)

    drops = [
        item
        for item in (consumable_list + all_equipment_list)
        if item is not None
    ]
    shuffle(drops)

    if from_attack:
        text = f'{enemy_char.full_name_with_level} foi derrotado e deixou'
    else:
        text = f'{enemy_char.full_name_with_level} fugiu e deixou para trás'

    await send_drop_message(
        context=context,
        items=drops,
        text=text,
        message_id=message_id,
        silent=silent,
    )


AMBUSH_HANDLERS = [
    CallbackQueryHandler(
        defend_enemy_attack,
        pattern=PATTERN_DEFEND
    ),
    CallbackQueryHandler(
        player_attack_enemy,
        pattern=PATTERN_ATTACK
    ),
    CallbackQueryHandler(
        check_enemy_attributes,
        pattern=PATTERN_ATTRIBUTES
    ),
]
