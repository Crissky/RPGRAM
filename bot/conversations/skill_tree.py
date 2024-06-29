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
    ACTION_LEARN_SKILL_BUTTON_TEXT,
    ACTION_UPGRADE_SKILL_BUTTON_TEXT,
    ACTION_USE_SKILL_BUTTON_TEXT,
    COMMANDS,
    LIST_LEARN_SKILL_BUTTON_TEXT,
    LIST_UPGRADE_SKILL_BUTTON_TEXT,
    PATTERN_ACTION_LEARN_SKILL,
    PATTERN_ACTION_UPGRADE_SKILL,
    PATTERN_ACTION_USE_SKILL,
    PATTERN_CHECK_UPGRADE_SKILL,
    PATTERN_CHECK_USE_SKILL,
    PATTERN_LIST_LEARN_SKILL,
    PATTERN_LIST_UPGRADE_SKILL,
    PATTERN_LIST_USE_SKILL,
    PATTERN_MAIN,
    PATTERN_CHECK_LEARN_SKILL,
    PATTERN_SKILL_BACK_LIST_LEARN,
    PATTERN_SKILL_BACK_LIST_UPGRADE,
    PATTERN_SKILL_BACK_LIST_USE,
    PATTERN_SKILL_BACK_MAIN,
    REFRESH_SKILL_TREE_PATTERN,
    SECTION_TEXT_LEARN_SKILL_TREE,
    SECTION_TEXT_SKILL_TREE,
    LIST_USE_SKILL_BUTTON_TEXT,
    SECTION_TEXT_UPGRADE_SKILL_TREE,
    SECTION_TEXT_USE_SKILL_TREE
)
from bot.constants.create_char import COMMANDS as create_char_commands
from bot.constants.filters import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.functions.char import get_char_attribute, save_char
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

from repository.mongo.models.character import CharacterModel
from rpgram.characters.char_base import BaseCharacter
from rpgram.item import Item
from rpgram.skills.factory import skill_list_factory
from rpgram.skills.skill_base import BaseSkill


@alert_if_not_chat_owner_to_anyway(alert_text=ACCESS_DENIED)
@print_basic_infos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        markdown_skill_tree_sheet = 'Escolha uma opção.'
        main_buttons = get_main_buttons(user_id=user_id,)
        refresh_close_button = get_refresh_close_button(
            user_id=user_id,
            refresh_data=REFRESH_SKILL_TREE_PATTERN,
            to_detail=False
        )
        reply_markup = InlineKeyboardMarkup([
            main_buttons,
            refresh_close_button
        ])

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
async def list_use_skill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await reply_typing(
        function_caller='SKILL_TREE.LIST_USE_SKILL()',
        update=update,
        context=context,
    )
    char_model = CharacterModel()
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    message_id = update.effective_message.id
    silent = get_attribute_group_or_player(chat_id, 'silent')
    query = update.callback_query
    char: BaseCharacter = char_model.get(user_id)

    skill_list = char.skill_tree.skill_list
    skill_name_list = [
        (
            f'*H{i+1:02}*: '
            f'*{skill_class.name.upper()}* '
            f'(Nível: {skill_class.level})'
        )
        for i, skill_class in enumerate(skill_list)
    ]
    if skill_name_list:
        markdown_skill_tree_sheet = '\n'.join(skill_name_list)
    else:
        markdown_skill_tree_sheet = 'Você ainda não aprendeu uma habilidade!!!'

    skill_buttons = get_skill_buttons(
        skill_list=skill_list,
        user_id=user_id,
        to_check_use=True
    )
    back_button = get_back_button(user_id=user_id, to_main=True)
    reply_markup = InlineKeyboardMarkup(
        skill_buttons +
        [back_button]
    )

    markdown_skill_tree_sheet = create_text_in_box(
        text=markdown_skill_tree_sheet,
        section_name=SECTION_TEXT_USE_SKILL_TREE,
        section_start=SECTION_HEAD_SKILL_TREE_START,
        section_end=SECTION_HEAD_SKILL_TREE_END
    )

    await edit_message_text(
        function_caller='SKILL_TREE.LIST_USE_SKILL()',
        new_text=markdown_skill_tree_sheet,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        need_response=False,
        markdown=True,
        reply_markup=reply_markup,
    )


