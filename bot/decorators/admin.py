from telegram import Update
from telegram.constants import ChatMemberStatus
from telegram.ext import ContextTypes, ConversationHandler


def need_are_admin(callback):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        print('@NEED_ARE_ADMIN')
        status = None
        user_id = update.effective_user.id
        chat_member = await update.effective_chat.get_member(user_id)
        if chat_member:
            status = chat_member.status

        if status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            print('\tAUTORIZADO')
            return await callback(update, context)
        else:
            await update.effective_message.reply_text(
                f'Esse comando só pode ser usado por administradores.',
                allow_sending_without_reply=True
            )
            return ConversationHandler.END
    return wrapper
