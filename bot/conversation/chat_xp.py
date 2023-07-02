'''
Módulo responsável por gerenciar o ganho de xp dos jogadores ao enviarem 
mensagens nos grupos.
'''


from random import randint

from telegram import Update
from telegram.error import Forbidden
from telegram.ext import (
    ContextTypes,
    MessageHandler
)

from bot.constants.filters import ALLOW_GAIN_XP_FILTER
from bot.decorators import (
    skip_if_dead_char,
    skip_if_no_singup_group,
    skip_if_no_singup_player,
    print_basic_infos
)
from bot.functions.general import get_attribute_group_or_player

from functions.datetime import (
    utc_to_brazil_datetime,
    add_random_minutes_now,
    replace_tzinfo
)

from repository.mongo import (
    GroupModel,
    CharacterModel,
    PlayerModel
)


@skip_if_no_singup_group
@skip_if_no_singup_player
@skip_if_dead_char
@print_basic_infos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    player_model = PlayerModel()
    char_model = CharacterModel()
    group_model = GroupModel()

    user_name = update.effective_user.name
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    message_date = update.effective_message.date
    message_date = utc_to_brazil_datetime(message_date)
    silent = get_attribute_group_or_player(chat_id, 'silent')

    if user_id in context.user_data:
        player = context.user_data[user_id]
    else:
        player = player_model.get(user_id)

    if (xp_cooldown := player.xp_cooldown):
        xp_cooldown = replace_tzinfo(xp_cooldown)
        if message_date < xp_cooldown:
            print('XP em cooldown.')
            return

    player_char = char_model.get(user_id)
    group = group_model.get(chat_id)

    player.xp_cooldown = add_random_minutes_now(message_date)
    context.user_data[user_id] = player
    player_model.save(player)

    level = player_char.base_stats.level
    level_bonus = group.character_multiplier_xp * level
    multiplier_xp = group.multiplier_xp

    add_xp = int((randint(1, 10) + level_bonus) * multiplier_xp)

    player_char.base_stats.xp = add_xp
    char_model.save(player_char)
    new_level = player_char.base_stats.level

    if new_level > level:
        await update.effective_message.reply_text(
            f'Parabéns!!!\n'
            f'{user_name} passou de nível! '
            f'Seu personagem agora está no nível {new_level}.',
            disable_notification=silent
        )
    elif player.verbose:
        try:
            await update.effective_user.send_message(
                f'Você ganhou {add_xp} de XP.\n'
                f'Experiência: {player_char.bs.show_xp}',
                disable_notification=silent
            )
        except Forbidden as error:
            print(
                'Usuário não pode receber mensagens privadas. '
                'Ele precisa iniciar uma conversa com o bot. '
                f'(Erro: {error})'
            )


CHAT_XP_HANDLER = MessageHandler(
    ALLOW_GAIN_XP_FILTER,
    start
)
