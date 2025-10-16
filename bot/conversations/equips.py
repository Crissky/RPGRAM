'''
Módulo responsável por gerenciar as requisiçães de visualização das 
informações dos jogadores.
'''


from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    PrefixHandler,
)
from telegram.error import BadRequest

from bot.constants.equips import (
    ACCESS_DENIED,
    COMMANDS,
    REFRESH_EQUIPS_PATTERN,
    SECTION_TEXT_EQUIPS
)
from bot.constants.filters import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.functions.chat import (
    MIN_AUTODELETE_TIME,
    answer,
    edit_message_text,
    get_random_refresh_text,
    get_refresh_close_button,
    is_verbose,
    reply_text,
    reply_typing
)
from bot.decorators import (
    alert_if_not_chat_owner,
    confusion,
    need_have_char,
    print_basic_infos,
    skip_if_dead_char,
    skip_if_immobilized,
)
from bot.functions.general import get_attribute_group_or_player
from constant.text import SECTION_HEAD_EQUIPS_END, SECTION_HEAD_EQUIPS_START
from function.text import create_text_in_box

from repository.mongo import BagModel, CharacterModel, EquipsModel, ItemModel
from rpgram import Equips, Item
from rpgram.boosters import Equipment
from rpgram.characters import BaseCharacter


@alert_if_not_chat_owner(alert_text=ACCESS_DENIED)
@need_have_char
@skip_if_dead_char
@skip_if_immobilized
@confusion()
@print_basic_infos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await reply_typing(
        function_caller='EQUIPS.START()',
        update=update,
        context=context,
    )
    bag_model = BagModel()
    char_model = CharacterModel()
    equips_model = EquipsModel()
    item_model = ItemModel()
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    message_id = update.effective_message.id
    query = update.callback_query
    args = context.args
    verbose = is_verbose(args)

    if query:
        data = eval(query.data)
        refresh = data.get(REFRESH_EQUIPS_PATTERN, False)
        if data.get('verbose') == 'v':
            verbose = True

    silent = get_attribute_group_or_player(chat_id, 'silent')
    equips: Equips = equips_model.get(user_id)
    if not equips:
        player_character: BaseCharacter = char_model.get(user_id)
        equips = player_character.equips
        equips_model.save(player_character.equips)

    if equips and query and not refresh:  # Desequipa um equipamento
        data = eval(query.data)
        equip_id = data['equip_id']
        try:
            equipment: Equipment = item_model.get(equip_id)
            old_equipment = equips.unequip(equipment)
            old_equipment_item = Item(old_equipment)
            bag_model.add(old_equipment_item, user_id)
            equips_model.save(equips)
            text = f'Você desequipou "{old_equipment.name}".'
            await answer(query=query, text=text)
        except ValueError as error:
            await answer(query=query, text=str(error), show_alert=True)

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

            markdown_equips_sheet = create_text_in_box(
                text=markdown_equips_sheet,
                section_name=SECTION_TEXT_EQUIPS,
                section_start=SECTION_HEAD_EQUIPS_START,
                section_end=SECTION_HEAD_EQUIPS_END
            )

            try:
                await edit_message_text(
                    function_caller='EQUIPS.START()',
                    new_text=markdown_equips_sheet,
                    context=context,
                    chat_id=chat_id,
                    message_id=message_id,
                    need_response=False,
                    markdown=True,
                    reply_markup=reply_markup,
                )
            except BadRequest as error:
                await answer(query=query, text=str(error))
        else:
            markdown_equips_sheet = create_text_in_box(
                text=markdown_equips_sheet,
                section_name=SECTION_TEXT_EQUIPS,
                section_start=SECTION_HEAD_EQUIPS_START,
                section_end=SECTION_HEAD_EQUIPS_END
            )
            await reply_text(
                function_caller='EQUIPS.START()',
                text=markdown_equips_sheet,
                context=context,
                update=update,
                markdown=True,
                silent=silent,
                reply_markup=reply_markup,
                allow_sending_without_reply=True,
                need_response=False,
                skip_retry=False,
                auto_delete_message=MIN_AUTODELETE_TIME,
            )
    else:
        text = (
            'Seu personagem ainda não possui equipamentos.\n'
            f'Equips: {equips}'
        )
        await reply_text(
            function_caller='EQUIPS.START()',
            text=text,
            context=context,
            update=update,
            silent=silent,
            allow_sending_without_reply=True,
            need_response=False,
            skip_retry=False,
            auto_delete_message=MIN_AUTODELETE_TIME,
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
    equips_keyboard.append(
        get_refresh_close_button(
            user_id,
            refresh_data=REFRESH_EQUIPS_PATTERN,
            to_detail=True
        )
    )

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
        start, pattern=fr'^{{"{REFRESH_EQUIPS_PATTERN}":1'
    ),
]
