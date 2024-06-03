'''
Módulo responsável por gerenciar o comando de configuração de grupo.
'''


from telegram import Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import CommandHandler, ContextTypes, PrefixHandler

from bot.constants.config_player import COMMANDS
from bot.constants.filters import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.functions.chat import (
    REPLY_CHAT_ACTION_KWARGS,
    call_telegram_message_function,
    get_close_keyboard
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
    await call_telegram_message_function(
        function_caller='CONFIG_PLAYER.START()',
        function=update.effective_message.reply_chat_action,
        context=context,
        need_response=False,
        skip_retry=True,
        **REPLY_CHAT_ACTION_KWARGS
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
            reply_text_kwargs = dict(
                text=(
                    f'Configurado "{attribute}" para "{value}".\n\n'
                    f'{player}'
                ),
                disable_notification=silent,
                reply_markup=get_close_keyboard(user_id=user_id),
                allow_sending_without_reply=True
            )
            await call_telegram_message_function(
                function_caller='CONFIG_PLAYER.START()',
                function=update.effective_message.reply_text,
                context=context,
                need_response=False,
                skip_retry=False,
                **reply_text_kwargs,
            )
        except (KeyError, ValueError) as error:
            reply_text_kwargs = dict(
                text=str(error),
                disable_notification=silent,
                reply_markup=get_close_keyboard(user_id=user_id),
                allow_sending_without_reply=True
            )
            await call_telegram_message_function(
                function_caller='CONFIG_PLAYER.START()',
                function=update.effective_message.reply_text,
                context=context,
                need_response=False,
                skip_retry=False,
                **reply_text_kwargs,
            )
    elif 'default' in args or 'padrao' in args or 'padrão' in args:
        player['VERBOSE'] = 'false'
        player['SILENT'] = 'false'
        player_model.save(player)
        reply_text_kwargs = dict(
            text=(
                f'Configurado para os valores padrões.\n\n'
                f'{player}'
            ),
            disable_notification=silent,
            reply_markup=get_close_keyboard(user_id=user_id),
            allow_sending_without_reply=True
        )
        await call_telegram_message_function(
            function_caller='CONFIG_PLAYER.START()',
            function=update.effective_message.reply_text,
            context=context,
            need_response=False,
            skip_retry=False,
            **reply_text_kwargs,
        )
    elif len(args) == 1 and ('update' in args or 'atualizar' in args):
        user_name = update.effective_user.name
        player.name = user_name
        player_model.save(player)

        player_char: BaseCharacter = char_model.get(user_id)
        if player_char:
            player_char.update_player_name(new_name=user_name)
            char_model.save(player_char)

        reply_text_kwargs = dict(
            text=(
                f'Informações do jogador "{user_name}" foram atualizadas.\n\n'
                f'{player}'
            ),
            disable_notification=silent,
            reply_markup=get_close_keyboard(user_id=user_id),
            allow_sending_without_reply=True
        )
        await call_telegram_message_function(
            function_caller='CONFIG_PLAYER.START()',
            function=update.effective_message.reply_text,
            context=context,
            need_response=False,
            skip_retry=False,
            **reply_text_kwargs,
        )
    elif len(args) != 2:
        text = escape_basic_markdown_v2(
            'Envie o ATRIBUTO e o VALOR que deseja configurar.\n'
            'Atributos:\n`VERBOSE`\n`SILENT`'
        )

        reply_text_kwargs = dict(
            text=text,
            disable_notification=silent,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=get_close_keyboard(user_id=user_id),
            allow_sending_without_reply=True
        )
        await call_telegram_message_function(
            function_caller='CONFIG_PLAYER.START()',
            function=update.effective_message.reply_text,
            context=context,
            need_response=False,
            skip_retry=False,
            **reply_text_kwargs,
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
