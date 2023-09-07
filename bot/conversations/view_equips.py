'''
Módulo responsável por gerenciar as requisiçães de visualização das 
informações dos jogadores.
'''


from telegram import Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    PrefixHandler,
)

from bot.constants.view_equips import COMMANDS
from bot.constants.filters import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.decorators import need_have_char, print_basic_infos
from bot.functions.general import get_attribute_group_or_player

from repository.mongo import CharacterModel, EquipsModel


@print_basic_infos
@need_have_char
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_message.reply_chat_action(ChatAction.TYPING)
    char_model = CharacterModel()
    equips_model = EquipsModel()
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    silent = get_attribute_group_or_player(chat_id, 'silent')
    args = context.args
    equips = equips_model.get(user_id)

    if not equips:
        player_character = char_model.get(user_id)
        equips = player_character.equips
        equips_model.save(player_character.equips)

    verbose = False
    if args:
        verbose = 'verbose' in args[0] or 'v' in args[0]

    if equips:
        markdown_player_sheet = equips.get_all_sheets(
            verbose=verbose, markdown=True
        )
        await update.effective_message.reply_text(
            f'{markdown_player_sheet}',
            parse_mode=ParseMode.MARKDOWN_V2,
            disable_notification=silent
        )
    else:
        await update.effective_message.reply_text(
            f'Seu personagem ainda não possui equipamentos.\n'
            f'Equips: {equips}',
            disable_notification=silent
        )

VIEW_EQUIPS_HANDLERS = [
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
    )
]
