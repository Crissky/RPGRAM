from datetime import timedelta
from random import choices, randint

from bson import ObjectId
from telegram import Update
from telegram.ext import ContextTypes
from bot.constants.job import BASE_JOB_KWARGS
from bot.conversations.enemy import job_start_ambush
from bot.conversations.item import job_find_treasure
from bot.conversations.puzzle import job_start_puzzle
from bot.conversations.quest_item import job_start_item_quest
from bot.conversations.word_game import job_start_wordgame
from bot.functions.date_time import is_boosted_day
from bot.functions.general import get_event_random_minutes
from function.date_time import get_brazil_time_now
from repository.mongo.models.config import GroupModel
from rpgram.group import Group


MAX_EVENT_TIMES = 2


def add_event_points_from_player(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> Group:
    group_model = GroupModel()
    chat_id = update.effective_chat.id

    group: Group = group_model.get(chat_id)
    can_trigger_event = group.add_event_points_from_player()
    if can_trigger_event:
        num_events = 1 + group.get_extra_event_points()
        create_event(context=context, num_events=num_events)
        group.reset_event_points()

    group_model.save(group)

    return group


def add_event_points_from_group(chat_id) -> Group:
    group_model = GroupModel()
    group: Group = group_model.get(chat_id)
    group.add_event_points_from_group()
    group_model.save(group)

    return group


def create_event(
    context: ContextTypes.DEFAULT_TYPE,
    num_events: int = 1
):
    chat_id = context._chat_id
    now = get_brazil_time_now()
    mult_times = randint(1, MAX_EVENT_TIMES) if is_boosted_day(now) else 1
    total_events = num_events * mult_times
    events = {
        'treasure': 100,
        'ambush': 15,
        'quest_item': 12,
        'puzzle': 8,
        'wordgame': 6,
    }
    population = list(events.keys())
    weights = events.values()

    for i in range(total_events):
        minutes = get_event_random_minutes(multiplier=i)
        event_name = choices(population, weights=weights)[0]
        print(
            f'CREATE_EVENT(): Evento escolhido "{event_name}" '
            f'({i+1}/{total_events}) que iniciará em {minutes} minutos.'
        )

        if event_name == 'treasure':
            job_callback = job_find_treasure
        elif event_name == 'ambush':
            job_callback = job_start_ambush
        elif event_name == 'quest_item':
            job_callback = job_start_item_quest
        elif event_name == 'puzzle':
            job_callback = job_start_puzzle
        elif event_name == 'wordgame':
            job_callback = job_start_wordgame
        else:
            raise ValueError(f'"{event_name}" não é um evento válido.')
        
        job_callback_name = job_callback.__name__.upper()
        job_name = f'{job_callback_name}_{ObjectId()}'
        context.job_queue.run_once(
            callback=job_callback,
            when=timedelta(minutes=minutes),
            chat_id=chat_id,
            name=job_name,
            job_kwargs=BASE_JOB_KWARGS,
        )
