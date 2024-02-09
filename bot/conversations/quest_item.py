from random import choice, randint

from telegram import InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot.constants.quest_item import (
    ARRIVAL_NARRATION,
    REPLY_TEXT_GEMSTONE_ITEM,
    REPLY_TEXT_HEAL_CURE_ITEM,
    REPLY_TEXT_IDENTIFY_ITEM,
    REPLY_TEXT_REVIVE_ITEM,
    REPLY_TEXT_TROCADO_ITEM,
    REPLY_TEXT_XP_ITEM,
    SECTION_TEXT_QUEST
)
from bot.functions.config import get_attribute_group
from bot.functions.date_time import is_boosted_day
from bot.functions.general import get_attribute_group_or_player

from constant.text import SECTION_QUEST_END, SECTION_QUEST_START

from function.date_time import get_brazil_time_now
from function.text import create_text_in_box, escape_for_citation_markdown_v2
from repository.mongo.populate.enemy import choice_enemy_name, choice_enemy_race_name

from repository.mongo.populate.item import create_random_consumable

from rpgram.consumables import (
    CureConsumable,
    HealingConsumable,
    ReviveConsumable,
    GemstoneConsumable,
    IdentifyingConsumable,
    TrocadoPouchConsumable,
    XPConsumable
)
from rpgram import Item


async def job_create_quest_item(context: ContextTypes.DEFAULT_TYPE):
    '''Cria job da quest de pedido de items
    '''

    job = context.job
    chat_id = job.chat_id
    now = get_brazil_time_now()
    times = randint(1, 2) if is_boosted_day(now) else 1
    for i in range(times):
        minutes_in_seconds = randint(1, 179) * 60
        print(
            f'JOB_CREATE_QUEST_ITEM() - {now}: '
            f'Evento de item inicia em {minutes_in_seconds // 60} minutos.'
        )
        context.job_queue.run_once(
            callback=job_start_quest_item,
            when=minutes_in_seconds,
            name=f'JOB_CREATE_QUEST_ITEM_{i}',
            chat_id=chat_id,
        )


async def job_start_quest_item(context: ContextTypes.DEFAULT_TYPE):
    '''Envia a mensagem de pedido de ajuda para o grupo.
    '''

    job = context.job
    chat_id = job.chat_id
    group_level = get_attribute_group(chat_id, 'group_level')
    silent = get_attribute_group_or_player(chat_id, 'silent')
    consumable_item = create_random_consumable(
        group_level=group_level,
        random_level=True,
    )
    name = choice_enemy_name()
    race = choice_enemy_race_name()
    helped_name = f'{name} ({race})'
    quest_text = get_quest_text(consumable_item)
    narration_text = choice(ARRIVAL_NARRATION)
    text = (
        f'{narration_text}\n\n'
        f'>{helped_name}: {quest_text}'
    )
    text = create_text_in_box(
        text=text,
        section_name=SECTION_TEXT_QUEST,
        section_start=SECTION_QUEST_START,
        section_end=SECTION_QUEST_END,
        clean_func=escape_for_citation_markdown_v2
    )
    quest_button = get_quest_button()
    reply_markup = InlineKeyboardMarkup([quest_button])
    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        disable_notification=silent,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=reply_markup,
    )
    job_data = {
        'helped_name': helped_name,
        'item': consumable_item,
    }
    job_name = get_job_quest_name(job_data)


def get_quest_text(item: Item) -> str:
    if isinstance(item, (CureConsumable, HealingConsumable)):
        text = choice(REPLY_TEXT_HEAL_CURE_ITEM)
    elif isinstance(item, ReviveConsumable):
        text = choice(REPLY_TEXT_REVIVE_ITEM)
    elif isinstance(item, IdentifyingConsumable):
        text = choice(REPLY_TEXT_IDENTIFY_ITEM)
    elif isinstance(item, XPConsumable):
        text = choice(REPLY_TEXT_XP_ITEM)
    elif isinstance(item, TrocadoPouchConsumable):
        text = choice(REPLY_TEXT_TROCADO_ITEM)
    elif isinstance(item, GemstoneConsumable):
        text = choice(REPLY_TEXT_GEMSTONE_ITEM)

    name = item.name
    quantidade = item.quantity
    item_text = f'{quantidade}x{name}'
    text = text.format(item=item_text)

    return text


def get_quest_button():
    ...


def get_job_quest_name(job_data: dict) -> str:
    helped_name = job_data['helped_name']
    item = job_data['consumable_item']
    item_id = item._id

    return f'JOB_QUEST_ITEM_{helped_name}_{item_id}'
