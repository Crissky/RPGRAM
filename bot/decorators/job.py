from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from function.date_time import get_brazil_time_now

from repository.mongo import GroupModel
from rpgram import Group


def skip_if_spawn_timeout(callback):
    # @wraps serve para manter os metadados das funções que receberão o 
    # decorator, como o nome da função.
    @wraps(callback)
    async def wrapper(context: ContextTypes.DEFAULT_TYPE):
        print('@SKIP_IF_SPAWN_TIMEOUT')
        group_model = GroupModel()
        job = context.job
        job_name = job.name
        chat_id = job.chat_id
        group: Group = group_model.get(chat_id)
        spawn_start_time = group.spawn_start_time
        spawn_end_time = group.spawn_end_time
        now = get_brazil_time_now()
        time = now.strftime("%H:%M")

        print(
            f'[{chat_id}] {group.name}: Hora: {time}.\n'
            f'Horário de spawn: {spawn_start_time}H - {spawn_end_time}H.'
        )
        if now.hour >= spawn_start_time and now.hour < spawn_end_time:
            print('\tAUTORIZADO - DENTRO DO HORÁRIO DE EVENTOS DO GRUPO.')
            return await callback(context)
        else:
            print(
                f'Evento {job_name} foi skipado, '
                'pois está fora do horário de spawn do grupo.\n'
            )
    return wrapper


def skip_command_if_spawn_timeout(callback):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        print('@SKIP_COMMAND_IF_SPAWN_TIMEOUT')
        group_model = GroupModel()
        chat_id = update.effective_chat.id
        group: Group = group_model.get(chat_id)
        spawn_start_time = group.spawn_start_time
        spawn_end_time = group.spawn_end_time
        now = get_brazil_time_now()
        time = now.strftime("%H:%M")

        print(
            f'[{chat_id}] {group.name}: Hora: {time}.\n'
            f'Horário de spawn: {spawn_start_time}H - {spawn_end_time}H.'
        )
        if now.hour >= spawn_start_time and now.hour < spawn_end_time:
            print('\tAUTORIZADO - DENTRO DO HORÁRIO DE EVENTOS DO GRUPO.')
            return await callback(update, context)
        else:
            print(
                'Evento chat_xp.start foi skipado, '
                'pois está fora do horário de spawn do grupo.\n'
            )
    return wrapper
