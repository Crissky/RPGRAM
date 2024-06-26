'''
Módulo responsável por gerenciar o comando de configuração de grupo.
'''


from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes, PrefixHandler

from bot.constants.config_group import COMMANDS
from bot.constants.filters import (
    BASIC_COMMAND_IN_GROUP_FILTER,
    PREFIX_COMMANDS
)
from bot.functions.chat import (
    call_telegram_message_function,
    get_close_keyboard,
    reply_typing
)
from bot.decorators import print_basic_infos, need_are_admin, need_singup_group
from bot.functions.general import get_attribute_group_or_player
from function.text import escape_basic_markdown_v2

from repository.mongo import GroupModel
from rpgram import Group


@print_basic_infos
@need_singup_group
@need_are_admin
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await reply_typing(
        function_caller='CONFIG_GROUP.START()',
        update=update,
        context=context,
    )
    group_model = GroupModel()
    chat_id = update.effective_chat.id
    silent = get_attribute_group_or_player(chat_id, 'silent')
    args = context.args
    group: Group = group_model.get(chat_id)

    if len(args) == 2:
        attribute = args[0]
        value = args[1]
        try:
            group[attribute] = value
            group_model.save(group)
            reply_text_kwargs = dict(
                text=(
                    f'Configurado "{attribute}" para "{value}".\n\n'
                    f'{group}'
                ),
                disable_notification=silent,
                reply_markup=get_close_keyboard(None),
                allow_sending_without_reply=True
            )
            await call_telegram_message_function(
                function_caller='CONFIG_GROUP.START()',
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
                reply_markup=get_close_keyboard(None),
                allow_sending_without_reply=True
            )
            await call_telegram_message_function(
                function_caller='CONFIG_GROUP.START()',
                function=update.effective_message.reply_text,
                context=context,
                need_response=False,
                skip_retry=False,
                **reply_text_kwargs,
            )
    elif 'default' in args or 'padrao' in args or 'padrão' in args:
        group['VERBOSE'] = 'false'
        group['SILENT'] = 'false'
        group['START_TIME'] = '6'
        group['END_TIME'] = '20'
        group['MULTIPLIER_XP'] = '1'
        group['CHAR_MULTIPLIER_XP'] = '1'
        group_model.save(group)
        reply_text_kwargs = dict(
            text=(
                f'Configurado para os valores padrões.\n\n'
                f'{group}'
            ),
            disable_notification=silent,
            reply_markup=get_close_keyboard(None),
            allow_sending_without_reply=True
        )
        await call_telegram_message_function(
            function_caller='CONFIG_GROUP.START()',
            function=update.effective_message.reply_text,
            context=context,
            need_response=False,
            skip_retry=False,
            **reply_text_kwargs,
        )
    elif len(args) == 1 and ('update' in args or 'atualizar' in args):
        chat_name = update.effective_chat.effective_name
        group.name = chat_name
        group_model.save(group)
        reply_text_kwargs = dict(
            text=(
                f'Informações do grupo "{chat_name}" foram atualizadas.\n\n'
                f'{group}'
            ),
            disable_notification=silent,
            reply_markup=get_close_keyboard(None),
            allow_sending_without_reply=True
        )
        await call_telegram_message_function(
            function_caller='CONFIG_GROUP.START()',
            function=update.effective_message.reply_text,
            context=context,
            need_response=False,
            skip_retry=False,
            **reply_text_kwargs,
        )
    elif len(args) != 2:
        text = escape_basic_markdown_v2(
            'Envie o ATRIBUTO e o VALOR que deseja configurar.\n'
            'Atributos:\n`VERBOSE`\n`SILENT`\n`START_TIME`\n`END_TIME`\n'
            '`MULTIPLIER_XP`\n`CHAR_MULTIPLIER_XP`'
        )

        reply_text_kwargs = dict(
            text=text,
            disable_notification=silent,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=get_close_keyboard(None),
            allow_sending_without_reply=True
        )
        await call_telegram_message_function(
            function_caller='CONFIG_GROUP.START()',
            function=update.effective_message.reply_text,
            context=context,
            need_response=False,
            skip_retry=False,
            **reply_text_kwargs,
        )


CONFIG_GROUP_HANDLERS = [
    PrefixHandler(
        PREFIX_COMMANDS,
        COMMANDS,
        start,
        BASIC_COMMAND_IN_GROUP_FILTER
    ),
    CommandHandler(
        COMMANDS,
        start,
        BASIC_COMMAND_IN_GROUP_FILTER
    )
]
