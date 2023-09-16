'''
Módulo responsável por gerenciar os comandos de ajuda.
'''

from typing import Iterable

from telegram.constants import ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    PrefixHandler,
)

from bot.constants.help import ACCESS_DENIED, CALLBACK_BACK_HELP, COMMANDS
from bot.constants.add_stats import COMMANDS as add_stats_commands
from bot.constants.bag import COMMANDS as bag_commands
from bot.constants.battle import COMMANDS as battle_commands
from bot.constants.config_group import COMMANDS as config_group_commands
from bot.constants.config_player import COMMANDS as config_player_commands
from bot.constants.create_char import COMMANDS as create_char_commands
from bot.constants.sign_up_group import COMMANDS as sign_up_group_commands
from bot.constants.sign_up_player import COMMANDS as sign_up_player_commands
from bot.constants.view_char import COMMANDS as view_char_commands
from bot.constants.view_group import COMMANDS as view_group_commands
from bot.constants.view_player import COMMANDS as view_player_commands
from bot.constants.rest import COMMANDS as rest_commands
from bot.constants.view_equips import COMMANDS as view_equips_commands
from bot.constants.filters import (
    BASIC_COMMAND_FILTER,
    PREFIX_COMMANDS
)
from bot.decorators import print_basic_infos
from bot.functions.general import get_attribute_group_or_player

from constant.text import SECTION_HEAD

from function.text import escape_basic_markdown_v2
from rpgram.enums.emojis import EmojiEnum


@print_basic_infos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = update.effective_user.id
    if query:
        data = eval(query.data)
        data_user_id = data['user_id']
        # Não executa se outro usuário mexer na ajuda
        if data_user_id != user_id:
            await query.answer(text=ACCESS_DENIED, show_alert=True)
            return ConversationHandler.END

    chat_id = update.effective_chat.id
    silent = get_attribute_group_or_player(chat_id, 'silent')
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
    rest_cmd = command_to_string(rest_commands)
    bag_cmd = command_to_string(bag_commands)
    equips_cmd = command_to_string(view_equips_commands)

    text = escape_basic_markdown_v2(
        f'{SECTION_HEAD.format("COMANDOS")}\n\n'

        f'*CRIAR CONTA DO GRUPO*: /{sign_up_group_commands[0]}\n'
        f'INFO: Cria uma conta para o grupo.\n'
        f'Atalhos: {sign_up_group_cmd}\n\n'

        f'*CRIAR CONTA DE JOGADOR*: /{sign_up_player_commands[0]}\n'
        f'INFO: Cria uma conta para o jogador.\n'
        f'Atalhos: {sign_up_player_cmd}\n\n'

        f'*CRIAR PERSONAGEM*: /{create_char_commands[0]}\n'
        f'INFO: Cria um personagem para o jogador.\n'
        f'Atalhos: {create_char_cmd}\n\n'

        f'*INFORMAÇÕES DO GRUPO*: /{view_group_commands[0]}\n'
        f'INFO: Exibe as informações do grupo.\n'
        f'Atalhos: {view_group_cmd}\n\n'

        f'*INFORMAÇÕES DO JOGADOR*: /{view_player_commands[0]}\n'
        f'INFO: Exibe as informações do jogador.\n'
        f'Atalhos: {view_player_cmd}\n\n'

        f'*INFORMAÇÕES DO PERSONAGEM*: /{view_char_commands[0]}\n'
        f'INFO: Exibe as informações do personagem.\n'
        f'Atalhos: {view_char_cmd}\n\n'

        f'*ADICIONAR/EXIBIR ESTATISTICAS*: /{add_stats_commands[0]}\n'
        f'INFO: Exibe ou Adiciona estatisticas no personagem.\n'
        f'Atalhos: {add_stats_cmd}\n\n'

        f'*CONFIGURAÇÃO DO GRUPO*: /{config_group_commands[0]}\n'
        f'INFO: Configura preferências do grupo.\n'
        f'Atalhos: {config_group_cmd}\n\n'

        f'*CONFIGURAÇÃO DO JOGADOR*: /{config_player_commands[0]}\n'
        f'INFO: Configura preferências do jogador.\n'
        f'Atalhos: {config_player_cmd}\n\n'

        f'*CRIAR BATALHA*: /{battle_commands[0]}\n'
        f'INFO: Inicia uma batalha no grupo.\n'
        f'Atalhos: {battle_cmd}\n\n'

        f'*INICIAR DESCANSO*: /{rest_commands[0]}\n'
        f'INFO: Recupera HP do personagem a cada hora (mesmo se estiver 0).\n'
        f'Atalhos: {rest_cmd}\n\n'

        f'*BOLSA*: /{bag_commands[0]}\n'
        f'INFO: Exibe o conteúdo da bolsa.\n'
        f'Atalhos: {bag_cmd}\n\n'

        f'*EQUIPAMENTOS*: /{view_equips_commands[0]}\n'
        f'INFO: Exibe os itens equipados no personagem.\n'
        f'Atalhos: {equips_cmd}\n\n'
    )
    await update.effective_message.reply_markdown_v2(
        text,
        disable_notification=silent,
        reply_markup=get_help_reply_markup(update),
    )


async def details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    query = update.callback_query
    data = eval(query.data)
    option = data['option']
    data_user_id = data['user_id']

    if data_user_id != user_id:  # Não executa se outro usuário mexer na ajuda
        await query.answer(text=ACCESS_DENIED, show_alert=True)
        return ConversationHandler.END

    text = get_details_text(option)

    await query.edit_message_text(
        text=text,
        reply_markup=get_help_reply_markup(update),
        parse_mode=ParseMode.MARKDOWN_V2,

    )


