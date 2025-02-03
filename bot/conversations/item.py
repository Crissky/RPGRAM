'''
Módulo responsável por gerenciar o evento de Baú do Tesouro.
'''


from datetime import timedelta
from random import choice
from typing import Iterable

from bson import ObjectId
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update
)
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
    TRAP_DAMAGE_TYPE_RATIO,
)
from bot.constants.job import BASE_JOB_KWARGS
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
from bot.functions.char import (
    add_conditions_from_trap,
    add_trap_damage,
    add_xp
)
from bot.functions.chat import (
    answer,
    call_telegram_message_function,
    delete_message,
    delete_message_from_context,
    edit_message_text,
    edit_message_text_and_forward,
    reply_typing
)
from bot.functions.config import get_attribute_group
from bot.functions.general import (
    get_attribute_group_or_player
)
from constant.text import (
    SECTION_HEAD_OPEN_TREASURE_END,
    SECTION_HEAD_OPEN_TREASURE_START,
    SECTION_HEAD_TRAP_END,
    SECTION_HEAD_TRAP_START,
    SECTION_HEAD_TREASURE_END,
    SECTION_HEAD_TREASURE_START
)
from function.text import create_text_in_box, escape_markdown_v2

from repository.mongo import BagModel
from repository.mongo.populate.item import create_random_item
from rpgram import Bag
from rpgram.boosters import Equipment
from rpgram.consumables import Consumable
from rpgram.enums import EmojiEnum


TREASURES_CHAT_DATA_KEY = 'treasures'
MINUTES_TO_TIMEOUT_FIND_TREASURE = 60


@skip_if_spawn_timeout
async def job_find_treasure(context: ContextTypes.DEFAULT_TYPE):
    '''Envia uma mensagem para o grupo com as opções de INVESTIGAR ou IGNORAR 
    uma busca por tesouro. A mensagem é gerada de maneira aleatória.
    '''

    print('JOB_FIND_TREASURE()')
    job = context.job
    chat_id = job.chat_id
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

    call_telegram_kwargs = dict(
        chat_id=chat_id,
        text=text,
        disable_notification=silent,
        reply_markup=reply_markup,
    )
    response = await call_telegram_message_function(
        function_caller='JOB_FIND_TREASURE()',
        function=context.bot.send_message,
        context=context,
        auto_delete_message=False,
        **call_telegram_kwargs,
    )
    message_id = response.message_id
    treasures = context.chat_data.get(TREASURES_CHAT_DATA_KEY, None)
    if isinstance(treasures, dict):
        treasures[message_id] = True
    else:
        context.chat_data[TREASURES_CHAT_DATA_KEY] = {message_id: True}

    context.job_queue.run_once(
        callback=job_timeout_find_treasure,
        when=timedelta(minutes=MINUTES_TO_TIMEOUT_FIND_TREASURE),
        data={'message_id': message_id},
        name=f'JOB_TIMEOUT_FIND_TREASURE_{ObjectId()}',
        chat_id=chat_id,
        job_kwargs=BASE_JOB_KWARGS,
    )


async def job_timeout_find_treasure(context: ContextTypes.DEFAULT_TYPE):
    '''Job que exclui a mensagem do Baú do Tesouro e retira no dicionário o 
    ID do mesmo após um tempo pré determinado.
    '''

    print('JOB_TIMEOUT_FIND_TREASURE()')
    job = context.job
    data = job.data
    message_id = data['message_id']
    treasures = context.chat_data.get(TREASURES_CHAT_DATA_KEY, {})
    treasures.pop(message_id, None)

    await delete_message_from_context(
        function_caller='JOB_TIMEOUT_FIND_TREASURE()',
        context=context,
        message_id=message_id
    )


