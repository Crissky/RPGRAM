'''
Módulo responsável por gerenciar as requisiçães de visualização das 
informações dos jogadores.
'''


from telegram import Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    PrefixHandler,
)

from bot.constants.view_char import ACCESS_DENIED, COMMANDS, REFRESH_VIEW_CHAR_PATTERN, SECTION_TEXT_CHAR
from bot.constants.create_char import COMMANDS as create_char_commands
from bot.constants.filters import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.conversations.close import get_close_keyboard, get_random_refresh_text, get_refresh_close_keyboard
from bot.decorators import print_basic_infos
from bot.functions.general import get_attribute_group_or_player
from constant.text import SECTION_HEAD_CHAR_END, SECTION_HEAD_CHAR_START
from function.text import create_text_in_box

from repository.mongo import CharacterModel


@print_basic_infos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_message.reply_chat_action(ChatAction.TYPING)
    char_model = CharacterModel()
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    silent = get_attribute_group_or_player(chat_id, 'silent')
    query = update.callback_query
    args = context.args

    player_character = char_model.get(user_id)
    verbose = False
    self_char = True

    if query:
        data = eval(query.data)
        refresh = data.get(REFRESH_VIEW_CHAR_PATTERN, False)
        data_user_id = data['user_id']

        # Não executa se outro usuário mexer na bolsa
        if data_user_id != user_id:
            await query.answer(text=ACCESS_DENIED, show_alert=True)
            return None

    if args and len(args) in [1, 2]:
        if args[0].startswith('@'):
            self_char = False
            player_name = args[0]
            query = {'player_name': player_name}
            new_player_character = char_model.get(query=query)
            if not new_player_character:
                await update.effective_message.reply_text(
                    f'{player_name} não possui um personamgem.',
                    disable_notification=silent
                )
                return None
            player_character = new_player_character
            verbose = 'verbose' in args[1:2] or 'v' in args[1:2]
        else:
            verbose = 'verbose' in args[0] or 'v' in args[0]

    if player_character:
        markdown_player_sheet = player_character.get_all_sheets(
            verbose=verbose, markdown=True
        )

        # Cria os botões de refresh/fechar ou botão de fechar
        if self_char:
            reply_markup = get_refresh_close_keyboard(
                user_id=user_id,
                refresh_data=REFRESH_VIEW_CHAR_PATTERN
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

            await query.edit_message_text(
                f'{markdown_player_sheet}',
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=reply_markup
            )
        else:
            markdown_player_sheet = create_text_in_box(
                text=markdown_player_sheet,
                section_name=SECTION_TEXT_CHAR,
                section_start=SECTION_HEAD_CHAR_START,
                section_end=SECTION_HEAD_CHAR_END
            )

            await update.effective_message.reply_text(
                markdown_player_sheet,
                parse_mode=ParseMode.MARKDOWN_V2,
                disable_notification=silent,
                reply_markup=reply_markup
            )
    else:
        await update.effective_message.reply_text(
            f'Você ainda não criou um personagem!\n'
            f'Crie o seu personagem com o comando /{create_char_commands[0]}.',
            disable_notification=silent
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
