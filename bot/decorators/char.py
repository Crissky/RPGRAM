from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from repository.mongo import PlayerCharacterModel
from bot.conversation.create_char import COMMANDS


def need_have_char(callback):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        print('@NEED_HAVE_CHAR')
        player_char_model = PlayerCharacterModel()
        user_id = update.effective_user.id

        if player_char_model.get(user_id):
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
        player_char_model = PlayerCharacterModel()
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id

        if player_char_model.get(user_id):
            return await callback(update, context)
        else:
            print(f'\tUSER: {user_id} SKIPPED in CHAT: {chat_id} - NO CHAR')
            return ConversationHandler.END
    return wrapper
