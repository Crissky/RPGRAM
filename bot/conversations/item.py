from random import choice, randint

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update
)
from telegram.constants import ChatAction, ParseMode
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
)
from bot.constants.item import (
    CALLBACK_TEXT_GET,
    CALLBACK_TEXT_IGNORE,
    ESCAPED_CALLBACK_TEXT_GET,
    ESCAPED_CALLBACK_TEXT_IGNORE,
    MAX_DROP_ITEMS,
    REPLY_TEXTS_FIND_TRAP_DAMAGE,
    REPLY_TEXTS_FIND_TRAP_OPEN,
    REPLY_TEXTS_FIND_TREASURE_START,
    REPLY_TEXTS_FIND_TREASURE_MIDDLE,
    REPLY_TEXTS_FIND_TREASURE_END,
    REPLY_TEXTS_FIND_TREASURE_OPEN,
    REPLY_TEXTS_IGNORE_TREASURE,
    SECTION_TEXT_ACTIVATED_TRAP,
    SECTION_TEXT_DROP_TREASURE,
    SECTION_TEXT_OPEN_TREASURE,
    TRAP_TYPE_DAMAGE_MULTIPLIER,
)
from bot.constants.rest import COMMANDS as rest_commands
from bot.conversations.bag import send_drop_message
from bot.decorators import (
    need_singup_group,
    print_basic_infos,
    skip_if_dead_char,
    skip_if_immobilized,
)
from bot.decorators.char import confusion
from bot.decorators.job import skip_if_spawn_timeout
from bot.functions.bag import drop_random_items_from_bag
from bot.functions.char import add_conditions_trap, add_damage, add_xp
from bot.functions.date_time import is_boosted_day
from bot.functions.general import get_attribute_group_or_player
from constant.text import (
    SECTION_HEAD_OPEN_TREASURE_END,
    SECTION_HEAD_OPEN_TREASURE_START,
    SECTION_HEAD_TRAP_END,
    SECTION_HEAD_TRAP_START,
    SECTION_HEAD_TREASURE_END,
    SECTION_HEAD_TREASURE_START
)
from function.date_time import get_brazil_time_now
from function.text import create_text_in_box, escape_markdown_v2

from repository.mongo import BagModel, ItemModel
from repository.mongo.populate.item import create_random_item
from rpgram import Bag
from rpgram.boosters import Equipment
from rpgram.consumables import Consumable
from rpgram.enums import EmojiEnum


@skip_if_spawn_timeout
async def job_create_find_treasure(context: ContextTypes.DEFAULT_TYPE):
    '''Cria um evento de busca de tesouro que ocorrerá entre 1 e 29 minutos.
    Está função é chamada em cada 00 e 30 minutos de cada hora.
    '''
    job = context.job
    chat_id = int(job.chat_id)  # chat_id vem como string
    now = get_brazil_time_now()

    times = randint(1, 2) if is_boosted_day(now) else 1
    for i in range(times):
        minutes_in_seconds = randint(1, 29) * 60
        print(
            f'JOB_CREATE_FIND_TREASURE() - {now}: '
            f'Evento de item inicia em {minutes_in_seconds // 60} minutos.'
        )
        context.job_queue.run_once(
            callback=job_find_treasure,
            when=minutes_in_seconds,
            name=f'JOB_CREATE_EVENTE_TREASURE_{i}',
            chat_id=chat_id,
        )


async def job_find_treasure(context: ContextTypes.DEFAULT_TYPE):
    '''Envia uma mensagem para o grupo com as opções de INVESTIGAR ou IGNORAR 
    uma busca por tesouro. A mensagem é gerada de maneira aleatória.
    '''
    job = context.job
    chat_id = int(job.chat_id)  # chat_id vem como string
    silent = get_attribute_group_or_player(chat_id, 'silent')
    text = choice(REPLY_TEXTS_FIND_TREASURE_START)
    text += choice(REPLY_TEXTS_FIND_TREASURE_MIDDLE)
    text += choice(REPLY_TEXTS_FIND_TREASURE_END)
    text = create_text_in_box(
        text=text,
        section_name=SECTION_TEXT_DROP_TREASURE,
        section_start=SECTION_HEAD_TREASURE_START,
        section_end=SECTION_HEAD_TREASURE_END,
        clean_func=None
    )
    inline_keyboard = [[
        InlineKeyboardButton(
            f'{EmojiEnum.INSPECT.value}Investigar',
            callback_data=CALLBACK_TEXT_GET
        ),
        InlineKeyboardButton(
            f'Ignorar{EmojiEnum.IGNORE.value}',
            callback_data=CALLBACK_TEXT_IGNORE
        ),
    ]]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)

    response = await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        disable_notification=silent,
        reply_markup=reply_markup,
    )
    message_id = response.message_id
    treasures = context.chat_data.get('treasures', None)
    if isinstance(treasures, dict):
        treasures[message_id] = True
    else:
        context.chat_data['treasures'] = {message_id: True}


