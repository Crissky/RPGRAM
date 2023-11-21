'''
Módulo responsável por exibir e adicionar pontos de stats dos personagens.
'''


from typing import List
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    PrefixHandler
)

from bot.constants.add_stats import (
    ACCESS_DENIED,
    ATTRIBUTE_LIST,
    COMMANDS,
    POINTS_OPTION_LIST
)
from bot.constants.filters import (
    BASIC_COMMAND_FILTER,
    PREFIX_COMMANDS,
)
from bot.decorators import (
    need_have_char,
    need_not_in_battle,
    print_basic_infos,
    skip_if_dead_char,
    skip_if_immobilized,
)
from bot.functions.general import get_attribute_group_or_player
from bot.functions.keyboard import reshape_row_buttons

from function.text import escape_markdown_v2

from repository.mongo import CharacterModel
from rpgram.characters import BaseCharacter
from rpgram.constants.text import BASE_ATTRIBUTE_EMOJI_TEXT
from rpgram.enums.emojis import EmojiEnum


@skip_if_immobilized
@skip_if_dead_char
@print_basic_infos
@need_have_char
@need_not_in_battle
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_chat_action(ChatAction.TYPING)
    char_model = CharacterModel()
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    args = context.args
    query = update.callback_query

    if query:
        data = eval(query.data)
        data_user_id = data['user_id']

        # Não executa se outro usuário mexer na bolsa
        if data_user_id != user_id:
            await query.answer(text=ACCESS_DENIED, show_alert=True)
            return None

        # Apaga o Mensagem
        if data.get('close', False):
            await query.answer('Fechando Estatísticas...')
            await query.delete_message()
            return None

        if args is None:
            args = []
            args.append(data['attribute'])
            args.append(data['value'])

    text = ''
    verbose = False
    player_char = char_model.get(user_id)
    silent = get_attribute_group_or_player(chat_id, 'silent')
    if len(args) == 2:
        attribute = args[0].upper()
        value = args[1]
        try:
            player_char.base_stats[attribute] = value
            char_model.save(player_char)
            text = escape_markdown_v2(
                f'Adicionado "{value}" ponto(s) no atributo "{attribute}".\n\n'
            )
        except (KeyError, ValueError) as error:
            text = str(error)
            if query:
                await query.answer(text=text, show_alert=True)
            else:
                await update.effective_message.reply_text(
                    text,
                    disable_notification=silent
                )
            return None
    elif len(args) > 2:
        await update.effective_message.reply_text(
            'Envie somente o ATRIBUTO e o VALOR que deseja adicionar.',
            disable_notification=silent
        )
        return None
    elif len(args) == 1:
        verbose = 'verbose' == args[0] or 'v' == args[0]

    status_sheet = player_char.status.get_all_sheets(
        verbose=verbose,
        markdown=True
    )
    combat_stats_sheets = player_char.cs.get_all_sheets(
        verbose=verbose,
        markdown=True
    )
    addstats_buttons = get_addstats_buttons(user_id, player_char)
    close_button = get_close_button(user_id=user_id)
    reply_markup = InlineKeyboardMarkup([
        *addstats_buttons,
        close_button
    ])
    if query:
        await query.edit_message_text(
            f'{text}'
            f'{status_sheet}\n'
            f'{combat_stats_sheets}',
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=reply_markup,
        )
    else:
        await update.effective_message.reply_text(
            f'{text}'
            f'{status_sheet}\n'
            f'{combat_stats_sheets}',
            parse_mode=ParseMode.MARKDOWN_V2,
            disable_notification=silent,
            reply_markup=reply_markup,
        )


def get_addstats_buttons(
    user_id: int,
    char: BaseCharacter
) -> List[List[InlineKeyboardButton]]:
    addstats_buttons = []
    points = char.bs.points
    for attribute in ATTRIBUTE_LIST:
        for points_option in POINTS_OPTION_LIST:
            if points_option <= points:
                text = (
                    f'{BASE_ATTRIBUTE_EMOJI_TEXT[attribute]} x{points_option}'
                )
                addstats_buttons.append(
                    InlineKeyboardButton(
                        text=text,
                        callback_data=(
                            f'{{"attribute":"{attribute}",'
                            f'"value":{points_option},'
                            f'"user_id":{user_id}}}'
                        )
                    )
                )
    # Calcula quantas linhas terão os botões de acordo com o número de pontos
    buttons_per_row = 1
    for option in reversed(POINTS_OPTION_LIST):
        if option <= points:
            buttons_per_row = POINTS_OPTION_LIST.index(option) + 1
            break
    return reshape_row_buttons(
        addstats_buttons,
        buttons_per_row=buttons_per_row
    )


def get_close_button(user_id) -> List[InlineKeyboardButton]:
    return [
        InlineKeyboardButton(
            f'{EmojiEnum.CLOSE.value}Fechar',
            callback_data=(
                f'{{"close":1,'
                f'"user_id":{user_id}}}'
            )
        )
    ]


ADD_STATS_HANDLERS = [
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
    CallbackQueryHandler(start, pattern=r'^{"attribute":'),
    CallbackQueryHandler(start, pattern=r'^{"close":1'),
]
