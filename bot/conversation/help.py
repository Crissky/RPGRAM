from typing import Iterable
from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    PrefixHandler,
)

from bot.conversation.constants import (
    BASIC_COMMAND_FILTER,
    PREFIX_COMMANDS
)
from bot.conversation.sign_up_group import COMMANDS as sign_up_group_commands
from bot.conversation.sign_up_player import COMMANDS as sign_up_player_commands
from bot.conversation.create_char import COMMANDS as create_char_commands
from bot.conversation.view_group import COMMANDS as view_group_commands
from bot.conversation.view_player import COMMANDS as view_player_commands
from bot.conversation.view_char import COMMANDS as view_char_commands


COMMANDS = ['help', 'ajuda']


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sign_up_group_cmd = command_to_string(sign_up_group_commands)
    sign_up_player_cmd = command_to_string(sign_up_player_commands)
    create_char_cmd = command_to_string(create_char_commands)
    view_group_cmd = command_to_string(view_group_commands)
    view_player_cmd = command_to_string(view_player_commands)
    view_char_cmd = command_to_string(view_char_commands)

    await update.effective_message.reply_text(
        f'COMANDOS:\n\n'
        f'CRIAR CONTA DO GRUPO: /{sign_up_group_commands[0]}\n'
        f'Atalhos:\n'
        f'{sign_up_group_cmd}\n\n'

        f'CRIAR CONTA DE JOGADOR: /{sign_up_player_commands[0]}\n'
        f'Atalhos:\n'
        f'{sign_up_player_cmd}\n\n'

        f'CRIAR PERSONAGEM: /{create_char_commands[0]}\n'
        f'Atalhos:\n'
        f'{create_char_cmd}\n\n'

        f'INFORMAÇÃES DO GRUPO: /{view_group_commands[0]}\n'
        f'Atalhos:\n'
        f'{view_group_cmd}\n\n'

        f'INFORMAÇÃES DO JOGADOR: /{view_player_commands[0]}\n'
        f'Atalhos:\n'
        f'{view_player_cmd}\n\n'

        f'INFORMAÇÃES DO PERSONAGEM: /{view_char_commands[0]}\n'
        f'Atalhos:\n'
        f'{view_char_cmd}\n\n'
    )


def command_to_string(command: Iterable) -> str:
    return '\n'.join([f'!{cmd}'for cmd in command])


HELP_HANDLERS = [
    PrefixHandler(
        PREFIX_COMMANDS,
        COMMANDS,
        help,
        BASIC_COMMAND_FILTER
    ),
    CommandHandler(
        COMMANDS,
        help,
        BASIC_COMMAND_FILTER
    )
]
