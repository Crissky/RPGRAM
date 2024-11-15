from operator import attrgetter
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    PrefixHandler,
)

from bot.constants.filters import (
    BASIC_COMMAND_IN_GROUP_FILTER,
    PREFIX_COMMANDS
)
from bot.constants.view_level import COMMANDS, SECTION_TEXT_LEVEL_CHARS
from bot.decorators import (
    need_singup_group,
    need_singup_player,
    print_basic_infos
)
from bot.functions.char import get_player_chars_from_group
from bot.functions.chat import (
    call_telegram_message_function,
    get_close_keyboard
)
from bot.functions.general import get_attribute_group_or_player
from constant.text import (
    SECTION_HEAD_LEVEL_CHARS_END,
    SECTION_HEAD_LEVEL_CHARS_START
)
from function.text import create_text_in_box
from rpgram.constants.text import LEVEL_EMOJI_TEXT, XP_EMOJI_TEXT


@print_basic_infos
@need_singup_player
@need_singup_group
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    silent = get_attribute_group_or_player(chat_id, 'silent')
    char_list = get_player_chars_from_group(chat_id=chat_id, is_alive=False)
    char_list = sorted(
        char_list,
        key=attrgetter('level', 'xp'),
        reverse=True
    )
    text = ''

    for i, char in enumerate(char_list):
        i += 1
        text += (
            f'{i:02}. {char.player_name}\n'
            f'*{LEVEL_EMOJI_TEXT}*: {char.level}\n'
            f'*{XP_EMOJI_TEXT}*: {char.bs.show_xp}\n\n'
        )

    text = create_text_in_box(
        text=text,
        section_name=SECTION_TEXT_LEVEL_CHARS,
        section_start=SECTION_HEAD_LEVEL_CHARS_START,
        section_end=SECTION_HEAD_LEVEL_CHARS_END,
    )
    reply_text_kwargs = dict(
        text=text,
        parse_mode=ParseMode.MARKDOWN_V2,
        disable_notification=silent,
        reply_markup=get_close_keyboard(None),
        allow_sending_without_reply=True
    )
    await call_telegram_message_function(
        function_caller='VIEW_LEVEL.START()',
        function=update.effective_message.reply_text,
        context=context,
        need_response=False,
        skip_retry=False,
        **reply_text_kwargs,
    )


VIEW_LEVEL_HANDLERS = [
    PrefixHandler(
        PREFIX_COMMANDS,
        COMMANDS,
        start,
        BASIC_COMMAND_IN_GROUP_FILTER
    ),
    CommandHandler(
        COMMANDS,
        start,
        BASIC_COMMAND_IN_GROUP_FILTER
    )
]
