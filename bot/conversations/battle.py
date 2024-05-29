'''
Módulo responsável por gerenciar as batalhas

context.chat_data['battle_response'] -> Message que exibe informações da luta
context.chat_data['battle_id'] -> _id da batalha
context.chat_data['action'] -> Ação do atacante
context.chat_data['defender_index'] -> Índice do alvo na lista "turn_order"
'''


from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    PrefixHandler
)

from bot.constants.battle import (
    COMMANDS,
    CANCEL_COMMANDS,
    CALLBACK_ENTER_BLUE_TEAM,
    CALLBACK_ENTER_RED_TEAM,
    CALLBACK_START_BATTLE,
    CALLBACK_PHYSICAL_ATTACK,
    CALLBACK_PRECISION_ATTACK,
    CALLBACK_MAGICAL_ATTACK,
    ATTACK_TYPE,
    ACTIONS,
    ACTIONS_LABELS,
    CALLBACK_DODGE,
    CALLBACK_DEFEND,
    DEFENSE_TYPE,
    REACTIONS_LABELS,
    TEAMS,
)
from bot.functions.chat import answer, edit_message_text
from rpgram.enums import EmojiEnum
from bot.constants.filters import (
    BASIC_COMMAND_IN_GROUP_FILTER,
    PREFIX_COMMANDS
)
from bot.conversations.rest import stop_resting
from bot.decorators import print_basic_infos, need_have_char, need_singup_group
from bot.functions.general import get_attribute_group_or_player

from constant.time import ONE_HOUR_IN_SECONDS

from repository.mongo import (
    BattleModel,
    CharacterModel,
    GroupModel
)

from rpgram import Battle, Dice
from rpgram.characters import BaseCharacter, PlayerCharacter
from rpgram.errors import EmptyTeamError


# ROUTES
(
    ENTER_BATTLE_ROUTES,
    SELECT_ACTION_ROUTES,
    SELECT_TARGET_ROUTES,
    SELECT_REACTION_ROUTES,
    END_ROUTES,
) = range(5)


@need_singup_group
@need_have_char
@print_basic_infos
async def battle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('battle_start')
    battle_model = BattleModel()
    chat_id = update.effective_chat.id
    silent = get_attribute_group_or_player(chat_id, 'silent')
    chat_battle = battle_model.get(query={'chat_id': chat_id})

    if not chat_battle:
        battle = Battle(blue_team=[], red_team=[], chat_id=chat_id)
        battle_result = battle_model.save(battle)
        battle_id = battle_result.inserted_id
    elif chat_battle.started is True:
        battle_id = chat_battle._id
        user_name = chat_battle.current_player.player_name
        reply_markup = get_action_inline_keyboard()
        response = await update.effective_message.reply_text(
            f'A batalha retomada!\n'
            f'{user_name}, escolha sua ação.\n\n'
            f'{chat_battle.get_sheet()}\n',
            reply_markup=reply_markup,
            disable_notification=silent,
            allow_sending_without_reply=True
        )
        context.chat_data['battle_response'] = response
        context.chat_data['battle_id'] = battle_id
        return SELECT_ACTION_ROUTES
    elif chat_battle:
        battle = chat_battle
        battle_id = chat_battle._id

    reply_markup = get_enter_battle_inline_keyboard()
    response = await update.effective_message.reply_text(
        battle.get_teams_sheet(),
        reply_markup=reply_markup,
        disable_notification=silent,
        allow_sending_without_reply=True
    )
    context.chat_data['battle_response'] = response
    context.chat_data['battle_id'] = battle_id
    return ENTER_BATTLE_ROUTES


