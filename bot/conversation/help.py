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
from bot.conversation.add_stats import COMMANDS as add_stats_commands
from bot.conversation.create_char import COMMANDS as create_char_commands
from bot.conversation.sign_up_group import COMMANDS as sign_up_group_commands
from bot.conversation.sign_up_player import COMMANDS as sign_up_player_commands
from bot.conversation.view_char import COMMANDS as view_char_commands
from bot.conversation.view_group import COMMANDS as view_group_commands
from bot.conversation.view_player import COMMANDS as view_player_commands
from bot.decorators import print_basic_infos
from constants.text import SECTION_HEAD


COMMANDS = ['help', 'ajuda']


@print_basic_infos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sign_up_group_cmd = command_to_string(sign_up_group_commands)
    sign_up_player_cmd = command_to_string(sign_up_player_commands)
    create_char_cmd = command_to_string(create_char_commands)
    view_group_cmd = command_to_string(view_group_commands)
    view_player_cmd = command_to_string(view_player_commands)
    view_char_cmd = command_to_string(view_char_commands)
    add_stats_cmd = command_to_string(add_stats_commands)

    await update.effective_message.reply_text(
        SECTION_HEAD.format('COMANDOS') + '\n'

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

        f'ADICIONAR ESTATISTICAS: /{add_stats_commands[0]}\n'
        f'Argumentos: [<ATRIBUTO> <VALOR>]\n'
        f'Exemplo: "/{add_stats_commands[0]} FOR 10" '
        f'(Adiciona 10 pontos em FORÇA).\n'
        f'OBS: Pode ser usado sem argumentos para exibir as estatísticas.\n'
        f'Atalhos:\n'
        f'{add_stats_cmd}\n'
    )


def command_to_string(command: Iterable) -> str:
    return '\n'.join([f'!{cmd}'for cmd in command])


HELP_HANDLERS = [
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
