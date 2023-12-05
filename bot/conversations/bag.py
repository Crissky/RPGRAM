from itertools import zip_longest
from typing import List

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    ContextTypes,
    PrefixHandler,
)

from bot.constants.bag import (
    ACCESS_DENIED,
    CALLBACK_CLOSE_BAG,
    CALLBACK_TEXT_DESTROY_ITEM,
    CALLBACK_TEXT_SORT_ITEMS,
    CANCEL_COMMANDS,
    CLOSE_BAG_BUTTON_TEXT,
    COMMANDS,
    CONSUMABLE_SORT_DOWN_BUTTON_TEXT,
    CONSUMABLE_SORT_UP_BUTTON_TEXT,
    DESTROY_ITEM_BUTTON_TEXT,
    DISCARD_MANY_BUTTON_TEXT,
    EQUIP_BUTTON_TEXT,
    EQUIPMENT_POWER_SORT_DOWN_BUTTON_TEXT,
    EQUIPMENT_POWER_SORT_UP_BUTTON_TEXT,
    EQUIPMENT_RARITY_SORT_DOWN_BUTTON_TEXT,
    EQUIPMENT_RARITY_SORT_UP_BUTTON_TEXT,
    ESCAPED_CALLBACK_TEXT_DESTROY_ITEM,
    ESCAPED_CALLBACK_TEXT_SORT_ITEMS,
    IDENTIFY_BUTTON_TEXT,
    ITEMS_PER_PAGE,
    EQUIP_LEFT_BUTTON_TEXT,
    NAV_BACK_BUTTON_TEXT,
    NAV_PREVIOUS_BUTTON_TEXT,
    NAV_END_BUTTON_TEXT,
    NAV_NEXT_BUTTON_TEXT,
    NAV_START_BUTTON_TEXT,
    SORT_ITEMS_BUTTON_TEXT,
    TAKE_BUTTON_TEXT,
    DROPUSE_MANY_MAX,
    EQUIP_RIGHT_BUTTON_TEXT,
    DROPUSE_QUANTITY_OPTION_LIST,
    USE_MANY_BUTTON_TEXT
)

from bot.constants.filters import (
    BASIC_COMMAND_FILTER,
    PREFIX_COMMANDS
)
from bot.decorators import (
    need_not_in_battle,
    print_basic_infos,
    retry_after,
    skip_if_dead_char,
    skip_if_no_have_char,
    skip_if_no_singup_player,
    skip_if_immobilized,
    confusion,
)
from bot.functions.bag import (
    get_identifying_lens,
    get_item_by_position,
    have_identifying_lens,
    sub_identifying_lens
)
from bot.functions.char import save_char
from bot.functions.general import get_attribute_group_or_player
from bot.functions.keyboard import remove_buttons_by_text, reshape_row_buttons
from constant.text import TITLE_HEAD
from constant.time import TEN_MINUTES_IN_SECONDS
from repository.mongo import BagModel, CharacterModel, EquipsModel, ItemModel
from rpgram import Bag, Item
from rpgram.boosters import Equipment
from rpgram.consumables import Consumable
from rpgram.enums import EmojiEnum, EquipmentEnum


# ROUTES
(
    START_ROUTES,
    CHECK_ROUTES,
    USE_ROUTES,
    SORT_ROUTES,
) = range(4)