# ENTER_BATTLE_ROUTES
@need_have_char
@print_basic_infos
async def enter_battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('enter_battle')
    battle_model = BattleModel()
    character_model = CharacterModel()
    query = update.callback_query
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    message_id = update.effective_message.message_id
    battle_id = context.chat_data['battle_id']
    character = character_model.get(user_id)
    character_id = character._id
    battle = battle_model.get(battle_id)
    other_battle = battle_model.get(
        query={'$and': [
            {'$or': [{'blue_team': character_id}, {'red_team': character_id}]},
            {'chat_id': {'$ne': chat_id}}
        ]}
    )

    if query.data == CALLBACK_START_BATTLE:
        if not battle.in_battle(character):
            query_text = (
                'Você não pode iniciar a batalha, '
                'pois seu personagem não está participando dela.'
            )
            await answer(query=query, text=query_text, show_alert=True)
            return ENTER_BATTLE_ROUTES
        user_name = battle.current_player.player_name
        reply_markup = get_action_inline_keyboard()
        try:
            battle.start_battle()
            battle_model.save(battle)
            await answer(query=query, text='A BATALHA COMEÇOU!!!')
            new_text = (
                f'A batalha começou!\n'
                f'{user_name}, escolha sua ação.\n\n'
                f'{battle.get_sheet()}\n'
            )
            await edit_message_text(
                function_caller='BATTLE.ENTER_BATTLE()',
                new_text=new_text,
                context=context,
                chat_id=chat_id,
                message_id=message_id,
                need_response=False,
                markdown=False,
                reply_markup=reply_markup,
            )

            return SELECT_ACTION_ROUTES
        except EmptyTeamError as error:
            await answer(query=query, text=f'{error}', show_alert=True)
            return ENTER_BATTLE_ROUTES

    if not other_battle and character.is_alive:
        team = query.data
        time = TEAMS[team]
        resting_status = ''
        if check_if_change_for_same_team(team, character, battle):
            query_text = f'Seu personagem já está no Time {time}!'
            await answer(query=query, text=query_text)
            return ENTER_BATTLE_ROUTES
        battle.enter_battle(character, team)
        battle_model.save(battle)
        if stop_resting(user_id, context):
            resting_status = '\nVocê parou de descansar!'
        reply_markup = get_enter_battle_inline_keyboard()
        query_text = f'Seu personagem entrou no Time {time}! {resting_status}'
        await answer(query=query, text=query_text)
        await edit_message_text(
            function_caller='BATTLE.ENTER_BATTLE()',
            new_text=battle.get_teams_sheet(),
            context=context,
            chat_id=chat_id,
            message_id=message_id,
            need_response=False,
            markdown=False,
            reply_markup=reply_markup,
        )
    elif character.is_dead:
        query_text = 'Seu personagem não pode entrar em batalha com 0 de HP.'
        await answer(query=query, text=query_text, show_alert=True)
    elif other_battle:
        group_model = GroupModel()
        chat_id = other_battle.chat_id
        group = group_model.get(chat_id)
        query_text = (
            f'Seu personagem já em uma batalha no grupo "{group.name}"!'
        )
        await answer(query=query, text=query_text, show_alert=True)


# SELECT_ACTION_ROUTES
async def select_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('select_action')
    battle_model = BattleModel()
    character_model = CharacterModel()
    query = update.callback_query
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    message_id = update.effective_message.message_id
    battle_id = context.chat_data['battle_id']
    battle = battle_model.get(battle_id)
    character = character_model.get(user_id)

    if character == battle.current_player:
        action = query.data
        context.chat_data['action'] = action
        user_name = update.effective_user.name
        inline_keyboard = []
        for i, char in enumerate(battle.turn_order):
            inline_keyboard.append(
                [InlineKeyboardButton(
                    f'{battle.get_char_emojis(char)} {char.name}',
                    callback_data=i
                )]
            )
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        query_text = f'Você selecionou: "{ACTIONS[action]}"'
        await answer(query=query, text=query_text)
        new_text = (
            f'{user_name}, selecione o alvo para "{ACTIONS[action]}".\n\n'
            f'{battle.get_sheet()}\n'
        )
        await edit_message_text(
            function_caller='BATTLE.SELECT_ACTION()',
            new_text=new_text,
            context=context,
            chat_id=chat_id,
            message_id=message_id,
            need_response=False,
            markdown=False,
            reply_markup=reply_markup,
        )

        return SELECT_TARGET_ROUTES
    else:
        query_text = 'Ainda não é o seu turno!!'
        await answer(query=query, text=query_text, show_alert=True)
        return SELECT_ACTION_ROUTES


# SELECT_TARGET_ROUTES
async def select_defender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('select_defender')
    battle_model = BattleModel()
    character_model = CharacterModel()
    query = update.callback_query
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    message_id = update.effective_message.message_id
    battle_id = context.chat_data['battle_id']
    battle = battle_model.get(battle_id)
    character = character_model.get(user_id)

    if character == battle.current_player:
        defender_index = int(query.data)
        context.chat_data['defender_index'] = defender_index
        defender = battle.turn_order[defender_index]
        defender_user_name = defender.player_name
        action = context.chat_data['action']

        reply_markup = get_reaction_inline_keyboard()
        query_text = f'Você selecionou: "{defender.name}"'
        await answer(query=query, text=query_text)
        new_text = (
            f'{defender.name} ({defender_user_name}), '
            f'seu personagem foi alvo de "{ACTIONS[action]}".\n'
            f'Selecione sua reação.\n\n'
            f'{battle.get_sheet()}\n'
        )
        await edit_message_text(
            function_caller='BATTLE.SELECT_DEFENDER()',
            new_text=new_text,
            context=context,
            chat_id=chat_id,
            message_id=message_id,
            need_response=False,
            markdown=False,
            reply_markup=reply_markup,
        )

        return SELECT_REACTION_ROUTES
    else:
        query_text = 'Ainda não é o seu turno!!'
        await answer(query=query, text=query_text, show_alert=True)
        return SELECT_TARGET_ROUTES


