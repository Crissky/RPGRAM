'''
Módulo responsável por gerenciar as requisiçães de visualização das 
informações dos jogadores.
'''


from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    PrefixHandler,
)

from bot.constants.reset_char import (
    COMMANDS,
)
from bot.constants.view_char import (
    ACCESS_DENIED,
    SECTION_TEXT_CHAR
)
from bot.constants.filters import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.functions.char import save_char
from bot.functions.chat import (
    reply_text,
    reply_typing
)
from bot.decorators import print_basic_infos
from bot.decorators.player import alert_if_not_chat_owner
from constant.text import SECTION_HEAD_CHAR_END, SECTION_HEAD_CHAR_START
from function.text import create_text_in_box

from repository.mongo import CharacterModel
from rpgram.characters import BaseCharacter


@alert_if_not_chat_owner(alert_text=ACCESS_DENIED)
@print_basic_infos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await reply_typing(
        function_caller='RESET_CHAR.START()',
        update=update,
        context=context,
    )
    char_model = CharacterModel()
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    player_character: BaseCharacter = char_model.get(user_id)

    if player_character:
        player_character.bs.reset_stats()
        save_char(char=player_character)
        markdown_player_sheet = player_character.get_all_sheets(
            verbose=False,
            markdown=True
        )
        markdown_player_sheet = create_text_in_box(
            text=markdown_player_sheet,
            section_name=SECTION_TEXT_CHAR,
            section_start=SECTION_HEAD_CHAR_START,
            section_end=SECTION_HEAD_CHAR_END
        )

        await reply_text(
            function_caller='REST_STATS()',
            text=markdown_player_sheet,
            context=context,
            user_id=user_id,
            update=update,
            chat_id=chat_id,
            need_response=False,
            markdown=True,
        )

RESET_CHAR_HANDLERS = [
    PrefixHandler(
        PREFIX_COMMANDS,
        COMMANDS,
        start,
        BASIC_COMMAND_FILTER
    ),
    CommandHandler(
        COMMANDS,
        start,
        BASIC_COMMAND_FILTER
    ),
]
