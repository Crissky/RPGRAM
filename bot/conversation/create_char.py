import re
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    MessageEntity,
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
from telegram.constants import ChatAction

from repository.mongo import (
    ClasseModel,
    PlayerModel,
    PlayerCharacterModel,
    RaceModel,
)
from rpgram.characters import PlayerCharacter


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

# CALLBACK DATA
CALLBACK_TEXT_YES = 'yes'
CALLBACK_TEXT_NO = 'no'
CALLBACK_TEXT_RACES = '|'.join(RaceModel().get_all(fields=['name']))
CALLBACK_TEXT_CLASSES = '|'.join(ClasseModel().get_all(fields=['name']))

COMMANDS = ['createchar', 'criarpersonagem']


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    update.effective_message.reply_chat_action(ChatAction.TYPING)
    player_model = PlayerModel()
    player_character_model = PlayerCharacterModel()
    race_model = RaceModel()
    user_name = update.effective_user.name
    player_id = update.effective_user.id

    if not player_model.get(player_id):
        response = await update.effective_message.reply_text(
            f'Você precisa criar um perfil para criar um personagem.\n'
            f'Para isso, utilize o comando /criarconta.'
        )

        return ConversationHandler.END

    if (player_character := player_character_model.get(player_id)):
        inline_keyboard = [
            [
                InlineKeyboardButton("Sim", callback_data=CALLBACK_TEXT_YES),
                InlineKeyboardButton("Não", callback_data=CALLBACK_TEXT_NO),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        response = await update.effective_message.reply_text(
            f'Olá {user_name}, vocé já possui uma personagem criado.\n'
            f'Gostaria de deletá-lo?\n\n'
            f'Personagem:\n'
            f'{player_character}',
            reply_markup=reply_markup,
        )
        context.user_data['response'] = response
        return DELETE_ROUTES

    inline_keyboard = [
        [InlineKeyboardButton(race, callback_data=race)]
        for race in race_model.get_all(fields=['name'])
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    response = await update.effective_message.reply_text(
        'Vamos começar a criar o seu personagem.\n'
        'Você pode cancelar a criação a qualquer momento '
        'usando o comando /cancel.\n\n'
        'Escolha uma das raças abaixo:',
        reply_markup=reply_markup,
    )
    context.user_data['response'] = response

    return CONFIRM_RACE_ROUTES


async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    race_model = RaceModel()
    query = update.callback_query
    inline_keyboard = [
        [InlineKeyboardButton(race, callback_data=race)]
        for race in race_model.get_all(fields=['name'])
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    await query.edit_message_text(
        'Escolha uma das raças abaixo:',
        reply_markup=reply_markup,
    )

    return CONFIRM_RACE_ROUTES


async def confirm_race(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> int:
    race_model = RaceModel()
    query = update.callback_query
    race_name = query.data
    context.user_data['race'] = race_name
    description = ''

    if (race := race_model.get(race_name)):
        description = race.description

    inline_keyboard = [
        [
            InlineKeyboardButton("Sim", callback_data=CALLBACK_TEXT_YES),
            InlineKeyboardButton("Não", callback_data=CALLBACK_TEXT_NO),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    await query.edit_message_text(
        f'Gostaria de criar um personagem com a raça "{race_name}"?\n\n'
        f'Descrição da Raça:\n'
        f'{description}\n'
        f'{race}',
        reply_markup=reply_markup,
    )

    return SELECT_CLASSE_ROUTES


async def select_classe(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> int:
    classe_model = ClasseModel()
    query = update.callback_query
    race_name = context.user_data['race']

    inline_keyboard = [
        [InlineKeyboardButton(classe, callback_data=classe)]
        for classe in classe_model.get_all(fields=['name'])
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    await query.edit_message_text(
        f'Ótimo!!! O seu personagem será um "{race_name}".\n\n'
        f'Agora escolha uma das classes abaixo:',
        reply_markup=reply_markup,
    )

    return CONFIRM_CLASSE_ROUTES


async def confirm_classe(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> int:
    classe_model = ClasseModel()
    query = update.callback_query
    classe_name = query.data
    context.user_data['classe'] = classe_name
    description = ''

    if (classe := classe_model.get(classe_name)):
        description = classe.description

    inline_keyboard = [
        [
            InlineKeyboardButton("Sim", callback_data=CALLBACK_TEXT_YES),
            InlineKeyboardButton("Não", callback_data=CALLBACK_TEXT_NO),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    await query.edit_message_text(
        f'Gostaria de criar um personagem da classe "{classe_name}"?\n\n'
        f'Descrição da Raça:\n'
        f'{description}\n'
        f'{classe}',
        reply_markup=reply_markup,
    )

    return SELECT_NAME_ROUTES


async def select_name(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> int:
    query = update.callback_query
    classe_name = context.user_data['classe']

    await query.edit_message_text(
        f'Ótimo!!! O seu personagem será um "{classe_name}".\n\n'
        f'Agora escreva o nome do seu personagem.\n'
        f'O nome de personagem deve conter entre 3 e 50 caracteres, '
        f'apenas letras, números, espaços, e traço "-"'
    )

    return CREATE_CHAR_ROUTES


async def create_char(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> int:
    character_name = update.effective_message.text.strip()
    if not is_valid_char_name(character_name):
        await update.effective_message.reply_text(
            f'"{character_name}" não é um nome de personagem válido.\n\n'
            f'O nome de personagem deve conter entre 3 e 50 caracteres, '
            f'apenas letras, números, espaços, e traço "-"'
        )

        return CREATE_CHAR_ROUTES

    race_model = RaceModel()
    classe_model = ClasseModel()
    player_character_model = PlayerCharacterModel()
    user_name = update.effective_user.name
    player_id = update.effective_user.id
    race_name = context.user_data['race']
    classe_name = context.user_data['classe']
    race = race_model.get(race_name)
    classe = classe_model.get(classe_name)
    player_character = PlayerCharacter(
        player_id=player_id,
        player_name=user_name,
        char_name=character_name,
        classe=classe,
        race=race,
    )
    player_character_model.save(player_character)
    player_character = player_character_model.get(player_id)

    if player_character:
        await update.effective_message.reply_text(
            f'Personagem Criado com sucesso!!!\n\n'
            f'{player_character}'
        )
    else:
        await update.effective_message.reply_text(
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
        )

    if 'response' in context.user_data:
        response = context.user_data['response']
        chat_id = response.chat_id
        message_id = response.id
        print(
            f'create_char.create_char(): '
            f'chat_id: {chat_id}, message_id: {message_id}'
        )
        await update.get_bot().delete_message(
            chat_id=chat_id,
            message_id=message_id,
        )

    clean_user_data(context)

    return ConversationHandler.END


async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    player_character_model = PlayerCharacterModel()
    player_id = update.effective_user.id
    query = update.callback_query

    if (player_character_model.delete(player_id)):
        await query.edit_message_text('Personagem deletado com sucesso!')
    else:
        await query.edit_message_text(
            'Algo deu errado ao deletar o personagem. '
            'Tente novamente mais tarde.\n\n'
            'Se o problema persistir, contacte o meu desenvolvedor.'
        )

    clean_user_data(context)

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    new_text = "Tchau! Você pode criar um personagem mais tarde."

    if 'response' in context.user_data:
        response = context.user_data['response']
        chat_id = response.chat_id
        message_id = response.id
        print(
            f'create_char.cancel(): '
            f'chat_id: {chat_id}, message_id: {message_id}'
        )
        await update.get_bot().edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=new_text,
        )
    elif update.callback_query:
        # await update.callback_query.answer()
        await update.callback_query.edit_message_text(new_text)

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
        CommandHandler("createchar", start),
        CommandHandler("criarpersonagem", start),
        MessageHandler(
            filters.Regex(rf'^!({"|".join(COMMANDS)})$') &
            ~filters.FORWARDED &
            ~filters.UpdateType.EDITED &
            ~filters.Entity(MessageEntity.URL) &
            ~filters.Entity(MessageEntity.TEXT_LINK),
            start
        )
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
                ~filters.FORWARDED &
                ~filters.UpdateType.EDITED &
                ~filters.Entity(MessageEntity.URL) &
                ~filters.Entity(MessageEntity.TEXT_LINK),
                create_char
            )
        ]
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

if __name__ == '__main__':
    race_model = RaceModel()
    print([
        InlineKeyboardButton(race, callback_data=race)
        for race in race_model.get_all(fields=['name'])
    ])
