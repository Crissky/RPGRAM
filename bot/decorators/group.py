from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.constants.sign_up_group import COMMANDS
from repository.mongo import GroupModel


def need_singup_group(callback):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        print('@NEED_SINGUP_GROUP')
        group_model = GroupModel()
        chat_id = update.effective_chat.id

        if group_model.exists(chat_id):
            print('\tAUTORIZADO - GRUPO POSSUI CADASTRO.')
            return await callback(update, context)
        else:
            await update.effective_message.reply_text(
                f'É necessário cadastrar o grupo para utilizar esse comando.\n'
                f'Cadastre o grupo com o comando /{COMMANDS[0]}.',
                allow_sending_without_reply=True
            )
            return ConversationHandler.END
    return wrapper


def skip_if_no_singup_group(callback):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(f'@SKIP_IF_NO_SINGUP_GROUP')
        group_model = GroupModel()
        chat_id = update.effective_chat.id

        if group_model.exists(chat_id):
            return await callback(update, context)
        else:
            print(f'\tSKIPPED in CHAT: {chat_id} - NO ACCOUNT GROUP')
            return ConversationHandler.END
    return wrapper
