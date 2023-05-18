from random import randint

from telegram import Update
from telegram.ext import (
    ContextTypes,
    MessageHandler
)

from bot.conversation.constants import ALLOW_WRITE_TEXT_IN_GROUP_FILTER
from bot.decorators import (
    skip_if_no_have_char,
    print_basic_infos
)
from functions.datetime import get_brazil_time_now, add_random_minutes_now
from repository.mongo import (
    GroupConfigurationModel,
    PlayerCharacterModel,
    PlayerModel
)


@skip_if_no_have_char
@print_basic_infos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    player_model = PlayerModel()
    player_char_model = PlayerCharacterModel()
    group_config_model = GroupConfigurationModel()
    user_id = update.effective_user.id
    user_name = update.effective_user.name
    chat_id = update.effective_chat.id
    now = get_brazil_time_now()

    if user_id in context.user_data:
        player = context.user_data[user_id]
    else:
        player = player_model.get(user_id)

    if (xp_cooldown := player.xp_cooldown):
        if now < xp_cooldown:
            print('XP em cooldown.')
            return

    group_config = group_config_model.get(chat_id)
    player_char = player_char_model.get(user_id)

    player.xp_cooldown = add_random_minutes_now()
    context.user_data[user_id] = player
    player_model.save(player)

    level = player_char.base_stats.level
    level_multiplier_xp = group_config.player_multiplier_xp * level
    multiplier_xp = group_config.multiplier_xp

    add_xp = (randint(1, 5) + level_multiplier_xp) * multiplier_xp

    player_char.base_stats.xp = add_xp
    player_char_model.save(player_char)
    new_level = player_char.base_stats.level

    if new_level > level:
        await update.effective_message.reply_text(
            f'Parabéns!!!\n'
            f'{user_name} passou de nível! '
            f'Seu personagem agora está no nível {new_level}.'
        )


CHAT_XP_HANDLER = MessageHandler(
    ALLOW_WRITE_TEXT_IN_GROUP_FILTER,
    start
)
