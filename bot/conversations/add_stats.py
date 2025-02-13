'''
Módulo responsável por exibir e adicionar pontos de stats dos personagens.
'''


from typing import List
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
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
    POINTS_OPTION_LIST,
    REFRESH_ADD_STATS_PATTERN,
    SECTION_TEXT_STATS
)
from bot.constants.filters import (
    BASIC_COMMAND_FILTER,
    PREFIX_COMMANDS,
)
from bot.functions.chat import (
    MIN_AUTODELETE_TIME,
    answer,
    edit_message_text,
    get_random_refresh_text,
    get_refresh_close_button,
    is_verbose,
    reply_text,
    reply_typing
)
from bot.decorators import (
    confusion,
    need_have_char,
    print_basic_infos,
    skip_if_dead_char,
    skip_if_immobilized,
)
from bot.decorators.player import alert_if_not_chat_owner
from bot.functions.general import get_attribute_group_or_player
from bot.functions.keyboard import reshape_row_buttons
from constant.text import SECTION_HEAD_STATS_END, SECTION_HEAD_STATS_START

from function.text import create_text_in_box, escape_markdown_v2

from repository.mongo import CharacterModel
from rpgram.characters import BaseCharacter
from rpgram.constants.text import BASE_ATTRIBUTE_EMOJI_TEXT


@alert_if_not_chat_owner(alert_text=ACCESS_DENIED)
@skip_if_dead_char
@skip_if_immobilized
@confusion()
@print_basic_infos
@need_have_char
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await reply_typing(
        function_caller='ADD_STATS.START()',
        update=update,
        context=context,
    )
    char_model = CharacterModel()
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    message_id = update.effective_message.id
    args = context.args
    query = update.callback_query
    verbose = False

    if query:
        data = eval(query.data)
        refresh = data.get(REFRESH_ADD_STATS_PATTERN, False)
        if data.get('verbose') == 'v':
            verbose = True

        if args is None:
            args = []
            if not refresh:
                args.append(data['attribute'])
                args.append(data['value'])

    text = ''
    player_char: BaseCharacter = char_model.get(user_id)
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
                await answer(query=query, text=text, show_alert=True)
            else:
                await reply_text(
                    function_caller='ADD_STATS.START()',
                    text=text,
                    context=context,
                    update=update,
                    silent=silent,
                    allow_sending_without_reply=True,
                    need_response=False,
                    skip_retry=False,
                    auto_delete_message=MIN_AUTODELETE_TIME
                )
            return None
    elif len(args) > 2:
        text = 'Envie somente o ATRIBUTO e o VALOR que deseja adicionar.'
        await reply_text(
            function_caller='ADD_STATS.START()',
            text=text,
            context=context,
            update=update,
            silent=silent,
            allow_sending_without_reply=True,
            need_response=False,
            skip_retry=False,
            auto_delete_message=MIN_AUTODELETE_TIME
        )
        return None
    elif len(args) == 1:
        verbose = is_verbose(args)

    status_sheet = player_char.status.get_all_sheets(
        verbose=verbose,
        markdown=True
    )
    combat_stats_sheets = player_char.cs.get_all_sheets(
        verbose=verbose,
        markdown=True
    )
    addstats_buttons = get_addstats_buttons(user_id, player_char)
    refresh_close_button = get_refresh_close_button(
        user_id=user_id,
        refresh_data=REFRESH_ADD_STATS_PATTERN,
        to_detail=True
    )
    reply_markup = InlineKeyboardMarkup([
        *addstats_buttons,
        refresh_close_button
    ])
    text = (
        f'{text}'
        f'{status_sheet}\n'
        f'{combat_stats_sheets}'
    )

    if query:
        if refresh:
            '''"refresh_text" é usado para modificar a mensagem de maneira
            aleatória para tentar evitar um erro (BadRequest)
            quando não há mudanças no "markdown_equips_sheet" usado na
            função "edit_message_text".'''
            refresh_text = get_random_refresh_text()
            text = (
                f'{refresh_text}\n'
                f'{text}'
            )

        text = create_text_in_box(
            text=text,
            section_name=SECTION_TEXT_STATS,
            section_start=SECTION_HEAD_STATS_START,
            section_end=SECTION_HEAD_STATS_END
        )

        await edit_message_text(
            function_caller='ADD_STATS.START()',
            new_text=text,
            context=context,
            chat_id=chat_id,
            message_id=message_id,
            need_response=False,
            markdown=True,
            reply_markup=reply_markup
        )
    else:
        text = create_text_in_box(
            text=text,
            section_name=SECTION_TEXT_STATS,
            section_start=SECTION_HEAD_STATS_START,
            section_end=SECTION_HEAD_STATS_END
        )

        await reply_text(
            function_caller='ADD_STATS.START()',
            text=text,
            context=context,
            update=update,
            markdown=True,
            silent=silent,
            reply_markup=reply_markup,
            allow_sending_without_reply=True,
            need_response=False,
            skip_retry=False,
            auto_delete_message=MIN_AUTODELETE_TIME,
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
    CallbackQueryHandler(
        start, pattern=fr'^{{"{REFRESH_ADD_STATS_PATTERN}":1'
    ),
]
