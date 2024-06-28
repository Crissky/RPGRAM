'''
Módulo responsável pela criação de personagens.
'''


import re

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    PrefixHandler,
    filters,
)

from bot.constants.create_char import (
    COMMANDS,
    CALLBACK_TEXT_YES,
    CALLBACK_TEXT_NO,
    CALLBACK_TEXT_RACES,
    CALLBACK_TEXT_CLASSES,
)
from bot.constants.filters import (
    BASIC_COMMAND_FILTER,
    PREFIX_COMMANDS
)
from bot.constants.sign_up_player import COMMANDS as COMMANDS_SIGN_UP_PLAYER
from bot.decorators import print_basic_infos
from bot.functions.chat import (
    call_telegram_message_function,
    edit_message_text,
    reply_typing
)
from bot.functions.general import get_attribute_group_or_player

from constant.time import TEN_MINUTES_IN_SECONDS

from repository.mongo import (
    ClasseModel,
    PlayerModel,
    CharacterModel,
    RaceModel,
    EquipsModel
)

from rpgram.boosters import Classe, Race
from rpgram.characters import BaseCharacter, PlayerCharacter


# ROUTES
(
    START_ROUTES,
    DELETE_ROUTES,
    CONFIRM_RACE_ROUTES,
    SELECT_CLASSE_ROUTES,
    CONFIRM_CLASSE_ROUTES,
    SELECT_NAME_ROUTES,
    CREATE_CHAR_ROUTES,
) = range(7)


