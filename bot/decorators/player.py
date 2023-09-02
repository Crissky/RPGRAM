from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.constants.sign_up_player import COMMANDS
from repository.mongo import PlayerModel


def need_singup_player(callback):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        print('@NEED_SINGUP_PLAYER')
        player_model = PlayerModel()
        user_id = update.effective_user.id

        if player_model.exists(user_id):
            print('\tAUTORIZADO - USUÁRIO POSSUI CONTA.')
            return await callback(update, context)
        else:
            await update.effective_message.reply_text(
                f'Você precisa criar sua conta para utilizar esse comando.\n'
                f'Crie a conta com o comando /{COMMANDS[0]}.'
            )
            return ConversationHandler.END
    return wrapper


def skip_if_no_singup_player(callback):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(f'@SKIP_IF_NO_SINGUP_PLAYER')
        player_model = PlayerModel()
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id

        if player_model.exists(user_id):
            return await callback(update, context)
        else:
            print(f'\tUSER: {user_id} SKIPPED in CHAT: {chat_id} - NO ACCOUNT')
            return ConversationHandler.END
    return wrapper