# SELECT_REACTION_ROUTES
async def select_reaction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('select_reaction')
    battle_model = BattleModel()
    character_model = CharacterModel()
    query = update.callback_query
    user_id = update.effective_user.id
    message_id = update.effective_message.message_id
    battle_id = context.chat_data['battle_id']
    battle = battle_model.get(battle_id)
    character = character_model.get(user_id)
    defender_index = context.chat_data['defender_index']

    if character == battle.turn_order[defender_index]:
        text = ''
        attacker_char = battle.current_player
        defender_char = character
        action = context.chat_data['action']
        acao = ACTIONS[action]
        reaction = query.data
        attacker_dice = Dice(character=attacker_char, faces=20)
        defender_dice = Dice(character=defender_char, faces=20)
        report = battle.action(
            attacker_char=attacker_char,
            defender=defender_char,
            action=action,
            reaction=reaction,
            attacker_dice=attacker_dice,
            defender_dice=defender_dice,
        )
        battle_model.save(battle)
        character_model.save(report['attacker'])
        character_model.save(report['defender'])

        attacker_dice_text = report['attack']['dice_text']
        hit = report['attack']['hit']
        total_hit = report['attack']['total_hit']
        accuracy = report['attack']['accuracy']
        atk = report['attack']['atk']
        total_atk = report['attack']['total_atk']
        atk_type = ATTACK_TYPE[report['attack']['action']]

        defender_dice_text = report['defense']['dice_text']
        evasion = report['defense']['evasion']
        total_evasion = report['defense']['total_evasion']
        dodge_score = report['defense']['dodge_score']
        _def = report['defense']['def']
        total_def = report['defense']['total_def']
        damage = report['defense']['damage']
        def_type = DEFENSE_TYPE[report['attack']['action']]

        if report['defense']['is_miss']:
            text += f'{defender_char.name} esquivou do "{acao}"!\n\n'
            text += (
                f'{attacker_char.name} {total_hit} '
                f'({hit}){EmojiEnum.HIT.value} '
                f'pontos de ACERTO.\n'
                f'Chance de ACERTO: {accuracy:.2f}%.\n'
            )
            text += (
                f'{defender_char.name} {total_evasion} '
                f'({evasion}){EmojiEnum.EVASION.value} '
                f'pontos de EVASÃO.\n'
                f'Valor da EVASÃO: {dodge_score:.2f}%.\n'
            )
        elif damage >= 0:
            if report['defense']['reaction'] == 'dodge':
                half_def = _def // 2
                text += (
                    f'{defender_char.name} falhou em esquivar '
                    f'e como penalidade bloqueou somente com '
                    f'50% ({half_def}){def_type} de defesa.\n\n'
                    f'Chance de ACERTO: {accuracy:.2f}% [{total_hit}]'
                    f'{EmojiEnum.HIT.value}.\n'
                    f'Valor da EVASÃO: '
                    f'{dodge_score:.2f}% [{total_evasion}]'
                    f'{EmojiEnum.EVASION.value}.'
                    f'\n\n'
                )
            text += (
                f'{attacker_char.name} causou '
                f'{damage}{atk_type} de dano '
                f'em {defender_char.name} com o "{acao}".\n\n'
            )
            text += (
                f'{attacker_char.name} atacou com {total_atk} '
                f'({atk}){atk_type} pontos.\n'
            )
            if report['defense']['reaction'] != 'dodge':
                text += (
                    f'{defender_char.name} defendeu com {total_def} '
                    f'({_def}){def_type} pontos.\n'
                )
        elif damage < 0:
            text += (
                f'{attacker_char.name} curou '
                f'{-damage}{EmojiEnum.HEALING.value} pontos de vida '
                f'de {defender_char.name}.\n'
            )

        text += (
            f'\n{attacker_char.name}[{attacker_dice_text}].\n'
        )
        text += f'{defender_char.name}[{defender_dice_text}].\n'

        reply_markup = get_action_inline_keyboard()
        callback = SELECT_ACTION_ROUTES

        winner = battle.get_winner()
        if winner:
            if winner in TEAMS.keys():
                text += (
                    f'\nA batalha terminou!\n'
                    f'O vencedor foi o Time {TEAMS[winner]}!!!\n\n'
                ).upper()
            elif winner == 'draw':
                text += '\nA BATALHA TERMINOU EMPATADA!\n\n'
            group_model = GroupModel()
            chat_id = update.effective_chat.id
            group = group_model.get(chat_id)
            multiplier_xp = group.multiplier_xp
            report_xp = battle.share_xp(multiplier_xp)
            reply_markup = None
            battle_model.delete(battle_id)
            callback = ConversationHandler.END
            blue = TEAMS[CALLBACK_ENTER_BLUE_TEAM]
            red = TEAMS[CALLBACK_ENTER_RED_TEAM]
            text += (
                f'O Time {blue} recebeu {report_xp["blue"]} pontos de XP e o '
                f'Time {red} recebeu {report_xp["red"]} pontos de XP.\n'
            )
            for char in battle.turn_order:
                if isinstance(char, PlayerCharacter):
                    character_model.save(char)

        new_text = (
            f'{text}\n'
            f'{battle.get_sheet()}\n'
        )
        await edit_message_text(
            function_caller='BATTLE.SELECT_REACTION()',
            new_text=new_text,
            context=context,
            chat_id=chat_id,
            message_id=message_id,
            need_response=False,
            markdown=False,
            reply_markup=reply_markup,
        )

        return callback
    else:
        query_text = 'Seu personagem não é alvo do ataque!'
        await answer(query=query, text=query_text, show_alert=True)
        return SELECT_REACTION_ROUTES


