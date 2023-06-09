from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ChatAction
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    PrefixHandler
)

from bot.conversation.constants import (
    BASIC_COMMAND_IN_GROUP_FILTER,
    PREFIX_COMMANDS
)
from bot.decorators import need_have_char
from bot.decorators import print_basic_infos
from repository.mongo import BattleModel, CharacterModel
from rpgram import Battle

# ROUTES
(
    ENTER_BATTLE_ROUTES,
    SELECT_ACTION_ROUTES,
    SELECT_TARGET_ROUTES,
    SELECT_REACTION_ROUTES,
    END_ROUTES,
) = range(5)


# CALLBACK DATA
# ENTER IN BATTLE
CALLBACK_ENTER_BLUE_TEAM = 'blue'
CALLBACK_ENTER_RED_TEAM = 'red'
CALLBACK_START_BATTLE = 'start_battle'

# ACTIONS
CALLBACK_PHYSICAL_ATTACK = 'physical_attack'
CALLBACK_PRECISION_ATTACK = 'precision_attack'
CALLBACK_MAGICAL_ATTACK = 'magical_attack'

ACTIONS = {
    CALLBACK_PHYSICAL_ATTACK: 'Ataque Físico',
    CALLBACK_PRECISION_ATTACK: 'Ataque de Precisão',
    CALLBACK_MAGICAL_ATTACK: 'Ataque Mágico',
}

# REACTIONS
CALLBACK_DODGE = 'dodge'
CALLBACK_DEFEND = 'defend'

REACTIONS = {
    CALLBACK_DODGE: 'Esquivar',
    CALLBACK_DEFEND: 'Defender'
}

COMMANDS = ['duel', 'duelo']


@need_have_char
@print_basic_infos
async def battle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('battle_start')
    await update.effective_message.reply_chat_action(ChatAction.TYPING)
    battle_model = BattleModel()
    character_model = CharacterModel()
    user_id = update.effective_user.id
    character_id = character_model.get(user_id, fields={'_id': 1})
    battle = battle_model.get(
        query={'$or': [
            {'blue_team': character_id['_id']},
            {'red_team': character_id['_id']}
        ]}
    )

    if not battle:
        character = character_model.get(user_id)
        battle = Battle(blue_team=[character], red_team=[])
        battle_result = battle_model.save(battle)
        battle_id = battle_result.inserted_id
        inline_keyboard = [[
            InlineKeyboardButton(
                "ENTRAR", callback_data=CALLBACK_ENTER_RED_TEAM
            )
        ]]
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        response = await update.effective_message.reply_text(
            battle.get_teams_sheet(),
            reply_markup=reply_markup,
        )
        context.chat_data['battle_response'] = response
        context.chat_data['battle_id'] = battle_id
        return ENTER_BATTLE_ROUTES

    await update.message.reply_text("Você já está em uma batalha.")
    return ConversationHandler.END


