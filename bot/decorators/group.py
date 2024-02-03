from telegram import Update
from telegram.constants import ChatType
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


def allow_only_in_group(callback):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        print('@NEED_USE_IN_GROUP')
        if update.effective_chat.type == ChatType.PRIVATE:
            await update.effective_message.reply_text(
                f'Esse comando só pode ser usado em um grupo.',
                allow_sending_without_reply=True
            )
            return ConversationHandler.END
        else:
            return await callback(update, context)

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
