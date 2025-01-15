from datetime import timedelta
from math import sqrt
from random import choice
from time import sleep
from typing import List, Union

from bson import ObjectId
from telegram import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update
)
from telegram.constants import ParseMode
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    ContextTypes,
    PrefixHandler,
)

from bot.constants.bag import (
    ACCESS_DENIED,
    ALL_RESTORE_CONSUMABLES_TUPLE,
    CALLBACK_CLOSE_BAG,
    CALLBACK_TEXT_DESTROY_ITEM,
    CALLBACK_TEXT_SORT_ITEMS,
    CANCEL_COMMANDS,
    CHRYSUS_EQUIPMENT_SELL,
    CHRYSUS_GEMSTONE_SELL,
    CHRYSUS_OTHERS_SELL,
    CHRYSUS_POTION_SELL,
    CLOSE_BAG_BUTTON_TEXT,
    COLLECT_MANY_BUTTON_TEXT,
    COLLECT_MANY_BUTTON_VERBOSE_TEXT,
    COMMANDS,
    COMPARE_INFO_BUTTON_TEXT,
    CONSUMABLE_SORT_DOWN_BUTTON_TEXT,
    CONSUMABLE_SORT_UP_BUTTON_TEXT,
    DESTROY_ITEM_BUTTON_TEXT,
    DISCARD_MANY_BUTTON_TEXT,
    DISCARD_MANY_BUTTON_VERBOSE_TEXT,
    EQUIP_BUTTON_TEXT,
    EQUIP_INFO_BUTTON_TEXT,
    EQUIPMENT_POWER_SORT_DOWN_BUTTON_TEXT,
    EQUIPMENT_POWER_SORT_UP_BUTTON_TEXT,
    EQUIPMENT_RARITY_SORT_DOWN_BUTTON_TEXT,
    EQUIPMENT_RARITY_SORT_UP_BUTTON_TEXT,
    IDENTIFY_BUTTON_TEXT,
    ITEMS_PER_PAGE,
    EQUIP_LEFT_BUTTON_TEXT,
    NAV_BACK_BUTTON_TEXT,
    NAV_NEXT_ITEM_BUTTON_TEXT,
    NAV_PREVIOUS_BUTTON_TEXT,
    NAV_END_BUTTON_TEXT,
    NAV_NEXT_BUTTON_TEXT,
    NAV_PREVIOUS_ITEM_BUTTON_TEXT,
    NAV_START_BUTTON_TEXT,
    PATTERN_CLOSE_BAG,
    PATTERN_DESTROY_ITEM,
    PATTERN_DROP,
    PATTERN_EQUIP_INFO,
    PATTERN_GET_DROP,
    PATTERN_IDENTIFY,
    PATTERN_ITEM,
    PATTERN_PAGE,
    PATTERN_SELL,
    PATTERN_SORT,
    PATTERN_SORT_ITEMS,
    PATTERN_USE,
    SECTION_TEXT_CONSUMABLE,
    SECTION_TEXT_EQUIPMENT,
    SECTION_TEXT_GEMSTONE,
    SECTION_TEXT_TROCADO_POUCH,
    SELL_MANY_BUTTON_TEXT,
    SELL_MANY_BUTTON_VERBOSE_TEXT,
    SORT_ITEMS_BUTTON_TEXT,
    TAKE_BUTTON_TEXT,
    EQUIP_RIGHT_BUTTON_TEXT,
    DROPUSE_QUANTITY_OPTION_LIST,
    TRANSMUTE_ITEM_BUTTON_TEXT,
    USE_MANY_BUTTON_TEXT,
    USE_MANY_BUTTON_VERBOSE_TEXT,
    VERBOSE_BUTTONS_THRESHOLD,
)

from bot.constants.filters import (
    BASIC_COMMAND_FILTER,
    PREFIX_COMMANDS
)
from bot.constants.job import BASE_JOB_KWARGS
from bot.constants.seller import SELLER_NAME
from bot.constants.chat_xp import SECTION_TEXT_XP
from bot.decorators import (
    print_basic_infos,
    retry_after,
    skip_if_dead_char,
    skip_if_no_singup_player,
    skip_if_immobilized,
    confusion,
)
from bot.functions.bag import (
    LIMIT_ITEM_IN_BAG,
    exist_item_in_bag_by_position,
    exists_in_bag,
    get_identifying_lens,
    get_item_from_bag_by_position,
    get_page_and_item_pos,
    have_identifying_lens,
    is_full_bag,
    sub_identifying_lens_from_bag
)
from bot.functions.char import add_xp, save_char
from bot.functions.chat import (
    answer,
    call_telegram_message_function,
    callback_data_to_dict,
    callback_data_to_string,
    delete_message,
    delete_message_from_context,
    edit_message_text,
    message_edit_reply_markup,
    reply_typing,
    send_alert_or_message,
    send_private_message
)
from bot.functions.general import get_attribute_group_or_player
from bot.functions.keyboard import remove_buttons_by_text, reshape_row_buttons
from bot.functions.player import (
    get_player_id_by_name,
    get_player_name,
    get_player_trocado
)
from constant.text import (
    SECTION_HEAD_CONSUMABLE_END,
    SECTION_HEAD_CONSUMABLE_START,
    SECTION_HEAD_EQUIPMENT_END,
    SECTION_HEAD_EQUIPMENT_START,
    SECTION_HEAD_GEMSTONE_END,
    SECTION_HEAD_GEMSTONE_START,
    SECTION_HEAD_TROCADO_POUCH_END,
    SECTION_HEAD_TROCADO_POUCH_START,
    SECTION_HEAD_XP_END,
    SECTION_HEAD_XP_START,
    TEXT_SEPARATOR,
    TITLE_HEAD
)
from constant.time import TEN_MINUTES_IN_SECONDS
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
from rpgram import Bag, Equips, Item, Player
from rpgram.boosters import Equipment
from rpgram.characters import BaseCharacter
from rpgram.consumables import (
    Consumable,
    GemstoneConsumable,
    TrocadoPouchConsumable
)
from rpgram.enums import EmojiEnum, EquipmentEnum, TrocadoEnum


DROPS_CHAT_DATA_KEY = 'drops'
MINUTES_TO_TIMEOUT_DROP = 60



# ROUTES
(
    START_ROUTES,
    CHECK_ROUTES,
    USE_ROUTES,
    SORT_ROUTES,
) = range(4)


