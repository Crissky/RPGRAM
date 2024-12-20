from datetime import timedelta
from random import randint
from bson import ObjectId
from telegram import Update
from telegram.ext import ContextTypes

from bot.constants.job import BASE_JOB_KWARGS
from bot.decorators.job import skip_if_spawn_timeout
from bot.functions.config import get_attribute_group
from bot.functions.date_time import is_boosted_day
from function.date_time import get_brazil_time_now
from repository.mongo.populate.tools import choice_rarity
from rpgram.minigames.secret_word.secret_word import SecretWordGame


async def create_wordgame_event(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    '''Cria job do Desafio de Palavra de Hermes.
    '''

    chat_id = update.effective_chat.id
    now = get_brazil_time_now()
    times = randint(1, 2) if is_boosted_day(now) else 1
    for i in range(times):
        minutes = randint(1 + (i*20), 10 + (i*20))
        print(
            f'CREATE_WORDGAME_EVENT() - {now}: '
            f'Evento de item inicia em {minutes} minutos.'
        )
        context.job_queue.run_once(
            callback=job_start_wordgame,
            when=timedelta(minutes=minutes),
            chat_id=chat_id,
            name=f'JOB_CREATE_WORDGAME_{ObjectId()}',
            job_kwargs=BASE_JOB_KWARGS,
        )


@skip_if_spawn_timeout
async def job_start_wordgame(context: ContextTypes.DEFAULT_TYPE):
    '''Envia a mensagem com o Desafio de Palavra de Hermes.
    '''

    print('JOB_START_WORDGAME()')
    job = context.job
    chat_id = job.chat_id
    group_level = get_attribute_group(chat_id, 'group_level')
    silent = get_attribute_group(chat_id, 'silent')
    rarity = choice_rarity(group_level)
    grid = SecretWordGame(rarity=rarity)
    