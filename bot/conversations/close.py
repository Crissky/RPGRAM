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


@alert_if_not_chat_owner(alert_text=ACCESS_DENIED)
@print_basic_infos
@skip_if_no_have_char
async def close(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    if query:
        await query.answer('Fechando conversa...')
        await query.delete_message()


CLOSE_MSG_HANDLER = CallbackQueryHandler(
    close,
    pattern=f'^{{"command":"{ESCAPED_CALLBACK_CLOSE}"'
)