# ENTER_BATTLE_ROUTES
async def enter_battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('enter_battle')
    await update.effective_message.reply_chat_action(ChatAction.TYPING)
    battle_model = BattleModel()
    character_model = CharacterModel()
    query = update.callback_query
    user_id = update.effective_user.id
    battle_id = context.chat_data['battle_id']
    character = character_model.get(user_id)
    battle = battle_model.get(battle_id)

    if query.data == CALLBACK_START_BATTLE:
        user_name = battle.current_player.player_name
        inline_keyboard = [
            [
                InlineKeyboardButton(
                    "ATAQUE FÍSICO", callback_data=CALLBACK_PHYSICAL_ATTACK
                )
            ],
            [
                InlineKeyboardButton(
                    "ATAQUE DE PRECISÃO",
                    callback_data=CALLBACK_PRECISION_ATTACK
                )
            ],
            [
                InlineKeyboardButton(
                    "ATAQUE MÁGICO", callback_data=CALLBACK_MAGICAL_ATTACK
                )
            ]
        ]
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        await query.answer('A BATALHA COMEÇOU!!!')
        await query.edit_message_text(
            f'A batalha começou!\n'
            f'{user_name}, escolha sua ação.\n\n'
            f'{battle.get_sheet()}\n',
            reply_markup=reply_markup
        )
        return SELECT_ACTION_ROUTES

    if character not in battle.turn_order:
        team = query.data
        battle.enter_battle(character, team)
        battle_model.save(battle)
        inline_keyboard = [
            [
                InlineKeyboardButton(
                    "ENTRAR NO TIME AZUL",
                    callback_data=CALLBACK_ENTER_BLUE_TEAM
                )
            ],
            [
                InlineKeyboardButton(
                    "ENTRAR NO TIME VERMELHO",
                    callback_data=CALLBACK_ENTER_RED_TEAM
                )
            ],
            [
                InlineKeyboardButton(
                    "COMEÇAR BATALHA",
                    callback_data=CALLBACK_START_BATTLE
                )
            ]
        ]
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        await query.answer('Você entrou na batalha!')
        await query.edit_message_text(
            battle.get_teams_sheet(),
            reply_markup=reply_markup,
        )
        return ENTER_BATTLE_ROUTES
    else:
        await query.answer('Você já está na batalha!', show_alert=True)


# SELECT_ACTION_ROUTES
async def select_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('select_action')
    await update.effective_message.reply_chat_action(ChatAction.TYPING)
    battle_model = BattleModel()
    character_model = CharacterModel()
    query = update.callback_query
    user_id = update.effective_user.id
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
                [InlineKeyboardButton(char.name, callback_data=i)]
            )
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        await query.answer(f'Você selecionou: "{ACTIONS[action]}"')
        await query.edit_message_text(
            f'{user_name}, selecione o alvo para "{ACTIONS[action]}".\n\n'
            f'{battle.get_sheet()}\n',
            reply_markup=reply_markup
        )
        return SELECT_TARGET_ROUTES
    else:
        await query.answer('Ainda não é o seu turno!!', show_alert=True)
        return SELECT_ACTION_ROUTES


# SELECT_TARGET_ROUTES
async def select_target(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('select_target')
    await update.effective_message.reply_chat_action(ChatAction.TYPING)
    battle_model = BattleModel()
    character_model = CharacterModel()
    query = update.callback_query
    user_id = update.effective_user.id
    battle_id = context.chat_data['battle_id']
    battle = battle_model.get(battle_id)
    character = character_model.get(user_id)

    if character == battle.current_player:
        target_index = int(query.data)
        context.chat_data['target_index'] = target_index
        target = battle.turn_order[target_index]
        target_user_name = target.player_name
        action = context.chat_data['action']
        inline_keyboard = [
            [
                InlineKeyboardButton("DEFENDER", callback_data=CALLBACK_DEFEND)
            ],
            [
                InlineKeyboardButton("ESQUIVAR", callback_data=CALLBACK_DODGE)
            ],
        ]
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        await query.answer(f'Você selecionou: "{target.name}"')
        await query.edit_message_text(
            f'{target.name} ({target_user_name}), '
            f'você foi alvo de "{ACTIONS[action]}".\n'
            f'Selecione sua reação.\n\n'
            f'{battle.get_teams_sheet()}',
            reply_markup=reply_markup,
        )
        return SELECT_REACTION_ROUTES
    else:
        await query.answer('Ainda não é o seu turno!!', show_alert=True)
        return SELECT_TARGET_ROUTES


# SELECT_REACTION_ROUTES


async def battle_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    battle_model = BattleModel()
    response = context.chat_data['battle_response']
    battle_id = context.chat_data['battle_id']
    battle_model.delete(battle_id)
    await response.delete()

    return ConversationHandler.END

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
                select_target, pattern=(
                    f'^\d\d?$'
                )
            )],
        SELECT_REACTION_ROUTES: []
    },
    fallbacks=[CommandHandler("battle_cancel", battle_cancel)],
    per_user=False
)
