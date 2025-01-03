from datetime import datetime, timedelta
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot.functions.chat import call_telegram_message_function
from constant.text import (
    SECTION_HEAD_CHRISTMAS_END,
    SECTION_HEAD_CHRISTMAS_START,
    SECTION_HEAD_NEW_YEAR_END,
    SECTION_HEAD_NEW_YEAR_START
)
from function.date_time import get_brazil_time_now
from function.text import create_text_in_box


async def job_new_year(context: ContextTypes.DEFAULT_TYPE):
    '''Envia Mensagem de Feliz Ano Novo para o grupo.
    '''

    print(f'JOB_NEW_YEAR()')
    job = context.job
    chat_id = job.chat_id
    text = (
        '*SAUDAÇÕES, BRAVOS AVENTUREIROS!*\n\n'
        'À meia-noite, as estrelas dançam no véu da noite, '
        'marcando o fim de mais um ciclo no grande tapete do tempo. '
        'Eis que o Novo Ano surge como um grimório de páginas vazias, '
        'aguardando vossas histórias de coragem, amizade e glória.\n\n'

        'Que vossas espadas jamais enferrujem, '
        'que vossos feitiços resplandeçam com poder renovado, '
        'e que os ventos soprem a favor de vossas jornadas. '
        'Que as tavernas estejam sempre acolhedoras, '
        'os caminhos cheios de descobertas, e os desafios, '
        'dignos de heróis como vós.\n\n'

        'Lembrai-vos, companheiros, '
        'que a verdadeira magia reside nos laços forjados ao '
        'calor das fogueiras e nos feitos que gravamos nas lendas. '
        'Que o ano que se inicia seja um capítulo repleto de '
        'aventuras épicas, '
        'recompensas fabulosas e a doce melodia da vitória.\n\n'

        '*Aos vossos pés, um mundo de possibilidades. '
        'Às vossas mãos, o destino do amanhã.*\n\n'

        'Feliz Ano Novo, bravos desbravadores! '
        'Que o próximo amanhecer vos encontre com o coração leve '
        'e o espírito pronto para mais um ano de conquistas lendárias!'
    )
    text = create_text_in_box(
        text=text,
        section_name=f'FELIZ ANO NOVO',
        section_start=SECTION_HEAD_NEW_YEAR_START,
        section_end=SECTION_HEAD_NEW_YEAR_END,
    )
    send_message_kwargs = dict(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN_V2,
        disable_notification=False,
    )

    await call_telegram_message_function(
        function_caller='JOB_NEW_YEAR()',
        function=context.bot.send_message,
        context=context,
        **send_message_kwargs
    )


async def job_christmas(context: ContextTypes.DEFAULT_TYPE):
    '''Envia Mensagem de Feliz Ano Novo para o grupo.
    '''

    print(f'JOB_CHRISTMAS()')
    job = context.job
    chat_id = job.chat_id
    text = (
        '*SAUDAÇÕES, VALOROSOS AVENTUREIROS!*\n\n'

        'Neste dia em que os sinos ecoam por vales e montanhas, '
        'e a luz das velas ilumina os salões das tavernas, '
        'celebremos juntos o espírito do Natal. '
        'É tempo de repousar as espadas, '
        'aquecer-se junto à lareira e partilhar histórias e risos '
        'com aqueles que caminham ao vosso lado.\n\n'

        'Que o brilho das estrelas guie vossos passos, '
        'e que a generosidade que marca este dia aqueça vossos corações '
        'como o mais puro dos encantamentos. '
        'Assim como as chamas da lareira repelem o frio, '
        'que o calor da amizade e da bondade vos protejam das sombras.\n\n'

        'Recordai-vos, companheiros, '
        'que nem todo tesouro é feito de ouro e prata. '
        'Às vezes, os maiores presentes são os laços de irmandade, '
        'os gestos de coragem e o simples fato de saber que nunca se '
        'está sozinho na jornada.\n\n'

        '*Que o Natal vos traga paz, '
        'esperança e o desejo renovado de buscar novas aventuras. '
        'Que vossos dias sejam longos e vossos caminhos prósperos.*\n\n'

        'Feliz Natal, bravos heróis! '
        'Que as bênçãos deste dia vos acompanhem por todas as estradas '
        'que o destino vos reserva!'
    )
    text = create_text_in_box(
        text=text,
        section_name=f'FELIZ NATAL',
        section_start=SECTION_HEAD_CHRISTMAS_START,
        section_end=SECTION_HEAD_CHRISTMAS_END,
    )
    send_message_kwargs = dict(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN_V2,
        disable_notification=False,
    )

    await call_telegram_message_function(
        function_caller='JOB_CHRISTMAS()',
        function=context.bot.send_message,
        context=context,
        **send_message_kwargs
    )


NOW = get_brazil_time_now()
SEASON_JOBS_DEFINITIONS = [
    {
        'callback': job_new_year,
        'when': datetime(NOW.year, 1, 1, 0, 0, 0),
    },
    {
        'callback': job_christmas,
        'when': datetime(NOW.year, 12, 24, 23, 0, 0),
    },
]
