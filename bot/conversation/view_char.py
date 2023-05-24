'''
Arquivo responsável por gerenciar as requisiçães de visualização das 
informações dos jogadores.
'''

from telegram import Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    PrefixHandler,
)
from bot.conversation.constants import BASIC_COMMAND_FILTER, PREFIX_COMMANDS

from bot.conversation.create_char import COMMANDS as create_char_commands
from bot.decorators import print_basic_infos
from repository.mongo import PlayerCharacterModel


COMMANDS = ['personagem', 'char']


@print_basic_infos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_message.reply_chat_action(ChatAction.TYPING)
    player_char_model = PlayerCharacterModel()
    user_id = update.effective_user.id
    args = context.args

    verbose = False
    if len(args) == 1:
        verbose = 'verbose' == args[0] or 'v' == args[0]

    if (player_character := player_char_model.get(user_id)):
        markdown_player_sheet = player_character.get_all_sheets(
            verbose=verbose, markdown=True
        )
        await update.effective_message.reply_text(
            f'{markdown_player_sheet}',
            parse_mode=ParseMode.MARKDOWN_V2
        )
    else:
        await update.effective_message.reply_text(
            f'Você ainda não criou um personagem!\n'
            f'Crie o seu personagem com o comando /{create_char_commands[0]}.'
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