@alert_if_not_chat_owner_to_callback_data_to_dict(alert_text=ACCESS_DENIED)
@print_basic_infos
async def list_upgrade_skill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await reply_typing(
        function_caller='SKILL_TREE.LIST_UPGRADE_SKILL()',
        update=update,
        context=context,
    )
    char_model = CharacterModel()
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    message_id = update.effective_message.id
    silent = get_attribute_group_or_player(chat_id, 'silent')
    query = update.callback_query
    char: BaseCharacter = char_model.get(user_id)

    skill_list = char.skill_tree.skill_list
    skill_name_list = [
        (
            f'*H{i+1:02}*: '
            f'*{skill_class.name.upper()}* '
            f'(Nível: {skill_class.level})'
        )
        for i, skill_class in enumerate(skill_list)
    ]
    if skill_name_list:
        markdown_skill_tree_sheet = '\n'.join(skill_name_list)
    else:
        markdown_skill_tree_sheet = 'Você ainda não aprendeu uma habilidade!!!'

    skill_buttons = get_skill_buttons(
        skill_list=skill_list,
        user_id=user_id,
        to_check_upgrade=True
    )
    back_button = get_back_button(user_id=user_id, to_main=True)
    reply_markup = InlineKeyboardMarkup(
        skill_buttons +
        [back_button]
    )

    markdown_skill_tree_sheet = create_text_in_box(
        text=markdown_skill_tree_sheet,
        section_name=SECTION_TEXT_UPGRADE_SKILL_TREE,
        section_start=SECTION_HEAD_SKILL_TREE_START,
        section_end=SECTION_HEAD_SKILL_TREE_END
    )

    await edit_message_text(
        function_caller='SKILL_TREE.LIST_UPGRADE_SKILL()',
        new_text=markdown_skill_tree_sheet,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        need_response=False,
        markdown=True,
        reply_markup=reply_markup,
    )


@alert_if_not_chat_owner_to_callback_data_to_dict(alert_text=ACCESS_DENIED)
@print_basic_infos
async def list_learn_skill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await reply_typing(
        function_caller='SKILL_TREE.LIST_LEARN_SKILL()',
        update=update,
        context=context,
    )
    char_model = CharacterModel()
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    message_id = update.effective_message.id
    silent = get_attribute_group_or_player(chat_id, 'silent')
    query = update.callback_query
    char: BaseCharacter = char_model.get(user_id)
    skill_list = []

    try:
        skill_list = char.skill_tree.learnable_skill_list
        skill_name_list = [
            (
                f'*H{i+1:02}*: '
                f'*{skill_class.NAME.upper()}* '
                f'(Rank: {skill_class.RANK})'
            )
            for i, skill_class in enumerate(skill_list)
        ]
        if skill_name_list:
            markdown_skill_tree_sheet = '\n'.join(skill_name_list)
        else:
            markdown_skill_tree_sheet = (
                'Você já sabe tudo o que tinha para ser aprendido!!!'
            )
    except ValueError as e:
        print(e)
        markdown_skill_tree_sheet = (
            f'Não foi possível carregar a lista de habilidades da '
            f'classe {char.classe_name}.'
        )

    skill_buttons = get_skill_buttons(
        skill_list=skill_list,
        user_id=user_id,
        to_check_learn=True
    )
    back_button = get_back_button(user_id=user_id, to_main=True)
    reply_markup = InlineKeyboardMarkup(
        skill_buttons +
        [back_button]
    )

    markdown_skill_tree_sheet = create_text_in_box(
        text=markdown_skill_tree_sheet,
        section_name=SECTION_TEXT_LEARN_SKILL_TREE,
        section_start=SECTION_HEAD_SKILL_TREE_START,
        section_end=SECTION_HEAD_SKILL_TREE_END
    )

    await edit_message_text(
        function_caller='SKILL_TREE.LIST_LEARN_SKILL()',
        new_text=markdown_skill_tree_sheet,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        need_response=False,
        markdown=True,
        reply_markup=reply_markup,
    )


