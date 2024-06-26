'''
Módulo responsável por gerenciar as requisiçães de visualização das 
informações dos jogadores.
'''


from operator import attrgetter
from typing import List
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    PrefixHandler,
)

from bot.constants.bag import NAV_BACK_BUTTON_TEXT
from bot.constants.skill_tree import (
    ACCESS_DENIED,
    COMMANDS,
    PATTERN_MAIN,
    PATTERN_SKILL,
    PATTERN_SKILL_BACK,
    REFRESH_SKILL_TREE_PATTERN,
    SECTION_TEXT_SKILL_TREE
)
from bot.constants.create_char import COMMANDS as create_char_commands
from bot.constants.filters import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.functions.char import get_char_attribute
from bot.functions.chat import (
    call_telegram_message_function,
    callback_data_to_dict,
    callback_data_to_string,
    edit_message_text,
    get_close_button,
    get_random_refresh_text,
    get_refresh_close_button,
    get_refresh_close_keyboard,
    is_verbose,
    reply_text,
    reply_typing
)
from bot.decorators import print_basic_infos
from bot.decorators.player import (
    alert_if_not_chat_owner,
    alert_if_not_chat_owner_to_anyway,
    alert_if_not_chat_owner_to_callback_data_to_dict
)
from bot.functions.general import get_attribute_group_or_player
from bot.functions.keyboard import reshape_row_buttons
from constant.text import (
    SECTION_HEAD_SKILL_TREE_END,
    SECTION_HEAD_SKILL_TREE_START
)
from function.text import create_text_in_box

from rpgram.item import Item
from rpgram.skills.factory import skill_list_factory
from rpgram.skills.skill_base import BaseSkill


@alert_if_not_chat_owner_to_anyway(alert_text=ACCESS_DENIED)
@print_basic_infos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await reply_typing(
        function_caller='SKILL_TREE.START()',
        update=update,
        context=context,
    )
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    message_id = update.effective_message.id
    silent = get_attribute_group_or_player(chat_id, 'silent')
    query = update.callback_query
    classe_name = get_char_attribute(user_id=user_id, attribute='classe_name')
    refresh = False

    if query:
        data = eval(query.data)
        refresh = data.get(REFRESH_SKILL_TREE_PATTERN, False)

    if classe_name:
        try:
            skill_list = skill_list_factory(classe_name)
            skill_list = sorted(skill_list, key=attrgetter('RANK', 'NAME'))
            skill_name_list = [
                (
                    f'*H{i+1:02}*: '
                    f'*{skill_class.NAME.upper()}* '
                    f'(Rank: {skill_class.RANK})'
                )
                for i, skill_class in enumerate(skill_list)
            ]
            markdown_skill_tree_sheet = '\n'.join(skill_name_list)
        except ValueError as e:
            print(e)
            markdown_skill_tree_sheet = (
                f'Não foi possível carregar a lista de habilidades da '
                f'classe {classe_name}.'
            )

        skill_buttons = get_skill_buttons(
            skill_list=skill_list,
            user_id=user_id,
        )
        refresh_close_button = get_refresh_close_button(
            user_id=user_id,
            refresh_data=REFRESH_SKILL_TREE_PATTERN,
            to_detail=False
        )
        reply_markup = InlineKeyboardMarkup(
            skill_buttons +
            [refresh_close_button]
        )

        if refresh:
            '''"refresh_text" é usado para modificar a mensagem de maneira
            aleatória para tentar evitar um erro (BadRequest)
            quando não há mudanças no "markdown_player_sheet" usado na
            função "edit_message_text".'''
            refresh_text = get_random_refresh_text()
            markdown_skill_tree_sheet = (
                f'{refresh_text}\n'
                f'{markdown_skill_tree_sheet}'
            )

        markdown_skill_tree_sheet = create_text_in_box(
            text=markdown_skill_tree_sheet,
            section_name=SECTION_TEXT_SKILL_TREE,
            section_start=SECTION_HEAD_SKILL_TREE_START,
            section_end=SECTION_HEAD_SKILL_TREE_END
        )

        if query:
            await edit_message_text(
                function_caller='SKILL_TREE.START()',
                new_text=markdown_skill_tree_sheet,
                context=context,
                chat_id=chat_id,
                message_id=message_id,
                need_response=False,
                markdown=True,
                reply_markup=reply_markup,
            )
        else:
            await reply_text(
                function_caller='SKILL_TREE.START()',
                text=markdown_skill_tree_sheet,
                context=context,
                update=update,
                need_response=False,
                markdown=True,
                reply_markup=reply_markup,
                silent=silent
            )
    else:
        text = (
            f'Você ainda não criou um personagem!\n'
            f'Crie o seu personagem com o comando '
            f'/{create_char_commands[0]}.'
        )
        await reply_text(
            function_caller='SKILL_TREE.START()',
            text=text,
            context=context,
            update=update,
            need_response=False,
            markdown=True,
            silent=silent
        )


