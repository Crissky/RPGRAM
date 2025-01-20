from telegram.ext import ContextTypes

from bot.decorators.job import skip_if_spawn_timeout
from bot.functions.event import add_event_points_from_group


@skip_if_spawn_timeout
async def job_add_event_points(context: ContextTypes.DEFAULT_TYPE):
    '''Adiciona pontos de evento ao grupo.
    '''

    job = context.job
    chat_id = job.chat_id
    group = add_event_points_from_group(chat_id=chat_id)

    print(f'JOB_ADD_EVENT_POINTS() - {group.show_event_points}.')
