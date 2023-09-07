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
    ACCESS_DENIED,
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
from constant.time import TEN_MINUTES_IN_SECONDS
from repository.mongo import BagModel, CharacterModel, EquipsModel
from rpgram import Bag
from rpgram.boosters import Equipment
from rpgram import Consumable
from rpgram.enums import EmojiEnum


# ROUTES
ITEM_ROUTES = 1


@skip_if_no_singup_player
@skip_if_no_have_char
@need_not_in_battle
@print_basic_infos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Envia ou edita mensagem contendo uma página dos itens do jogador'''
    bag_model = BagModel()
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_name = update.effective_user.name
    query = update.callback_query
    silent = get_attribute_group_or_player(chat_id, 'silent')

    if query:
        data = eval(query.data)
        page = data['page']  # starts zero
        data_user_id = data['user_id']

        # Não executa se outro usuário mexer na bolsa
        if data_user_id != user_id:
            await query.answer(text=ACCESS_DENIED, show_alert=True)
            return ITEM_ROUTES

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

    items_buttons = []
    # Criando texto e botões dos itens
    for index, item in enumerate(items):
        markdown_text += f'*Ⅰ{(index + 1)}:* '
        markdown_text += item.get_sheet(verbose=True, markdown=True)
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

    navigation_keyboard = []
    if have_back_page:  # Cria botão de Voltar Página
        navigation_keyboard.append(
            InlineKeyboardButton(
                text=f'{EmojiEnum.PREVIOUS.value} Anterior',
                callback_data=f'{{"page":{page - 1},"user_id":{user_id}}}'
            )
        )
    if have_next_page:  # Cria botão de Avançar Página
        navigation_keyboard.append(
            InlineKeyboardButton(
                text=f'Próxima {EmojiEnum.NEXT.value}',
                callback_data=f'{{"page":{page + 1},"user_id":{user_id}}}'
            )
        )

    cancel_button = [InlineKeyboardButton(
        text=f'{EmojiEnum.CLOSE_BAG.value}Fechar Bolsa',
        callback_data=(
            f'{{"command":"{CALLBACK_CLOSE_BAG}","user_id":{user_id}}}'
        )
    )]
    reply_markup = InlineKeyboardMarkup(
        reshaped_items_buttons + [navigation_keyboard] + [cancel_button]
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

    return ITEM_ROUTES


async def check_item(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Edita a mensagem com as informações do item escolhido.
    '''
    bag_model = BagModel()
    equips_model = EquipsModel()
    user_id = update.effective_user.id
    query = update.callback_query
    data = eval(query.data)
    item_pos = data['item']
    page = data['page']
    data_user_id = data['user_id']

    if data_user_id != user_id:  # Não executa se outro usuário mexer na bolsa
        await query.answer(text=ACCESS_DENIED, show_alert=True)
        return ITEM_ROUTES

    item_index = (ITEMS_PER_PAGE * page) + item_pos
    player_bag = bag_model.get(
        query={'player_id': user_id},
        fields={'items_ids': {'$slice': [item_index, 1]}},
        partial=False
    )
    item = player_bag[0]
    markdown_text = item.get_all_sheets(verbose=True, markdown=True)
    if isinstance(item.item, Equipment):
        equips = equips_model.get(user_id)
        markdown_text = equips.compare(item.item)
        use_text = f'{EmojiEnum.TO_EQUIP.value}Equipar'
    elif isinstance(item.item, Consumable):
        use_text = f'{EmojiEnum.USE_POTION.value}Usar'

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            text=use_text,
            callback_data=(
                f'{{"use":1,"item":{item_pos},'
                f'"page":{page},"user_id":{user_id}}}'
            )
        )],
        [InlineKeyboardButton(
            text='Voltar', callback_data=(
                f'{{"page":{page},"user_id":{user_id}}}'
            )
        )]
    ])
    # Edita mensagem com as informações do item escolhido
    await query.edit_message_text(
        text=markdown_text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN_V2
    )
    return ITEM_ROUTES


async def use_item(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Usa ou equipa o item do jogador.
    '''
    bag_model = BagModel()
    char_model = CharacterModel()
    equips_model = EquipsModel()
    user_id = update.effective_user.id
    query = update.callback_query
    data = eval(query.data)
    item_pos = data['item']
    page = data['page']
    data_user_id = data['user_id']

    if data_user_id != user_id:  # Não executa se outro usuário mexer na bolsa
        await query.answer(text=ACCESS_DENIED, show_alert=True)
        return ITEM_ROUTES

    item_index = (ITEMS_PER_PAGE * page) + item_pos
    player_bag = bag_model.get(
        query={'player_id': user_id},
        fields={'items_ids': {'$slice': [item_index, 1]}},
        partial=False
    )
    item = player_bag[0]
    player_character = char_model.get(user_id)

    old_equipments = []
    if isinstance(item.item, Equipment):  # Tenta equipar o item
        equipment = item.item
        try:
            old_equipments = player_character.equips.equip(equipment)
            await query.answer(text=f'Você equipou "{equipment.name}".\n\n')
        except Exception as error:
            print(error)
            await query.answer(
                text=(
                    f'Equipamento "{equipment.name}" não pode ser equipado.'
                    f'\n\n{error}'
                ),
                show_alert=True
            )
            return ITEM_ROUTES
    elif isinstance(item.item, Consumable):  # Tenta usar o item
        consumable = item.item
        try:
            old_hp = player_character.cs.show_hit_points
            consumable.use(player_character)
            new_hp = player_character.cs.show_hit_points
            await query.answer(
                text=(
                    f'Você usou o item "{consumable.name}".\n'
                    f'Descrição: "{consumable.description}".\n\n'
                    f'HP: {old_hp} ››› {new_hp}.'
                ),
                show_alert=True
            )
        except Exception as error:
            print(error)
            await query.answer(
                text=(
                    f'Item "{consumable.name}" não pode ser usado.\n\n{error}'
                ),
                show_alert=True
            )
            return ITEM_ROUTES

    # Carrega a bolsa com todos os itens
    player_bag = bag_model.get(query={'player_id': user_id})
    player_bag.remove(slot=item_index)  # Remove o item usado/equipado da bolsa
    markdown_player_sheet = player_character.get_all_sheets(
        verbose=False, markdown=True
    )

    # Adiciona na bolsa os equipamentos que já estavam equipados
    # e que foram substituídos
    for old_equipment in old_equipments:
        player_bag.add(old_equipment)

    bag_model.save(player_bag)
    char_model.save(player_character)
    equips_model.save(player_character.equips)

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            text='Voltar', callback_data=(
                f'{{"page":{page},"user_id":{user_id}}}'
            )
        )]
    ])
    # Edita mensagem com as informações do personagem do jogador
    await query.edit_message_text(
        text=markdown_player_sheet,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN_V2
    )

    return ITEM_ROUTES


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
            return ITEM_ROUTES

        await query.answer('Fechando Bolsa...')
        await query.delete_message()

        return ConversationHandler.END

    return ITEM_ROUTES


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
            CallbackQueryHandler(start, pattern=r'^{"page":'),
            CallbackQueryHandler(check_item, pattern=r'^{"item":'),
            CallbackQueryHandler(use_item, pattern=r'^{"use":1'),
            CallbackQueryHandler(
                cancel, pattern=f'{{"command":"{CALLBACK_CLOSE_BAG}"'),
        ]
    },
    fallbacks=[
        CommandHandler(CANCEL_COMMANDS, cancel)
    ],
    allow_reentry=True,
    conversation_timeout=TEN_MINUTES_IN_SECONDS,
)
