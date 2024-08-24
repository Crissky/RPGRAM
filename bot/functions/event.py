from random import choices

from telegram import Update
from telegram.ext import ContextTypes
from bot.conversations.enemy import create_ambush_event
from bot.conversations.item import create_find_treasure_event
from bot.conversations.puzzle import create_puzzle_event
from bot.conversations.quest_item import create_item_quest_event
from repository.mongo.models.config import GroupModel
from rpgram.group import Group


async def add_event_points_from_player(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> Group:
    group_model = GroupModel()
    chat_id = update.effective_chat.id

    group: Group = group_model.get(chat_id)
    can_trigger_event = group.add_event_points_from_player()
    if can_trigger_event:
        total_events = 1 + group.get_extra_event_points()
        for _ in range(total_events):
            await create_event(update=update, context=context)
        group.reset_event_points()

    group_model.save(group)

    return group


def add_event_points_from_group(chat_id) -> Group:
    group_model = GroupModel()
    group: Group = group_model.get(chat_id)
    group.add_event_points_from_group()
    group_model.save(group)

    return group


async def create_event(update: Update, context: ContextTypes.DEFAULT_TYPE):
    events = {
        'treasure': 100,
        'ambush': 15,
        'quest_item': 12,
        'puzzle': 8,
    }
    population = list(events.keys())
    weights = events.values()
    event_name = choices(population, weights=weights)[0]
    print(f'CREATE_EVENT(): Evento escolhido "{event_name}"')

    if event_name == 'treasure':
        await create_find_treasure_event(update=update, context=context)
    elif event_name == 'ambush':
        await create_ambush_event(update=update, context=context)
    elif event_name == 'quest_item':
        await create_item_quest_event(update=update, context=context)
    elif event_name == 'puzzle':
        await create_puzzle_event(update=update, context=context)
    else:
        raise ValueError(f'"{event_name}" não é um evento válido.')
