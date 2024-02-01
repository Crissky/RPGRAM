from typing import List
from telegram import Update
from telegram.constants import ParseMode, ChatAction
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    PrefixHandler
)
from bot.constants.bag import ITEMS_PER_PAGE
from bot.constants.filters import BASIC_COMMAND_FILTER, PREFIX_COMMANDS

from bot.constants.seller import (
    ACCESS_DENIED,
    CANCEL_COMMANDS,
    COMMANDS,
    SELLER_NAME,
    TOTAL_CONSUMABLES,
    TOTAL_EQUIPMENTS,
    TOTAL_MEAN_LEVELS
)
from bot.conversations.bag import cancel
from bot.decorators.battle import need_not_in_battle
from bot.decorators.char import (
    confusion,
    skip_if_dead_char,
    skip_if_immobilized,
    skip_if_no_have_char
)
from bot.decorators.job import skip_if_spawn_timeout
from bot.decorators.player import skip_if_no_singup_player
from bot.decorators.print import print_basic_infos
from bot.decorators.retry import retry_after
from bot.functions.char import get_chars_level_from_group
from bot.functions.chat import send_alert_or_message
from bot.functions.general import get_attribute_group_or_player
from bot.functions.player import get_player_trocado
from constant.text import TITLE_HEAD
from constant.time import TEN_MINUTES_IN_SECONDS
from function.lista import mean_level

from function.text import escape_basic_markdown_v2

from repository.mongo import BagModel, ItemModel
from repository.mongo.populate.item import (
    create_random_consumable,
    create_random_equipment
)

from rpgram import Bag, Item
from rpgram.consumables import GemstoneConsumable, TrocadoPouchConsumable
from rpgram.enums import EmojiEnum


# ROUTES
(
    START_ROUTES,
    CHECK_ROUTES,
    USE_ROUTES,
    SORT_ROUTES,
) = range(4)


@skip_if_dead_char
@skip_if_immobilized
@confusion(START_ROUTES)
@skip_if_no_singup_player
@skip_if_no_have_char
@need_not_in_battle
@print_basic_infos
@retry_after
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Inicia o bot do vendedor.
    '''

    await update.effective_message.reply_chat_action(ChatAction.TYPING)
    bag_model = BagModel()
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_name = update.effective_user.name
    query = update.callback_query
    args = context.args
    silent = get_attribute_group_or_player(chat_id, 'silent')
    trocado = get_player_trocado(user_id)

    page = 0
    if query:
        data = eval(query.data)
        page = data['page']  # starts zero
        data_user_id = data['user_id']
        retry_state = data.get('retry_state')

        # Não executa se outro usuário mexer na bolsa
        if data_user_id != user_id:
            await query.answer(text=ACCESS_DENIED, show_alert=True)
            return retry_state

    skip_slice = ITEMS_PER_PAGE * page
    size_slice = ITEMS_PER_PAGE + 1

    seller_bag = bag_model.get(
        query={'player_id': chat_id},
        fields={'items_ids': {'$slice': [skip_slice, size_slice]}},
        partial=False
    )
    if not seller_bag:  # Cria uma bolsa caso o jogador não tenha uma.
        text = (
            f'Desculpe, {user_name}, mas eu não tenho itens para vender no '
            f'momento. Volte mais tarde.'
        )
        await send_alert_or_message(
            function_caller='START_SELLER()',
            context=context,
            query=query,
            text=text,
            chat_id=chat_id,
            user_id=user_id,
            show_alert=True
        )
        return

    markdown_text = (
        f'\n*Loja de {SELLER_NAME}* — {EmojiEnum.PAGE.value}: {page + 1:02}\n'
        f'*Peso*: {seller_bag.weight_text}\n'
        f'*{user_name}*: {trocado}{EmojiEnum.TROCADO.value}\n\n'
    )

    items = seller_bag[:]
    have_back_page = False
    have_next_page = False
    if page > 0:
        have_back_page = True
    if len(items) > ITEMS_PER_PAGE:
        items = seller_bag[:-1]
        have_next_page = True
    elif all((len(items) == 0, not query)):
        text = (
            f'Desculpe, {user_name}, mas eu não tenho itens para vender no '
            f'momento. Volte mais tarde.'
        )
        await update.effective_message.reply_text(
            text=text,
            disable_notification=silent,
            allow_sending_without_reply=True
        )
        return ConversationHandler.END

    markdown_text += get_item_texts(items=items)
    markdown_text = TITLE_HEAD.format(markdown_text)
    markdown_text = escape_basic_markdown_v2(markdown_text)
    if not query:  # Envia Resposta com o texto da tabela de itens e botões
        await update.effective_message.reply_text(
            text=markdown_text,
            disable_notification=silent,
            # reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN_V2,
            allow_sending_without_reply=True
        )
    else:  # Edita Resposta com o texto da tabela de itens e botões
        await query.edit_message_text(
            text=markdown_text,
            # reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN_V2
        )

    return CHECK_ROUTES


@skip_if_spawn_timeout
async def job_create_new_items(context: ContextTypes.DEFAULT_TYPE):
    '''Cria novos itens para a bag do vendedor.
    '''

    print('JOB_CREATE_NEW_ITEMS()')
    bag_model = BagModel()
    item_model = ItemModel()
    job = context.job
    chat_id = job.chat_id
    group_level = get_attribute_group_or_player(chat_id, 'group_level')
    silent = get_attribute_group_or_player(chat_id, 'silent')
    chars_level_list = get_chars_level_from_group(chat_id)
    mean_level_list = mean_level(chars_level_list, TOTAL_MEAN_LEVELS)

    seller_bag = Bag(
        items=[],
        player_id=chat_id,
    )

    for char_level in mean_level_list:
        for _ in range(TOTAL_EQUIPMENTS):
            equipment_item = create_random_equipment(
                equip_type=None,
                group_level=char_level,
            )
            equipment = equipment_item.item
            item_model.save(equipment)
            seller_bag.add(equipment_item)

    for _ in range(TOTAL_CONSUMABLES):
        consumable_item = create_random_consumable(
            group_level=group_level,
            ignore_list=[TrocadoPouchConsumable, GemstoneConsumable]
        )
        new_quantity = consumable_item.quantity * 2
        consumable_item.add(new_quantity)
        seller_bag.add(consumable_item)

    seller_bag.sort_by_equip_type()
    bag_model.save(seller_bag)

    await context.bot.send_message(
        chat_id=chat_id,
        text=escape_basic_markdown_v2(f'{SELLER_NAME}\n{seller_bag}'),
        disable_notification=silent,
        parse_mode=ParseMode.MARKDOWN_V2,
    )


def get_item_texts(items: List[Item]) -> str:
    markdown_text = ''
    zero_fill = 2
    if items:
        zero_fill = max(len(str(item.quantity)) for item in items)
    for index, item in enumerate(items):
        markdown_text += f'*Ⅰ{(index + 1):02}:* '
        markdown_text += item.get_sheet(
            verbose=True,
            markdown=True,
            zero_fill=zero_fill
        )
        markdown_text += f'*Preço*: {item.price_text}\n\n'

    return markdown_text.strip() + '\n'


SELLER_HANDLER = ConversationHandler(
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

    },
    fallbacks=[
        CommandHandler(CANCEL_COMMANDS, cancel)
    ],
    allow_reentry=True,
    conversation_timeout=TEN_MINUTES_IN_SECONDS,
)
