from telegram import Update
from telegram.ext import (
    PrefixHandler,
    ContextTypes
)
from bot.conversation.create_char import COMMANDS as create_char_commands
from bot.conversation.sign_up_group import COMMANDS as sign_up_group_commands
from bot.conversation.sign_up_player import COMMANDS as sign_up_player_commands


COMMANDS = ['help', 'ajuda']


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    create_char_cmd = '\n'.join([f'!{cmd}'for cmd in create_char_commands])
    sign_up_player_cmd = '\n'.join(
        [f'!{cmd}'for cmd in sign_up_player_commands]
    )
    sign_up_group_cmd = '\n'.join([f'!{cmd}'for cmd in sign_up_group_commands])
    await update.message.reply_text(
        f'COMANDOS:\n\n'
        f'Criar Conta do Grupo: /criargrupo\n'
        f'Atalhos:\n'
        f'{sign_up_group_cmd}\n\n'
        
        f'Criar Conta de Jogador: /criargrupo\n'
        f'Atalhos:\n'
        f'{sign_up_player_cmd}\n\n'
        
        f'Criar Personagem: /criargrupo\n'
        f'Atalhos:\n'
        f'{create_char_cmd}\n\n'
    )

HELP_HANDLER = PrefixHandler(['!', '/'], COMMANDS, help)