def get_details_text(option: str) -> str:
    text = ''
    if option in add_stats_commands:
        add_stats_cmd = command_to_string(add_stats_commands)
        text = (
            f'*ADICIONAR/EXIBIR ESTATISTICAS*: /{add_stats_commands[0]}\n'
            f'Argumentos: [<ATRIBUTO> <VALOR>]\n'
            f'Exemplo: "/{add_stats_commands[0]} FOR 10" '
            f'(Adiciona 10 pontos em FORÇA).\n'
            f'OBS: Pode ser usado sem argumentos para exibir as estatísticas '
            f'do personagem. '
            f'Use o argumento "verbose" ou "v" para exibir as estatísticas '
            f'com mais detalhes.\n'
            f'Atalhos: {add_stats_cmd}\n\n'
        )
    elif option in config_group_commands:
        config_group_cmd = command_to_string(config_group_commands)
        text = (
            f'*CONFIGURAÇÃO DO GRUPO*: /{config_group_commands[0]}\n'
            f'Argumentos: [<CONFIGURAÇÃO> <VALOR>]\n'
            f'Configurações:\n'
            f'    "verbose": [true/false]. Configura se o bot vai falar muito.'
            f'\n'
            f'    "silent": [true/false]. Configura se as notificações do bot '
            f'no '
            f'grupo terão som.\n'
            f'    "spawn_start_time": inteiro[0-24]. Hora de início do spawn.'
            f'\n'
            f'    "spawn_end_time": inteiro[0-24]. Hora de fim do spawn.\n'
            f'    "multiplier_xp": decimal[0-5]. Multiplicador de XP.\n'
            f'    "char_multiplier_xp": decimal[0-10]. Multiplicador do bônus '
            f'de '
            f'XP baseado no nível do personagem.\n'
            f'Argumentos: [default]\n'
            f'    Retorna a configuração do grupo para o padrão.\n'
            f'Argumentos: [update]\n'
            f'    Atualiza as informações do grupo.\n'
            f'Atalhos: {config_group_cmd}\n\n'
        )
    elif option in config_player_commands:
        config_player_cmd = command_to_string(config_player_commands)
        text = (
            f'*CONFIGURAÇÃO DO JOGADOR*: /{config_player_commands[0]}\n'
            f'Argumentos: [<CONFIGURAÇÃO> <VALOR>]\n'
            f'Configurações:\n'
            f'    "verbose": [true/false]. Configura se o bot vai envia '
            f'mensagens '
            f'privadas para o jogador.\n'
            f'    "silent": [true/false]. Configura se as notificações do bot '
            f'no '
            f'chat privado terão som.\n'
            f'Argumentos: [default]\n'
            f'    Retorna a configuração do jogador para o padrão.\n'
            f'Argumentos: [update]\n'
            f'    Atualiza as informações do jogador.\n'
            f'Atalhos: {config_player_cmd}\n\n'
        )
    elif option in view_equips_commands:
        equips_cmd = command_to_string(view_equips_commands)
        text = (
            f'*EQUIPAMENTOS*: /{view_equips_commands[0]}\n'
            f'INFO: Mostra os equipamentos do personagem.\n'
            f'Use o argumento "verbose" ou "v" para exibir os equipamentos e '
            f'as estatísticas que os equipamentos garantem com mais detalhes.\n'
            f'Atalhos: {equips_cmd}\n\n'
        )
    else:
        raise ValueError(f'Opção de ajuda não encontrada: {option}')

    return escape_basic_markdown_v2(text)


def get_help_reply_markup(update: Update):
    user_id = update.effective_user.id
    reply_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=add_stats_commands[0].title(),
                callback_data=(
                    f'{{"option":"{add_stats_commands[0]}",'
                    f'"user_id":{user_id}}}'
                )
            ),
            InlineKeyboardButton(
                text=config_group_commands[0].title(),
                callback_data=(
                    f'{{"option":"{config_group_commands[0]}",'
                    f'"user_id":{user_id}}}'
                )
            ),
        ],
        [
            InlineKeyboardButton(
                text=config_player_commands[0].title(),
                callback_data=(
                    f'{{"option":"{config_player_commands[0]}",'
                    f'"user_id":{user_id}}}'
                )
            ),
            InlineKeyboardButton(
                text=view_equips_commands[0].title(),
                callback_data=(
                    f'{{"option":"{view_equips_commands[0]}",'
                    f'"user_id":{user_id}}}'
                )
            ),
        ],
        [
            InlineKeyboardButton(
                text='Atributos',
                callback_data=(
                    f'{{"option":"atributos",'
                    f'"user_id":{user_id}}}'
                )
            ),
            InlineKeyboardButton(
                text='Itens',
                callback_data=(
                    f'{{"option":"itens",'
                    f'"user_id":{user_id}}}'
                )
            ),
        ],
        [
            InlineKeyboardButton(
                text=f'{EmojiEnum.BACK.value}Voltar',
                callback_data=(
                    f'{{"{CALLBACK_BACK_HELP}":1,'
                    f'"user_id":{user_id}}}'
                )
            )
        ]
    ])
    return reply_markup


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
    ),
    CallbackQueryHandler(start, pattern=fr'^{{"{CALLBACK_BACK_HELP}":'),
    CallbackQueryHandler(details, pattern=r'^{"option":'),
]
