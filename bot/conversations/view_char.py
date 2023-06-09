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

from bot.constants.view_char import COMMANDS
from bot.constants.create_char import COMMANDS as create_char_commands
from bot.constants.filters import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.decorators import print_basic_infos
from bot.functions.general import get_attribute_group_or_player

from repository.mongo import CharacterModel


@print_basic_infos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_message.reply_chat_action(ChatAction.TYPING)
    char_model = CharacterModel()
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    silent = get_attribute_group_or_player(chat_id, 'silent')
    args = context.args

    player_character = char_model.get(user_id)
    verbose = False
    if len(args) in [1, 2]:
        if args[0].startswith('@'):
            player_name = args[0]
            query = {'player_name': player_name}
            new_player_character = char_model.get(query=query)
            if not new_player_character:
                await update.effective_message.reply_text(
                    f'{player_name} não possui um personamgem.',
                    disable_notification=silent
                )
                return
            player_character = new_player_character
            verbose = 'verbose' in args[1:2] or 'v' in args[1:2]
        else:
            verbose = 'verbose' in args[0] or 'v' in args[0]

    if (player_character):
        markdown_player_sheet = player_character.get_all_sheets(
            verbose=verbose, markdown=True
        )
        await update.effective_message.reply_text(
            f'{markdown_player_sheet}',
            parse_mode=ParseMode.MARKDOWN_V2,
            disable_notification=silent
        )
    else:
        await update.effective_message.reply_text(
            f'Você ainda não criou um personagem!\n'
            f'Crie o seu personagem com o comando /{create_char_commands[0]}.',
            disable_notification=silent
        )

VIEW_CHAR_HANDLERS = [
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
