from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
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
    START_BATTLE_ROUTES,
    END_ROUTES
) = range(3)

# CALLBACK DATA

CALLBACK_ENTER_BLUE = 'enter_blue'
CALLBACK_ENTER_RED = 'enter_red'
CALLBACK_START_BATTLE = 'start_battle'


COMMANDS = ['duel', 'duelo']


@need_have_char
@print_basic_infos
async def battle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
                "ENTRAR", callback_data=CALLBACK_ENTER_RED
            )
        ]]
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        response = await update.effective_message.reply_text(
            battle.get_teams_sheet(),
            reply_markup=reply_markup,
        )
        context.chat_data['battle_response'] = response
        context.chat_data['battle_id'] = battle_id
        print('battle_id', battle_id)
        return ENTER_BATTLE_ROUTES

    await update.message.reply_text("Você já está em uma batalha.")
    return ConversationHandler.END


async def entering_battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    print(query.data)
    battle_model = BattleModel()
    character_model = CharacterModel()
    user_id = update.effective_user.id
    battle_id = context.chat_data['battle_id']
    character = character_model.get(user_id)
    battle = battle_model.get(battle_id)
    print('battle_id', battle_id)
    print('battle', battle)

    if query.data == CALLBACK_START_BATTLE:
        await query.edit_message_text(
            f'A batalha começou!\n'
            f'{battle.get_sheet()}\n'
        )
        return START_BATTLE_ROUTES
    if character not in battle.turn_order:
        team = ''
        if query.data == CALLBACK_ENTER_BLUE:
            team = 'blue'
        elif query.data == CALLBACK_ENTER_RED:
            team = 'red'
        battle.enter_battle(character, team)
        battle_model.save(battle)
        inline_keyboard = [
            [
                InlineKeyboardButton(
                    "ENTRAR NO TIME AZUL", callback_data=CALLBACK_ENTER_BLUE
                )
            ],
            [
                InlineKeyboardButton(
                    "ENTRAR NO TIME VERMELHO", callback_data=CALLBACK_ENTER_RED
                )
            ],
            [
                InlineKeyboardButton(
                    "COMEÇAR BATALHA", callback_data=CALLBACK_START_BATTLE
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
        await query.answer('Você já está em uma batalha!')


async def battle_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

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
                entering_battle, pattern=(
                    f'^{CALLBACK_ENTER_BLUE}|'
                    f'{CALLBACK_ENTER_RED}|'
                    f'{CALLBACK_START_BATTLE}$'
                )
            ),
        ]
    },
    fallbacks=[CommandHandler("battle_cancel", battle_cancel)],
    per_user=False
)
