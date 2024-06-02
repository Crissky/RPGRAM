from telegram import Update
from telegram.constants import ChatMemberStatus
from telegram.ext import ContextTypes, ConversationHandler

from bot.functions.chat import call_telegram_message_function


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
            reply_text_kwargs = dict(
                text=f'Esse comando só pode ser usado por administradores.',
                allow_sending_without_reply=True
            )
            await call_telegram_message_function(
                function_caller='ADMIN.START()',
                function=update.effective_message.reply_text,
                context=context,
                need_response=False,
                skip_retry=False,
                **reply_text_kwargs,
            )
            return ConversationHandler.END
    return wrapper
