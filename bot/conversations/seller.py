from itertools import zip_longest
from random import choice
from typing import List
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode, ChatAction
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    PrefixHandler
)
from bot.constants.bag import (
    DROPUSE_QUANTITY_OPTION_LIST,
    ITEMS_PER_PAGE,
    NAV_BACK_BUTTON_TEXT,
    NAV_END_BUTTON_TEXT,
    NAV_NEXT_BUTTON_TEXT,
    NAV_PREVIOUS_BUTTON_TEXT,
    NAV_START_BUTTON_TEXT
)
from bot.constants.filters import BASIC_COMMAND_FILTER, PREFIX_COMMANDS

from bot.constants.seller import (
    ACCESS_DENIED,
    BUY_MANY_BUTTON_TEXT,
    CALLBACK_LEAVE_SHOP,
    CANCEL_COMMANDS,
    COMMANDS,
    LEAVE_SHOP_BUTTON_TEXT,
    NOT_ENOUGH_MONEY,
    PATTERN_BUY,
    PATTERN_LEAVE_SHOP,
    PATTERN_SELL_ITEM,
    PATTERN_SELL_PAGE,
    REPLY_TEXT_NEW_ITEMS_ARRIVED,
    REPLY_TEXT_NO_HAVE_ITEMS,
    SECTION_TEXT_SHOP,
    SELLER_NAME,
    TOTAL_CONSUMABLES,
    TOTAL_EQUIPMENTS,
    TOTAL_MEAN_LEVELS
)
from bot.decorators.battle import need_not_in_battle
from bot.decorators.char import (
    confusion,
    skip_if_dead_char,
    skip_if_immobilized,
    skip_if_no_have_char
)
from bot.decorators import (
    allow_only_in_group,
    need_singup_group,
    skip_if_spawn_timeout,
    skip_if_no_singup_player,
    print_basic_infos,
    retry_after,
)
from bot.functions.bag import get_item_from_bag_by_position
from bot.functions.char import get_chars_level_from_group
from bot.functions.chat import (
    answer,
    call_telegram_message_function,
    callback_data_to_dict,
    callback_data_to_string,
    delete_message,
    edit_message_text,
    message_edit_reply_markup
)
from bot.functions.config import get_attribute_group
from bot.functions.general import get_attribute_group_or_player
from bot.functions.keyboard import reshape_row_buttons
from bot.functions.player import get_player_trocado
from constant.text import (
    SECTION_HEAD_SHOP_END,
    SECTION_HEAD_SHOP_START,
    SHOP_TITLE_HEAD
)
from constant.time import TEN_MINUTES_IN_SECONDS
from function.lista import mean_level

from function.text import (
    create_text_in_box,
    escape_basic_markdown_v2,
    escape_for_citation_markdown_v2
)

from repository.mongo import (
    BagModel,
    CharacterModel,
    EquipsModel,
    ItemModel,
    PlayerModel
)
from repository.mongo.populate.item import (
    create_random_consumable,
    create_random_equipment
)

from rpgram import Bag, Item
from rpgram.boosters import Equipment
from rpgram.characters.char_base import BaseCharacter
from rpgram.consumables import GemstoneConsumable, TrocadoPouchConsumable
from rpgram.consumables.consumable import Consumable
from rpgram.enums import EmojiEnum


# ROUTES
(
    START_ROUTES,
    CHECK_ROUTES,
    BUY_ROUTES,
) = range(3)