@alert_if_not_chat_owner_to_callback_data_to_dict(alert_text=ACCESS_DENIED)
@print_basic_infos
async def check_skill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await reply_typing(
        function_caller='SKILL_TREE.CHECK_SKILL()',
        update=update,
        context=context,
    )
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    message_id = update.effective_message.id
    silent = get_attribute_group_or_player(chat_id, 'silent')
    query = update.callback_query
    classe_name = get_char_attribute(user_id=user_id, attribute='classe_name')
    data = callback_data_to_dict(query.data)
    skill_index = data['skill']

    try:
        skill_list = skill_list_factory(classe_name)
        skill_list = sorted(skill_list, key=attrgetter('RANK', 'NAME'))
        skill_class: BaseSkill = skill_list[skill_index]
        markdown_skill_tree_sheet = (
            f'*Habilidade*: *{skill_class.NAME.upper()}*\n'
            f'Rank: {skill_class.RANK}\n\n'
            f'*Descrição*: {skill_class.DESCRIPTION}\n'
        )
    except ValueError as e:
        print(e)
        markdown_skill_tree_sheet = (
            f'Não foi possível carregar a habilidades da '
            f'classe {classe_name}.'
        )

    back_button = get_back_button(user_id=user_id)
    reply_markup = InlineKeyboardMarkup([
        back_button
    ])

    markdown_skill_tree_sheet = create_text_in_box(
        text=markdown_skill_tree_sheet,
        section_name=SECTION_TEXT_SKILL_TREE,
        section_start=SECTION_HEAD_SKILL_TREE_START,
        section_end=SECTION_HEAD_SKILL_TREE_END
    )

    await edit_message_text(
        function_caller='SKILL_TREE.CHECK_SKILL()',
        new_text=markdown_skill_tree_sheet,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        need_response=False,
        markdown=True,
        reply_markup=reply_markup,
    )


def get_skill_buttons(
    skill_list: List[BaseSkill],
    user_id: int,
) -> List[List[InlineKeyboardButton]]:

    items_buttons = []
    # Criando texto e botões dos itens
    for index, _ in enumerate(skill_list):
        items_buttons.append(InlineKeyboardButton(
            text=f'H{index + 1:02}',
            callback_data=callback_data_to_string({
                'skill': index,
                'user_id': user_id,
            })
        ))

    reshaped_items_buttons = reshape_row_buttons(
        buttons=items_buttons,
        buttons_per_row=5
    )

    return reshaped_items_buttons


def get_back_button(user_id: int) -> List[InlineKeyboardButton]:
    return [
        InlineKeyboardButton(
            text=NAV_BACK_BUTTON_TEXT,
            callback_data=callback_data_to_string({
                'skill_back': 1,
                'user_id': user_id,
            })
        )
    ]


SKILL_TREE_HANDLERS = [
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
    CallbackQueryHandler(start, pattern=PATTERN_MAIN),
    CallbackQueryHandler(start, pattern=PATTERN_SKILL_BACK),
    CallbackQueryHandler(check_skill, pattern=PATTERN_SKILL),
]
