from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot.constants.seller import (
    SELLER_NAME,
    TOTAL_CONSUMABLES,
    TOTAL_EQUIPMENTS
)
from bot.decorators.job import skip_if_spawn_timeout
from bot.functions.char import get_chars_level_from_group
from bot.functions.general import get_attribute_group_or_player

from function.text import escape_basic_markdown_v2

from repository.mongo import BagModel, ItemModel
from repository.mongo.populate.item import (
    create_random_consumable,
    create_random_equipment
)

from rpgram import Bag
from rpgram.consumables import GemstoneConsumable, TrocadoPouchConsumable


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

    seller_bag = Bag(
        items=[],
        player_id=chat_id,
    )

    for char_level in chars_level_list:
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

    response = await context.bot.send_message(
        chat_id=chat_id,
        text=escape_basic_markdown_v2(f'{SELLER_NAME}\n{seller_bag}'),
        disable_notification=silent,
        parse_mode=ParseMode.MARKDOWN_V2,
    )
