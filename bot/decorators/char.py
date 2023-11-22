from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.constants.create_char import COMMANDS
from repository.mongo import CharacterModel, StatusModel
from rpgram.conditions.debuff import IMMOBILIZED_DEBUFFS_NAMES
from rpgram.enums.debuff import DEBUFF_FULL_NAMES


def need_have_char(callback):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        print('@NEED_HAVE_CHAR')
        char_model = CharacterModel()
        user_id = update.effective_user.id

        if char_model.exists(user_id):
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

        if char_model.exists(user_id):
            return await callback(update, context)
        else:
            print(f'\tUSER: {user_id} SKIPPED in CHAT: {chat_id} - NO CHAR')
            return ConversationHandler.END
    return wrapper


def skip_if_dead_char(callback):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(f'@SKIP_IF_DEAD_CHAR')
        char_model = CharacterModel()
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id
        char = char_model.get(user_id)

        if char and char.is_alive():
            return await callback(update, context)
        else:
            print(f'\tUSER: {user_id} SKIPPED in CHAT: {chat_id} - DEAD CHAR')
            query = update.callback_query
            char_hit_points = ''
            if char:
                char_hit_points = f'HP: {char.combat_stats.show_hit_points}'
            if query:
                await query.answer(
                    f'Essa ação não pode ser realizada, pois seu personagem '
                    f'está morto.\n\n'
                    f'{char_hit_points}',
                    show_alert=True
                )
            return ConversationHandler.END
    return wrapper


def skip_if_immobilized(callback):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        print('@SKIP_IF_IMMOBILIZED')
        char_model = CharacterModel()
        status_model = StatusModel()
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id
        # char = char_model.get(user_id)
        query = {
            'player_id': user_id,
            'condition_args.name': {
                '$in': IMMOBILIZED_DEBUFFS_NAMES
            }
        }
        status = status_model.get(query=query, fields=['condition_args'])
        if not status:
            return await callback(update, context)
        else:
            print(
                f'\tUSER: {user_id} SKIPPED in '
                f'CHAT: {chat_id} - IMMOBILIZED CHAR'
            )
            query = update.callback_query
            conditions = status['condition_args']
            text = (
                f'Essa ação não pode ser realizada, pois seu personagem '
                f'está '
            )
            conditions_names = [
                DEBUFF_FULL_NAMES[condition['name'].upper()]
                for condition in conditions
                if condition['name'] in IMMOBILIZED_DEBUFFS_NAMES
            ]
            text += ', '.join(conditions_names)
            if query:
                await query.answer(text, show_alert=True)
            else:
                await update.effective_message.reply_text(text)
            return ConversationHandler.END
    return wrapper