@print_basic_infos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await reply_typing(
        function_caller='CREATE_CHAR.START()',
        update=update,
        context=context,
    )
    player_model = PlayerModel()
    char_model = CharacterModel()
    race_model = RaceModel()
    user_name = update.effective_user.name
    player_id = update.effective_user.id
    chat_id = update.effective_chat.id
    silent = get_attribute_group_or_player(chat_id, 'silent')

    if not player_model.get(player_id):
        reply_text_kwargs = dict(
            text=(
                f'Você precisa criar um perfil para criar um personagem.\n'
                f'Para isso, utilize o comando /{COMMANDS_SIGN_UP_PLAYER[0]}.'
            ),
            disable_notification=silent,
            allow_sending_without_reply=True
        )
        response = await call_telegram_message_function(
            function_caller='CREATE_CHAR.START()',
            function=update.effective_message.reply_text,
            context=context,
            need_response=True,
            skip_retry=False,
            **reply_text_kwargs,
        )

        return ConversationHandler.END

    player_character: BaseCharacter = char_model.get(player_id)
    if player_character:
        inline_keyboard = [
            [
                InlineKeyboardButton("Sim", callback_data=CALLBACK_TEXT_YES),
                InlineKeyboardButton("Não", callback_data=CALLBACK_TEXT_NO),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        reply_text_kwargs = dict(
            text=(
                f'Olá {user_name}, vocé já possui uma personagem criado.\n'
                f'Gostaria de apagá-lo?\n'
                f'APÓS APAGADO, O PERSONAGEM NÃO PODE SER RECUPERADO!!!\n\n'
                f'Personagem:\n'
                f'{player_character}'
            ),
            reply_markup=reply_markup,
            disable_notification=silent,
            allow_sending_without_reply=True
        )
        response = await call_telegram_message_function(
            function_caller='CREATE_CHAR.START()',
            function=update.effective_message.reply_text,
            context=context,
            need_response=True,
            skip_retry=False,
            **reply_text_kwargs,
        )
        context.user_data['response'] = response
        return DELETE_ROUTES

    inline_keyboard = [
        [InlineKeyboardButton(race, callback_data=race)]
        for race in race_model.get_all(query={'enemy': False}, fields=['name'])
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    reply_text_kwargs = dict(
        text=(
            'Vamos começar a criar o seu personagem.\n'
            'Você pode cancelar a criação a qualquer momento '
            'usando o comando /cancel.\n\n'
            'Escolha uma das raças abaixo:'
        ),
        reply_markup=reply_markup,
        disable_notification=silent,
        allow_sending_without_reply=True
    )
    response = await call_telegram_message_function(
        function_caller='CREATE_CHAR.START()',
        function=update.effective_message.reply_text,
        context=context,
        need_response=True,
        skip_retry=False,
        **reply_text_kwargs,
    )
    context.user_data['response'] = response

    return CONFIRM_RACE_ROUTES


# SELECT_CLASSE_ROUTES
@print_basic_infos
async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    race_model = RaceModel()
    query = update.callback_query
    chat_id = update.effective_chat.id
    message_id = update.effective_message.id
    inline_keyboard = [
        [InlineKeyboardButton(race, callback_data=race)]
        for race in race_model.get_all(query={'enemy': False}, fields=['name'])
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    new_text = 'Escolha uma das raças abaixo:'
    await edit_message_text(
        function_caller='CREATE_CHAR.START()',
        new_text=new_text,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        need_response=False,
        markdown=False,
        reply_markup=reply_markup,
    )

    return CONFIRM_RACE_ROUTES


# CONFIRM_RACE_ROUTES
@print_basic_infos
async def confirm_race(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> int:
    race_model = RaceModel()
    query = update.callback_query
    chat_id = update.effective_chat.id
    message_id = update.effective_message.id
    race_name = query.data
    context.user_data['race'] = race_name
    description = ''

    race: Race = race_model.get(race_name)
    if race:
        description = race.description

    inline_keyboard = [
        [
            InlineKeyboardButton("Sim", callback_data=CALLBACK_TEXT_YES),
            InlineKeyboardButton("Não", callback_data=CALLBACK_TEXT_NO),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    new_text = (
        f'Gostaria de criar um personagem com a raça "{race_name}"?\n\n'
        f'Descrição da Raça:\n'
        f'{description}\n'
        f'{race}'
    )
    await edit_message_text(
        function_caller='CREATE_CHAR.CONFIRM_RACE()',
        new_text=new_text,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        need_response=False,
        markdown=False,
        reply_markup=reply_markup,
    )

    return SELECT_CLASSE_ROUTES


# SELECT_CLASSE_ROUTES, SELECT_NAME_ROUTES
@print_basic_infos
async def select_classe(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> int:
    classe_model = ClasseModel()
    query = update.callback_query
    chat_id = update.effective_chat.id
    message_id = update.effective_message.id
    race_name = context.user_data['race']

    inline_keyboard = [
        [InlineKeyboardButton(classe, callback_data=classe)]
        for classe in classe_model.get_all(fields=['name'])
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    new_text = (
        f'Ótimo!!! O seu personagem será um "{race_name}".\n\n'
        f'Agora escolha uma das classes abaixo:'
    )
    await edit_message_text(
        function_caller='CREATE_CHAR.SELECT_CLASSE()',
        new_text=new_text,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        need_response=False,
        markdown=False,
        reply_markup=reply_markup,
    )

    return CONFIRM_CLASSE_ROUTES


# CONFIRM_CLASSE_ROUTES
@print_basic_infos
async def confirm_classe(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> int:
    classe_model = ClasseModel()
    query = update.callback_query
    chat_id = update.effective_chat.id
    message_id = update.effective_message.id
    classe_name = query.data
    context.user_data['classe'] = classe_name
    description = ''

    classe: Classe = classe_model.get(classe_name)
    if classe:
        description = classe.description

    inline_keyboard = [
        [
            InlineKeyboardButton("Sim", callback_data=CALLBACK_TEXT_YES),
            InlineKeyboardButton("Não", callback_data=CALLBACK_TEXT_NO),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    new_text = (
        f'Gostaria de criar um personagem da classe "{classe_name}"?\n\n'
        f'Descrição da Raça:\n'
        f'{description}\n'
        f'{classe}'
    )
    await edit_message_text(
        function_caller='CREATE_CHAR.CONFIRM_CLASSE()',
        new_text=new_text,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        need_response=False,
        markdown=False,
        reply_markup=reply_markup,
    )

    return SELECT_NAME_ROUTES


# SELECT_NAME_ROUTES
@print_basic_infos
async def select_name(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> int:
    query = update.callback_query
    chat_id = update.effective_chat.id
    message_id = update.effective_message.id
    classe_name = context.user_data['classe']

    new_text = (
        f'Ótimo!!! O seu personagem será um "{classe_name}".\n\n'
        f'Agora escreva o nome do seu personagem.\n'
        f'O nome de personagem deve conter entre 3 e 50 caracteres, '
        f'apenas letras, números, espaços, e traço "-".'
    )
    await edit_message_text(
        function_caller='CREATE_CHAR.SELECT_NAME()',
        new_text=new_text,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        need_response=False,
        markdown=False,
    )

    return CREATE_CHAR_ROUTES


# CREATE_CHAR_ROUTES
@print_basic_infos
async def create_char(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> int:
    character_name = update.effective_message.text.strip()
    chat_id = update.effective_chat.id
    silent = get_attribute_group_or_player(chat_id, 'silent')
    if not is_valid_char_name(character_name):
        reply_text_kwargs = dict(
            text=(
                f'"{character_name}" não é um nome de personagem válido.\n\n'
                f'O nome de personagem deve conter entre 3 e 50 caracteres, '
                f'apenas letras, números, espaços, e traço "-".'
            ),
            disable_notification=silent,
            allow_sending_without_reply=True
        )
        await call_telegram_message_function(
            function_caller='CREATE_CHAR.CREATE_CHAR()',
            function=update.effective_message.reply_text,
            context=context,
            need_response=False,
            skip_retry=False,
            **reply_text_kwargs,
        )

        return CREATE_CHAR_ROUTES

    race_model = RaceModel()
    classe_model = ClasseModel()
    char_model = CharacterModel()
    equips_model = EquipsModel()
    user_name = update.effective_user.name
    player_id = update.effective_user.id
    race_name = context.user_data['race']
    classe_name = context.user_data['classe']
    race: Race = race_model.get(race_name)
    classe: Classe = classe_model.get(classe_name)
    player_character = PlayerCharacter(
        player_id=player_id,
        player_name=user_name,
        char_name=character_name,
        classe=classe,
        race=race,
    )
    char_model.save(player_character)
    equips_model.save(player_character.equips)
    player_character: BaseCharacter = char_model.get(player_id)

    if player_character:
        reply_text_kwargs = dict(
            text=(
                f'Personagem Criado com sucesso!!!\n\n'
                f'{player_character}'
            ),
            disable_notification=silent,
            allow_sending_without_reply=True
        )
        await call_telegram_message_function(
            function_caller='CREATE_CHAR.CREATE_CHAR()',
            function=update.effective_message.reply_text,
            context=context,
            need_response=False,
            skip_retry=False,
            **reply_text_kwargs,
        )
    else:
        reply_text_kwargs = dict(
            text=(
                'Algo deu errado ao criar o personagem. '
                'Tente novamente mais tarde.\n\n'
                'Se o problema persistir, contacte o meu desenvolvedor.\n\n'
                f'user_name: {user_name}\n'
                f'player_id: {player_id}\n'
                f'race_name: {race_name}\n'
                f'classe_name: {classe_name}\n'
                f'character_name: {character_name}\n'
                f'race:\n{race}\n'
                f'classe:\n{classe}\n'
            ),
            disable_notification=silent,
            allow_sending_without_reply=True
        )
        await call_telegram_message_function(
            function_caller='CREATE_CHAR.CREATE_CHAR()',
            function=update.effective_message.reply_text,
            context=context,
            need_response=False,
            skip_retry=False,
            **reply_text_kwargs,
        )

    if 'response' in context.user_data:
        response = context.user_data['response']
        chat_id = response.chat_id
        message_id = response.id
        print(
            f'{__name__}.create_char(): '
            f'chat_id: {chat_id}, message_id: {message_id}'
        )
        delete_message_kwargs = dict(
            chat_id=chat_id,
            message_id=message_id,
        )
        await call_telegram_message_function(
            function_caller='CREATE_CHAR.CREATE_CHAR()',
            function=context.bot.delete_message,
            context=context,
            need_response=False,
            skip_retry=False,
            **delete_message_kwargs,
        )

    clean_user_data(context)

    return ConversationHandler.END


# DELETE_ROUTES
@print_basic_infos
async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    char_model = CharacterModel()
    chat_id = update.effective_chat.id
    player_id = update.effective_user.id
    message_id = update.effective_message.id
    query = update.callback_query

    if (char_model.delete(player_id)):
        new_text = ('Personagem deletado com sucesso!')
    else:
        new_text = (
            'Algo deu errado ao deletar o personagem. '
            'Tente novamente mais tarde.\n\n'
            'Se o problema persistir, contacte o meu desenvolvedor.'
        )
    await edit_message_text(
        function_caller='CREATE_CHAR.DELETE()',
        new_text=new_text,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        need_response=False,
        markdown=False,
    )

    clean_user_data(context)

    return ConversationHandler.END


# DELETE_ROUTES
@print_basic_infos
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    new_text = "Tchau! Você pode criar um personagem mais tarde."
    chat_id = update.effective_chat.id
    message_id = update.effective_message.id

    print(
        f'{__name__}.cancel():',
        f'chat_id: {chat_id}, message_id: {message_id}'
    )
    await edit_message_text(
        function_caller='CREATE_CHAR.CANCEL()',
        new_text=new_text,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        need_response=False,
        markdown=False,
    )
    if 'response' in context.user_data:
        del context.user_data['response']

    clean_user_data(context)

    return ConversationHandler.END


def clean_user_data(context: ContextTypes.DEFAULT_TYPE) -> None:
    keys = ['response', 'race', 'classe']
    for key in keys:
        if key in context.user_data:
            del context.user_data[key]


def is_valid_char_name(text):
    is_valid = True
    if len(text) < 3 or len(text) > 50:
        is_valid = False
    if re.search(r'[^à-úa-z0-9 -]|^[0-9 -]', text, re.IGNORECASE):
        is_valid = False
    return is_valid


CREATE_CHAR_HANDLER = ConversationHandler(
    entry_points=[
        PrefixHandler(
            PREFIX_COMMANDS,
            COMMANDS,
            start,
            BASIC_COMMAND_FILTER
        ),
        CommandHandler(COMMANDS, start, BASIC_COMMAND_FILTER),
    ],
    states={
        DELETE_ROUTES: [
            CallbackQueryHandler(delete, pattern=f'^{CALLBACK_TEXT_YES}$'),
            CallbackQueryHandler(cancel, pattern=f'^{CALLBACK_TEXT_NO}$')
        ],
        CONFIRM_RACE_ROUTES: [
            CallbackQueryHandler(
                confirm_race, pattern=f'^{CALLBACK_TEXT_RACES}$'
            )
        ],
        SELECT_CLASSE_ROUTES: [
            CallbackQueryHandler(
                select_classe, pattern=f'^{CALLBACK_TEXT_YES}$'
            ),
            CallbackQueryHandler(start_over, pattern=f'^{CALLBACK_TEXT_NO}$')
        ],
        CONFIRM_CLASSE_ROUTES: [
            CallbackQueryHandler(
                confirm_classe, pattern=f'^{CALLBACK_TEXT_CLASSES}$'
            )
        ],
        SELECT_NAME_ROUTES: [
            CallbackQueryHandler(
                select_name, pattern=f'^{CALLBACK_TEXT_YES}$'
            ),
            CallbackQueryHandler(
                select_classe, pattern=f'^{CALLBACK_TEXT_NO}$'
            )
        ],
        CREATE_CHAR_ROUTES: [
            MessageHandler(
                filters.TEXT &
                ~filters.COMMAND &
                BASIC_COMMAND_FILTER,
                create_char
            )
        ]
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    conversation_timeout=TEN_MINUTES_IN_SECONDS,
    allow_reentry=True
)

if __name__ == '__main__':
    race_model = RaceModel()
    print([
        InlineKeyboardButton(race, callback_data=race)
        for race in race_model.get_all(query={'enemy': False}, fields=['name'])
    ])