@allow_only_in_group
@need_singup_group
@skip_if_no_singup_player
@need_not_in_battle
@skip_if_dead_char
@skip_if_immobilized
@confusion(START_ROUTES)
@print_basic_infos
@retry_after
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Inicia o bot do vendedor.
    '''

    await update.effective_message.reply_chat_action(ChatAction.TYPING)
    bag_model = BagModel()
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    message_id = update.effective_message.id
    user_name = update.effective_user.name
    query = update.callback_query
    silent = get_attribute_group_or_player(chat_id, 'silent')
    trocado = get_player_trocado(user_id)

    page = 0
    if query:
        data = callback_data_to_dict(query.data)
        page = data['sell_page']  # starts zero
        data_user_id = data['user_id']
        retry_state = data.get('retry_state')

        # Não executa se outro usuário mexer na bolsa
        if data_user_id != user_id:
            await answer(query=query, text=ACCESS_DENIED, show_alert=True)
            return retry_state

    skip_slice = ITEMS_PER_PAGE * page
    size_slice = ITEMS_PER_PAGE + 1

    seller_bag = bag_model.get(
        query={'player_id': chat_id},
        fields={'items_ids': {'$slice': [skip_slice, size_slice]}},
        partial=False
    )

    items = seller_bag[:] if seller_bag else []
    have_back_page = False
    have_next_page = False
    if page > 0:
        have_back_page = True
    if len(items) > ITEMS_PER_PAGE:
        items = seller_bag[:-1]
        have_next_page = True
    elif all((len(items) == 0, not query)):
        text = f'>{SELLER_NAME}: ' + choice(REPLY_TEXT_NO_HAVE_ITEMS)
        text = escape_for_citation_markdown_v2(text)
        await update.effective_message.reply_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN_V2,
            disable_notification=silent,
            allow_sending_without_reply=True
        )
        return ConversationHandler.END

    # Criando os Botões
    reshaped_items_buttons = get_seller_item_buttons(
        items=items,
        page=page,
        user_id=user_id,
    )
    navigation_keyboard = get_sell_navigation_buttons(
        have_back_page=have_back_page,
        have_next_page=have_next_page,
        page=page,
        user_id=user_id,
    )
    extremes_navigation_keyboard = get_sell_extremes_navigation_buttons(
        have_back_page=have_back_page,
        have_next_page=have_next_page,
        user_id=user_id,
        seller_id=chat_id,
    )
    cancel_button = get_leave_shop_button(user_id=user_id)

    reply_markup = InlineKeyboardMarkup(
        reshaped_items_buttons +
        [navigation_keyboard] +
        [extremes_navigation_keyboard] +
        [cancel_button]
    )

    markdown_text = (
        f'\n*Loja de {SELLER_NAME}* — {EmojiEnum.PAGE.value}: {page + 1:02}\n'
        f'*Peso*: {seller_bag.weight_text}\n'
        f'*{user_name}*: {trocado}{EmojiEnum.TROCADO.value}\n\n'
    )
    markdown_text += get_item_texts(items=items)
    markdown_text = SHOP_TITLE_HEAD.format(markdown_text)
    markdown_text = escape_basic_markdown_v2(markdown_text)
    if not query:  # Envia Resposta com o texto da tabela de itens e botões
        await update.effective_message.reply_text(
            text=markdown_text,
            disable_notification=silent,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN_V2,
            allow_sending_without_reply=True
        )
    else:  # Edita Resposta com o texto da tabela de itens e botões
        await edit_message_text(
            function_caller='SELLER.START()',
            new_text=markdown_text,
            context=context,
            chat_id=chat_id,
            message_id=message_id,
            need_response=False,
            markdown=True,
            reply_markup=reply_markup,
        )

    return CHECK_ROUTES


@retry_after
async def check_sell_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Edita a mensagem com as informações do item escolhido.
    '''

    message_id = update.effective_message.id
    message = update.effective_message
    query = update.callback_query
    try:
        old_reply_markup = query.message.reply_markup
        await message_edit_reply_markup(
            function_caller='SELLER.CHECK_SELL_ITEM()',
            message=message,
            context=context,
            need_response=True,
            reply_markup=None,
        )
    except Exception as e:
        print(type(e), e)
        return ConversationHandler.END

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_name = update.effective_user.name
    silent = get_attribute_group_or_player(chat_id, 'silent')
    trocado = get_player_trocado(user_id)
    data = callback_data_to_dict(query.data)
    item_pos = data['sell_item']
    page = data['sell_page']
    data_user_id = data['user_id']

    if data_user_id != user_id:  # Não executa se outro usuário mexer na bolsa
        await answer(query=query, text=ACCESS_DENIED, show_alert=True)
        await message_edit_reply_markup(
            function_caller='SELLER.CHECK_SELL_ITEM()',
            message=message,
            context=context,
            need_response=True,
            reply_markup=old_reply_markup,
        )

        return CHECK_ROUTES

    item = get_item_from_bag_by_position(chat_id, page, item_pos)
    price_text = get_discount_price_text(price=item.price, user_id=user_id)
    markdown_text = (
        f'*{user_name}*: {trocado}{EmojiEnum.TROCADO.value}\n'
        f'*Preço*: {price_text}\n\n'
    )
    if isinstance(item.item, Equipment):
        equips_model = EquipsModel()
        equips = equips_model.get(user_id)
        markdown_text += equips.compare(item.item, is_sell=True)
    elif isinstance(item.item, Consumable):
        markdown_text += item.get_all_sheets(
            verbose=True,
            markdown=True,
            show_quantity=True,
            is_sell=True
        )

    # Criando os Botões
    buy_buttons = get_buy_buttons(
        page=page,
        user_id=user_id,
        item_pos=item_pos,
        item=item,
        trocado=trocado,
    )
    back_button = get_sell_back_button(
        page=page,
        user_id=user_id,
        retry_state=BUY_ROUTES
    )
    reply_markup = InlineKeyboardMarkup([
        *buy_buttons,
        back_button
    ])

    # Edita mensagem com as informações do item escolhido
    markdown_text = create_text_in_box(
        text=markdown_text,
        section_name=SECTION_TEXT_SHOP,
        section_start=SECTION_HEAD_SHOP_START,
        section_end=SECTION_HEAD_SHOP_END,
    )
    if user_id == chat_id:
        await edit_message_text(
            function_caller='SELLER.CHECK_SELL_ITEM()',
            new_text=markdown_text,
            context=context,
            chat_id=chat_id,
            message_id=message_id,
            need_response=False,
            markdown=True,
            reply_markup=reply_markup,
        )
    else:
        await update.effective_chat.send_message(
            text=markdown_text,
            reply_markup=reply_markup,
            disable_notification=silent,
            parse_mode=ParseMode.MARKDOWN_V2
        )
        await delete_message(
            function_caller='CHECK_SELL_ITEM()',
            context=context,
            query=query
        )

    return BUY_ROUTES


