from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.constants.sign_up_player import COMMANDS
from bot.functions.chat import (
    MIN_AUTODELETE_TIME,
    answer,
    callback_data_to_dict,
    reply_text
)
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
            text = (
                f'Você precisa criar sua conta '
                f'para utilizar esse comando.\n'
                f'Crie a conta com o comando /{COMMANDS[0]}.'
            )
            await reply_text(
                function_caller='PLAYER.NEED_SINGUP_PLAYER()',
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


def alert_if_not_chat_owner(
    retry_state=ConversationHandler.END,
    alert_text='⛔VOCÊ NÃO TEM ACESSO A ESSA MENSAGEM⛔'
):
    '''Não executa a ação quando o botão é clicado por um usuário que não 
    seja o dono da mensagem e envia um alerta para o usuário que clicou no 
    botão.'''

    def decorator(callback):
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            print('@SKIP_IF_NOT_CHAT_OWNER')
            user_id = update.effective_user.id
            query = update.callback_query

            if query:
                data = eval(query.data)
                data_user_id = data['user_id']
                if data_user_id != user_id and data_user_id is not None:
                    if isinstance(alert_text, str):
                        await answer(
                            query=query,
                            text=alert_text,
                            show_alert=True
                        )
                    return retry_state

            return await callback(update, context)

        return wrapper
    return decorator


def alert_if_not_chat_owner_to_callback_data_to_dict(
    retry_state=ConversationHandler.END,
    alert_text='⛔VOCÊ NÃO TEM ACESSO A ESSA MENSAGEM⛔'
):
    '''Não executa a ação quando o botão é clicado por um usuário que não 
    seja o dono da mensagem e envia um alerta para o usuário que clicou no 
    botão.'''

    def decorator(callback):
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            print('@ALERT_IF_NOT_CHAT_OWNER_TO_CALLBACK_DATA_TO_DICT')
            user_id = update.effective_user.id
            query = update.callback_query

            if query:
                data = callback_data_to_dict(query.data)
                data_user_id = data['user_id']
                if data_user_id != user_id and data_user_id is not None:
                    if isinstance(alert_text, str):
                        await answer(
                            query=query,
                            text=alert_text,
                            show_alert=True
                        )
                    return retry_state

            return await callback(update, context)

        return wrapper
    return decorator


def alert_if_not_chat_owner_to_anyway(
    retry_state=ConversationHandler.END,
    alert_text='⛔VOCÊ NÃO TEM ACESSO A ESSA MENSAGEM⛔'
):
    '''Não executa a ação quando o botão é clicado por um usuário que não 
    seja o dono da mensagem e envia um alerta para o usuário que clicou no 
    botão.'''

    def decorator(callback):
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            print('@ALERT_IF_NOT_CHAT_OWNER_TO_ANYWAY')
            user_id = update.effective_user.id
            query = update.callback_query

            if query:
                try:
                    data = callback_data_to_dict(query.data)
                except TypeError as e:
                    print('@ALERT_IF_NOT_CHAT_OWNER_TO_ANYWAY', e)
                    data = eval(query.data)
                data_user_id = data['user_id']
                if data_user_id != user_id and data_user_id is not None:
                    if isinstance(alert_text, str):
                        await answer(
                            query=query,
                            text=alert_text,
                            show_alert=True
                        )
                    return retry_state

            return await callback(update, context)

        return wrapper
    return decorator
