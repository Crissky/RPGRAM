from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
)

from bot.constants.close import (
    ACCESS_DENIED,
    ESCAPED_CALLBACK_CLOSE
)
from bot.decorators import (
    skip_if_no_have_char,
    alert_if_not_chat_owner,
    print_basic_infos
)
from bot.functions.chat import answer, delete_message


@alert_if_not_chat_owner(alert_text=ACCESS_DENIED)
@print_basic_infos
@skip_if_no_have_char
async def close(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Fecha uma mensagem.
    """

    print('CLOSE() - FECHANDO MENSAGEM')
    query = update.callback_query

    if query:
        await answer(query=query, text='Fechando conversa...')
        await delete_message(
            function_caller='CLOSE()',
            context=context,
            query=query,
        )


CLOSE_MSG_HANDLER = CallbackQueryHandler(
    close,
    pattern=f'^{{"command":"{ESCAPED_CALLBACK_CLOSE}"'
)