@skip_if_no_singup_player
@skip_if_dead_char
@skip_if_immobilized
@confusion(START_ROUTES)
@print_basic_infos
@retry_after
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Envia ou edita mensagem contendo uma página dos itens do jogador
    '''

    await reply_typing(
        function_caller='BAG.START()',
        update=update,
        context=context,
    )
    bag_model = BagModel()
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    message_id = update.effective_message.id
    user_name = update.effective_user.name
    query = update.callback_query
    args = context.args
    silent = get_attribute_group_or_player(chat_id, 'silent')

    if args and args[0].startswith('@'):
        target_name = args[0]
        target_id = get_player_id_by_name(target_name)
        if target_id is None:
            text = (
                f'O jogador "{target_name}" não existe '
                f'(Não possui o objeto Player).'
            )
            return await send_alert_or_message(
                function_caller='START_BAG()',
                context=context,
                query=query,
                text=text,
                chat_id=chat_id,
                user_id=user_id,
                show_alert=True
            )
    else:
        target_id = user_id

    page = 0
    if query:
        data = callback_data_to_dict(query.data)
        page = data['page']  # starts zero
        data_user_id = data['user_id']
        target_id = data['target_id']
        retry_state = data.get('retry_state')

        # Não executa se outro usuário mexer na bolsa
        if data_user_id != user_id:
            await answer(query=query, text=ACCESS_DENIED, show_alert=True)
            return retry_state

    target_name = get_player_name(target_id)

    skip_slice = ITEMS_PER_PAGE * page
    size_slice = ITEMS_PER_PAGE + 1

    player_bag: Bag = bag_model.get(
        query={'player_id': user_id},
        fields={'items_ids': {'$slice': [skip_slice, size_slice]}},
        partial=False
    )
    # Cria uma bolsa caso o jogador não tenha uma.
    if not isinstance(player_bag, Bag):
        player_bag = Bag(
            items=[],
            player_id=user_id
        )
        bag_model.save(player_bag)

    items = player_bag[:]
    have_back_page = False
    have_next_page = False
    if page > 0:
        have_back_page = True
    if len(items) > ITEMS_PER_PAGE:
        items = player_bag[:-1]
        have_next_page = True
    elif all((len(items) == 0, not query)):
        reply_text_kwargs = dict(
            text='Você não tem itens na sua bolsa.',
            disable_notification=silent,
            allow_sending_without_reply=True
        )
        await call_telegram_message_function(
            function_caller='BAG.START()',
            function=update.effective_message.reply_text,
            context=context,
            need_response=False,
            skip_retry=False,
            **reply_text_kwargs,
        )
        return ConversationHandler.END

    # Criando os Botões
    reshaped_items_buttons = get_item_buttons(
        items=items,
        page=page,
        user_id=user_id,
        target_id=target_id
    )

    navigation_keyboard = get_navigation_buttons(
        have_back_page=have_back_page,
        have_next_page=have_next_page,
        page=page,
        user_id=user_id,
        target_id=target_id
    )
    extremes_navigation_keyboard = get_extremes_navigation_buttons(
        have_back_page=have_back_page,
        have_next_page=have_next_page,
        user_id=user_id,
        target_id=target_id
    )

    sort_items_button = get_sort_button(
        page=page,
        user_id=user_id,
        target_id=target_id
    )
    cancel_button = get_close_bag_button(user_id=user_id, target_id=target_id)
    reply_markup = InlineKeyboardMarkup(
        reshaped_items_buttons +
        [navigation_keyboard] +
        [extremes_navigation_keyboard] +
        [sort_items_button + cancel_button]
    )

    markdown_text = (
        f'\n*Bolsa de {user_name}* — {EmojiEnum.PAGE.value}: {page + 1:02}\n'
        f'*Peso*: {player_bag.weight_text}\n'
    )
    markdown_text += get_trocado_and_target_text(
        user_id=user_id,
        target_id=target_id
    )
    markdown_text += get_item_texts(items=items)
    markdown_text = TITLE_HEAD.format(markdown_text)
    markdown_text = escape_basic_markdown_v2(markdown_text)
    if not query:  # Envia Resposta com o texto da tabela de itens e botões
        reply_text_kwargs = dict(
            text=markdown_text,
            disable_notification=silent,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN_V2,
            allow_sending_without_reply=True
        )
        await call_telegram_message_function(
            function_caller='BAG.START()',
            function=update.effective_message.reply_text,
            context=context,
            need_response=False,
            skip_retry=False,
            **reply_text_kwargs,
        )
    else:  # Edita Resposta com o texto da tabela de itens e botões
        await edit_message_text(
            function_caller='BAG.START()',
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
async def check_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Edita a mensagem com as informações do item escolhido.
    '''
    message = update.effective_message
    message_id = update.effective_message.id
    query = update.callback_query

    try:
        old_reply_markup = query.message.reply_markup
        await message_edit_reply_markup(
            function_caller='BAG.CHECK_ITEM()',
            message=message,
            context=context,
            need_response=True,
            reply_markup=None,
        )
    except Exception as e:
        print(type(e), e)
        return ConversationHandler.END

    equips_model = EquipsModel()
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    data = callback_data_to_dict(query.data)
    item_pos = data['item']
    page = data['page']
    data_user_id = data['user_id']
    target_id = data['target_id']
    equip_info = data.get('equip_info')

    if data_user_id != user_id:  # Não executa se outro usuário mexer na bolsa
        await answer(query=query, text=ACCESS_DENIED, show_alert=True)
        await message_edit_reply_markup(
            function_caller='BAG.CHECK_ITEM()',
            message=message,
            context=context,
            need_response=True,
            reply_markup=old_reply_markup,
        )

        return CHECK_ROUTES

    silent = get_attribute_group_or_player(chat_id, 'silent')
    item = get_item_from_bag_by_position(user_id, page, item_pos)
    target_name = get_player_name(target_id)
    markdown_text = get_trocado_and_target_text(
        user_id=user_id,
        target_id=target_id
    )
    if item:
        markdown_text += item.get_all_sheets(
            verbose=True,
            markdown=True,
            show_quantity=True
        )
    equip_buttons = []
    use_buttons = [[]]
    equip_info_identify_button = []
    if isinstance(item.item, Equipment):
        equips: Equips = equips_model.get(user_id)
        if not equip_info:
            markdown_text = equips.compare(item.item)
            equip_info_identify_button.append(
                InlineKeyboardButton(
                    text=EQUIP_INFO_BUTTON_TEXT,
                    callback_data=callback_data_to_string({
                        'equip_info': 1,
                        'item': item_pos,
                        'page': page,
                        'user_id': user_id,
                        'target_id': target_id
                    })
                )
            )
        else:
            markdown_text = item.item.get_sheet(verbose=True, markdown=True)
            equip_info_identify_button.append(
                InlineKeyboardButton(
                    text=COMPARE_INFO_BUTTON_TEXT,
                    callback_data=callback_data_to_string({
                        'equip_info': 0,
                        'item': item_pos,
                        'page': page,
                        'user_id': user_id,
                        'target_id': target_id
                    })
                )
            )
        if item.item.equip_type == EquipmentEnum.ONE_HAND:
            equip_buttons = [
                InlineKeyboardButton(
                    text=EQUIP_LEFT_BUTTON_TEXT,
                    callback_data=callback_data_to_string({
                        'use': 1,
                        'item': item_pos,
                        'hand': 'L',
                        'page': page,
                        'user_id': user_id,
                        'target_id': target_id
                    })
                ),
                InlineKeyboardButton(
                    text=EQUIP_RIGHT_BUTTON_TEXT,
                    callback_data=callback_data_to_string({
                        'use': 1,
                        'item': item_pos,
                        'hand': 'R',
                        'page': page,
                        'user_id': user_id,
                        'target_id': target_id
                    })
                )
            ]
        else:
            equip_buttons = [
                InlineKeyboardButton(
                    text=EQUIP_BUTTON_TEXT,
                    callback_data=callback_data_to_string({
                        'use': 1,
                        'item': item_pos,
                        'page': page,
                        'user_id': user_id,
                        'target_id': target_id
                    })
                )
            ]

        if have_identifying_lens(user_id) and item.item.identifiable:
            equip_info_identify_button.append(
                InlineKeyboardButton(
                    text=IDENTIFY_BUTTON_TEXT,
                    callback_data=callback_data_to_string({
                        'identify': 1,
                        'item': item_pos,
                        'page': page,
                        'user_id': user_id,
                        'target_id': target_id
                    })
                )
            )
    elif isinstance(item.item, Consumable):
        use_buttons = get_use_consumable_buttons(
            page=page,
            user_id=user_id,
            target_id=target_id,
            item_pos=item_pos,
            item=item
        )

    discard_buttons = []
    sell_buttons = []
    navigation_item_buttons = []
    if item:
        discard_buttons = get_discard_buttons(
            page=page,
            user_id=user_id,
            target_id=target_id,
            item_pos=item_pos,
            item=item
        )
        sell_buttons = get_sell_buttons(
            page=page,
            user_id=user_id,
            target_id=target_id,
            item_pos=item_pos,
            item=item
        )
        navigation_item_buttons = get_navigation_item_buttons(
            page=page,
            user_id=user_id,
            target_id=target_id,
            item_pos=item_pos,
            quantity=item.quantity
        )
    back_button = get_back_button(
        page=page,
        user_id=user_id,
        target_id=target_id,
        retry_state=USE_ROUTES
    )
    reply_markup = InlineKeyboardMarkup([
        equip_buttons,
        *use_buttons,
        equip_info_identify_button,
        *discard_buttons,
        *sell_buttons,
        navigation_item_buttons,
        back_button
    ])

    # Edita mensagem com as informações do item escolhido
    markdown_text = escape_basic_markdown_v2(markdown_text)
    await edit_message_text(
        function_caller='CHECK_ITEM()',
        new_text=markdown_text,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        need_response=False,
        markdown=True,
        reply_markup=reply_markup,
    )

    return USE_ROUTES


