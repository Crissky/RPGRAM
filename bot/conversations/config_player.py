'''
Módulo responsável por gerenciar o comando de configuração de grupo.
'''


from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, PrefixHandler

from bot.constants.config_player import COMMANDS
from bot.constants.filters import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.functions.chat import (
    MIN_AUTODELETE_TIME,
    reply_text,
    reply_typing
)
from bot.decorators import print_basic_infos, need_singup_player
from bot.functions.general import get_attribute_group_or_player
from function.text import escape_basic_markdown_v2

from repository.mongo import CharacterModel, PlayerModel
from rpgram import Player
from rpgram.characters import BaseCharacter


@print_basic_infos
@need_singup_player
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await reply_typing(
        function_caller='CONFIG_PLAYER.START()',
        update=update,
        context=context,
    )
    player_model = PlayerModel()
    char_model = CharacterModel()
    args = context.args
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    silent = get_attribute_group_or_player(chat_id, 'silent')
    player: Player = player_model.get(user_id)

    if len(args) == 2:
        attribute = args[0]
        value = args[1]
        try:
            player[attribute] = value
            player_model.save(player)
            text = (
                f'Configurado "{attribute}" para "{value}".\n\n'
                f'{player}'
            )
            await reply_text(
                function_caller='CONFIG_PLAYER.START()',
                text=text,
                context=context,
                update=update,
                silent=silent,
                allow_sending_without_reply=True,
                close_by_owner=True,
                need_response=False,
                skip_retry=False,
                auto_delete_message=MIN_AUTODELETE_TIME,
            )
        except (KeyError, ValueError) as error:
            text = str(error)
            await reply_text(
                function_caller='CONFIG_PLAYER.START()',
                text=text,
                context=context,
                update=update,
                silent=silent,
                allow_sending_without_reply=True,
                close_by_owner=True,
                need_response=False,
                skip_retry=False,
                auto_delete_message=MIN_AUTODELETE_TIME,
            )
    elif 'default' in args or 'padrao' in args or 'padrão' in args:
        player['VERBOSE'] = 'false'
        player['SILENT'] = 'false'
        player_model.save(player)
        text = (
            f'Configurado para os valores padrões.\n\n'
            f'{player}'
        )
        await reply_text(
            function_caller='CONFIG_PLAYER.START()',
            text=text,
            context=context,
            update=update,
            silent=silent,
            allow_sending_without_reply=True,
            close_by_owner=True,
            need_response=False,
            skip_retry=False,
            auto_delete_message=MIN_AUTODELETE_TIME,
        )
    elif len(args) == 1 and ('update' in args or 'atualizar' in args):
        user_name = update.effective_user.name
        player.name = user_name
        player_model.save(player)

        player_char: BaseCharacter = char_model.get(user_id)
        if player_char:
            player_char.update_player_name(new_name=user_name)
            char_model.save(player_char)

        text = (
            f'Informações do jogador "{user_name}" foram atualizadas.\n\n'
            f'{player}'
        )
        await reply_text(
            function_caller='CONFIG_PLAYER.START()',
            text=text,
            context=context,
            update=update,
            silent=silent,
            allow_sending_without_reply=True,
            close_by_owner=True,
            need_response=False,
            skip_retry=False,
            auto_delete_message=MIN_AUTODELETE_TIME,
        )
    elif len(args) != 2:
        text = escape_basic_markdown_v2(
            'Envie o ATRIBUTO e o VALOR que deseja configurar.\n'
            'Atributos:\n`VERBOSE`\n`SILENT`'
        )
        await reply_text(
            function_caller='CONFIG_PLAYER.START()',
            text=text,
            context=context,
            update=update,
            markdown=True,
            silent=silent,
            allow_sending_without_reply=True,
            close_by_owner=True,
            need_response=False,
            skip_retry=False,
            auto_delete_message=MIN_AUTODELETE_TIME,
        )


CONFIG_PLAYER_HANDLERS = [
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