async def battle_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    battle_model = BattleModel()
    response = context.chat_data['battle_response']
    battle_id = context.chat_data['battle_id']
    battle_model.delete(battle_id)
    await response.delete()
    del context.chat_data['battle_response']
    del context.chat_data['battle_id']

    return ConversationHandler.END


def check_if_change_for_same_team(
    team_name: str,
    character: BaseCharacter,
    battle: Battle,
) -> bool:
    return any((
        (
            CALLBACK_ENTER_BLUE_TEAM == team_name and
            battle.in_blue_team(character)
        ),
        (
            CALLBACK_ENTER_RED_TEAM == team_name and
            battle.in_red_team(character)
        )
    ))


def get_enter_battle_inline_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                f'{EmojiEnum.TEAM_BLUE.value}ENTRAR NO TIME AZUL',
                callback_data=CALLBACK_ENTER_BLUE_TEAM
            )
        ],
        [
            InlineKeyboardButton(
                f'{EmojiEnum.TEAM_RED.value}ENTRAR NO TIME VERMELHO',
                callback_data=CALLBACK_ENTER_RED_TEAM
            )
        ],
        [
            InlineKeyboardButton(
                "COMEÇAR BATALHA",
                callback_data=CALLBACK_START_BATTLE
            )
        ]
    ])


def get_action_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                ACTIONS_LABELS[CALLBACK_PHYSICAL_ATTACK],
                callback_data=CALLBACK_PHYSICAL_ATTACK
            )
        ],
        [
            InlineKeyboardButton(
                ACTIONS_LABELS[CALLBACK_PRECISION_ATTACK],
                callback_data=CALLBACK_PRECISION_ATTACK
            )
        ],
        [
            InlineKeyboardButton(
                ACTIONS_LABELS[CALLBACK_MAGICAL_ATTACK],
                callback_data=CALLBACK_MAGICAL_ATTACK
            )
        ]
    ])


def get_reaction_inline_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                REACTIONS_LABELS[CALLBACK_DEFEND],
                callback_data=CALLBACK_DEFEND
            )
        ],
        [
            InlineKeyboardButton(
                REACTIONS_LABELS[CALLBACK_DODGE],
                callback_data=CALLBACK_DODGE
            )
        ],
    ])


BATTLE_HANDLER = ConversationHandler(
    entry_points=[
        PrefixHandler(
            PREFIX_COMMANDS,
            COMMANDS,
            battle_start,
            BASIC_COMMAND_IN_GROUP_FILTER
        ),
        CommandHandler(COMMANDS, battle_start, BASIC_COMMAND_IN_GROUP_FILTER),
    ],
    states={
        ENTER_BATTLE_ROUTES: [
            CallbackQueryHandler(
                enter_battle, pattern=(
                    f'^{CALLBACK_ENTER_BLUE_TEAM}|'
                    f'{CALLBACK_ENTER_RED_TEAM}|'
                    f'{CALLBACK_START_BATTLE}$'
                )
            ),
        ],
        SELECT_ACTION_ROUTES: [
            CallbackQueryHandler(
                select_action, pattern=(
                    f'^{CALLBACK_PHYSICAL_ATTACK}|'
                    f'{CALLBACK_PRECISION_ATTACK}|'
                    f'{CALLBACK_MAGICAL_ATTACK}$'
                )
            )
        ],
        SELECT_TARGET_ROUTES: [
            CallbackQueryHandler(
                select_defender, pattern=(
                    f'^\d\d?$'
                )
            )
        ],
        SELECT_REACTION_ROUTES: [
            CallbackQueryHandler(
                select_reaction, pattern=(
                    f'^{CALLBACK_DODGE}|{CALLBACK_DEFEND}$'
                )
            )
        ]
    },
    fallbacks=[
        CommandHandler(
            CANCEL_COMMANDS, battle_cancel)
    ],
    per_user=False,
    conversation_timeout=ONE_HOUR_IN_SECONDS
)