@need_singup_group
@skip_if_dead_char
@skip_if_immobilized
@confusion()
@print_basic_infos
async def inspect_treasure(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Cria de maneira aleatória um item (Consumable/Equipment) para o jogador 
    que clicou no botão de investigar e salva o item em sua bolsa.
    '''

    query = update.callback_query
    message_id = update.effective_message.message_id
    treasures = {}

    # Checa se o baú pode ser aberto, se não, cancela a ação e apaga a mensagem
    # Só pode ser aberto se no dicionário drop contiver o message_id como chave
    # e True como valor. Caso contrário, cancela a ação e apaga a mensagem.
    if 'treasures' in context.chat_data:
        treasures = context.chat_data['treasures']
        if treasures.get(message_id, None) is not True:
            treasures.pop(message_id, None)
            await query.answer(
                f'Este tesouro já foi descoberto.', show_alert=True
            )
            await query.delete_message()

            return ConversationHandler.END

    await update.effective_message.reply_chat_action(ChatAction.TYPING)
    bag_model = BagModel()
    items_model = ItemModel()
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_name = update.effective_user.name
    group_level = get_attribute_group_or_player(chat_id, 'group_level')
    silent = get_attribute_group_or_player(chat_id, 'silent')
    bag_exists = bag_model.exists(user_id)

    if not bag_exists:
        player_bag = Bag(
            items=[],
            player_id=user_id,
        )
        bag_model.save(player_bag)

    items = create_random_item(group_level, max_items=MAX_DROP_ITEMS)
    if isinstance(items, int):
        treasures.pop(message_id, None)
        return await activated_trap(
            damage=items,
            group_level=group_level,
            user_id=user_id,
            user_name=user_name,
            update=update,
            context=context
        )

    text_find_treasure_open = choice(REPLY_TEXTS_FIND_TREASURE_OPEN).lower()
    text = f'{user_name}, {text_find_treasure_open}\n\n'

    min_xp = group_level
    max_xp = int(group_level * 1.5)
    report_xp = add_xp(chat_id, user_id, min_xp=min_xp, max_xp=max_xp)
    text += report_xp['text']
    text = escape_markdown_v2(text)
    text = create_text_in_box(
        text=text,
        section_name=SECTION_TEXT_OPEN_TREASURE,
        section_start=SECTION_HEAD_OPEN_TREASURE_START,
        section_end=SECTION_HEAD_OPEN_TREASURE_END,
    )

    await query.edit_message_text(
        text=text,
        parse_mode=ParseMode.MARKDOWN_V2
    )

    if isinstance(items, list):
        for item in items:
            if isinstance(item.item, Equipment):
                items_model.save(item.item)
            elif not isinstance(item.item, (Consumable, Equipment)):
                raise TypeError(
                    f'Variável item é do tipo "{type(item.item)}", '
                    f'mas precisa ser do tipo "Consumable" ou "Equipment".\n'
                    f'Item: {item.item}'
                )
            await send_drop_message(
                update=update,
                context=context,
                items=item,
                text='O baú dropou o item',
                silent=silent,
            )
    else:
        raise TypeError(
            f'Variável items é do tipo "{type(items)}", mas precisar ser '
            f'do tipo "int" para dano de armadilhas ou do tipo "list" '
            f'para uma lista de itens que o jogador encontrou no baú.\n'
            f'Items: {items}.'
        )

    treasures.pop(message_id, None)

    return ConversationHandler.END


async def activated_trap(
    damage: int,
    group_level: int,
    user_id: int,
    user_name: str,
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    (
        text_find_trap_open,
        trap_type_damage,
        trap_conditions
    ) = choice(REPLY_TEXTS_FIND_TRAP_OPEN)
    text_find_trap_damage = choice(REPLY_TEXTS_FIND_TRAP_DAMAGE).format(
        user_name=user_name
    )
    type_damage_name = trap_type_damage.name
    type_damage_multiplier = TRAP_TYPE_DAMAGE_MULTIPLIER[type_damage_name]
    damage = int(type_damage_multiplier * damage)

    damage_report = add_damage(
        damage,
        user_id=user_id,
        type_damage=trap_type_damage
    )
    condition_report = add_conditions_trap(
        conditions_trap=trap_conditions,
        group_level=group_level,
        char=damage_report['char']
    )

    absolute_damage = damage_report['absolute_damage']
    condition_report_text = condition_report["text"]
    text = (
        f'{text_find_trap_open}\n\n'
        f'{text_find_trap_damage} "{absolute_damage}"({damage}) '
        f'pontos de dano do tipo "{trap_type_damage.value}".\n\n'
        f'{condition_report_text}'
    )
    if damage_report['dead']:
        drop_items = drop_random_items_from_bag(user_id=user_id)
        await send_drop_message(
            update=update,
            context=context,
            items=drop_items,
            text=f'{user_name} morreu e dropou o item',
            silent=True,
        )
        text += 'Seus pontos de vida chegaram a zero.\n'
        text += (
            f'Use o comando /{rest_commands[0]} '
            f'para descansar e poder continuar a sua jornada.\n\n'
        )
    text += f'{damage_report["text"]}\n'
    text += f'{damage_report.get("guard_text")}'
    text = create_text_in_box(
        text=text,
        section_name=SECTION_TEXT_ACTIVATED_TRAP,
        section_start=SECTION_HEAD_TRAP_START,
        section_end=SECTION_HEAD_TRAP_END,
        clean_func=None
    )

    await query.edit_message_text(text=text)

    return ConversationHandler.END


@need_singup_group
@skip_if_dead_char
@skip_if_immobilized
@confusion()
@print_basic_infos
async def ignore_treasure(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Apaga a mensagem de busca de tesouro quando um jogador 
    clica em IGNORAR.
    '''

    query = update.callback_query
    message_id = update.effective_message.message_id
    treasures = context.chat_data.get('treasures', {})
    treasures.pop(message_id, None)

    if query:
        text = choice(REPLY_TEXTS_IGNORE_TREASURE)
        await query.edit_message_text(text=text)
    return ConversationHandler.END


TREASURE_HANDLERS = [
    CallbackQueryHandler(
        inspect_treasure,
        pattern=f'^{ESCAPED_CALLBACK_TEXT_GET}$',
    ),
    CallbackQueryHandler(
        ignore_treasure,
        pattern=f'^{ESCAPED_CALLBACK_TEXT_IGNORE}$',
    ),
]