@need_singup_group
@skip_if_dead_char
@skip_if_immobilized
@confusion()
@print_basic_infos
async def inspect_treasure(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Cria de maneira aleatória um item (Consumable/Equipment) para o jogador 
    que clicou no botão de investigar e salva o item em sua bolsa.
    '''

    print('INSPECT_TREASURE()')
    query = update.callback_query
    message_id = update.effective_message.message_id
    treasures = {}

    # Checa se o baú pode ser aberto, se não, cancela a ação e apaga a mensagem
    # Só pode ser aberto se no dicionário drop contiver o message_id como chave
    # e True como valor. Caso contrário, cancela a ação e apaga a mensagem.
    if context.chat_data and TREASURES_CHAT_DATA_KEY in context.chat_data:
        treasures = context.chat_data[TREASURES_CHAT_DATA_KEY]
    if treasures.get(message_id, None) is not True:
        treasures.pop(message_id, None)
        query_text = f'Este tesouro já foi descoberto.'
        await answer(query=query, text=query_text, show_alert=True)
        await delete_message(
            function_caller='INSPECT_TREASURE()',
            context=context,
            query=query,
        )

        return ConversationHandler.END

    await reply_typing(
        function_caller='ITEM.INSPECT_TREASURE()',
        update=update,
        context=context,
    )
    bag_model = BagModel()
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_name = update.effective_user.name
    group_level = get_attribute_group(chat_id, 'group_level')
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

    await edit_message_text_and_forward(
        function_caller='INSPECT_TREASURE()',
        new_text=text,
        user_ids=user_id,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        need_response=False,
        markdown=True,
    )

    if isinstance(items, (list, Iterable)):
        for item in items:
            if not isinstance(item.item, (Consumable, Equipment)):
                raise TypeError(
                    f'Variável item é do tipo "{type(item.item)}", '
                    f'mas precisa ser do tipo "Consumable" ou "Equipment".\n'
                    f'Item: {item.item}'
                )
            await send_drop_message(
                context=context,
                items=item,
                text='O baú dropou o item',
                update=update,
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
    '''Ativa armadilha que causa dano e debuffs ao jogador que 
    tentou abrir o baú.
    '''

    print('ACTIVATED_TRAP()')
    chat_id = update.effective_chat.id
    message_id = update.effective_message.message_id
    (
        text_open_trap,
        trap_damage_type_enum,
        trap_condition_list
    ) = choice(REPLY_TEXTS_FIND_TRAP_OPEN)
    text_find_trap_damage = choice(
        REPLY_TEXTS_FIND_TRAP_DAMAGE
    ).format(user_name=user_name)
    type_damage_name = trap_damage_type_enum.name
    type_damage_ratio = TRAP_DAMAGE_TYPE_RATIO[type_damage_name]

    condition_report = add_conditions_from_trap(
        condition_list=trap_condition_list,
        group_level=group_level,
        user_id=user_id
    )
    damage_report = add_trap_damage(
        min_ratio_damage=type_damage_ratio,
        char=condition_report['char'],
        damage_type=trap_damage_type_enum
    )

    damage = (
        damage_report['attack']
        if 'attack' in damage_report
        else damage_report['damage']
    )
    absolute_damage = damage_report['absolute_damage']
    condition_report_text = condition_report["text"]
    text = (
        f'{text_open_trap}\n\n'
        f'{text_find_trap_damage} "{absolute_damage}"({damage}) '
        f'pontos de dano do tipo "{trap_damage_type_enum.value}".\n\n'
        f'{condition_report_text}'
    )
    if damage_report['dead']:
        drop_items = drop_random_items_from_bag(user_id=user_id)
        await send_drop_message(
            context=context,
            items=drop_items,
            text=f'{user_name} morreu e dropou o item',
            update=update,
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

    await edit_message_text_and_forward(
        function_caller='ACTIVATED_TRAP()',
        new_text=text,
        user_ids=user_id,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        need_response=False,
        markdown=False,
    )

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

    print('IGNORE_TREASURE()')
    query = update.callback_query
    chat_id = update.effective_chat.id
    message_id = update.effective_message.message_id
    treasures = context.chat_data.get(TREASURES_CHAT_DATA_KEY, {})
    treasures.pop(message_id, None)

    if query:
        text = choice(REPLY_TEXTS_IGNORE_TREASURE)
        await edit_message_text(
            function_caller='ITEM.IGNORE_TREASURE()',
            new_text=text,
            context=context,
            chat_id=chat_id,
            message_id=message_id,
            need_response=False,
            markdown=False,
        )

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
