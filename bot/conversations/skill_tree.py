'''
Módulo responsável por gerenciar as requisiçães de visualização das 
informações dos jogadores.
'''


from operator import attrgetter
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    PrefixHandler,
)

from bot.constants.skill_tree import (
    ACCESS_DENIED,
    COMMANDS,
    REFRESH_SKILL_TREE_PATTERN,
    SECTION_TEXT_SKILL_TREE
)
from bot.constants.create_char import COMMANDS as create_char_commands
from bot.constants.filters import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.functions.char import get_char_attribute
from bot.functions.chat import (
    REPLY_CHAT_ACTION_KWARGS,
    call_telegram_message_function,
    edit_message_text,
    get_random_refresh_text,
    get_refresh_close_keyboard,
    is_verbose
)
from bot.decorators import print_basic_infos
from bot.decorators.player import alert_if_not_chat_owner
from bot.functions.general import get_attribute_group_or_player
from constant.text import (
    SECTION_HEAD_SKILL_TREE_END,
    SECTION_HEAD_SKILL_TREE_START
)
from function.text import create_text_in_box

from repository.mongo import CharacterModel
from rpgram.characters import BaseCharacter
from rpgram.skills.factory import skill_list_factory


@alert_if_not_chat_owner(alert_text=ACCESS_DENIED)
@print_basic_infos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await call_telegram_message_function(
        function_caller='SKILL_TREE.START()',
        function=update.effective_message.reply_chat_action,
        context=context,
        need_response=False,
        skip_retry=True,
        **REPLY_CHAT_ACTION_KWARGS
    )
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    message_id = update.effective_message.id
    silent = get_attribute_group_or_player(chat_id, 'silent')
    query = update.callback_query
    args = context.args
    classe_name = get_char_attribute(user_id=user_id, attribute='classe_name')
    verbose = is_verbose(args)

    if query:
        data = eval(query.data)
        refresh = data.get(REFRESH_SKILL_TREE_PATTERN, False)
        if data.get('verbose') == 'v':
            verbose = True

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

        # Cria os botões de refresh/fechar ou botão de fechar
        reply_markup = get_refresh_close_keyboard(
            user_id=user_id,
            refresh_data=REFRESH_SKILL_TREE_PATTERN,
            to_detail=False
        )

        if query:
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
            markdown_skill_tree_sheet = create_text_in_box(
                text=markdown_skill_tree_sheet,
                section_name=SECTION_TEXT_SKILL_TREE,
                section_start=SECTION_HEAD_SKILL_TREE_START,
                section_end=SECTION_HEAD_SKILL_TREE_END
            )

            reply_text_kwargs = dict(
                text=markdown_skill_tree_sheet,
                parse_mode=ParseMode.MARKDOWN_V2,
                disable_notification=silent,
                reply_markup=reply_markup,
                allow_sending_without_reply=True
            )
            await call_telegram_message_function(
                function_caller='SKILL_TREE.START()',
                function=update.effective_message.reply_text,
                context=context,
                need_response=False,
                skip_retry=False,
                **reply_text_kwargs,
            )
    else:
        reply_text_kwargs = dict(
            text=(
                f'Você ainda não criou um personagem!\n'
                f'Crie o seu personagem com o comando '
                f'/{create_char_commands[0]}.'
            ),
            disable_notification=silent,
            allow_sending_without_reply=True
        )
        await call_telegram_message_function(
            function_caller='SKILL_TREE.START()',
            function=update.effective_message.reply_text,
            context=context,
            need_response=False,
            skip_retry=False,
            **reply_text_kwargs,
        )

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
    CallbackQueryHandler(
        start, pattern=fr'^{{"{REFRESH_SKILL_TREE_PATTERN}":1'
    ),
]