@skip_if_dead_char
@skip_if_immobilized
@confusion(USE_ROUTES)
@print_basic_infos
@retry_after
async def use_item(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Usa ou equipa o item do jogador.
    '''
    message = update.effective_message
    query = update.callback_query
    try:
        old_reply_markup = query.message.reply_markup
        await message_edit_reply_markup(
            function_caller='BAG.USE_ITEM()',
            message=message,
            context=context,
            need_response=True,
            reply_markup=None,
        )
    except Exception as e:
        print(type(e), e)
        return ConversationHandler.END

    char_model = CharacterModel()
    user_id = update.effective_user.id
    data = callback_data_to_dict(query.data)
    item_pos = data['item']
    page = data['page']
    data_user_id = data['user_id']
    target_id = data['target_id']
    use_quantity = data['use']
    hand = data.get('hand')

    if data_user_id != user_id:  # Não executa se outro usuário mexer na bolsa
        await answer(query=query, text=ACCESS_DENIED, show_alert=True)
        await message_edit_reply_markup(
            function_caller='BAG.USE_ITEM()',
            message=message,
            context=context,
            need_response=True,
            reply_markup=old_reply_markup,
        )

        return USE_ROUTES

    item = get_item_from_bag_by_position(user_id, page, item_pos)
    if isinstance(item.item, Equipment):
        player_character: BaseCharacter = char_model.get(user_id)
    elif isinstance(item.item, Consumable):
        player_character: BaseCharacter = char_model.get(target_id)

    if isinstance(item.item, Consumable):  # Tenta usar o item
        await use_item_consumable(
            user_id=user_id,
            target_id=target_id,
            item=item,
            character=player_character,
            use_quantity=use_quantity,
            page=page,
            item_pos=item_pos,
            context=context,
            query=query,
        )
        if item.quantity <= 0:
            return START_ROUTES
        return USE_ROUTES
    elif isinstance(item.item, Equipment):  # Tenta equipar o item
        old_equipments = await use_item_equipment(
            user_id=user_id,
            target_id=target_id,
            item=item,
            character=player_character,
            hand=hand,
            page=page,
            item_pos=item_pos,
            query=query,
            context=context,
            old_reply_markup=old_reply_markup,
        )
        if not isinstance(old_equipments, list):
            return USE_ROUTES
        else:
            return START_ROUTES


async def use_item_equipment(
    user_id: int,
    target_id: int,
    item: Item,
    character: BaseCharacter,
    hand: str,
    page: int,
    item_pos: int,
    query: CallbackQuery,
    context: ContextTypes.DEFAULT_TYPE,
    old_reply_markup: InlineKeyboardMarkup
) -> List[Equipment]:
    '''Tenta equipar o item.
    '''

    bag_model = BagModel()
    equipment = item.item
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    message = query.message
    old_equipments = None
    try:
        old_equipments = character.equips.equip(equipment, hand)
        await answer(query=query, text=f'Você equipou "{equipment.name}".')
    except Exception as error:
        print(error)
        await answer(query=query, text=f'{error}', show_alert=True)
        await message_edit_reply_markup(
            function_caller='BAG.USE_ITEM_EQUIPMENT()',
            message=message,
            context=context,
            need_response=True,
            reply_markup=old_reply_markup,
        )

        return USE_ROUTES

    bag_model.sub(item, user_id)
    # Adiciona na bolsa os equipamentos que já estavam equipados
    # e que foram substituídos
    for old_equipment in old_equipments:
        old_equipment_item = Item(old_equipment)
        bag_model.add(old_equipment_item, user_id)

    save_char(char=character, equips=True)

    markdown_player_sheet = character.get_all_sheets(
        verbose=False,
        markdown=True
    )
    markdown_player_sheet = escape_basic_markdown_v2(markdown_player_sheet)
    navigation_item_buttons = get_navigation_item_buttons(
        page=page,
        user_id=user_id,
        target_id=target_id,
        item_pos=item_pos,
        quantity=0
    )
    back_button = get_back_button(
        page=page,
        user_id=user_id,
        target_id=target_id,
        retry_state=START_ROUTES
    )
    reply_markup = InlineKeyboardMarkup([
        navigation_item_buttons,
        back_button
    ])
    await edit_message_text(
        function_caller='USE_ITEM_EQUIPMENT()',
        new_text=markdown_player_sheet,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        need_response=False,
        markdown=True,
        reply_markup=reply_markup,
    )

    return old_equipments


async def use_item_consumable(
    user_id: int,
    target_id: int,
    item: Item,
    character: BaseCharacter,
    use_quantity: int,
    page: int,
    item_pos: int,
    context: ContextTypes.DEFAULT_TYPE,
    query: CallbackQuery,
) -> None:
    '''Usa o item consumível
    '''

    bag_model = BagModel()
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    name = item.name
    use_quantity = min(item.quantity, use_quantity)
    all_report_text = [f'Reporting({use_quantity:02}):']
    target_name = get_player_name(target_id)
    user_name = get_player_name(user_id)
    try:
        for i in range(use_quantity):
            report = item.use(character)
            all_report_text.append(f'{i+1:02}: {report["text"]}')
            bag_model.sub(item, user_id)
        text = f'Você usou {use_quantity} "{name}".\n'
        save_char(char=character)

        await answer(query=query, text=text)
    except Exception as error:
        print(error)
        query_text = f'Item "{name}" não pode ser usado.\n\n{error}'
        await answer(query=query, text=query_text, show_alert=True)
    finally:
        all_report_text = '\n'.join(all_report_text)
        markdown_text = get_trocado_and_target_text(
            user_id=user_id,
            target_id=target_id
        )
        markdown_text += item.get_all_sheets(
            verbose=True,
            markdown=True,
            show_quantity=True
        )
        markdown_text = (
            f'{markdown_text}'
            f'\n{TEXT_SEPARATOR}\n\n'
            f'{all_report_text}'
        )
        if item.quantity <= 0:
            navigation_item_buttons = get_navigation_item_buttons(
                page=page,
                user_id=user_id,
                target_id=target_id,
                item_pos=item_pos,
                quantity=item.quantity
            )
            back_button = get_back_button(
                page=page,
                user_id=user_id,
                target_id=target_id,
                retry_state=USE_ROUTES
            )
            reply_markup = InlineKeyboardMarkup([
                navigation_item_buttons,
                back_button
            ])
        else:
            use_buttons = get_use_consumable_buttons(
                page=page,
                user_id=user_id,
                target_id=target_id,
                item_pos=item_pos,
                item=item
            )
            discard_buttons = get_discard_buttons(
                page=page,
                user_id=user_id,
                target_id=target_id,
                item_pos=item_pos,
                item=item
            )
            sell_buttons = get_sell_buttons(
                page=page,
                user_id=user_id,
                target_id=target_id,
                item_pos=item_pos,
                item=item
            )
            navigation_item_buttons = get_navigation_item_buttons(
                page=page,
                user_id=user_id,
                target_id=target_id,
                item_pos=item_pos,
                quantity=item.quantity
            )
            back_button = get_back_button(
                page=page,
                user_id=user_id,
                target_id=target_id,
                retry_state=USE_ROUTES
            )
            reply_markup = InlineKeyboardMarkup([
                *use_buttons,
                *discard_buttons,
                *sell_buttons,
                navigation_item_buttons,
                back_button
            ])
        markdown_text = escape_basic_markdown_v2(markdown_text)
        await edit_message_text(
            function_caller='USE_ITEM_CONSUMABLE()',
            new_text=markdown_text,
            context=context,
            chat_id=chat_id,
            message_id=message_id,
            need_response=False,
            markdown=True,
            reply_markup=reply_markup,
        )

        if user_id != target_id:
            private_text = escape_basic_markdown_v2(
                f'{user_name} usou item em você.\n\n{all_report_text}'
            )
            await send_private_message(
                function_caller='USE_ITEM_CONSUMABLE()',
                context=context,
                text=private_text,
                user_id=target_id,
                markdown=True,
                close_by_owner=False,
            )


@skip_if_dead_char
@skip_if_immobilized
@confusion(USE_ROUTES)
@print_basic_infos
@retry_after
async def identify_item(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    '''identifica um equipamento.
    '''

    chat_id = update.effective_chat.id
    message_id = update.effective_message.message_id
    message = update.effective_message
    query = update.callback_query

    try:
        old_reply_markup = query.message.reply_markup
        await message_edit_reply_markup(
            function_caller='BAG.IDENTIFY_ITEM()',
            message=message,
            context=context,
            need_response=True,
            reply_markup=None,
        )
    except Exception as e:
        print(type(e), e)
        return ConversationHandler.END

    item_model = ItemModel()
    equips_model = EquipsModel()
    user_id = update.effective_user.id
    data = callback_data_to_dict(query.data)
    item_pos = data['item']
    page = data['page']
    data_user_id = data['user_id']
    target_id = data['target_id']
    use_quantity = data['identify']

    if data_user_id != user_id:  # Não executa se outro usuário mexer na bolsa
        await answer(query=query, text=ACCESS_DENIED, show_alert=True)
        await message_edit_reply_markup(
            function_caller='BAG.IDENTIFY_ITEM()',
            message=message,
            context=context,
            need_response=True,
            reply_markup=old_reply_markup,
        )
        return USE_ROUTES

    item_equipment = get_item_from_bag_by_position(user_id, page, item_pos)
    equipment = item_equipment.item
    if not equipment.identifiable:
        text = '⛔ESSE EQUIPAMENTO NÃO PODE SER IDENTIFICADO⛔'
        await answer(query=query, text=text, show_alert=True)
    elif have_identifying_lens(user_id):
        consumable_identifier = get_identifying_lens()
        report = consumable_identifier.use(equipment)
        report_text = report['text']
        item_model.save(equipment)
        sub_identifying_lens_from_bag(user_id)
        name = consumable_identifier.name
        text = (
            f'{report_text}\n\n'
            f'Você usou {use_quantity} "{name}".\n'
        )
        await answer(query=query, text=text, show_alert=True)
    else:
        text = '⛔VOCÊ NÃO TEM UM ITEM DE IDENTIFICAÇÃO⛔'
        await answer(query=query, text=text, show_alert=True)

    equips: Equips = equips_model.get(user_id)
    markdown_text = equips.compare(equipment)
    reply_markup = remove_buttons_by_text(
        old_reply_markup,
        IDENTIFY_BUTTON_TEXT
    )
    markdown_text = escape_basic_markdown_v2(markdown_text)
    await edit_message_text(
        function_caller='IDENTIFY_ITEM()',
        new_text=markdown_text,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        need_response=False,
        markdown=True,
        reply_markup=reply_markup,
    )

    return USE_ROUTES


@skip_if_dead_char
@skip_if_immobilized
@confusion(USE_ROUTES)
@print_basic_infos
@retry_after
async def sell_item(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    '''Vende o item do jogador.
    '''

    chat_id = update.effective_chat.id
    message_id = update.effective_message.message_id
    message = update.effective_message
    query = update.callback_query

    try:
        old_reply_markup = query.message.reply_markup
        await message_edit_reply_markup(
            function_caller='BAG.SELL_ITEM()',
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
    user_id = update.effective_user.id
    data = callback_data_to_dict(query.data)
    item_pos = data['item']
    page = data['page']
    data_user_id = data['user_id']
    target_id = data['target_id']
    sell_quantity = data['sell']

    if data_user_id != user_id:  # Não executa se outro usuário mexer na bolsa
        await answer(query=query, text=ACCESS_DENIED, show_alert=True)
        await message_edit_reply_markup(
            function_caller='BAG.SELL_ITEM()',
            message=message,
            context=context,
            need_response=True,
            reply_markup=old_reply_markup,
        )
        return USE_ROUTES

    player: Player = player_model.get(user_id)
    item = get_item_from_bag_by_position(user_id, page, item_pos)
    sell_quantity = min(sell_quantity, item.quantity)
    item_sell_price = get_bonus_price(price=item.sell_price, user_id=user_id)
    trocado = int(sell_quantity * item_sell_price)
    player.add_trocado(trocado)

    bag_model.sub(item, user_id, quantity=sell_quantity)
    player_model.save(player)

    item.sub(quantity=sell_quantity)

    if item.quantity <= 0 or isinstance(item.item, Equipment):
        navigation_item_buttons = get_navigation_item_buttons(
            page=page,
            user_id=user_id,
            target_id=target_id,
            item_pos=item_pos,
            quantity=item.quantity
        )
        back_button = get_back_button(
            page=page,
            user_id=user_id,
            target_id=target_id,
            retry_state=START_ROUTES
        )
        reply_markup = InlineKeyboardMarkup([
            navigation_item_buttons,
            back_button
        ])
    else:
        use_buttons = get_use_consumable_buttons(
            page=page,
            user_id=user_id,
            target_id=target_id,
            item_pos=item_pos,
            item=item
        )
        discard_buttons = get_discard_buttons(
            page=page,
            user_id=user_id,
            target_id=target_id,
            item_pos=item_pos,
            item=item
        )
        sell_buttons = get_sell_buttons(
            page=page,
            user_id=user_id,
            target_id=target_id,
            item_pos=item_pos,
            item=item
        )
        navigation_item_buttons = get_navigation_item_buttons(
            page=page,
            user_id=user_id,
            target_id=target_id,
            item_pos=item_pos,
            quantity=item.quantity
        )
        back_button = get_back_button(
            page=page,
            user_id=user_id,
            target_id=target_id,
            retry_state=USE_ROUTES
        )
        reply_markup = InlineKeyboardMarkup([
            *use_buttons,
            *discard_buttons,
            *sell_buttons,
            navigation_item_buttons,
            back_button
        ])

    markdown_text = get_trocado_and_target_text(
        user_id=user_id,
        target_id=target_id
    )

    if isinstance(item.item, TrocadoPouchConsumable):
        markdown_text += (
            f'Você coletou {trocado}{EmojiEnum.TROCADO.value} de '
            f'"{sell_quantity}x {item.name}" e esta com um total de '
            f'{player.trocado_text}.\n\n'
        )
    else:
        chrysus_quote = f'>*{SELLER_NAME}*: '
        if isinstance(item.item, Equipment):
            chrysus_quote += choice(CHRYSUS_EQUIPMENT_SELL)
        elif isinstance(item.item, ALL_RESTORE_CONSUMABLES_TUPLE):
            chrysus_quote += choice(CHRYSUS_POTION_SELL)
        elif isinstance(item.item, GemstoneConsumable):
            chrysus_quote += choice(CHRYSUS_GEMSTONE_SELL)
        else:
            chrysus_quote += choice(CHRYSUS_OTHERS_SELL)

        markdown_text = (
            f'{chrysus_quote}\n\n'
            f'{markdown_text}'
            f'Você vendeu "{sell_quantity}x {item.name}" e faturou '
            f'{trocado}{EmojiEnum.TROCADO.value}.\n'
            f'Agora você tem {player.trocado_text}.\n\n'
        )

    markdown_text += item.get_all_sheets(
        verbose=True,
        markdown=True,
        show_quantity=True
    )
    markdown_text = escape_for_citation_markdown_v2(markdown_text)
    await edit_message_text(
        function_caller='SELL_ITEM()',
        new_text=markdown_text,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        need_response=False,
        markdown=True,
        reply_markup=reply_markup,
    )

    if item.quantity <= 0:
        return START_ROUTES
    return USE_ROUTES


@skip_if_dead_char
@skip_if_immobilized
@confusion(USE_ROUTES)
@print_basic_infos
@retry_after
async def drop_item(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    '''drop o item do jogador.
    '''
    message_id = update.effective_message.message_id
    message = update.effective_message
    query = update.callback_query

    try:
        old_reply_markup = query.message.reply_markup
        await message_edit_reply_markup(
            function_caller='BAG.DROP_ITEM()',
            message=message,
            context=context,
            need_response=True,
            reply_markup=None,
        )
    except Exception as e:
        print(type(e), e)
        return ConversationHandler.END

    bag_model = BagModel()
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_name = update.effective_user.name
    data = callback_data_to_dict(query.data)
    item_pos = data['item']
    page = data['page']
    data_user_id = data['user_id']
    target_id = data['target_id']
    drop = data['drop']
    silent = get_attribute_group_or_player(chat_id, 'silent')

    if data_user_id != user_id:  # Não executa se outro usuário mexer na bolsa
        await answer(query=query, text=ACCESS_DENIED, show_alert=True)
        await message_edit_reply_markup(
            function_caller='BAG.DROP_ITEM()',
            message=message,
            context=context,
            need_response=True,
            reply_markup=old_reply_markup,
        )
        return USE_ROUTES

    item = get_item_from_bag_by_position(user_id, page, item_pos)
    drop = min(drop, item.quantity)

    bag_model.sub(item, user_id, quantity=-(drop))

    navigation_item_buttons = get_navigation_item_buttons(
        page=page,
        user_id=user_id,
        target_id=target_id,
        item_pos=item_pos,
        quantity=(item.quantity - drop),
    )
    back_button = get_back_button(
        page=page,
        user_id=user_id,
        target_id=target_id,
        retry_state=START_ROUTES
    )
    reply_markup = InlineKeyboardMarkup([
        navigation_item_buttons,
        back_button
    ])
    markdown_text = f'Você dropou o item "{drop}x {item.name}".'
    markdown_text = escape_basic_markdown_v2(markdown_text)
    await edit_message_text(
        function_caller='DROP_ITEM()',
        new_text=markdown_text,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        need_response=False,
        markdown=True,
        reply_markup=reply_markup,
    )

    # Envia mensagem de drop do item, se ele foi dropado no grupo
    if chat_id != user_id:
        text = f'{user_name} dropou o item'
        item.quantity = drop
        await send_drop_message(
            update=update,
            context=context,
            items=item,
            text=text,
            silent=silent,
        )

    return START_ROUTES


@skip_if_dead_char
@skip_if_immobilized
@confusion()
@print_basic_infos
async def get_drop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Pega o item dropado
    '''

    query = update.callback_query
    message_id = update.effective_message.message_id
    drops = {}

    # Checa se o item pode ser pego, se não, cancela a ação e apaga a mensagem
    # Só pode ser pego se no dicionário drop contiver o message_id como chave e
    # True como valor. Caso contrário, cancela a ação e apaga a mensagem.
    if DROPS_CHAT_DATA_KEY in context.chat_data:
        drops = context.chat_data[DROPS_CHAT_DATA_KEY]
        if drops.get(message_id, None) is not True:
            drops.pop(message_id, None)
            query_text = f'Este item não existe mais.'
            await answer(query=query, text=query_text, show_alert=True)
            await delete_message(
                function_caller='GET_DROP()',
                context=context,
                query=query
            )

            return ConversationHandler.END
    else:
        create_and_put_drop_dict(context=context)
        query_text = f'Este item não existe mais.'
        await answer(query=query, text=query_text, show_alert=True)
        await delete_message(
            function_caller='GET_DROP()',
            context=context,
            query=query
        )

        return ConversationHandler.END

    bag_model = BagModel()
    item_model = ItemModel()
    user_id = update.effective_user.id
    data = callback_data_to_dict(query.data)
    item_id = data['_id']
    drop = data['drop']

    if is_full_bag(user_id) and not exists_in_bag(user_id, item_id=item_id):
        query_text = (
            f'Você não pode pegar mais itens, pois sua bolsa está cheia. '
            f'A bolsa não pode ter mais de {LIMIT_ITEM_IN_BAG} '
            f'tipos de itens diferentes.'
        )
        await answer(query=query, text=query_text, show_alert=True)

        return ConversationHandler.END

    item: Union[Consumable, Equipment] = item_model.get(item_id)
    if item:
        item = Item(item, quantity=drop)
        bag_model.add(item, user_id)
        drops.pop(message_id, None)

        query_text = f'Você pegou "{drop}x {item.name}".'
        await answer(query=query, text=query_text, show_alert=True)
    else:
        drops.pop(message_id, None)
        print(
            f'get_drop() - Item não existe mais: _id: {item_id} item: {item}.'
        )
        query_text = f'Este item não existe mais.'
        await answer(query=query, text=query_text, show_alert=True)

    await delete_message(
        function_caller='GET_DROP()',
        context=context,
        query=query
    )

    return ConversationHandler.END


@skip_if_dead_char
@skip_if_immobilized
@confusion()
@print_basic_infos
async def destroy_drop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Quebra o item dropado
    '''
    item_model = ItemModel()
    player_model = PlayerModel()
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    query = update.callback_query
    message_id = update.effective_message.message_id
    drops = context.chat_data.get(DROPS_CHAT_DATA_KEY, {})
    answer_text = 'Quebrando o item...'

    if drops.get(message_id, None) is True:
        data = callback_data_to_dict(query.data)
        item_id = data['_id']
        item: Union[Consumable, Equipment] = item_model.get(item_id)
        if isinstance(item, Equipment):
            power = item.power
            base_xp = power // 5
            report_xp = add_xp(
                chat_id=chat_id,
                user_id=user_id,
                base_xp=base_xp,
                to_add_level_bonus=False
            )
            text = f'Você quebrou o item "{item.name}".\n\n'
            text += report_xp['text']
            text = create_text_in_box(
                text=text,
                section_name=SECTION_TEXT_XP,
                section_start=SECTION_HEAD_XP_START,
                section_end=SECTION_HEAD_XP_END,
                clean_func=None,
            )
            player: Player = player_model.get(user_id)
            if report_xp['level_up']:
                silent = get_attribute_group_or_player(chat_id, 'silent')
                reply_text_kwargs = dict(
                    text=text,
                    disable_notification=silent,
                    allow_sending_without_reply=True
                )
                await call_telegram_message_function(
                    function_caller='BAG.START()',
                    function=update.effective_message.reply_text,
                    context=context,
                    need_response=False,
                    skip_retry=False,
                    **reply_text_kwargs,
                )
            elif player.verbose:
                await send_private_message(
                    function_caller='DESTROY_DROP()',
                    context=context,
                    text=text,
                    user_id=user_id,
                    chat_id=chat_id,
                    close_by_owner=False,
                )
    else:
        answer_text = 'Este item não existe mais.'

    try:
        drops.pop(message_id, None)
        await answer(query=query, text=answer_text)
        await delete_message(
            function_caller='DESTROY_DROP()',
            context=context,
            query=query
        )
    except Exception as e:
        print('destroy_drop():', type(e), e)

    return ConversationHandler.END


@print_basic_infos
async def choice_sort_items(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    '''Selecionar como será ordenado os itens
    '''
    message = update.effective_message
    query = update.callback_query

    try:
        old_reply_markup = query.message.reply_markup
        await message_edit_reply_markup(
            function_caller='BAG.CHOICE_SORT_ITEMS()',
            message=message,
            context=context,
            need_response=True,
            reply_markup=None,
        )
    except Exception as e:
        print(type(e), e)
        return ConversationHandler.END

    user_id = update.effective_user.id
    data = callback_data_to_dict(query.data)
    page = data['page']
    data_user_id = data['user_id']
    target_id = data['target_id']

    if data_user_id != user_id:  # Não executa se outro usuário mexer na bolsa
        await answer(query=query, text=ACCESS_DENIED, show_alert=True)
        await message_edit_reply_markup(
            function_caller='BAG.CHOICE_SORT_ITEMS()',
            message=message,
            context=context,
            need_response=True,
            reply_markup=old_reply_markup,
        )

        return CHECK_ROUTES

    sort_buttons = get_sort_buttons(
        page=page,
        user_id=user_id,
        target_id=target_id,
    )
    back_button = get_back_button(
        page=page,
        user_id=user_id,
        target_id=target_id,
        retry_state=SORT_ROUTES
    )
    reply_markup = InlineKeyboardMarkup(
        sort_buttons + [back_button]
    )
    await message_edit_reply_markup(
        function_caller='BAG.CHOICE_SORT_ITEMS()',
        message=message,
        context=context,
        need_response=True,
        reply_markup=reply_markup,
    )

    return SORT_ROUTES


@print_basic_infos
async def sort_items(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    '''Ordena os itens da bolsa
    '''
    chat_id = update.effective_chat.id
    message_id = update.effective_message.message_id
    message = update.effective_message
    query = update.callback_query

    try:
        old_reply_markup = query.message.reply_markup
        await message_edit_reply_markup(
            function_caller='BAG.SORT_ITEMS()',
            message=message,
            context=context,
            need_response=True,
            reply_markup=None,
        )
    except Exception as e:
        print(type(e), e)
        return ConversationHandler.END

    bag_model = BagModel()
    user_id = update.effective_user.id
    data = callback_data_to_dict(query.data)
    page = data['page']
    data_user_id = data['user_id']
    target_id = data['target_id']
    sort = data['sort']

    if data_user_id != user_id:  # Não executa se outro usuário mexer na bolsa
        await answer(query=query, text=ACCESS_DENIED, show_alert=True)
        await message_edit_reply_markup(
            function_caller='BAG.SORT_ITEMS()',
            message=message,
            context=context,
            need_response=True,
            reply_markup=old_reply_markup,
        )

        return CHECK_ROUTES

    await answer(query=query, text='Ordenando itens...')

    player_bag: Bag = bag_model.get(query={'player_id': user_id})

    if sort == 'consumable_up':
        player_bag.sort_by_equip_type()
    elif sort == 'consumable_down':
        player_bag.sort_by_equip_type(False)
    elif sort == 'power_up':
        player_bag.sort_by_power()
    elif sort == 'power_down':
        player_bag.sort_by_power(False)
    elif sort == 'rarity_up':
        player_bag.sort_by_rarity()
    elif sort == 'rarity_down':
        player_bag.sort_by_rarity(False)

    bag_model.save(player_bag)

    back_button = get_back_button(
        page=0,
        user_id=user_id,
        target_id=target_id,
        retry_state=START_ROUTES
    )
    reply_markup = InlineKeyboardMarkup([back_button])
    new_text = 'Itens ordenados com sucesso!'
    await edit_message_text(
        function_caller='SORT_ITEMS()',
        new_text=new_text,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        need_response=False,
        markdown=False,
        reply_markup=reply_markup,
    )

    return START_ROUTES


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Apaga a mensagem quando o jogador dono da bolsa
    clica em Fechar A Bolsa.
    '''
    user_id = update.effective_user.id
    query = update.callback_query
    if query:
        data = callback_data_to_dict(query.data)
        data_user_id = data['user_id']
        target_id = data['target_id']

        # Não executa se outro usuário mexer na bolsa
        if data_user_id != user_id:
            await answer(query=query, text=ACCESS_DENIED, show_alert=True)
            return CHECK_ROUTES

        await answer(query=query, text='Fechando Bolsa...')
        await delete_message(
            function_caller='CANCEL_BAG()',
            context=context,
            query=query
        )

        return ConversationHandler.END

    return START_ROUTES


async def send_drop_message(
    context: ContextTypes.DEFAULT_TYPE,
    items: List[Item],
    text: str,
    update: Update = None,
    chat_id: int = None,
    message_id: int = None,
    silent: bool = False,
):
    if update is None and chat_id is None:
        raise ValueError('update ou chat_id são requeridos')
    if isinstance(items, Item):
        items = [items]
    for i, item in enumerate(items):
        drop = item.quantity
        take_break_buttons = get_take_break_buttons(drop, item)
        reply_markup_drop = InlineKeyboardMarkup([take_break_buttons])
        markdown_item_sheet = item.get_all_sheets(verbose=True, markdown=True)
        markdown_item_sheet = f'{text}:\n\n{markdown_item_sheet}'

        if isinstance(item.item, GemstoneConsumable):
            markdown_item_sheet = create_text_in_box(
                text=markdown_item_sheet,
                section_name=SECTION_TEXT_GEMSTONE,
                section_start=SECTION_HEAD_GEMSTONE_START,
                section_end=SECTION_HEAD_GEMSTONE_END,
            )
        elif isinstance(item.item, TrocadoPouchConsumable):
            markdown_item_sheet = create_text_in_box(
                text=markdown_item_sheet,
                section_name=SECTION_TEXT_TROCADO_POUCH,
                section_start=SECTION_HEAD_TROCADO_POUCH_START,
                section_end=SECTION_HEAD_TROCADO_POUCH_END,
            )
        elif isinstance(item.item, Consumable):
            markdown_item_sheet = create_text_in_box(
                text=markdown_item_sheet,
                section_name=SECTION_TEXT_CONSUMABLE,
                section_start=SECTION_HEAD_CONSUMABLE_START,
                section_end=SECTION_HEAD_CONSUMABLE_END,
            )
        elif isinstance(item.item, Equipment):
            markdown_item_sheet = create_text_in_box(
                text=markdown_item_sheet,
                section_name=SECTION_TEXT_EQUIPMENT,
                section_start=SECTION_HEAD_EQUIPMENT_START,
                section_end=SECTION_HEAD_EQUIPMENT_END,
            )

        remaining = len(items) - i
        if isinstance(update, Update):
            call_telegram_kwargs = dict(
                function=update.effective_message.reply_text,
            )
        else:
            call_telegram_kwargs = dict(
                function=context.bot.send_message,
                chat_id=chat_id,
                reply_to_message_id=message_id,
            )

        call_telegram_kwargs['text'] = markdown_item_sheet
        call_telegram_kwargs['parse_mode'] = ParseMode.MARKDOWN_V2
        call_telegram_kwargs['disable_notification'] = silent
        call_telegram_kwargs['allow_sending_without_reply'] = True
        call_telegram_kwargs['reply_markup'] = reply_markup_drop

        response = await call_telegram_message_function(
            function_caller=f'SEND_DROP_MESSAGE(remaining={remaining})',
            context=context,
            auto_delete_message=False,
            **call_telegram_kwargs
        )

        drops_message_id = response.message_id
        drops = context.chat_data.get(DROPS_CHAT_DATA_KEY, None)
        if isinstance(drops, dict):
            drops[drops_message_id] = True
        else:
            create_and_put_drop_dict(context, drops_message_id)

        context.job_queue.run_once(
            callback=job_timeout_drop,
            when=timedelta(minutes=MINUTES_TO_TIMEOUT_DROP),
            data={'message_id': drops_message_id},
            name=f'JOB_TIMEOUT_DROP_{ObjectId()}',
            chat_id=context._chat_id,
            job_kwargs=BASE_JOB_KWARGS,
        )
        sleep(1)


def create_and_put_drop_dict(
    context: ContextTypes.DEFAULT_TYPE,
    drops_message_id: int = None
):
    '''Cria o dicionário de DROPS que indica quais items dropados ainda podem 
    ser pegos'''
    drop_dict = {drops_message_id: True} if drops_message_id else {}
    context.chat_data[DROPS_CHAT_DATA_KEY] = drop_dict


async def job_timeout_drop(context: ContextTypes.DEFAULT_TYPE):
    '''Job que exclui a mensagem do Drop e retira no dicionário o 
    ID do mesmo após um tempo pré determinado.
    '''

    print('JOB_TIMEOUT_DROP()')
    job = context.job
    data = job.data
    message_id = data['message_id']
    drops = context.chat_data.get(DROPS_CHAT_DATA_KEY)
    drops.pop(message_id, None)

    await delete_message_from_context(
        function_caller='JOB_TIMEOUT_DROP()',
        context=context,
        message_id=message_id
    )


def get_trocado_and_target_text(user_id: int, target_id: int) -> str:
    trocado = get_player_trocado(user_id)
    target_name = get_player_name(target_id)
    text = (
        f'*{TrocadoEnum.TROCADO.value}*: {trocado}{EmojiEnum.TROCADO.value}\n'
        f'*Alvo*: {target_name}\n\n'
    )

    return text


def get_bonus_price(
    price: int,
    user_id: int = None,
    player_character: BaseCharacter = None
) -> int:
    if user_id is None and player_character is None:
        raise ValueError('user_id or player_character precisa ser definido.')
    if player_character is None:
        char_model = CharacterModel()
        player_character: BaseCharacter = char_model.get(user_id)

    charisma = player_character.bs.charisma
    charisma_price_bonus = (sqrt(charisma) / 100) + 1
    final_price = price * charisma_price_bonus

    return int(final_price)


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

    return markdown_text


def get_item_buttons(
    items: List[Item],
    page: int,
    user_id: int,
    target_id: int
) -> List[List[InlineKeyboardButton]]:

    items_buttons = []
    # Criando texto e botões dos itens
    for index, _ in enumerate(items):
        items_buttons.append(InlineKeyboardButton(
            text=f'I{index + 1:02}',
            callback_data=callback_data_to_string({
                'item': index,
                'page': page,
                'user_id': user_id,
                'target_id': target_id
            })
        ))

    reshaped_items_buttons = reshape_row_buttons(
        buttons=items_buttons,
        buttons_per_row=5
    )

    return reshaped_items_buttons


def get_navigation_buttons(
    have_back_page: bool,
    have_next_page: bool,
    page: int,
    user_id: int,
    target_id: int
) -> List[InlineKeyboardButton]:

    navigation_keyboard = []
    if have_back_page:  # Cria botão de Voltar Página
        navigation_keyboard.append(
            InlineKeyboardButton(
                text=NAV_PREVIOUS_BUTTON_TEXT,
                callback_data=callback_data_to_string({
                    'page': (page - 1),
                    'user_id': user_id,
                    'target_id': target_id
                })
            )
        )
    if have_next_page:  # Cria botão de Avançar Página
        navigation_keyboard.append(
            InlineKeyboardButton(
                text=NAV_NEXT_BUTTON_TEXT,
                callback_data=callback_data_to_string({
                    'page': (page + 1),
                    'user_id': user_id,
                    'target_id': target_id
                })
            )
        )

    return navigation_keyboard


def get_extremes_navigation_buttons(
    have_back_page: bool,
    have_next_page: bool,
    user_id: int,
    target_id: int
) -> List[InlineKeyboardButton]:

    extremes_navigation_keyboard = []
    if have_back_page:  # Cria botão para a Primeira Página
        extremes_navigation_keyboard.append(
            InlineKeyboardButton(
                text=NAV_START_BUTTON_TEXT,
                callback_data=callback_data_to_string({
                    'page': 0,
                    'user_id': user_id,
                    'target_id': target_id
                })
            )
        )
    if have_next_page:  # Cria botão para a Última Página
        bag_model = BagModel()
        bag_length = bag_model.length('items_ids', user_id)
        total_pages = (bag_length - 1) // ITEMS_PER_PAGE
        total_pages = max(total_pages, 0)  # Evita números negativos
        extremes_navigation_keyboard.append(
            InlineKeyboardButton(
                text=NAV_END_BUTTON_TEXT,
                callback_data=callback_data_to_string({
                    'page': total_pages,
                    'user_id': user_id,
                    'target_id': target_id
                })
            )
        )

    return extremes_navigation_keyboard


def get_navigation_item_buttons(
    page: int,
    user_id: int,
    target_id: int,
    item_pos: int,
    quantity: int = None,
) -> List[InlineKeyboardButton]:
    navigation_item_buttons = []
    have_next_item = exist_item_in_bag_by_position(
        user_id=user_id,
        page=page,
        item_pos=item_pos + 1
    )

    if item_pos > 0 or page > 0:
        back_item_pos = (item_pos - 1)
        back_page, back_item_pos = get_page_and_item_pos(page, back_item_pos)
        navigation_item_buttons.append(
            InlineKeyboardButton(
                text=NAV_PREVIOUS_ITEM_BUTTON_TEXT,
                callback_data=callback_data_to_string({
                    'item': back_item_pos,
                    'page': back_page,
                    'user_id': user_id,
                    'target_id': target_id
                })
            )
        )

    if have_next_item:
        fwd_item_pos = (item_pos + 1)
        fwd_page = page
        fwd_page, fwd_item_pos = get_page_and_item_pos(page, fwd_item_pos)
        if quantity <= 0:
            fwd_item_pos = item_pos
            fwd_page = page
        navigation_item_buttons.append(
            InlineKeyboardButton(
                text=NAV_NEXT_ITEM_BUTTON_TEXT,
                callback_data=callback_data_to_string({
                    'item': fwd_item_pos,
                    'page': fwd_page,
                    'user_id': user_id,
                    'target_id': target_id
                })
            )
        )

    return navigation_item_buttons


def get_use_consumable_buttons(
    page: int,
    user_id: int,
    target_id: int,
    item_pos: int,
    item: Item
) -> List[InlineKeyboardButton]:
    use_buttons = []
    quantity = item.quantity
    if item.item.usable is True:
        for quantity_option in DROPUSE_QUANTITY_OPTION_LIST:
            if quantity_option <= quantity:
                if quantity < VERBOSE_BUTTONS_THRESHOLD:
                    text = USE_MANY_BUTTON_VERBOSE_TEXT.format(
                        quantity_option=f'{quantity_option:02}'
                    )
                else:
                    text = USE_MANY_BUTTON_TEXT.format(
                        quantity_option=f'{quantity_option:02}'
                    )
                use_buttons.append(
                    InlineKeyboardButton(
                        text=text,
                        callback_data=callback_data_to_string({
                            'use': quantity_option,
                            'item': item_pos,
                            'page': page,
                            'user_id': user_id,
                            'target_id': target_id
                        })
                    )
                )

    buttons_per_row = 4 if len(use_buttons) <= 4 else 3
    return reshape_row_buttons(
        buttons=use_buttons,
        buttons_per_row=buttons_per_row
    )


def get_discard_buttons(
    page: int,
    user_id: int,
    target_id: int,
    item_pos: int,
    item: Item
) -> List[InlineKeyboardButton]:
    drop_buttons = []
    quantity = item.quantity
    for quantity_option in DROPUSE_QUANTITY_OPTION_LIST:
        if quantity_option <= quantity:
            if quantity < VERBOSE_BUTTONS_THRESHOLD:
                text = DISCARD_MANY_BUTTON_VERBOSE_TEXT.format(
                    quantity_option=f'{quantity_option:02}'
                )
            else:
                text = DISCARD_MANY_BUTTON_TEXT.format(
                    quantity_option=f'{quantity_option:02}'
                )
            drop_buttons.append(
                InlineKeyboardButton(
                    text=text,
                    callback_data=callback_data_to_string({
                        'drop': quantity_option,
                        'item': item_pos,
                        'page': page,
                        'user_id': user_id,
                        'target_id': target_id
                    })
                )
            )

    buttons_per_row = 4 if len(drop_buttons) <= 4 else 3
    return reshape_row_buttons(
        buttons=drop_buttons,
        buttons_per_row=buttons_per_row
    )


def get_sell_buttons(
    page: int,
    user_id: int,
    target_id: int,
    item_pos: int,
    item: Item
) -> List[InlineKeyboardButton]:
    sell_buttons = []
    quantity = item.quantity
    for quantity_option in DROPUSE_QUANTITY_OPTION_LIST:
        if quantity_option <= quantity:
            if isinstance(item.item, TrocadoPouchConsumable):
                if quantity < VERBOSE_BUTTONS_THRESHOLD:
                    text = COLLECT_MANY_BUTTON_VERBOSE_TEXT.format(
                        quantity_option=f'{quantity_option:02}'
                    )
                else:
                    text = COLLECT_MANY_BUTTON_TEXT.format(
                        quantity_option=f'{quantity_option:02}'
                    )
            else:
                if quantity < VERBOSE_BUTTONS_THRESHOLD:
                    text = SELL_MANY_BUTTON_VERBOSE_TEXT.format(
                        quantity_option=f'{quantity_option:02}'
                    )
                else:
                    text = SELL_MANY_BUTTON_TEXT.format(
                        quantity_option=f'{quantity_option:02}'
                    )
            sell_buttons.append(
                InlineKeyboardButton(
                    text=text,
                    callback_data=callback_data_to_string({
                        'sell': quantity_option,
                        'item': item_pos,
                        'page': page,
                        'user_id': user_id,
                        'target_id': target_id
                    })
                )
            )

    if all((
        quantity > 0,
        quantity not in DROPUSE_QUANTITY_OPTION_LIST,
        isinstance(item.item, TrocadoPouchConsumable)
    )):
        if quantity < VERBOSE_BUTTONS_THRESHOLD:
            text = COLLECT_MANY_BUTTON_VERBOSE_TEXT.format(
                quantity_option=f'{quantity:02}'
            )
        else:
            text = COLLECT_MANY_BUTTON_TEXT.format(
                quantity_option=f'{quantity:02}'
            )
        sell_buttons.append(
            InlineKeyboardButton(
                text=text,
                callback_data=callback_data_to_string({
                    'sell': quantity,
                    'item': item_pos,
                    'page': page,
                    'user_id': user_id,
                    'target_id': target_id
                })
            )
        )

    buttons_per_row = 4 if len(sell_buttons) <= 4 else 3
    return reshape_row_buttons(
        buttons=sell_buttons,
        buttons_per_row=buttons_per_row
    )


def get_close_bag_button(
    user_id: int,
    target_id: int
) -> List[InlineKeyboardButton]:
    return [
        InlineKeyboardButton(
            text=CLOSE_BAG_BUTTON_TEXT,
            callback_data=callback_data_to_string({
                'command': CALLBACK_CLOSE_BAG,
                'user_id': user_id,
                'target_id': target_id
            })
        )]


def get_back_button(
    page: int,
    user_id: int,
    target_id: int,
    retry_state: int
) -> List[InlineKeyboardButton]:
    return [
        InlineKeyboardButton(
            text=NAV_BACK_BUTTON_TEXT,
            callback_data=callback_data_to_string({
                'page': page,
                'user_id': user_id,
                'target_id': target_id,
                'retry_state': retry_state
            })
        )
    ]


def get_take_break_buttons(
    drop: int,
    item: Item,
) -> List[InlineKeyboardButton]:
    item_id = str(item._id)
    destroy_text = DESTROY_ITEM_BUTTON_TEXT
    if isinstance(item.item, Equipment):
        destroy_text = TRANSMUTE_ITEM_BUTTON_TEXT
    return [
        InlineKeyboardButton(
            text=TAKE_BUTTON_TEXT,
            callback_data=callback_data_to_string({
                '_id': item_id,
                'drop': drop
            })
        ),
        InlineKeyboardButton(
            text=destroy_text,
            callback_data=callback_data_to_string({
                'act': CALLBACK_TEXT_DESTROY_ITEM,
                '_id': item_id
            })
        )]


def get_sort_button(
    page: int,
    user_id: int,
    target_id: int
) -> List[InlineKeyboardButton]:
    return [
        InlineKeyboardButton(
            text=SORT_ITEMS_BUTTON_TEXT,
            callback_data=callback_data_to_string({
                'command': CALLBACK_TEXT_SORT_ITEMS,
                'page': page,
                'user_id': user_id,
                'target_id': target_id
            })
        )]


def get_sort_buttons(
    page: int,
    user_id: str,
    target_id: int
) -> List[List[InlineKeyboardButton]]:

    return [
        [
            InlineKeyboardButton(
                text=CONSUMABLE_SORT_UP_BUTTON_TEXT,
                callback_data=callback_data_to_string({
                    'sort': 'consumable_up',
                    'page': page,
                    'user_id': user_id,
                    'target_id': target_id
                })
            ),
            InlineKeyboardButton(
                text=CONSUMABLE_SORT_DOWN_BUTTON_TEXT,
                callback_data=callback_data_to_string({
                    'sort': 'consumable_down',
                    'page': page,
                    'user_id': user_id,
                    'target_id': target_id
                })
            ),
        ],
        [
            InlineKeyboardButton(
                text=EQUIPMENT_POWER_SORT_UP_BUTTON_TEXT,
                callback_data=callback_data_to_string({
                    'sort': 'power_up',
                    'page': page,
                    'user_id': user_id,
                    'target_id': target_id
                })
            ),
            InlineKeyboardButton(
                text=EQUIPMENT_POWER_SORT_DOWN_BUTTON_TEXT,
                callback_data=callback_data_to_string({
                    'sort': 'power_down',
                    'page': page,
                    'user_id': user_id,
                    'target_id': target_id
                })
            ),
        ],
        [
            InlineKeyboardButton(
                text=EQUIPMENT_RARITY_SORT_UP_BUTTON_TEXT,
                callback_data=callback_data_to_string({
                    'sort': 'rarity_up',
                    'page': page,
                    'user_id': user_id,
                    'target_id': target_id
                })
            ),
            InlineKeyboardButton(
                text=EQUIPMENT_RARITY_SORT_DOWN_BUTTON_TEXT,
                callback_data=callback_data_to_string({
                    'sort': 'rarity_down',
                    'page': page,
                    'user_id': user_id,
                    'target_id': target_id
                })
            ),
        ]
    ]


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
        START_ROUTES: [
            CallbackQueryHandler(start, pattern=PATTERN_PAGE),
            CallbackQueryHandler(check_item, pattern=PATTERN_ITEM),
        ],
        CHECK_ROUTES: [
            CallbackQueryHandler(start, pattern=PATTERN_PAGE),
            CallbackQueryHandler(check_item, pattern=PATTERN_ITEM),
            CallbackQueryHandler(
                choice_sort_items,
                pattern=PATTERN_SORT_ITEMS
            ),
            CallbackQueryHandler(
                cancel, pattern=PATTERN_CLOSE_BAG
            ),
        ],
        USE_ROUTES: [
            CallbackQueryHandler(start, pattern=PATTERN_PAGE),
            CallbackQueryHandler(check_item, pattern=PATTERN_ITEM),
            CallbackQueryHandler(use_item, pattern=PATTERN_USE),
            CallbackQueryHandler(drop_item, pattern=PATTERN_DROP),
            CallbackQueryHandler(sell_item, pattern=PATTERN_SELL),
            CallbackQueryHandler(identify_item, pattern=PATTERN_IDENTIFY),
            CallbackQueryHandler(check_item, pattern=PATTERN_EQUIP_INFO),
        ],
        SORT_ROUTES: [
            CallbackQueryHandler(start, pattern=PATTERN_PAGE),
            CallbackQueryHandler(sort_items, pattern=PATTERN_SORT),
        ]
    },
    fallbacks=[
        CommandHandler(CANCEL_COMMANDS, cancel)
    ],
    allow_reentry=True,
    conversation_timeout=TEN_MINUTES_IN_SECONDS,
)
DROP_HANDLERS = [
    CallbackQueryHandler(
        get_drop, pattern=PATTERN_GET_DROP
    ),
    CallbackQueryHandler(
        destroy_drop, pattern=PATTERN_DESTROY_ITEM,
    )
]
