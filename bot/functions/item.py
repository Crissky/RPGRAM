from telegram import Update
from bot.conversations.bag import send_drop_message
from bot.functions.char import get_chars_level_from_group
from bot.functions.config import get_attribute_group
from repository.mongo.populate.item import (
    create_random_consumable,
    create_random_equipment
)
from rpgram.enums.rarity import RarityEnum


from telegram.ext import ContextTypes


from random import choice, randint, shuffle


async def drop_random_prize(
    context: ContextTypes.DEFAULT_TYPE,
    silent: bool,
    rarity: RarityEnum,
    update: Update = None,
    message_id: int = None,
    text: str = 'deixou cair como recompensa',
):
    '''Envia mensagens de drops de itens em um chat.
    '''

    chat_id = context._chat_id
    group_level = get_attribute_group(chat_id, 'group_level')
    char_level_list = get_chars_level_from_group(chat_id=chat_id)
    total_chars = len(char_level_list)
    min_quantity = max(1, total_chars)
    max_quantity = max(2, int(total_chars * 2))
    total_consumables = randint(min_quantity, max_quantity)
    total_equipments = randint(min_quantity, max_quantity)

    consumable_list = list(create_random_consumable(
        group_level=group_level,
        random_level=True,
        total_items=total_consumables
    ))
    all_equipment_list = [
        create_random_equipment(
            equip_type=None,
            group_level=choice(char_level_list),
            rarity=rarity.name,
            random_level=True,
            save_in_database=True,
        )
        for _ in range(total_equipments)
    ]
    drops = [
        item
        for item in (consumable_list + all_equipment_list)
        if item is not None
    ]

    shuffle(drops)
    await send_drop_message(
        context=context,
        items=drops,
        text=text,
        update=update,
        chat_id=chat_id,
        message_id=message_id,
        silent=silent,
    )
