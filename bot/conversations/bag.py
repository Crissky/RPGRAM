from itertools import zip_longest

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
from constant.text import TITLE_HEAD
from repository.mongo import BagModel
from rpgram import Bag
from rpgram.boosters import Equipment
from rpgram import Consumable


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
    user_name = update.effective_user.name
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

    markdown_text = f'\n*Bolsa de {user_name}* \(*Página* {page + 1}\)\n\n'

    items = player_bag[:]
    have_back_page = False
    have_next_page = False
    if page > 0:
        have_back_page = True
    if len(items) > ITEMS_PER_PAGE:
        items = player_bag[:-1]
        have_next_page = True
    elif len(items) == 0 and not query:
        await update.effective_message.reply_text(
            text='Você não tem itens na sua bolsa.',
            disable_notification=silent,
        )
        return ConversationHandler.END

    items_buttons = []
    for index, item in enumerate(items):
        markdown_text += f'*Ⅰ{(index + 1)}:* '
        markdown_text += item.get_sheet(verbose=True, markdown=True)
        markdown_text += '\n'
        items_buttons.append(InlineKeyboardButton(
            text=f'Item {index + 1}',
            callback_data=f'item={index},page={page}'
        ))

    reshaped_items_buttons = []
    for item1, item2 in zip_longest(items_buttons[0::2], items_buttons[1::2]):
        new_line = [item1, item2]
        if None in new_line:
            new_line.remove(None)
        reshaped_items_buttons.append(new_line)

    navigation_keyboard = []
    if have_back_page:
        navigation_keyboard.append(
            InlineKeyboardButton(
                text='⬅ Anterior',
                callback_data=str(page - 1)
            )
        )
    if have_next_page:
        navigation_keyboard.append(
            InlineKeyboardButton(
                text='Próxima ➡',
                callback_data=str(page + 1)
            )
        )

    cancel_button = [InlineKeyboardButton(
        text='🎒Fechar Bolsa',
        callback_data=CALLBACK_CLOSE_BAG
    )]
    reply_markup = InlineKeyboardMarkup(
        reshaped_items_buttons + [navigation_keyboard] + [cancel_button]
    )

    markdown_text = TITLE_HEAD.format(markdown_text)
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


async def check_item(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bag_model = BagModel()
    user_id = update.effective_user.id
    query = update.callback_query
    data = query.data.split(',')
    item = int(data[0].split('=')[1])
    page = int(data[1].split('=')[1])
    item_index = (ITEMS_PER_PAGE * page) + item
    player_bag = bag_model.get(
        query={'player_id': user_id},
        fields={'items_ids': {'$slice': [item_index, 1]}},
        partial=False
    )
    print(data)
    print(player_bag)
    item = player_bag[0]
    markdown_text = item.get_all_sheets(verbose=True, markdown=True)
    print(type(item))
    if isinstance(item.item, Equipment):
        use_text = 'Equipar (TO DO)'
    elif isinstance(item.item, Consumable):
        use_text = 'Usar (TO DO)'

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(text=use_text, callback_data='TO DO')],
        [InlineKeyboardButton(text='Voltar', callback_data=str(page))]
    ])
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
            CallbackQueryHandler(check_item, pattern=f'^item='),
            CallbackQueryHandler(cancel, pattern=f'^{CALLBACK_CLOSE_BAG}$'),
        ]
    },
    fallbacks=[
        CommandHandler(CANCEL_COMMANDS, cancel)
    ],
    per_user=True,
)
