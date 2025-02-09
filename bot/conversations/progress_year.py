'''
Módulo responsável por exibir diariamente a porcentagem do dia atual em 
relação ao total de dias do ano vigente.
'''


from datetime import datetime

from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from bot.functions.chat import call_telegram_message_function
from bot.functions.general import get_attribute_group_or_player
from constant.text import (
    SECTION_HEAD_PROGRESS_YEAR_END,
    SECTION_HEAD_PROGRESS_YEAR_START
)
from function.date_time import get_brazil_time_now
from function.text import create_text_in_box


async def show_percent_today(context: ContextTypes.DEFAULT_TYPE):
    '''Exibe a procentagem do dia atual em relação a quantidade de dias do ano
    atual.
    '''

    job = context.job
    chat_id = job.chat_id
    silent = get_attribute_group_or_player(chat_id, 'silent')
    percentage = percent_today()
    text = beautiful_percentage_bar(percentage)
    today = get_brazil_time_now()
    current_yday = today.timetuple().tm_yday
    year = today.year
    text = (
        f'Hoje é o *{current_yday}º dia de {year}*.\n'
        f'{text}'
    )

    text = create_text_in_box(
        text=text,
        section_name=f'PROGRESSO {today.year}',
        section_start=SECTION_HEAD_PROGRESS_YEAR_START,
        section_end=SECTION_HEAD_PROGRESS_YEAR_END,
    )

    call_telegram_kwargs = dict(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN_V2,
        disable_notification=silent
    )

    await call_telegram_message_function(
        function_caller='SHOW_PERCENT_TODAY()',
        function=context.bot.send_message,
        context=context,
        need_response=False,
        auto_delete_message=False,
        **call_telegram_kwargs
    )


def percent_today() -> float:
    '''
    Calcula a porcentagem do dia atual em relação a quantidade de dias do ano 
    atual.
    '''

    today = get_brazil_time_now()
    current_days = today.timetuple().tm_yday
    total_days = datetime(today.year, 12, 31).timetuple().tm_yday

    return (current_days / total_days * 100)


def beautiful_percentage_bar(percentage) -> str:
    '''
    Retorna uma bela barra preenchida de ocordo com a porcentagem.

    Args:
        percentage: Um float entre 0 e 100 representando a porcentagem.
    '''

    if not 0 <= percentage <= 100:
        raise ValueError('Percentage must be between 0 and 100.')

    bar_length = 15
    filled_length = int(percentage / 100 * bar_length)
    empty_length = bar_length - filled_length

    bar = '▰' * filled_length
    bar += '▱' * empty_length
    return f'{bar} {percentage:.1f}%'
