from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.functions.chat import call_telegram_message_function
from repository.mongo import BattleModel, CharacterModel


def need_not_in_battle(callback):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        print('@NEED_NOT_IN_BATTLE')
        battle_model = BattleModel()
        character_model = CharacterModel()
        user_id = update.effective_user.id
        character = character_model.get(user_id)
        character_id = character._id
        battle = battle_model.get(
            query={'$or': [
                {'blue_team': character_id},
                {'red_team': character_id}
            ]}
        )

        if not battle or not battle.started:
            print('\tAUTORIZADO - USUÁRIO NÃO ESTÁ EM BATALHA.')
            return await callback(update, context)
        else:
            chat = await update.get_bot().get_chat(battle.chat_id)
            chat_name = chat.effective_name
            reply_text_kwargs = dict(
                text=(
                    f'Você não pode usar esse comando enquanto '
                    f'estiver em batalha.\n'
                    f'Você está em uma batalha no grupo "{chat_name}".'
                ),
                allow_sending_without_reply=True
            )
            await call_telegram_message_function(
                function_caller='BATTLE.NEED_NOT_IN_BATTLE()',
                function=update.effective_message.reply_text,
                context=context,
                need_response=False,
                skip_retry=False,
                **reply_text_kwargs,
            )
            return ConversationHandler.END
    return wrapper
