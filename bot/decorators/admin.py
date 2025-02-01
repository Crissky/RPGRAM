from telegram import Update
from telegram.constants import ChatMemberStatus
from telegram.ext import ContextTypes, ConversationHandler

from bot.functions.chat import (
    MIN_AUTODELETE_TIME,
    call_telegram_message_function,
    reply_text
)


def need_are_admin(callback):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        print('@NEED_ARE_ADMIN')
        status = None
        user_id = update.effective_user.id
        get_member_kwags = dict(user_id=user_id)
        chat_member = await call_telegram_message_function(
            function_caller='ADMIN.NEED_ARE_ADMIN()',
            function=update.effective_chat.get_member,
            context=context,
            need_response=True,
            skip_retry=False,
            **get_member_kwags
        )
        if chat_member:
            status = chat_member.status

        if status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            print('\tAUTORIZADO')
            return await callback(update, context)
        else:
            text = f'Esse comando só pode ser usado por administradores.'
            await reply_text(
                function_caller='ADMIN.START()',
                text=text,
                context=context,
                update=update,
                allow_sending_without_reply=True,
                need_response=False,
                skip_retry=False,
                auto_delete_message=MIN_AUTODELETE_TIME,
            )
            return ConversationHandler.END
    return wrapper
