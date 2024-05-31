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
    player = player_model.get(user_id)

    if len(args) == 2:
        attribute = args[0]
        value = args[1]
        try:
            player[attribute] = value
            player_model.save(player)
            await update.effective_message.reply_text(
                f'Configurado "{attribute}" para "{value}".\n\n'
                f'{player}',
                disable_notification=silent,
                reply_markup=get_close_keyboard(user_id=user_id),
                allow_sending_without_reply=True
            )
        except (KeyError, ValueError) as error:
            await update.effective_message.reply_text(
                str(error),
                disable_notification=silent,
                reply_markup=get_close_keyboard(user_id=user_id),
                allow_sending_without_reply=True
            )
    elif 'default' in args or 'padrao' in args or 'padrão' in args:
        player['VERBOSE'] = 'false'
        player['SILENT'] = 'false'
        player_model.save(player)
        await update.effective_message.reply_text(
            f'Configurado para os valores padrões.\n\n'
            f'{player}',
            disable_notification=silent,
            reply_markup=get_close_keyboard(user_id=user_id),
            allow_sending_without_reply=True
        )
    elif len(args) == 1 and ('update' in args or 'atualizar' in args):
        user_name = update.effective_user.name
        player.name = user_name
        player_model.save(player)

        player_char = char_model.get(user_id)
        if player_char:
            player_char.update_player_name(new_name=user_name)
            char_model.save(player_char)

        await update.effective_message.reply_text(
            f'Informações do jogador "{user_name}" foram atualizadas.\n\n'
            f'{player}',
            disable_notification=silent,
            reply_markup=get_close_keyboard(user_id=user_id),
            allow_sending_without_reply=True
        )
    elif len(args) != 2:
        text = escape_basic_markdown_v2(
            'Envie o ATRIBUTO e o VALOR que deseja configurar.\n'
            'Atributos:\n`VERBOSE`\n`SILENT`'
        )

        await update.effective_message.reply_text(
            text,
            disable_notification=silent,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=get_close_keyboard(user_id=user_id),
            allow_sending_without_reply=True
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