@alert_if_not_chat_owner_to_callback_data_to_dict(alert_text=ACCESS_DENIED)
@print_basic_infos
async def check_use_skill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await reply_typing(
        function_caller='SKILL_TREE.CHECK_USE_SKILL()',
        update=update,
        context=context,
    )
    char_model = CharacterModel()
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    message_id = update.effective_message.id
    silent = get_attribute_group_or_player(chat_id, 'silent')
    query = update.callback_query
    char: BaseCharacter = char_model.get(user_id)
    data = callback_data_to_dict(query.data)
    skill_index = data['check_use_skill']

    try:
        skill_list = char.skill_tree.skill_list
        skill_class: BaseSkill = skill_list[skill_index]
        markdown_skill_tree_sheet = skill_class.description_text
    except ValueError as e:
        print(e)
        markdown_skill_tree_sheet = (
            f'Não foi possível carregar a habilidades da '
            f'classe {char.classe_name}.'
        )

    action_button = get_action_button(
        user_id=user_id,
        index=skill_index,
        to_action_use=True,
    )
    back_button = get_back_button(user_id=user_id, to_list_use=True)
    reply_markup = InlineKeyboardMarkup([
        action_button,
        back_button
    ])

    markdown_skill_tree_sheet = create_text_in_box(
        text=markdown_skill_tree_sheet,
        section_name=SECTION_TEXT_USE_SKILL_TREE,
        section_start=SECTION_HEAD_SKILL_TREE_START,
        section_end=SECTION_HEAD_SKILL_TREE_END
    )

    await edit_message_text(
        function_caller='SKILL_TREE.CHECK_USE_SKILL()',
        new_text=markdown_skill_tree_sheet,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        need_response=False,
        markdown=True,
        reply_markup=reply_markup,
    )