@skip_if_dead_char
# @skip_if_immobilized
@confusion(START_ROUTES)
@skip_if_no_singup_player
@skip_if_no_have_char
@need_not_in_battle
@print_basic_infos
@retry_after
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Envia ou edita mensagem contendo uma página dos itens do jogador
    '''
    await update.effective_message.reply_chat_action(ChatAction.TYPING)
    bag_model = BagModel()
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_name = update.effective_user.name
    query = update.callback_query
    silent = get_attribute_group_or_player(chat_id, 'silent')

    page = 0
    if query:
        data = eval(query.data)
        page = data['page']  # starts zero
        data_user_id = data['user_id']
        retry_state = data.get('retry_state', None)

        # Não executa se outro usuário mexer na bolsa
        if data_user_id != user_id:
            await query.answer(text=ACCESS_DENIED, show_alert=True)
            return retry_state

    skip_slice = ITEMS_PER_PAGE * page
    size_slice = ITEMS_PER_PAGE + 1

    player_bag = bag_model.get(
        query={'player_id': user_id},
        fields={'items_ids': {'$slice': [skip_slice, size_slice]}},
        partial=False
    )
    if not player_bag:  # Cria uma bolsa caso o jogador não tenha uma.
        player_bag = Bag(
            items=[],
            player_id=user_id
        )
        bag_model.save(player_bag)

    markdown_text = (
        f'\n*Bolsa de {user_name}* — {EmojiEnum.PAGE.value}: {page + 1:02}\n\n'
    )

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

    # Criando os Botões
    markdown_text += get_item_texts(items=items)
    reshaped_items_buttons = get_item_buttons(
        items=items, page=page, user_id=user_id
    )

    navigation_keyboard = get_navigation_buttons(
        have_back_page=have_back_page,
        have_next_page=have_next_page,
        page=page,
        user_id=user_id
    )
    extremes_navigation_keyboard = get_extremes_navigation_buttons(
        have_back_page=have_back_page,
        have_next_page=have_next_page,
        user_id=user_id
    )

    sort_items_button = get_sort_button(page=page, user_id=user_id)
    cancel_button = get_close_bag_button(user_id=user_id)
    reply_markup = InlineKeyboardMarkup(
        reshaped_items_buttons +
        [navigation_keyboard] +
        [extremes_navigation_keyboard] +
        [sort_items_button + cancel_button]
    )

    markdown_text = TITLE_HEAD.format(markdown_text)
    if not query:  # Envia Resposta com o texto da tabela de itens e botões
        await update.effective_message.reply_text(
            text=markdown_text,
            disable_notification=silent,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    else:  # Edita Resposta com o texto da tabela de itens e botões
        await query.edit_message_text(
            text=markdown_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN_V2
        )

    return CHECK_ROUTES


@retry_after
async def check_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Edita a mensagem com as informações do item escolhido.
    '''
    query = update.callback_query

    try:
        old_reply_markup = query.message.reply_markup
        await query.edit_message_reply_markup()
    except Exception as e:
        print(type(e), e)
        return ConversationHandler.END

    equips_model = EquipsModel()
    user_id = update.effective_user.id
    data = eval(query.data)
    item_pos = data['item']
    page = data['page']
    data_user_id = data['user_id']

    if data_user_id != user_id:  # Não executa se outro usuário mexer na bolsa
        await query.answer(text=ACCESS_DENIED, show_alert=True)
        await query.edit_message_reply_markup(reply_markup=old_reply_markup)
        return CHECK_ROUTES

    item = get_item_by_position(user_id, page, item_pos)
    markdown_text = item.get_all_sheets(
        verbose=True,
        markdown=True,
        show_quantity=True
    )
    equip_buttons = []
    use_buttons = [[]]
    identify_button = []
    if isinstance(item.item, Equipment):
        equips = equips_model.get(user_id)
        markdown_text = equips.compare(item.item)
        if item.item.equip_type == EquipmentEnum.ONE_HAND:
            equip_buttons = [
                InlineKeyboardButton(
                    text=EQUIP_LEFT_BUTTON_TEXT,
                    callback_data=(
                        f'{{"use":1,"item":{item_pos},"hand":"L",'
                        f'"page":{page},"user_id":{user_id}}}'
                    )
                ),
                InlineKeyboardButton(
                    text=EQUIP_RIGHT_BUTTON_TEXT,
                    callback_data=(
                        f'{{"use":1,"item":{item_pos},"hand":"R",'
                        f'"page":{page},"user_id":{user_id}}}'
                    )
                )
            ]
        else:
            equip_buttons = [
                InlineKeyboardButton(
                    text=EQUIP_BUTTON_TEXT,
                    callback_data=(
                        f'{{"use":1,"item":{item_pos},'
                        f'"page":{page},"user_id":{user_id}}}'
                    )
                )
            ]

        if have_identifying_lens(user_id) and item.item.identifiable:
            identify_button = [
                InlineKeyboardButton(
                    text=IDENTIFY_BUTTON_TEXT,
                    callback_data=(
                        f'{{"identify":1,"item":{item_pos},'
                        f'"page":{page},"user_id":{user_id}}}'
                    )
                )
            ]
    elif isinstance(item.item, Consumable):
        use_buttons = get_use_consumable_buttons(
            page=page, user_id=user_id, item_pos=item_pos, item=item
        )

    discard_buttons = get_discard_buttons(
        page=page, user_id=user_id, item_pos=item_pos, item=item
    )
    back_button = get_back_button(
        page=page, user_id=user_id, retry_state=USE_ROUTES
    )
    reply_markup = InlineKeyboardMarkup([
        equip_buttons,
        *use_buttons,
        identify_button,
        *discard_buttons,
        back_button
    ])
    # Edita mensagem com as informações do item escolhido
    await query.edit_message_text(
        text=markdown_text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN_V2
    )
    return USE_ROUTES


