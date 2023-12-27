from telegram.constants import ParseMode
from telegram.error import Forbidden
from telegram.ext import ContextTypes

from bot.functions.general import get_attribute_group_or_player


async def send_private_message(
    function_caller: str,
    context: ContextTypes.DEFAULT_TYPE,
    text: str,
    user_id: int,
    chat_id: int = None,
    markdown: bool = False,
):
    markdown = ParseMode.MARKDOWN_V2 if markdown else None

    try:
        silent = get_attribute_group_or_player(user_id, 'silent')
        await context.bot.send_message(
            chat_id=user_id,
            text=text,
            parse_mode=markdown,
            disable_notification=silent
        )
    except Forbidden as error:
        if isinstance(chat_id, int):
            silent = get_attribute_group_or_player(chat_id, 'silent')
            member = await context.bot.get_chat_member(
                chat_id=chat_id,
                user_id=user_id
            )
            user_name = member.user.name
            text = f'{user_name}\n{text}'
            await context.bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=markdown,
                disable_notification=silent,
            )
        else:
            print(
                f'SEND_PRIVATE_MESSAGE(): Usuário {user_id} não pode '
                f'receber mensagens privadas e um "chat_id" não foi passado. '
                f'Ele precisa iniciar uma conversa com o bot.\n'
                f'Function Caller: {function_caller}\n'
                f'(ERROR: {error})'
            )
