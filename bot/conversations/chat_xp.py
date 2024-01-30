'''
Módulo responsável por gerenciar o ganho de xp dos jogadores ao enviarem 
mensagens nos grupos.
'''


from telegram import Update
from telegram.ext import (
    ContextTypes,
    MessageHandler
)

from bot.constants.filters import ALLOW_GAIN_XP_FILTER
from bot.decorators import (
    skip_if_no_singup_group,
    skip_if_no_singup_player,
    print_basic_infos
)
from bot.decorators.char import skip_if_dead_char_silent
from bot.functions.char import add_xp
from bot.functions.chat import send_private_message
from bot.functions.general import get_attribute_group_or_player
from constant.text import SECTION_HEAD_XP_END, SECTION_HEAD_XP_START

from function.date_time import (
    utc_to_brazil_datetime,
    add_random_minutes_now,
    replace_tzinfo
)
from function.text import create_text_in_box

from repository.mongo import (
    PlayerModel
)


SECTION_TEXT_XP = 'EXPERIÊNCIA'


@skip_if_no_singup_group
@skip_if_no_singup_player
@skip_if_dead_char_silent
@print_basic_infos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    player_model = PlayerModel()

    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    message_date = update.effective_message.date
    message_date = utc_to_brazil_datetime(message_date)
    silent = get_attribute_group_or_player(chat_id, 'silent')

    player = player_model.get(user_id)

    if (xp_cooldown := player.xp_cooldown):
        xp_cooldown = replace_tzinfo(xp_cooldown)
        if message_date < xp_cooldown:
            print('XP em cooldown.')
            return None

    player.xp_cooldown = add_random_minutes_now(message_date)
    player_model.save(player)

    report_xp = add_xp(chat_id, user_id)
    text = report_xp['text']
    text = create_text_in_box(
        text=text,
        section_name=SECTION_TEXT_XP,
        section_start=SECTION_HEAD_XP_START,
        section_end=SECTION_HEAD_XP_END,
        clean_func=None,
    )

    if report_xp['level_up']:
        await update.effective_message.reply_text(
            text=text,
            disable_notification=silent,
            allow_sending_without_reply=True
        )
    elif player.verbose:
        await send_private_message(
            function_caller='CHAT_XP.START()',
            context=context,
            user_id=user_id,
            text=text,
        )


CHAT_XP_HANDLER = MessageHandler(
    ALLOW_GAIN_XP_FILTER,
    start
)
