'''
Módulo responsável por gerenciar as requisiçães de visualização das 
informações dos jogadores.
'''


from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    PrefixHandler,
)

from bot.constants.view_char import (
    ACCESS_DENIED,
    COMMANDS,
    REFRESH_VIEW_CHAR_PATTERN,
    SECTION_TEXT_CHAR
)
from bot.constants.create_char import COMMANDS as create_char_commands
from bot.constants.filters import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.functions.chat import (
    MIN_AUTODELETE_TIME,
    edit_message_text,
    get_close_keyboard,
    get_random_refresh_text,
    get_refresh_close_keyboard,
    is_verbose,
    reply_text,
    reply_typing
)
from bot.decorators import print_basic_infos
from bot.decorators.player import alert_if_not_chat_owner
from bot.functions.general import get_attribute_group_or_player
from constant.text import SECTION_HEAD_CHAR_END, SECTION_HEAD_CHAR_START
from function.text import create_text_in_box

from repository.mongo import CharacterModel
from rpgram.characters import BaseCharacter


@alert_if_not_chat_owner(alert_text=ACCESS_DENIED)
@print_basic_infos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await reply_typing(
        function_caller='VIEW_CHAR.START()',
        update=update,
        context=context,
    )
    char_model = CharacterModel()
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    message_id = update.effective_message.id
    silent = get_attribute_group_or_player(chat_id, 'silent')
    query = update.callback_query
    args = context.args
    player_character: BaseCharacter = char_model.get(user_id)
    verbose = is_verbose(args)
    self_char = True

    if query:
        data = eval(query.data)
        refresh = data.get(REFRESH_VIEW_CHAR_PATTERN, False)
        if data.get('verbose') == 'v':
            verbose = True

    if args and len(args) in [1, 2]:
        if args[0].startswith('@'):
            self_char = False
            player_name = args[0]
            m_query = {'player_name': player_name}
            new_player_character: BaseCharacter = char_model.get(query=m_query)
            if not new_player_character:
                text = f'{player_name} não possui um personamgem.'
                await reply_text(
                    function_caller='VIEW_CHAR.START()',
                    text=text,
                    context=context,
                    update=update,
                    silent=silent,
                    allow_sending_without_reply=True,
                    need_response=False,
                    skip_retry=False,
                    auto_delete_message=MIN_AUTODELETE_TIME,
                )

                return None
            player_character = new_player_character

    if player_character:
        markdown_player_sheet = player_character.get_all_sheets(
            verbose=verbose, markdown=True
        )

        # Cria os botões de refresh/fechar ou botão de fechar
        if self_char:
            reply_markup = get_refresh_close_keyboard(
                user_id=user_id,
                refresh_data=REFRESH_VIEW_CHAR_PATTERN,
                to_detail=True
            )
        else:
            reply_markup = get_close_keyboard(user_id=user_id)

        if query:
            if refresh:
                '''"refresh_text" é usado para modificar a mensagem de maneira
                aleatória para tentar evitar um erro (BadRequest)
                quando não há mudanças no "markdown_player_sheet" usado na
                função "edit_message_text".'''
                refresh_text = get_random_refresh_text()
                markdown_player_sheet = (
                    f'{refresh_text}\n'
                    f'{markdown_player_sheet}'
                )

            markdown_player_sheet = create_text_in_box(
                text=markdown_player_sheet,
                section_name=SECTION_TEXT_CHAR,
                section_start=SECTION_HEAD_CHAR_START,
                section_end=SECTION_HEAD_CHAR_END
            )

            await edit_message_text(
                function_caller='VIEW_CHAR.START()',
                new_text=markdown_player_sheet,
                context=context,
                chat_id=chat_id,
                message_id=message_id,
                need_response=False,
                markdown=True,
                reply_markup=reply_markup,
            )
        else:
            markdown_player_sheet = create_text_in_box(
                text=markdown_player_sheet,
                section_name=SECTION_TEXT_CHAR,
                section_start=SECTION_HEAD_CHAR_START,
                section_end=SECTION_HEAD_CHAR_END
            )

            await reply_text(
                function_caller='VIEW_CHAR.START()',
                text=markdown_player_sheet,
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
    else:
        text = (
            'Você ainda não criou um personagem!\n'
            'Crie o seu personagem com o comando '
            f'/{create_char_commands[0]}.'
        )
        await reply_text(
            function_caller='VIEW_CHAR.START()',
            text=text,
            context=context,
            update=update,
            silent=silent,
            allow_sending_without_reply=True,
            need_response=False,
            skip_retry=False,
            auto_delete_message=MIN_AUTODELETE_TIME,
        )

VIEW_CHAR_HANDLERS = [
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
        start, pattern=fr'^{{"{REFRESH_VIEW_CHAR_PATTERN}":1'
    ),
]
