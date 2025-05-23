'''
Módulo responsável por gerenciar o comando de configuração de grupo.
'''


from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, PrefixHandler

from bot.constants.config_group import COMMANDS
from bot.constants.filters import (
    BASIC_COMMAND_IN_GROUP_FILTER,
    PREFIX_COMMANDS
)
from bot.functions.chat import (
    MIN_AUTODELETE_TIME,
    reply_text,
    reply_typing
)
from bot.decorators import print_basic_infos, need_are_admin, need_singup_group
from bot.functions.config import update_total_players
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
    update_total_players(group=group)

    if len(args) == 2:
        attribute = args[0]
        value = args[1]
        try:
            group[attribute] = value
            group_model.save(group)
            text = (
                f'Configurado "{attribute}" para "{value}".\n\n'
                f'{group}'
            )
            await reply_text(
                function_caller='CONFIG_GROUP.START()',
                text=text,
                context=context,
                update=update,
                silent=silent,
                allow_sending_without_reply=True,
                close_by_owner=False,
                need_response=False,
                skip_retry=False,
                auto_delete_message=MIN_AUTODELETE_TIME,
            )
        except (KeyError, ValueError) as error:
            text = str(error)
            await reply_text(
                function_caller='CONFIG_GROUP.START()',
                text=text,
                context=context,
                update=update,
                silent=silent,
                allow_sending_without_reply=True,
                close_by_owner=False,
                need_response=False,
                skip_retry=False,
                auto_delete_message=MIN_AUTODELETE_TIME,
            )
    elif 'default' in args or 'padrao' in args or 'padrão' in args:
        group['VERBOSE'] = 'false'
        group['SILENT'] = 'false'
        group['START_TIME'] = '6'
        group['END_TIME'] = '20'
        group['MULTIPLIER_XP'] = '1'
        group['CHAR_MULTIPLIER_XP'] = '1'
        group_model.save(group)
        text = (
            f'Configurado para os valores padrões.\n\n'
            f'{group}'
        )
        await reply_text(
            function_caller='CONFIG_GROUP.START()',
            text=text,
            context=context,
            update=update,
            silent=silent,
            allow_sending_without_reply=True,
            close_by_owner=False,
            need_response=False,
            skip_retry=False,
            auto_delete_message=MIN_AUTODELETE_TIME,
        )
    elif len(args) == 1 and ('update' in args or 'atualizar' in args):
        chat_name = update.effective_chat.effective_name
        group.name = chat_name
        group_model.save(group)
        text = (
            f'Informações do grupo "{chat_name}" foram atualizadas.\n\n'
            f'{group}'
        )
        await reply_text(
            function_caller='CONFIG_GROUP.START()',
            text=text,
            context=context,
            update=update,
            silent=silent,
            allow_sending_without_reply=True,
            close_by_owner=False,
            need_response=False,
            skip_retry=False,
            auto_delete_message=MIN_AUTODELETE_TIME,
        )
    elif len(args) != 2:
        text = escape_basic_markdown_v2(
            'Envie o ATRIBUTO e o VALOR que deseja configurar.\n'
            'Atributos:\n`VERBOSE`\n`SILENT`\n`START_TIME`\n`END_TIME`\n'
            '`MULTIPLIER_XP`\n`CHAR_MULTIPLIER_XP`'
        )

        await reply_text(
            function_caller='CONFIG_GROUP.START()',
            context=context,
            text=text,
            update=update,
            markdown=True,
            silent=silent,
            allow_sending_without_reply=True,
            close_by_owner=False,
            need_response=False,
            skip_retry=False,
            auto_delete_message=MIN_AUTODELETE_TIME,
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
