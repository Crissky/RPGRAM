from bson import ObjectId
from telegram import CallbackQuery, Message

from telegram.constants import ParseMode
from telegram.error import Forbidden
from telegram.ext import ContextTypes

from bot.functions.general import get_attribute_group_or_player
from bot.functions.player import get_player_attribute_by_id


CALLBACK_KEY_LIST = [
    'act',
    'buy',
    'command',
    'drop',
    'hand',
    'identify',
    'item',
    'item_id',
    'page',
    'retry_state',
    'sell',
    'sell_item',
    'sell_item_id',
    'sell_page',
    'sort',
    'use',
    '_id',
    'user_id',
    'target_id',
    'enemy_id',
    'item_quest_job_name',
    '_all',
    'classe_name',
    'race_name',
]


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
        silent = get_player_attribute_by_id(user_id, 'silent')
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


async def send_alert_or_message(
    function_caller: str,
    context: ContextTypes.DEFAULT_TYPE,
    query: CallbackQuery,
    text: str,
    user_id: int,
    chat_id: int = None,
    markdown: bool = False,
    show_alert: bool = False,
):
    if query:
        return await query.answer(text=text, show_alert=show_alert)
    else:
        return await send_private_message(
            function_caller=function_caller,
            context=context,
            text=text,
            user_id=user_id,
            chat_id=chat_id,
            markdown=markdown
        )


async def forward_message(
    function_caller: str,
    user_id: int,
    message: Message = None,
    context: ContextTypes.DEFAULT_TYPE = None,
    chat_id: int = None,
    message_id: int = None,
):
    if context and not chat_id:
        raise ValueError('chat_id é necessário quando passado um context.')
    if context and not message_id:
        raise ValueError('message_id é necessário quando passado um context.')
    if not message and not context:
        raise ValueError('message ou context deve ser passado.')

    user_silent = get_player_attribute_by_id(user_id, 'silent')
    try:
        if message:
            await message.forward(
                chat_id=user_id,
                disable_notification=user_silent
            )
        elif context:
            await context.bot.forward_message(
                chat_id=user_id,
                from_chat_id=chat_id,
                message_id=message_id,
                disable_notification=user_silent
            )
    except Exception as error:
        print(f'{function_caller}: {error}')


def callback_data_to_string(callback_data: dict) -> str:
    items = []
    for key, value in callback_data.items():
        key_int = CALLBACK_KEY_LIST.index(key)
        if isinstance(value, (str, ObjectId)):
            items.append(f'{key_int}:"{value}"')
        else:
            items.append(f'{key_int}:{value}')
    text = ','.join(items)
    text = f'{{{text}}}'

    return text


def callback_data_to_dict(callback_data_str: str) -> dict:
    callback_data = eval(callback_data_str)
    callback_data = {
        CALLBACK_KEY_LIST[key]: value
        for key, value in callback_data.items()
    }
    return callback_data


if __name__ == '__main__':
    d = {
        'drop': 10,
        'item': 10,
        'page': 10,
        'user_id': 123456789,
        'target_id': "123456789"
    }
    print(d1 := callback_data_to_string(d))
    print(d2 := callback_data_to_dict(d1))
