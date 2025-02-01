'''
Módulo responsável por gerenciar as requisiçães de visualização de 
informações dos grupos.
'''


from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    PrefixHandler,
)

from bot.constants.view_group import COMMANDS, SECTION_TEXT_GROUP
from bot.constants.filters import (
    BASIC_COMMAND_IN_GROUP_FILTER,
    PREFIX_COMMANDS
)
from bot.functions.chat import (
    MIN_AUTODELETE_TIME,
    reply_text
)
from bot.decorators import print_basic_infos, need_singup_group
from bot.functions.config import update_total_players
from constant.text import SECTION_HEAD_GROUP_END, SECTION_HEAD_GROUP_START
from function.text import create_text_in_box

from repository.mongo import GroupModel
from rpgram import Group


@print_basic_infos
@need_singup_group
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    group_model = GroupModel()
    chat_id = update.effective_chat.id

    group: Group = group_model.get(chat_id)
    update_total_players(group=group)
    if group:
        text = create_text_in_box(
            text=f'{group}',
            section_name=SECTION_TEXT_GROUP,
            section_start=SECTION_HEAD_GROUP_START,
            section_end=SECTION_HEAD_GROUP_END,
            clean_func=None
        )
        await reply_text(
            function_caller='VIEW_GROUP.START()',
            text=text,
            context=context,
            update=update,
            close_by_owner=False,
            need_response=False,
            auto_delete_message=MIN_AUTODELETE_TIME,
        )


VIEW_GROUP_HANDLERS = [
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
