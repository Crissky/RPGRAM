import re

from random import choice, randint

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
)
from bot.constants.item import (
    REPLY_TEXTS_FIND_TREASURE_START,
    REPLY_TEXTS_FIND_TREASURE_MIDDLE,
    REPLY_TEXTS_FIND_TREASURE_END,
    REPLY_TEXTS_FIND_TREASURE_OPEN,
    REPLY_TEXTS_FIND_TREASURE_FINDING,
    REPLY_TEXTS_IGNORE_TREASURE,
)
from bot.decorators import (
    need_have_char,
    need_singup_group,
    print_basic_infos
)

from bot.functions.general import get_attribute_group_or_player
from telegram.ext import ConversationHandler

from repository.mongo import BagModel, ItemModel
from repository.mongo.populate.item import create_random_item
from rpgram import Bag, Consumable
from rpgram.boosters import Equipment


CALLBACK_TEXT_YES = '$get_item'
CALLBACK_TEXT_NO = '$drop_item'
ESCAPED_CALLBACK_TEXT_YES = re.escape(CALLBACK_TEXT_YES)
ESCAPED_CALLBACK_TEXT_NO = re.escape(CALLBACK_TEXT_NO)


async def job_create_find_treasure(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    chat_id = job.chat_id
    minutes_in_seconds = randint(1, 29) * 60
    context.job_queue.run_once(
        callback=job_find_treasure,
        when=minutes_in_seconds,
        name='JOB_CREATE_EVENTE_TREASURE',
        chat_id=chat_id,
    )


async def job_find_treasure(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    chat_id = job.chat_id
    silent = get_attribute_group_or_player(chat_id, 'silent')
    text = choice(REPLY_TEXTS_FIND_TREASURE_START)
    text += choice(REPLY_TEXTS_FIND_TREASURE_MIDDLE)
    text += choice(REPLY_TEXTS_FIND_TREASURE_END)
    inline_keyboard = [[
        InlineKeyboardButton(
            'Investigar', callback_data=CALLBACK_TEXT_YES),
        InlineKeyboardButton('Ignorar', callback_data=CALLBACK_TEXT_NO),
    ]]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)

    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        disable_notification=silent,
        reply_markup=reply_markup,
    )


@print_basic_infos
@need_singup_group
@need_have_char
async def inspect_treasure(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id
        user_name = update.effective_user.name
        group_level = get_attribute_group_or_player(chat_id, 'higher_level')
        bag_model = BagModel()
        items_model = ItemModel()
        player_bag = bag_model.get(query={'player_id': user_id})

        if not player_bag:
            player_bag = Bag(
                items=[],
                player_id=user_id,
            )

        item = create_random_item(group_level)
        if isinstance(item.item, Equipment):
            items_model.save(item.item)
            markdown_item_sheet = item.get_all_sheets(
                verbose=True, markdown=True
            )
        elif isinstance(item.item, Consumable):
            markdown_item_sheet = item.get_sheet(
                verbose=True, markdown=True
            )

        player_bag.add(item)
        bag_model.save(player_bag)
        print(markdown_item_sheet)
        await query.edit_message_text(
            text=(
                f'{choice(REPLY_TEXTS_FIND_TREASURE_OPEN)}\n\n'
                f'{choice(REPLY_TEXTS_FIND_TREASURE_FINDING).format(user_name=user_name)}\n'
                f'{markdown_item_sheet}'
            ),
            parse_mode=ParseMode.MARKDOWN_V2
        )
    return ConversationHandler.END


@print_basic_infos
@need_singup_group
@need_have_char
async def ignore_treasure(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        text = choice(REPLY_TEXTS_IGNORE_TREASURE)
        await query.edit_message_text(
            text=text
        )
    return ConversationHandler.END


TREASURE_HANDLERS = [
    CallbackQueryHandler(
        inspect_treasure,
        pattern=f'^{ESCAPED_CALLBACK_TEXT_YES}$',
    ),
    CallbackQueryHandler(
        ignore_treasure,
        pattern=f'^{ESCAPED_CALLBACK_TEXT_NO}$',
    ),
]