@skip_if_dead_char
@skip_if_immobilized
@confusion(BUY_ROUTES)
@print_basic_infos
@retry_after
async def buy_item(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Compra item da loja.
    '''

    message = update.effective_message
    message_id = update.effective_message.id
    query = update.callback_query
    try:
        old_reply_markup = query.message.reply_markup
        await message_edit_reply_markup(
            function_caller='SELLER.BUY_ITEM()',
            message=message,
            context=context,
            need_response=True,
            reply_markup=None,
        )
    except Exception as e:
        print(type(e), e)
        return ConversationHandler.END

    bag_model = BagModel()
    player_model = PlayerModel()
    char_model = CharacterModel()
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_name = update.effective_user.name
    silent = get_attribute_group_or_player(chat_id, 'silent')
    data = callback_data_to_dict(query.data)
    item_pos = data['sell_item']
    item_id = data['sell_item_id']
    page = data['sell_page']
    data_user_id = data['user_id']
    buy_quantity = data['buy']

    if data_user_id != user_id:  # Não executa se outro usuário mexer na bolsa
        await answer(query=query, text=ACCESS_DENIED, show_alert=True)
        await message_edit_reply_markup(
            function_caller='SELLER.BUY_ITEM()',
            message=message,
            context=context,
            need_response=True,
            reply_markup=old_reply_markup,
        )
        return BUY_ROUTES

    player = player_model.get(user_id)
    player_character = char_model.get(user_id)
    trocado = player.trocado
    item = get_item_from_bag_by_position(chat_id, page, item_pos)

    if item_id != str(item._id):
        query_text = 'O item não está mais disponível'
        answer(query=query, text=query_text, show_alert=True)
        back_button = get_sell_back_button(
            page=page,
            user_id=user_id,
            retry_state=START_ROUTES
        )
        reply_markup = InlineKeyboardMarkup([back_button])
        query.edit_message_reply_markup(reply_markup=reply_markup)
        return START_ROUTES

    buy_quantity = min(item.quantity, buy_quantity)
    item_price = get_discount_price(
        price=item.price,
        player_character=player_character
    )
    total_price = item_price * buy_quantity
    markdown_text = ''

    if total_price > trocado:
        answer(query=query, text=NOT_ENOUGH_MONEY, show_alert=True)
    elif trocado >= total_price:
        bag_model.sub(item, chat_id, buy_quantity)
        bag_model.add(item, user_id, buy_quantity)
        player.sub_trocado(total_price)
        player_model.save(player)
        trocado = player.trocado
        item.sub(buy_quantity)
        item_price_text = get_discount_price_text(
            price=item.price,
            player_character=player_character
        )
        markdown_text = (
            f'*{user_name}*: {trocado}{EmojiEnum.TROCADO.value}\n'
            f'*Preço*: {item_price_text}\n\n'
            f'Você comprou *{buy_quantity}x{item.name}* '
            f'por *{total_price}*{EmojiEnum.TROCADO.value}\n\n'
        )

    # Criando os Botões
    buy_buttons = [[]]
    if item.quantity > 0:
        buy_buttons = get_buy_buttons(
            page=page,
            user_id=user_id,
            item_pos=item_pos,
            item=item,
            trocado=trocado,
        )
        if isinstance(item.item, Equipment):
            equips_model = EquipsModel()
            equips = equips_model.get(user_id)
            markdown_text += equips.compare(item.item, is_sell=True)
        elif isinstance(item.item, Consumable):
            markdown_text += item.get_all_sheets(
                verbose=True,
                markdown=True,
                show_quantity=True,
                is_sell=True
            )

    back_button = get_sell_back_button(
        page=page,
        user_id=user_id,
        retry_state=BUY_ROUTES
    )
    reply_markup = InlineKeyboardMarkup([
        *buy_buttons,
        back_button
    ])

    markdown_text = create_text_in_box(
        text=markdown_text,
        section_name=SECTION_TEXT_SHOP,
        section_start=SECTION_HEAD_SHOP_START,
        section_end=SECTION_HEAD_SHOP_END,
    )
    if user_id == chat_id:
        await edit_message_text(
            function_caller='SELLER.BUY_ITEM()',
            new_text=markdown_text,
            context=context,
            chat_id=chat_id,
            message_id=message_id,
            need_response=False,
            markdown=True,
            reply_markup=reply_markup,
        )
    else:
        await update.effective_chat.send_message(
            text=markdown_text,
            reply_markup=reply_markup,
            disable_notification=silent,
            parse_mode=ParseMode.MARKDOWN_V2
        )
        await delete_message(
            function_caller='BUY_ITEM()',
            context=context,
            query=query
        )
    if item.quantity > 0:
        return BUY_ROUTES
    else:
        return START_ROUTES


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Apaga a mensagem quando o jogador dono da conversa da loja
    clica em Deixar a Loja.
    '''

    user_id = update.effective_user.id
    query = update.callback_query
    if query:
        data = callback_data_to_dict(query.data)
        data_user_id = data['user_id']

        # Não executa se outro usuário mexer na bolsa
        if data_user_id != user_id:
            await answer(query=query, text=ACCESS_DENIED, show_alert=True)
            return CHECK_ROUTES

        await answer(query=query, text='Deixando Loja...')
        await delete_message(
            function_caller='CANCEL_SELLER()',
            context=context,
            query=query
        )

        return ConversationHandler.END

    return START_ROUTES


@skip_if_spawn_timeout
async def job_create_new_items(context: ContextTypes.DEFAULT_TYPE):
    '''Cria novos itens para a bag do vendedor.
    '''

    print('JOB_CREATE_NEW_ITEMS()')
    bag_model = BagModel()
    job = context.job
    chat_id = job.chat_id
    group_level = get_attribute_group(chat_id, 'group_level')
    silent = get_attribute_group_or_player(chat_id, 'silent')
    chars_level_list = get_chars_level_from_group(chat_id)
    mean_level_list = mean_level(chars_level_list, TOTAL_MEAN_LEVELS)
    multiply_quantity = max(1, len(chars_level_list))

    seller_bag = Bag(
        items=[],
        player_id=chat_id,
    )

    for char_level in mean_level_list:
        for _ in range(TOTAL_EQUIPMENTS):
            equipment_item = create_random_equipment(
                equip_type=None,
                group_level=char_level,
                save_in_database=True
            )
            seller_bag.add(equipment_item)

    consumable_items_generator = create_random_consumable(
        group_level=group_level,
        ignore_list=[TrocadoPouchConsumable, GemstoneConsumable],
        min_consumable_quantity=(10 * multiply_quantity),
        max_consumable_quantity=(20 * multiply_quantity),
        total_items=TOTAL_CONSUMABLES
    )
    for consumable_item in consumable_items_generator:
        seller_bag.add(consumable_item)

    seller_bag.sort_by_equip_type()
    bag_model.save(seller_bag)

    text = escape_for_citation_markdown_v2(
        f'>{SELLER_NAME}: {choice(REPLY_TEXT_NEW_ITEMS_ARRIVED)}\n\n'
        f'Use o comando /{COMMANDS[0]} para acessar a *LOJA*.'
    )
    call_telegram_kwargs = dict(
        chat_id=chat_id,
        text=text,
        disable_notification=silent,
        parse_mode=ParseMode.MARKDOWN_V2,
    )

    await call_telegram_message_function(
        function_caller='JOB_CREATE_NEW_ITEMS()',
        function=context.bot.send_message,
        context=context,
        need_response=False,
        **call_telegram_kwargs
    )


def get_item_texts(items: List[Item]) -> str:
    markdown_text = ''
    zero_fill = 2
    if items:
        zero_fill = max(len(str(item.quantity)) for item in items)
    for index, item in enumerate(items):
        markdown_text += f'*Ⅰ{(index + 1):02}:*'
        markdown_text += item.get_sheet(
            verbose=True,
            markdown=True,
            zero_fill=zero_fill
        )
        markdown_text += f'*Preço*: {item.price_text}\n'

    return markdown_text.strip() + '\n'


def get_seller_item_buttons(
    items: List[Item],
    page: int,
    user_id: int,
) -> List[List[InlineKeyboardButton]]:

    items_buttons = []
    # Criando texto e botões dos itens
    for index, _ in enumerate(items):
        items_buttons.append(InlineKeyboardButton(
            text=f'I{index + 1:02}',
            callback_data=callback_data_to_string({
                'sell_item': index,
                'sell_page': page,
                'user_id': user_id,
            })
        ))

    reshaped_items_buttons = reshape_row_buttons(
        buttons=items_buttons,
        buttons_per_row=5
    )

    return reshaped_items_buttons


def get_sell_navigation_buttons(
    have_back_page: bool,
    have_next_page: bool,
    page: int,
    user_id: int,
) -> List[InlineKeyboardButton]:

    navigation_keyboard = []
    if have_back_page:  # Cria botão de Voltar Página
        navigation_keyboard.append(
            InlineKeyboardButton(
                text=NAV_PREVIOUS_BUTTON_TEXT,
                callback_data=callback_data_to_string({
                    'sell_page': (page - 1),
                    'user_id': user_id,
                })
            )
        )
    if have_next_page:  # Cria botão de Avançar Página
        navigation_keyboard.append(
            InlineKeyboardButton(
                text=NAV_NEXT_BUTTON_TEXT,
                callback_data=callback_data_to_string({
                    'sell_page': (page + 1),
                    'user_id': user_id,
                })
            )
        )

    return navigation_keyboard


def get_sell_extremes_navigation_buttons(
    have_back_page: bool,
    have_next_page: bool,
    user_id: int,
    seller_id: int,
) -> List[InlineKeyboardButton]:

    extremes_navigation_keyboard = []
    if have_back_page:  # Cria botão para a Primeira Página
        extremes_navigation_keyboard.append(
            InlineKeyboardButton(
                text=NAV_START_BUTTON_TEXT,
                callback_data=callback_data_to_string({
                    'sell_page': 0,
                    'user_id': user_id,
                })
            )
        )
    if have_next_page:  # Cria botão para a Última Página
        bag_model = BagModel()
        bag_length = bag_model.length('items_ids', seller_id)
        total_pages = (bag_length - 1) // ITEMS_PER_PAGE
        total_pages = max(total_pages, 0)  # Evita números negativos
        extremes_navigation_keyboard.append(
            InlineKeyboardButton(
                text=NAV_END_BUTTON_TEXT,
                callback_data=callback_data_to_string({
                    'sell_page': total_pages,
                    'user_id': user_id,
                })
            )
        )

    return extremes_navigation_keyboard


def get_leave_shop_button(user_id: int) -> List[InlineKeyboardButton]:
    return [
        InlineKeyboardButton(
            text=LEAVE_SHOP_BUTTON_TEXT,
            callback_data=callback_data_to_string({
                'command': CALLBACK_LEAVE_SHOP,
                'user_id': user_id,
            })
        )]


def get_sell_back_button(
    page: int,
    user_id: int,
    retry_state: int
) -> List[InlineKeyboardButton]:
    return [
        InlineKeyboardButton(
            text=NAV_BACK_BUTTON_TEXT,
            callback_data=callback_data_to_string({
                'sell_page': page,
                'user_id': user_id,
                'retry_state': retry_state
            })
        )
    ]


def get_buy_buttons(
    page: int,
    user_id: int,
    item_pos: int,
    item: Item,
    trocado: int,
) -> List[InlineKeyboardButton]:
    buy_buttons = []
    how_much_can_i_buy = int(trocado // item.price)
    quantity = min(item.quantity, how_much_can_i_buy)
    item_id = str(item._id)
    for quantity_option in DROPUSE_QUANTITY_OPTION_LIST:
        if quantity_option <= quantity:
            text = BUY_MANY_BUTTON_TEXT.format(
                quantity_option=quantity_option
            )
            buy_buttons.append(
                InlineKeyboardButton(
                    text=text,
                    callback_data=callback_data_to_string({
                        'buy': quantity_option,
                        'sell_item': item_pos,
                        'sell_page': page,
                        'sell_item_id': item_id,
                        'user_id': user_id,
                    })
                )
            )

    return reshape_row_buttons(buy_buttons, buttons_per_row=2)


def get_discount_price(
    price: int,
    user_id: int = None,
    player_character: BaseCharacter = None
) -> int:
    if user_id is None and player_character is None:
        raise ValueError('user_id or player_character precisa ser definido.')
    if player_character is None:
        char_model = CharacterModel()
        player_character = char_model.get(user_id)

    charisma = player_character.bs.charisma
    mod_charisma = player_character.bs.mod_charisma
    lowest_price = price // 2
    discount = price - (charisma + (mod_charisma * 2))
    final_price = max(lowest_price, discount)

    return int(final_price)


def get_discount_price_text(
    price: int,
    user_id: int = None,
    player_character: BaseCharacter = None
) -> str:
    discount_price = get_discount_price(
        price=price,
        user_id=user_id,
        player_character=player_character
    )

    return f'{discount_price}{EmojiEnum.TROCADO.value}'


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
        START_ROUTES: [
            CallbackQueryHandler(start, pattern=PATTERN_SELL_PAGE),
        ],
        CHECK_ROUTES: [
            CallbackQueryHandler(start, pattern=PATTERN_SELL_PAGE),
            CallbackQueryHandler(check_sell_item, pattern=PATTERN_SELL_ITEM),
            CallbackQueryHandler(cancel, pattern=PATTERN_LEAVE_SHOP),
        ],
        BUY_ROUTES: [
            CallbackQueryHandler(buy_item, pattern=PATTERN_BUY),
            CallbackQueryHandler(start, pattern=PATTERN_SELL_PAGE),
        ],
    },
    fallbacks=[
        CommandHandler(CANCEL_COMMANDS, cancel)
    ],
    allow_reentry=True,
    conversation_timeout=TEN_MINUTES_IN_SECONDS,
)
