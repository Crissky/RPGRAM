'''
Módulo responsável por gerenciar as requisiçães de visualização das 
informações dos jogadores.
'''


from random import choice
from typing import List
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    PrefixHandler,
)
from telegram.error import BadRequest

from bot.constants.help import ACCESS_DENIED
from bot.constants.equips import COMMANDS
from bot.constants.filters import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.conversations.close import get_close_button
from bot.decorators import (
    need_have_char,
    print_basic_infos,
    skip_if_dead_char,
    skip_if_immobilized,
)
from bot.decorators.char import confusion
from bot.functions.general import get_attribute_group_or_player

from repository.mongo import BagModel, CharacterModel, EquipsModel, ItemModel
from rpgram import Equips, Item
from rpgram.boosters import Equipment
from rpgram.enums import EmojiEnum, FaceEmojiEnum


@skip_if_dead_char
@skip_if_immobilized
@confusion
@print_basic_infos
@need_have_char
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_message.reply_chat_action(ChatAction.TYPING)
    bag_model = BagModel()
    char_model = CharacterModel()
    equips_model = EquipsModel()
    item_model = ItemModel()
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    query = update.callback_query
    args = context.args

    if query:
        data = eval(query.data)
        refresh = data.get('refresh', False)
        data_user_id = data['user_id']

        # Não executa se outro usuário mexer na bolsa
        if data_user_id != user_id:
            await query.answer(text=ACCESS_DENIED, show_alert=True)
            return None
        
        # Apaga o Mensagem
        if data.get('close', False):
            await query.answer('Fechando Equipamentos...')
            await query.delete_message()
            return None

    silent = get_attribute_group_or_player(chat_id, 'silent')
    equips = equips_model.get(user_id)
    if not equips:
        player_character = char_model.get(user_id)
        equips = player_character.equips
        equips_model.save(player_character.equips)

    verbose = False
    if args:
        verbose = 'verbose' in args[0] or 'v' in args[0]

    if equips and query and not refresh:  # Desequipa um equipamento
        data = eval(query.data)
        equip_id = data['equip_id']
        try:
            equipment = item_model.get(equip_id)
            old_equipment = equips.unequip(equipment)
            old_equipment_item = Item(old_equipment)
            bag_model.add(old_equipment_item, user_id)
            equips_model.save(equips)
            text = f'Você desequipou "{old_equipment.name}".'
            await query.answer(text)
        except ValueError as error:
            await query.answer(text=str(error), show_alert=True)

    if equips:
        reply_markup = get_equips_keyboard(equips, user_id)
        markdown_equips_sheet = equips.get_all_sheets(
            verbose=verbose, markdown=True
        )
        if query:
            if refresh:
                '''"refresh_text" é usado para modificar a mensagem de maneira
                aleatória para tentar evitar um erro (BadRequest)
                quando não há mudanças no "markdown_equips_sheet" usado na
                função "edit_message_text".'''
                refresh_text = get_random_refresh_text()
                markdown_equips_sheet = (
                    f'{refresh_text}\n'
                    f'{markdown_equips_sheet}'
                )
            try:
                await query.edit_message_text(
                    markdown_equips_sheet,
                    parse_mode=ParseMode.MARKDOWN_V2,
                    reply_markup=reply_markup,
                )
            except BadRequest as error:
                await query.answer(text=str(error))
        else:
            await update.effective_message.reply_text(
                f'{markdown_equips_sheet}',
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=reply_markup,
                disable_notification=silent
            )
    else:
        await update.effective_message.reply_text(
            f'Seu personagem ainda não possui equipamentos.\n'
            f'Equips: {equips}',
            disable_notification=silent
        )


def get_equips_keyboard(
    equips: Equips,
    user_id: int
) -> InlineKeyboardMarkup:
    equips_keyboard = []
    hands_buttons = []
    accessories_buttons = []
    if (helmet := equips.helmet):
        equips_keyboard.append([create_equipment_button(helmet, user_id)])
    if equips.left_hand or equips.right_hand:
        if (left_hand := equips.left_hand):
            hands_buttons.append(create_equipment_button(left_hand, user_id))
        if (right_hand := equips.right_hand):
            hands_buttons.append(
                create_equipment_button(right_hand, user_id, True)
            )
        if equips.equiped_two_handed_weapon():
            hands_buttons = hands_buttons[:1]
        equips_keyboard.append(hands_buttons)
    if (armor := equips.armor):
        equips_keyboard.append([create_equipment_button(armor, user_id)])
    if (boots := equips.boots):
        equips_keyboard.append([create_equipment_button(boots, user_id)])
    if (ring := equips.ring):
        accessories_buttons.append(create_equipment_button(ring, user_id))
    if (amulet := equips.amulet):
        accessories_buttons.append(create_equipment_button(amulet, user_id))
    equips_keyboard.append(accessories_buttons)
    equips_keyboard.append(get_refresh_close_button(user_id))

    return InlineKeyboardMarkup(equips_keyboard)


def create_equipment_button(
    equipment: Equipment,
    user_id: int,
    right: bool = False
) -> InlineKeyboardButton:
    equip_id = equipment._id
    text = f'{equipment.emoji_name_type}'
    if right:
        text = f'{equipment.name_emoji_type}'
    return InlineKeyboardButton(
        text,
        callback_data=(
            f'{{"equip_id":"{equip_id}",'
            f'"user_id":{user_id}}}'
        )
    )


def get_refresh_close_button(user_id) -> List[InlineKeyboardButton]:
    return [
        InlineKeyboardButton(
            f'{EmojiEnum.REFRESH.value}Atualizar',
            callback_data=(
                f'{{"refresh":1,'
                f'"user_id":{user_id}}}'
            )
        ),
        get_close_button(user_id=user_id, right_icon=True)
    ]


def get_random_refresh_text() -> str:
    emoji = choice(list(FaceEmojiEnum)).value
    return f'Atualizado{emoji}'


VIEW_EQUIPS_HANDLERS = [
    PrefixHandler(
        PREFIX_COMMANDS,
        COMMANDS,
        start,
        BASIC_COMMAND_FILTER
    ),
    CommandHandler(
        COMMANDS,
        start,
        BASIC_COMMAND_FILTER
    ),
    CallbackQueryHandler(
        start, pattern=r'^{"equip_id":'
    ),
    CallbackQueryHandler(
        start, pattern=r'^{"refresh":1'
    ),
]
