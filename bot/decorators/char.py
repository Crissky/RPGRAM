from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.conversation.create_char import COMMANDS
from repository.mongo import CharacterModel


def need_have_char(callback):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        print('@NEED_HAVE_CHAR')
        char_model = CharacterModel()
        user_id = update.effective_user.id

        if char_model.get(user_id):
            print('\tAUTORIZADO - USUÁRIO POSSUI PERSONAGEM.')
            return await callback(update, context)
        else:
            await update.effective_message.reply_text(
                f'Você ainda não criou um personagem!\n'
                f'Crie o seu personagem com o comando /{COMMANDS[0]}.'
            )
            return ConversationHandler.END
    return wrapper


def skip_if_no_have_char(callback):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(f'@SKIP_IF_NO_HAVE_CHAR')
        char_model = CharacterModel()
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id

        if char_model.get(user_id):
            return await callback(update, context)
        else:
            print(f'\tUSER: {user_id} SKIPPED in CHAT: {chat_id} - NO CHAR')
            return ConversationHandler.END
    return wrapper
