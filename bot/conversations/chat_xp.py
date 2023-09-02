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
from bot.functions.char import add_xp
from bot.functions.general import get_attribute_group_or_player

from function.datetime import (
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

    player.xp_cooldown = add_random_minutes_now(message_date)
    context.user_data[user_id] = player
    player_model.save(player)

    report_xp = add_xp(chat_id, user_id)
    level_up = report_xp['level_up']

    if level_up:
        group = report_xp['group']
        new_level = report_xp['level']
        await update.effective_message.reply_text(
            f'Parabéns!!!\n'
            f'{user_name} passou de nível! '
            f'Seu personagem agora está no nível {new_level}.',
            disable_notification=silent
        )
        if new_level > group.higher_level:
            group.higher_level = new_level
            group_model.save(group)
    elif player.verbose:
        xp = report_xp['xp']
        player_char = report_xp['char']
        try:
            await update.effective_user.send_message(
                f'Você ganhou {xp} de XP.\n'
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
