from telegram.ext import ContextTypes, ConversationHandler
from function.date_time import get_brazil_time_now

from repository.mongo import GroupModel


def skip_if_spawn_timeout(callback):
    async def wrapper(context: ContextTypes.DEFAULT_TYPE):
        print('@SKIP_IF_SPAWN_TIMEOUT')
        group_model = GroupModel()
        job = context.job
        chat_id = job.chat_id
        group = group_model.get(chat_id)
        spawn_start_time = group.spawn_start_time
        spawn_end_time = group.spawn_end_time
        now = get_brazil_time_now()

        print(
            f'[{chat_id}] {group.name}: Hora: {now.hour}:{now.minute}.\n'
            f'Horário de spawn: {spawn_start_time}H - {spawn_end_time}H.'
        )
        if now.hour >= spawn_start_time and now.hour < spawn_end_time:
            print('\tAUTORIZADO - DENTRO DO HORÁRIO DE EVENTOS DO GRUPO.')
            return await callback(context)
        else:
            print(
                f'Evento job_activate_conditions foi skipado, '
                f'pois está fora do horário de spawn do grupo.\n'
            )
    return wrapper
