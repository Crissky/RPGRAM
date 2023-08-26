from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    ContextTypes,
    PrefixHandler,
)
from bot.constants.bag import (
    CALLBACK_CLOSE_BAG,
    CANCEL_COMMANDS,
    COMMANDS,
    ITEMS_PER_PAGE
)

from bot.constants.filters import (
    BASIC_COMMAND_FILTER,
    PREFIX_COMMANDS
)
from bot.decorators import (
    need_not_in_battle,
    print_basic_infos,
    skip_if_no_have_char,
    skip_if_no_singup_player,
)
from bot.functions.general import get_attribute_group_or_player
from repository.mongo import BagModel
from rpgram import Bag


# ROUTES
ITEM_ROUTES = 1


@skip_if_no_singup_player
@skip_if_no_have_char
@need_not_in_battle
@print_basic_infos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bag_model = BagModel()
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    query = update.callback_query
    silent = get_attribute_group_or_player(chat_id, 'silent')

    if query:
        page = int(query.data)  # starts zero
        skip_slice = ITEMS_PER_PAGE * page
        size_slice = ITEMS_PER_PAGE + 1
    else:
        page = 0
        skip_slice = 0
        size_slice = ITEMS_PER_PAGE + 1

    player_bag = bag_model.get(
        query={'player_id': user_id},
        fields={'items_ids': {'$slice': [skip_slice, size_slice]}},
        partial=False
    )

    if not player_bag:
        player_bag = Bag(
            items=[],
            player_id=user_id
        )
        bag_model.save(player_bag)

    markdown_text = f'Página {page + 1}\n\n'
    items = player_bag[:]
    have_back_page = False
    have_next_page = False
    if page > 0:
        have_back_page = True
    if len(items) > ITEMS_PER_PAGE:
        items = player_bag[:-1]
        have_next_page = True

    for item in items:
        markdown_text += item.get_sheet(verbose=True, markdown=True)
        markdown_text += '\n'

    inline_keyboard = []
    cancel_button = [InlineKeyboardButton(
        text='Fechar Bolsa',
        callback_data=CALLBACK_CLOSE_BAG
    )]
    reply_markup = InlineKeyboardMarkup([cancel_button])
    if have_back_page:
        inline_keyboard.append(
            InlineKeyboardButton(
                text='Anterior',
                callback_data=str(page - 1)
            )
        )
    if have_next_page:
        inline_keyboard.append(
            InlineKeyboardButton(
                text='Próxima',
                callback_data=str(page + 1)
            )
        )
    if inline_keyboard:
        reply_markup = InlineKeyboardMarkup([inline_keyboard, cancel_button])

    if not query:
        await update.effective_message.reply_text(
            text=markdown_text,
            disable_notification=silent,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    else:
        await query.edit_message_text(
            text=markdown_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN_V2
        )

    return ITEM_ROUTES


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query:
        await query.answer('Fechando Bolsa...')
        await query.delete_message()

    return ConversationHandler.END


BAG_HANDLER = ConversationHandler(
    entry_points=[
        PrefixHandler(
            PREFIX_COMMANDS,
            COMMANDS,
            start,
            BASIC_COMMAND_FILTER
        ),
        CommandHandler(COMMANDS, start, BASIC_COMMAND_FILTER)
    ],
    states={
        ITEM_ROUTES: [
            CallbackQueryHandler(start, pattern=f'^\d\d?\d?$'),
            CallbackQueryHandler(cancel, pattern=f'^{CALLBACK_CLOSE_BAG}$'),
        ]
    },
    fallbacks=[
        CommandHandler(CANCEL_COMMANDS, cancel)
    ],
    per_user=True,
)
