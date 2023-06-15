'''
Módulo responsável por gerenciar os comandos de ajuda.
'''


from typing import Iterable

from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    PrefixHandler,
)

from bot.constants.help import COMMANDS
from bot.constants.add_stats import COMMANDS as add_stats_commands
from bot.constants.battle import COMMANDS as battle_commands
from bot.constants.config_group import COMMANDS as config_group_commands
from bot.constants.config_player import COMMANDS as config_player_commands
from bot.constants.create_char import COMMANDS as create_char_commands
from bot.constants.sign_up_group import COMMANDS as sign_up_group_commands
from bot.constants.sign_up_player import COMMANDS as sign_up_player_commands
from bot.constants.view_char import COMMANDS as view_char_commands
from bot.constants.view_group import COMMANDS as view_group_commands
from bot.constants.view_player import COMMANDS as view_player_commands
from bot.conversation.filters import (
    BASIC_COMMAND_FILTER,
    PREFIX_COMMANDS
)
from bot.decorators import print_basic_infos

from constants.text import SECTION_HEAD

from functions.text import escape_basic_markdown_v2


@print_basic_infos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sign_up_group_cmd = command_to_string(sign_up_group_commands)
    sign_up_player_cmd = command_to_string(sign_up_player_commands)
    create_char_cmd = command_to_string(create_char_commands)
    view_group_cmd = command_to_string(view_group_commands)
    view_player_cmd = command_to_string(view_player_commands)
    view_char_cmd = command_to_string(view_char_commands)
    add_stats_cmd = command_to_string(add_stats_commands)
    config_group_cmd = command_to_string(config_group_commands)
    config_player_cmd = command_to_string(config_player_commands)
    battle_cmd = command_to_string(battle_commands)

    text = escape_basic_markdown_v2(
        f'{SECTION_HEAD.format("COMANDOS")}\n\n'

        f'CRIAR CONTA DO GRUPO: /{sign_up_group_commands[0]}\n'
        f'Atalhos: {sign_up_group_cmd}\n\n'

        f'CRIAR CONTA DE JOGADOR: /{sign_up_player_commands[0]}\n'
        f'Atalhos: {sign_up_player_cmd}\n\n'

        f'CRIAR PERSONAGEM: /{create_char_commands[0]}\n'
        f'Atalhos: {create_char_cmd}\n\n'

        f'INFORMAÇÕES DO GRUPO: /{view_group_commands[0]}\n'
        f'Atalhos: {view_group_cmd}\n\n'

        f'INFORMAÇÕES DO JOGADOR: /{view_player_commands[0]}\n'
        f'Atalhos: {view_player_cmd}\n\n'

        f'INFORMAÇÕES DO PERSONAGEM: /{view_char_commands[0]}\n'
        f'Atalhos: {view_char_cmd}\n\n'

        f'ADICIONAR ESTATISTICAS: /{add_stats_commands[0]}\n'
        f'Argumentos: [<ATRIBUTO> <VALOR>]\n'
        f'Exemplo: "/{add_stats_commands[0]} FOR 10" '
        f'(Adiciona 10 pontos em FORÇA).\n'
        f'OBS: Pode ser usado sem argumentos para exibir as estatísticas. '
        f'Use o argumento "verbose" ou "v" para exibir com mais detalhes\n'
        f'Atalhos: {add_stats_cmd}\n\n'

        f'CONFIGURAÇÃO DO GRUPO: /{config_group_commands[0]}\n'
        f'Argumentos: [<CONFIGURAÇÃO> <VALOR>]\n'
        f'Configurações:\n'
        f'    "verbose": [true/false]. Configura se o bot vai falar muito.\n'
        f'    "spawn_start_time": inteiro[0-24]. Hora de início do spawn.\n'
        f'    "spawn_end_time": inteiro[0-24]. Hora de fim do spawn.\n'
        f'    "multiplier_xp": decimal[0-5]. Multiplicador de XP.\n'
        f'    "char_multiplier_xp": decimal[0-10]. Multiplicador do bônus de '
        f'XP baseado no nível do personagem.\n'
        f'Atalhos: {config_group_cmd}\n\n'

        f'CONFIGURAÇÃO DO JOGADOR: /{config_player_commands[0]}\n'
        f'Argumentos: [<CONFIGURAÇÃO> <VALOR>]\n'
        f'Configurações:\n'
        f'    "verbose": [true/false]. Configura se o bot vai envia mensagens '
        f'privadas.\n'
        f'Atalhos: {config_player_cmd}\n\n'

        f'CRIAR BATALHA: /{battle_commands[0]}\n'
        f'Atalhos: {battle_cmd}\n'
    )
    await update.effective_message.reply_markdown_v2(text)


def command_to_string(commands: Iterable) -> str:
    return ', '.join([f'`!{cmd}`'for cmd in commands])


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