@alert_if_not_chat_owner_to_callback_data_to_dict(alert_text=ACCESS_DENIED)
@print_basic_infos
async def check_upgrade_skill(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await reply_typing(
        function_caller='SKILL_TREE.CHECK_UPGRADE_SKILL()',
        update=update,
        context=context,
    )
    char_model = CharacterModel()
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    message_id = update.effective_message.id
    silent = get_attribute_group_or_player(chat_id, 'silent')
    query = update.callback_query
    char: BaseCharacter = char_model.get(user_id)
    data = callback_data_to_dict(query.data)
    skill_index = data['check_upgrade_skill']

    try:
        skill_list = char.skill_tree.skill_list
        skill_class: BaseSkill = skill_list[skill_index]
        markdown_skill_tree_sheet = skill_class.description_text
    except ValueError as e:
        print(e)
        markdown_skill_tree_sheet = (
            f'Não foi possível carregar a habilidades da '
            f'classe {char.classe_name}.'
        )

    action_button = get_action_button(
        user_id=user_id,
        index=skill_index,
        to_action_upgrade=True,
    )
    back_button = get_back_button(user_id=user_id, to_list_upgrade=True)
    reply_markup = InlineKeyboardMarkup([
        action_button,
        back_button
    ])

    markdown_skill_tree_sheet = create_text_in_box(
        text=markdown_skill_tree_sheet,
        section_name=SECTION_TEXT_UPGRADE_SKILL_TREE,
        section_start=SECTION_HEAD_SKILL_TREE_START,
        section_end=SECTION_HEAD_SKILL_TREE_END
    )

    await edit_message_text(
        function_caller='SKILL_TREE.CHECK_UPGRADE_SKILL()',
        new_text=markdown_skill_tree_sheet,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        need_response=False,
        markdown=True,
        reply_markup=reply_markup,
    )


@alert_if_not_chat_owner_to_callback_data_to_dict(alert_text=ACCESS_DENIED)
@print_basic_infos
async def check_learn_skill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await reply_typing(
        function_caller='SKILL_TREE.CHECK_LEARN_SKILL()',
        update=update,
        context=context,
    )
    char_model = CharacterModel()
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    message_id = update.effective_message.id
    silent = get_attribute_group_or_player(chat_id, 'silent')
    query = update.callback_query
    char: BaseCharacter = char_model.get(user_id)
    data = callback_data_to_dict(query.data)
    skill_index = data['check_learn_skill']

    try:
        skill_list = char.skill_tree.learnable_skill_list
        skill_class: BaseSkill = skill_list[skill_index]
        markdown_skill_tree_sheet = (
            f'*Habilidade*: *{skill_class.NAME.upper()}*\n'
            f'*Rank*: {skill_class.RANK}\n\n'
            f'*Descrição*: {skill_class.DESCRIPTION}\n\n'
            f'*Requerimentos*:\n{skill_class.REQUIREMENT}'
        )
    except ValueError as e:
        print(e)
        markdown_skill_tree_sheet = (
            f'Não foi possível carregar a habilidades da '
            f'classe {char.classe_name}.'
        )

    action_button = get_action_button(
        user_id=user_id,
        index=skill_index,
        to_action_learn=True,
    )
    back_button = get_back_button(user_id=user_id, to_list_learn=True)
    reply_markup = InlineKeyboardMarkup([
        action_button,
        back_button
    ])

    markdown_skill_tree_sheet = create_text_in_box(
        text=markdown_skill_tree_sheet,
        section_name=SECTION_TEXT_LEARN_SKILL_TREE,
        section_start=SECTION_HEAD_SKILL_TREE_START,
        section_end=SECTION_HEAD_SKILL_TREE_END
    )

    await edit_message_text(
        function_caller='SKILL_TREE.CHECK_LEARN_SKILL()',
        new_text=markdown_skill_tree_sheet,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        need_response=False,
        markdown=True,
        reply_markup=reply_markup,
    )


@alert_if_not_chat_owner_to_callback_data_to_dict(alert_text=ACCESS_DENIED)
@print_basic_infos
async def action_use_skill(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await reply_typing(
        function_caller='SKILL_TREE.ACTION_USE_SKILL()',
        update=update,
        context=context,
    )
    char_model = CharacterModel()
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    message_id = update.effective_message.id
    silent = get_attribute_group_or_player(chat_id, 'silent')
    query = update.callback_query
    char: BaseCharacter = char_model.get(user_id)
    data = callback_data_to_dict(query.data)
    skill_index = data['action_use_skill']

    try:
        skill_list = char.skill_tree.skill_list
        skill_class: BaseSkill = skill_list[skill_index]
        markdown_skill_tree_sheet = (
            f'ESTA FUNÇÃO AINDA NÃO FOI IMPLEMENTADA!!!\n\n'
            f'{skill_class}'
        )
    except ValueError as e:
        print(e)
        markdown_skill_tree_sheet = (
            f'Não foi possível carregar a habilidades da '
            f'classe {char.classe_name}.'
        )

    back_button = get_back_button(user_id=user_id, to_list_use=True)
    reply_markup = InlineKeyboardMarkup([
        back_button
    ])

    markdown_skill_tree_sheet = create_text_in_box(
        text=markdown_skill_tree_sheet,
        section_name=SECTION_TEXT_USE_SKILL_TREE,
        section_start=SECTION_HEAD_SKILL_TREE_START,
        section_end=SECTION_HEAD_SKILL_TREE_END
    )

    await edit_message_text(
        function_caller='SKILL_TREE.ACTION_USE_SKILL()',
        new_text=markdown_skill_tree_sheet,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        need_response=False,
        markdown=True,
        reply_markup=reply_markup,
    )


@alert_if_not_chat_owner_to_callback_data_to_dict(alert_text=ACCESS_DENIED)
@print_basic_infos
async def action_upgrade_skill(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await reply_typing(
        function_caller='SKILL_TREE.ACTION_UPGRADE_SKILL()',
        update=update,
        context=context,
    )
    char_model = CharacterModel()
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    message_id = update.effective_message.id
    silent = get_attribute_group_or_player(chat_id, 'silent')
    query = update.callback_query
    char: BaseCharacter = char_model.get(user_id)
    data = callback_data_to_dict(query.data)
    skill_index = data['action_upgrade_skill']

    try:
        skill_list = char.skill_tree.skill_list
        skill_class: BaseSkill = skill_list[skill_index]
        skill_report = char.skill_tree.upgrade_skill(skill_class)
        save_char(char)
        markdown_skill_tree_sheet = skill_report['text']
    except ValueError as e:
        print(e)
        markdown_skill_tree_sheet = (
            f'Não foi possível carregar a habilidades da '
            f'classe {char.classe_name}.'
        )

    back_button = get_back_button(user_id=user_id, to_list_upgrade=True)
    reply_markup = InlineKeyboardMarkup([
        back_button
    ])

    markdown_skill_tree_sheet = create_text_in_box(
        text=markdown_skill_tree_sheet,
        section_name=SECTION_TEXT_UPGRADE_SKILL_TREE,
        section_start=SECTION_HEAD_SKILL_TREE_START,
        section_end=SECTION_HEAD_SKILL_TREE_END
    )

    await edit_message_text(
        function_caller='SKILL_TREE.ACTION_UPGRADE_SKILL()',
        new_text=markdown_skill_tree_sheet,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        need_response=False,
        markdown=True,
        reply_markup=reply_markup,
    )


@alert_if_not_chat_owner_to_callback_data_to_dict(alert_text=ACCESS_DENIED)
@print_basic_infos
async def action_learn_skill(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await reply_typing(
        function_caller='SKILL_TREE.ACTION_LEARN_SKILL()',
        update=update,
        context=context,
    )
    char_model = CharacterModel()
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    message_id = update.effective_message.id
    silent = get_attribute_group_or_player(chat_id, 'silent')
    query = update.callback_query
    char: BaseCharacter = char_model.get(user_id)
    data = callback_data_to_dict(query.data)
    skill_index = data['action_learn_skill']

    try:
        skill_list = char.skill_tree.learnable_skill_list
        skill_class: BaseSkill = skill_list[skill_index]
        skill_report = char.skill_tree.learn_skill(skill_class)
        save_char(char)
        markdown_skill_tree_sheet = skill_report['text']
    except ValueError as e:
        print(e)
        markdown_skill_tree_sheet = (
            f'Não foi possível carregar a habilidades da '
            f'classe {char.classe_name}.'
        )

    back_button = get_back_button(user_id=user_id, to_list_learn=True)
    reply_markup = InlineKeyboardMarkup([
        back_button
    ])

    markdown_skill_tree_sheet = create_text_in_box(
        text=markdown_skill_tree_sheet,
        section_name=SECTION_TEXT_LEARN_SKILL_TREE,
        section_start=SECTION_HEAD_SKILL_TREE_START,
        section_end=SECTION_HEAD_SKILL_TREE_END
    )

    await edit_message_text(
        function_caller='SKILL_TREE.ACTION_LEARN_SKILL()',
        new_text=markdown_skill_tree_sheet,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        need_response=False,
        markdown=True,
        reply_markup=reply_markup,
    )


def get_main_buttons(user_id: int) -> List[InlineKeyboardButton]:
    return [
        InlineKeyboardButton(
            text=LIST_USE_SKILL_BUTTON_TEXT,
            callback_data=callback_data_to_string({
                'list_use_skill': 1,
                'user_id': user_id,
            })
        ),
        InlineKeyboardButton(
            text=LIST_LEARN_SKILL_BUTTON_TEXT,
            callback_data=callback_data_to_string({
                'list_learn_skill': 1,
                'user_id': user_id,
            })
        ),
        InlineKeyboardButton(
            text=LIST_UPGRADE_SKILL_BUTTON_TEXT,
            callback_data=callback_data_to_string({
                'list_upgrade_skill': 1,
                'user_id': user_id,
            })
        )
    ]


def get_skill_buttons(
    skill_list: List[BaseSkill],
    user_id: int,
    to_check_use: bool = False,
    to_check_learn: bool = False,
    to_check_upgrade: bool = False,
) -> List[List[InlineKeyboardButton]]:

    to_check_list = [to_check_use, to_check_learn, to_check_upgrade]
    if to_check_list.count(True) != 1:
        raise ValueError('Somente um dos "to_check" deve ser True.')
    elif to_check_use is True:
        command = 'check_use_skill'
    elif to_check_learn is True:
        command = 'check_learn_skill'
    elif to_check_upgrade is True:
        command = 'check_upgrade_skill'

    items_buttons = []
    # Criando texto e botões das habilidades
    for index, _ in enumerate(skill_list):
        items_buttons.append(InlineKeyboardButton(
            text=f'H{index + 1:02}',
            callback_data=callback_data_to_string({
                command: index,
                'user_id': user_id,
            })
        ))

    reshaped_items_buttons = reshape_row_buttons(
        buttons=items_buttons,
        buttons_per_row=5
    )

    return reshaped_items_buttons


def get_action_button(
    user_id: int,
    index: int,
    to_action_use: bool = False,
    to_action_learn: bool = False,
    to_action_upgrade: bool = False,
) -> List[InlineKeyboardButton]:
    to_check_list = [to_action_use, to_action_learn, to_action_upgrade]
    if to_check_list.count(True) != 1:
        raise ValueError('Somente um dos "to_check" deve ser True.')
    elif to_action_use is True:
        text = ACTION_USE_SKILL_BUTTON_TEXT
        command = 'action_use_skill'
    elif to_action_learn is True:
        text = ACTION_LEARN_SKILL_BUTTON_TEXT
        command = 'action_learn_skill'
    elif to_action_upgrade is True:
        text = ACTION_UPGRADE_SKILL_BUTTON_TEXT
        command = 'action_upgrade_skill'

    return [
        InlineKeyboardButton(
            text=text,
            callback_data=callback_data_to_string({
                command: index,
                'user_id': user_id,
            })
        )
    ]


def get_back_button(
    user_id: int,
    to_main: bool = False,
    to_list_use: bool = False,
    to_list_learn: bool = False,
    to_list_upgrade: bool = False,
) -> List[InlineKeyboardButton]:
    to_list_list = [to_main, to_list_use, to_list_learn, to_list_upgrade]
    if to_list_list.count(True) != 1:
        raise ValueError('Somente um dos "to_list" deve ser True.')
    elif to_main is True:
        command = 'main'
    elif to_list_use is True:
        command = 'list_use'
    elif to_list_learn is True:
        command = 'list_learn'
    elif to_list_upgrade is True:
        command = 'list_upgrade'

    return [
        InlineKeyboardButton(
            text=NAV_BACK_BUTTON_TEXT,
            callback_data=callback_data_to_string({
                'skill_back': command,
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
    # MAIN ROUTE
    CallbackQueryHandler(start, pattern=PATTERN_MAIN),
    CallbackQueryHandler(start, pattern=PATTERN_SKILL_BACK_MAIN),
    # LIST ROUTES
    CallbackQueryHandler(list_use_skill, pattern=PATTERN_LIST_USE_SKILL),
    CallbackQueryHandler(list_use_skill, pattern=PATTERN_SKILL_BACK_LIST_USE),
    CallbackQueryHandler(list_learn_skill, pattern=PATTERN_LIST_LEARN_SKILL),
    CallbackQueryHandler(
        list_learn_skill,
        pattern=PATTERN_SKILL_BACK_LIST_LEARN
    ),
    CallbackQueryHandler(
        list_upgrade_skill,
        pattern=PATTERN_LIST_UPGRADE_SKILL
    ),
    CallbackQueryHandler(
        list_upgrade_skill,
        pattern=PATTERN_SKILL_BACK_LIST_UPGRADE
    ),
    # CHECK ROUTES
    CallbackQueryHandler(check_use_skill, pattern=PATTERN_CHECK_USE_SKILL),
    CallbackQueryHandler(check_learn_skill, pattern=PATTERN_CHECK_LEARN_SKILL),
    CallbackQueryHandler(
        check_upgrade_skill,
        pattern=PATTERN_CHECK_UPGRADE_SKILL
    ),
    # ACTION ROUTES
    CallbackQueryHandler(
        action_use_skill,
        pattern=PATTERN_ACTION_USE_SKILL
    ),
    CallbackQueryHandler(
        action_learn_skill,
        pattern=PATTERN_ACTION_LEARN_SKILL
    ),
    CallbackQueryHandler(
        action_upgrade_skill,
        pattern=PATTERN_ACTION_UPGRADE_SKILL
    ),
]