@skip_if_dead_char
# @skip_if_immobilized
@confusion(USE_ROUTES)
@print_basic_infos
@retry_after
async def use_item(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Usa ou equipa o item do jogador.
    '''
    query = update.callback_query

    try:
        old_reply_markup = query.message.reply_markup
        await query.edit_message_reply_markup()
    except Exception as e:
        print(type(e), e)
        return ConversationHandler.END

    bag_model = BagModel()
    char_model = CharacterModel()
    user_id = update.effective_user.id
    data = eval(query.data)
    item_pos = data['item']
    page = data['page']
    data_user_id = data['user_id']
    use_quantity = data['use']
    hand = data.get('hand', None)

    if data_user_id != user_id:  # Não executa se outro usuário mexer na bolsa
        await query.answer(text=ACCESS_DENIED, show_alert=True)
        await query.edit_message_reply_markup(reply_markup=old_reply_markup)
        return USE_ROUTES

    item = get_item_by_position(user_id, page, item_pos)
    player_character = char_model.get(user_id)

    old_equipments = []
    if isinstance(item.item, Equipment):  # Tenta equipar o item
        equipment = item.item
        try:
            old_equipments = player_character.equips.equip(equipment, hand)
            await query.answer(text=f'Você equipou "{equipment.name}".')
        except Exception as error:
            print(error)
            await query.answer(
                text=(f'{error}'),
                show_alert=True
            )
            await query.edit_message_reply_markup(
                reply_markup=old_reply_markup
            )
            return USE_ROUTES
    elif isinstance(item.item, Consumable):  # Tenta usar o item
        # consumable = item.item
        name = item.name
        description = item.item.description
        use_quantity = min(item.quantity, use_quantity)
        try:
            for _ in range(use_quantity):
                report = item.use(player_character)
                report_text = report['text']
                bag_model.sub(item, user_id)
            text = (
                f'Você usou {use_quantity} "{name}".\n'
                f'Descrição: "{description}".\n\n'
                f'{report_text}\n'
            )
            save_char(player_character, status=True)

            await query.answer(
                text=text,
                show_alert=True
            )
        except Exception as error:
            print(error)
            await query.answer(
                text=(
                    f'Item "{name}" não pode ser usado.\n\n{error}'
                ),
                show_alert=True
            )
        finally:
            markdown_text = item.get_all_sheets(
                verbose=True,
                markdown=True,
                show_quantity=True
            )
            if item.quantity <= 0:
                back_button = get_back_button(
                    page=page, user_id=user_id, retry_state=USE_ROUTES
                )
                reply_markup = InlineKeyboardMarkup([back_button])
            else:
                use_buttons = get_use_consumable_buttons(
                    page=page,
                    user_id=user_id,
                    item_pos=item_pos,
                    item=item
                )
                discard_buttons = get_discard_buttons(
                    page=page,
                    user_id=user_id,
                    item_pos=item_pos,
                    item=item
                )
                back_button = get_back_button(
                    page=page,
                    user_id=user_id,
                    retry_state=USE_ROUTES
                )
                reply_markup = InlineKeyboardMarkup([
                    *use_buttons,
                    *discard_buttons,
                    back_button
                ])
            await query.edit_message_text(
                text=markdown_text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN_V2
            )
            return USE_ROUTES

    markdown_player_sheet = player_character.get_all_sheets(
        verbose=False, markdown=True
    )

    bag_model.sub(item, user_id)
    # Adiciona na bolsa os equipamentos que já estavam equipados
    # e que foram substituídos
    for old_equipment in old_equipments:
        old_equipment_item = Item(old_equipment)
        bag_model.add(old_equipment_item, user_id)

    save_char(player_character, equips=True)

    back_button = get_back_button(
        page=page, user_id=user_id, retry_state=START_ROUTES
    )
    reply_markup = InlineKeyboardMarkup([back_button])
    # Edita mensagem com as informações do personagem do jogador
    await query.edit_message_text(
        text=markdown_player_sheet,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN_V2
    )

    return START_ROUTES


@skip_if_dead_char
# @skip_if_immobilized
@confusion(USE_ROUTES)
@print_basic_infos
@retry_after
async def identify_item(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    '''identifica um equipamento.
    '''
    query = update.callback_query

    try:
        old_reply_markup = query.message.reply_markup
        await query.edit_message_reply_markup()
    except Exception as e:
        print(type(e), e)
        return ConversationHandler.END

    bag_model = BagModel()
    item_model = ItemModel()
    equips_model = EquipsModel()
    user_id = update.effective_user.id
    data = eval(query.data)
    item_pos = data['item']
    page = data['page']
    data_user_id = data['user_id']
    use_quantity = data['identify']

    if data_user_id != user_id:  # Não executa se outro usuário mexer na bolsa
        await query.answer(text=ACCESS_DENIED, show_alert=True)
        await query.edit_message_reply_markup(reply_markup=old_reply_markup)
        return USE_ROUTES

    item_equipment = get_item_by_position(user_id, page, item_pos)
    equipment = item_equipment.item
    if have_identifying_lens(user_id):
        consumable_identifier = get_identifying_lens()
        report = consumable_identifier.use(equipment)
        report_text = report['text']
        item_model.save(equipment)
        sub_identifying_lens(user_id)
        name = consumable_identifier.name
        description = consumable_identifier.description
        text = (
            f'Você usou {use_quantity} "{name}".\n'
            f'Descrição: "{description}".\n\n'
            f'{report_text}\n'
        )
        await query.answer(text=text, show_alert=True)
    else:
        text = '⛔VOCÊ NÃO TEM UM ITEM DE IDENTIFICAÇÃO⛔'
        await query.answer(text=text, show_alert=True)

    equips = equips_model.get(user_id)
    markdown_text = equips.compare(equipment)
    reply_markup = remove_buttons_by_text(
        old_reply_markup,
        IDENTIFY_BUTTON_TEXT
    )
    await query.edit_message_text(
        text=markdown_text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN_V2
    )

    return USE_ROUTES


@skip_if_dead_char
# @skip_if_immobilized
@confusion(USE_ROUTES)
@print_basic_infos
@retry_after
async def drop_item(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    '''drop o item do jogador.
    '''
    query = update.callback_query

    try:
        old_reply_markup = query.message.reply_markup
        await query.edit_message_reply_markup()
    except Exception as e:
        print(type(e), e)
        return ConversationHandler.END

    bag_model = BagModel()
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_name = update.effective_user.name
    data = eval(query.data)
    item_pos = data['item']
    page = data['page']
    data_user_id = data['user_id']
    drop = data['drop']
    silent = get_attribute_group_or_player(chat_id, 'silent')

    if data_user_id != user_id:  # Não executa se outro usuário mexer na bolsa
        await query.answer(text=ACCESS_DENIED, show_alert=True)
        await query.edit_message_reply_markup(reply_markup=old_reply_markup)
        return USE_ROUTES

    item = get_item_by_position(user_id, page, item_pos)
    drop = min(drop, item.quantity)
    markdown_item_sheet = item.get_all_sheets(verbose=True, markdown=True)

    bag_model.sub(item, user_id, quantity=-(drop))

    back_button = get_back_button(
        page=page, user_id=user_id, retry_state=START_ROUTES
    )
    reply_markup = InlineKeyboardMarkup([back_button])
    await query.edit_message_text(
        text=f'Você dropou o item "{drop}x {item.name}"\.',
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN_V2
    )

    # Envia mensagem de drop do item, se ele foi dropado no grupo
    if chat_id != user_id:
        item_id = str(item._id)
        take_break_buttons = get_take_break_buttons(drop, item_id)
        reply_markup_drop = InlineKeyboardMarkup([
            take_break_buttons
        ])
        response = await update.effective_message.reply_text(
            text=f'{user_name} dropou o item:\n\n{markdown_item_sheet}',
            disable_notification=silent,
            reply_markup=reply_markup_drop,
            parse_mode=ParseMode.MARKDOWN_V2
        )
        message_id = response.message_id
        drops = context.chat_data.get('drops', None)
        if isinstance(drops, dict):
            drops[message_id] = True
        else:
            context.chat_data['drops'] = {message_id: True}

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
    if 'drops' in context.chat_data:
        drops = context.chat_data['drops']
        if drops.get(message_id, None) is not True:
            drops.pop(message_id, None)
            await query.answer(f'Este item não existe mais.', show_alert=True)
            await query.delete_message()

            return ConversationHandler.END

    try:
        await query.edit_message_reply_markup()
    except Exception as e:
        print(type(e), e)
        return ConversationHandler.END

    bag_model = BagModel()
    item_model = ItemModel()
    user_id = update.effective_user.id
    data = eval(query.data)
    item_id = data['_id']
    drop = data['drop']

    item = item_model.get(item_id)
    if item:
        item = Item(item, quantity=drop)
        bag_model.add(item, user_id)

        await query.answer(
            f'Você pegou "{drop}x {item.name}".',
            show_alert=True
        )
    else:
        print(
            f'get_drop() - Item não existe mais: _id: {item_id} item: {item}.'
        )
        await query.answer(
            f'Este item não existe mais.',
            show_alert=True
        )

    drops.pop(message_id, None)
    await query.delete_message()

    return ConversationHandler.END


@skip_if_dead_char
@skip_if_immobilized
@confusion()
@print_basic_infos
async def destroy_drop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Quebra o item dropado
    '''
    query = update.callback_query
    message_id = update.effective_message.message_id
    drops = context.chat_data.get('drops', {})

    try:
        drops.pop(message_id, None)
        await query.answer('Quebrando o item...', show_alert=True)
        await query.delete_message()
    except Exception as e:
        print('destroy_drop():', type(e), e)

    return ConversationHandler.END


@print_basic_infos
async def choice_sort_items(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    '''Selecionar como será ordenado os itens
    '''
    query = update.callback_query

    try:
        old_reply_markup = query.message.reply_markup
        await query.edit_message_reply_markup()
    except Exception as e:
        print(type(e), e)
        return ConversationHandler.END

    user_id = update.effective_user.id
    data = eval(query.data)
    page = data['page']
    data_user_id = data['user_id']

    if data_user_id != user_id:  # Não executa se outro usuário mexer na bolsa
        await query.answer(text=ACCESS_DENIED, show_alert=True)
        await query.edit_message_reply_markup(reply_markup=old_reply_markup)
        return CHECK_ROUTES

    sort_buttons = get_sort_buttons(page=page, user_id=user_id)
    back_button = get_back_button(
        page=page, user_id=user_id, retry_state=SORT_ROUTES
    )
    reply_markup = InlineKeyboardMarkup(
        sort_buttons + [back_button]
    )
    await query.edit_message_reply_markup(reply_markup)
    return SORT_ROUTES


@print_basic_infos
async def sort_items(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    '''Ordena os itens da bolsa
    '''
    query = update.callback_query

    try:
        old_reply_markup = query.message.reply_markup
        await query.edit_message_reply_markup()
    except Exception as e:
        print(type(e), e)
        return ConversationHandler.END

    bag_model = BagModel()
    user_id = update.effective_user.id
    data = eval(query.data)
    page = data['page']
    data_user_id = data['user_id']
    sort = data['sort']

    if data_user_id != user_id:  # Não executa se outro usuário mexer na bolsa
        await query.answer(text=ACCESS_DENIED, show_alert=True)
        await query.edit_message_reply_markup(reply_markup=old_reply_markup)
        return CHECK_ROUTES

    await query.answer(text='Ordenando itens...')

    player_bag = bag_model.get(query={'player_id': user_id})

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
        page=0, user_id=user_id, retry_state=START_ROUTES
    )
    reply_markup = InlineKeyboardMarkup([back_button])
    await query.edit_message_text(
        text='Itens ordenados com sucesso!',
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
        data = eval(query.data)
        data_user_id = data['user_id']

        # Não executa se outro usuário mexer na bolsa
        if data_user_id != user_id:
            await query.answer(text=ACCESS_DENIED, show_alert=True)
            return CHECK_ROUTES

        await query.answer('Fechando Bolsa...')
        await query.delete_message()

        return ConversationHandler.END

    return START_ROUTES


def get_item_texts(items: List[Item]) -> str:
    markdown_text = ''
    for index, item in enumerate(items):
        markdown_text += f'*Ⅰ{(index + 1):02}:* '
        markdown_text += item.get_sheet(verbose=True, markdown=True)

    return markdown_text


def get_item_buttons(
    items: List[Item], page: int, user_id: int
) -> List[List[InlineKeyboardButton]]:

    items_buttons = []
    # Criando texto e botões dos itens
    for index, _ in enumerate(items):
        items_buttons.append(InlineKeyboardButton(
            text=f'Item {index + 1}',
            callback_data=(
                f'{{"item":{index},"page":{page},"user_id":{user_id}}}'
            )
        ))

    reshaped_items_buttons = []
    # Colocando dois botões de itens por linha
    for item1, item2 in zip_longest(items_buttons[0::2], items_buttons[1::2]):
        new_line = [item1, item2]
        if None in new_line:
            new_line.remove(None)
        reshaped_items_buttons.append(new_line)

    return reshaped_items_buttons


def get_navigation_buttons(
    have_back_page: bool, have_next_page: bool, page: int, user_id: int
) -> List[InlineKeyboardButton]:

    navigation_keyboard = []
    if have_back_page:  # Cria botão de Voltar Página
        navigation_keyboard.append(
            InlineKeyboardButton(
                text=NAV_PREVIOUS_BUTTON_TEXT,
                callback_data=f'{{"page":{page - 1},"user_id":{user_id}}}'
            )
        )
    if have_next_page:  # Cria botão de Avançar Página
        navigation_keyboard.append(
            InlineKeyboardButton(
                text=NAV_NEXT_BUTTON_TEXT,
                callback_data=f'{{"page":{page + 1},"user_id":{user_id}}}'
            )
        )

    return navigation_keyboard


def get_extremes_navigation_buttons(
    have_back_page: bool, have_next_page: bool, user_id: int
) -> List[InlineKeyboardButton]:

    extremes_navigation_keyboard = []
    if have_back_page:  # Cria botão para a Primeira Página
        extremes_navigation_keyboard.append(
            InlineKeyboardButton(
                text=NAV_START_BUTTON_TEXT,
                callback_data=f'{{"page":0,"user_id":{user_id}}}'
            )
        )
    if have_next_page:  # Cria botão para a Última Página
        bag_model = BagModel()
        bag_length = bag_model.length('items_ids', user_id)
        total_pages = (bag_length - 1) // ITEMS_PER_PAGE
        extremes_navigation_keyboard.append(
            InlineKeyboardButton(
                text=NAV_END_BUTTON_TEXT,
                callback_data=f'{{"page":{total_pages},"user_id":{user_id}}}'
            )
        )

    return extremes_navigation_keyboard


def get_use_consumable_buttons(
    page: int,
    user_id: int,
    item_pos: int,
    item: Item
) -> List[InlineKeyboardButton]:
    use_buttons = []
    quantity = item.quantity
    if item.item.usable is True:
        for quantity_option in DROPUSE_QUANTITY_OPTION_LIST:
            if quantity_option <= quantity:
                text = USE_MANY_BUTTON_TEXT.format(
                    quantity_option=quantity_option
                )
                use_buttons.append(
                    InlineKeyboardButton(
                        text=text,
                        callback_data=(
                            f'{{"use":{quantity_option},"item":{item_pos},'
                            f'"page":{page},"user_id":{user_id}}}'
                        )
                    )
                )

    return reshape_row_buttons(use_buttons, buttons_per_row=2)


def get_discard_buttons(
    page: int,
    user_id: int,
    item_pos: int,
    item: Item
) -> List[InlineKeyboardButton]:
    drop_buttons = []
    quantity = item.quantity
    for quantity_option in DROPUSE_QUANTITY_OPTION_LIST:
        if quantity_option <= quantity:
            text = DISCARD_MANY_BUTTON_TEXT.format(
                quantity_option=quantity_option
            )
            drop_buttons.append(
                InlineKeyboardButton(
                    text=text,
                    callback_data=(
                        f'{{"drop":{quantity_option},"item":{item_pos},'
                        f'"page":{page},"user_id":{user_id}}}'
                    )
                )
            )

    return reshape_row_buttons(drop_buttons, buttons_per_row=2)


def get_close_bag_button(user_id: int) -> List[InlineKeyboardButton]:
    return [
        InlineKeyboardButton(
            text=CLOSE_BAG_BUTTON_TEXT,
            callback_data=(
                f'{{"command":"{CALLBACK_CLOSE_BAG}","user_id":{user_id}}}'
            )
        )]


def get_back_button(
    page: int, user_id: int, retry_state: int
) -> List[InlineKeyboardButton]:
    return [
        InlineKeyboardButton(
            text=NAV_BACK_BUTTON_TEXT,
            callback_data=(
                f'{{"page":{page},"user_id":{user_id},'
                f'"retry_state":{retry_state}}}'
            )
        )
    ]


def get_take_break_buttons(
    drop: int, item_id: str
) -> List[InlineKeyboardButton]:
    return [
        InlineKeyboardButton(
            text=TAKE_BUTTON_TEXT,
            callback_data=(
                f'{{"_id":"{item_id}","drop":{drop}}}'
            )
        ),
        InlineKeyboardButton(
            text=DESTROY_ITEM_BUTTON_TEXT,
            callback_data=CALLBACK_TEXT_DESTROY_ITEM
        )]


def get_sort_button(
    page: int, user_id: str
) -> List[InlineKeyboardButton]:
    return [
        InlineKeyboardButton(
            text=SORT_ITEMS_BUTTON_TEXT,
            callback_data=(
                f'{{"command":"{CALLBACK_TEXT_SORT_ITEMS}",'
                f'"page":{page},"user_id":{user_id}}}'
            )
        )]


def get_sort_buttons(
    page: int, user_id: str
) -> List[List[InlineKeyboardButton]]:

    return [
        [
            InlineKeyboardButton(
                text=CONSUMABLE_SORT_UP_BUTTON_TEXT,
                callback_data=(
                    f'{{"sort":"consumable_up",'
                    f'"page":{page},"user_id":{user_id}}}'
                )
            ),
            InlineKeyboardButton(
                text=CONSUMABLE_SORT_DOWN_BUTTON_TEXT,
                callback_data=(
                    f'{{"sort":"consumable_down",'
                    f'"page":{page},"user_id":{user_id}}}'
                )
            ),
        ],
        [
            InlineKeyboardButton(
                text=EQUIPMENT_POWER_SORT_UP_BUTTON_TEXT,
                callback_data=(
                    f'{{"sort":"power_up",'
                    f'"page":{page},"user_id":{user_id}}}'
                )
            ),
            InlineKeyboardButton(
                text=EQUIPMENT_POWER_SORT_DOWN_BUTTON_TEXT,
                callback_data=(
                    f'{{"sort":"power_down",'
                    f'"page":{page},"user_id":{user_id}}}'
                )
            ),
        ],
        [
            InlineKeyboardButton(
                text=EQUIPMENT_RARITY_SORT_UP_BUTTON_TEXT,
                callback_data=(
                    f'{{"sort":"rarity_up",'
                    f'"page":{page},"user_id":{user_id}}}'
                )
            ),
            InlineKeyboardButton(
                text=EQUIPMENT_RARITY_SORT_DOWN_BUTTON_TEXT,
                callback_data=(
                    f'{{"sort":"rarity_down",'
                    f'"page":{page},"user_id":{user_id}}}'
                )
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
            CallbackQueryHandler(start, pattern=r'^{"page":'),
        ],
        CHECK_ROUTES: [
            CallbackQueryHandler(start, pattern=r'^{"page":'),
            CallbackQueryHandler(check_item, pattern=r'^{"item":'),
            CallbackQueryHandler(
                choice_sort_items,
                pattern=f'{{"command":"{ESCAPED_CALLBACK_TEXT_SORT_ITEMS}"'
            ),
            CallbackQueryHandler(
                cancel, pattern=f'{{"command":"{CALLBACK_CLOSE_BAG}"'
            ),
        ],
        USE_ROUTES: [
            CallbackQueryHandler(start, pattern=r'^{"page":'),
            CallbackQueryHandler(use_item, pattern=r'^{"use":'),
            CallbackQueryHandler(drop_item, pattern=r'^{"drop":(1|3|5|10)'),
            CallbackQueryHandler(identify_item, pattern=r'^{"identify":1'),
        ],
        SORT_ROUTES: [
            CallbackQueryHandler(start, pattern=r'^{"page":'),
            CallbackQueryHandler(sort_items, pattern=r'^{"sort":'),
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
        get_drop, pattern=r'^{"_id":'
    ),
    CallbackQueryHandler(
        destroy_drop, pattern=f'^{ESCAPED_CALLBACK_TEXT_DESTROY_ITEM}$',
    )
]
