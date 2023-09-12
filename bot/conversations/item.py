from random import choice, randint
from time import sleep

from telegram import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update
)
from telegram.constants import ChatAction, ParseMode
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
)
from bot.constants.bag import CALLBACK_TEXT_DESTROY_ITEM
from bot.constants.item import (
    CALLBACK_TEXT_GET,
    CALLBACK_TEXT_IGNORE,
    ESCAPED_CALLBACK_TEXT_GET,
    ESCAPED_CALLBACK_TEXT_IGNORE,
    REPLY_TEXTS_FIND_TRAP_DAMAGE,
    REPLY_TEXTS_FIND_TRAP_OPEN,
    REPLY_TEXTS_FIND_TREASURE_START,
    REPLY_TEXTS_FIND_TREASURE_MIDDLE,
    REPLY_TEXTS_FIND_TREASURE_END,
    REPLY_TEXTS_FIND_TREASURE_OPEN,
    REPLY_TEXTS_IGNORE_TREASURE,
)
from bot.constants.rest import COMMANDS as rest_commands
from bot.decorators import (
    need_have_char,
    need_singup_group,
    print_basic_infos
)
from bot.functions.char import add_damage, add_xp
from bot.functions.general import get_attribute_group_or_player
from telegram.ext import ConversationHandler
from function.datetime import get_brazil_time_now

from repository.mongo import BagModel, GroupModel, ItemModel
from repository.mongo.populate.item import create_random_item
from rpgram import Bag, Consumable
from rpgram.boosters import Equipment
from rpgram.enums import EmojiEnum


async def job_create_find_treasure(context: ContextTypes.DEFAULT_TYPE):
    '''Cria um evento de busca de tesouro que ocorrerá entre 1 e 29 minutos.
    Está função é chamada em cada 00 e 30 minutos de cada hora.
    '''
    group_model = GroupModel()
    job = context.job
    chat_id = int(job.chat_id)  # chat_id vem como string
    group = group_model.get(chat_id)
    spawn_start_time = group.spawn_start_time
    spawn_end_time = group.spawn_end_time
    now = get_brazil_time_now()

    if now.hour >= spawn_start_time and now.hour < spawn_end_time:
        weekend = [5, 6]
        times = randint(1, 2) if now.weekday() in weekend else 1
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
    else:
        print(
            f'Evento skipado, pois está fora do horário de spawn do grupo.\n'
            f'[{chat_id}] {group.name}: Hora: {now.hour}:{now.minute}.\n'
            f'Horário de spawn: {spawn_start_time}H - {spawn_end_time}H.'
        )


async def job_find_treasure(context: ContextTypes.DEFAULT_TYPE):
    '''Envia uma mensagem para o grupo com as opções de INVESTIGAR ou IGNORAR 
    uma busca por tesouro. A mensagem é gerada de maneira aleatória.
    '''
    job = context.job
    chat_id = int(job.chat_id)  # chat_id vem como string
    silent = get_attribute_group_or_player(chat_id, 'silent')
    print('job_find_treasure() - silent:', silent)
    text = choice(REPLY_TEXTS_FIND_TREASURE_START)
    text += choice(REPLY_TEXTS_FIND_TREASURE_MIDDLE)
    text += choice(REPLY_TEXTS_FIND_TREASURE_END)
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

    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        disable_notification=silent,
        reply_markup=reply_markup,
    )


@print_basic_infos
@need_singup_group
@need_have_char
async def inspect_treasure(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Cria de maneira aleatória um item (Consumable/Equipment) para o jogador 
    que clicou no botão de investigar e salva o item em sua bolsa.
    '''
    await update.effective_message.reply_chat_action(ChatAction.TYPING)
    bag_model = BagModel()
    items_model = ItemModel()
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_name = update.effective_user.name
    query = update.callback_query
    group_level = get_attribute_group_or_player(chat_id, 'group_level')
    silent = get_attribute_group_or_player(chat_id, 'silent')
    bag_exists = bag_model.exists(user_id)

    if not bag_exists:
        player_bag = Bag(
            items=[],
            player_id=user_id,
        )
        bag_model.save(player_bag)

    items = create_random_item(group_level)
    if isinstance(items, int):
        return await activated_trap(items, user_id, user_name, query)

    text_find_treasure_open = choice(REPLY_TEXTS_FIND_TREASURE_OPEN).lower()
    text = f'{user_name}, {text_find_treasure_open}\n\n'

    min_xp = group_level
    max_xp = int(group_level * 1.5)
    report_xp = add_xp(chat_id, user_id, min_xp=min_xp, max_xp=max_xp)
    level_up = report_xp['level_up']
    if level_up:
        new_level = report_xp['level']
        text += (
            f'{EmojiEnum.LEVEL_UP.value}'
            f'Parabéns\!\!\!{EmojiEnum.LEVEL_UP.value}\n'
            f'Você passou de nível\! '
            f'Seu personagem agora está no nível {new_level}\.'
        )
    else:
        xp = report_xp['xp']
        player_char = report_xp['char']
        text += (
            f'Você ganhou {xp} pontos de XP\.\n'
            f'Experiência: {player_char.bs.show_xp}'
        )

    print('inspect_treasure() - text:', text)
    await query.edit_message_text(
        text=text,
        parse_mode=ParseMode.MARKDOWN_V2
    )

    if isinstance(items, list):
        markdown_item_sheet = ''
        for item in items:
            time_sleep = 2
            sleep(time_sleep)
            item_id = str(item._id)
            drop = item.quantity
            reply_markup_drop = InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    text=f'{EmojiEnum.TAKE.value}Coletar',
                    callback_data=(
                        f'{{"_id":"{item_id}","drop":{drop}}}'
                    )
                ), InlineKeyboardButton(
                    text=f'Quebrar{EmojiEnum.DESTROY_ITEM.value}',
                    callback_data=CALLBACK_TEXT_DESTROY_ITEM
                )],
            ])

            if isinstance(item.item, Equipment):
                items_model.save(item.item)
            elif not isinstance(item.item, (Consumable, Equipment)):
                raise TypeError(
                    f'Variável item é do tipo "{type(item.item)}", '
                    f'mas precisa ser do tipo "Consumable" ou "Equipment".\n'
                    f'Item: {item.item}'
                )
            markdown_item_sheet = item.get_all_sheets(
                verbose=True, markdown=True
            )
            response = await update.effective_message.reply_text(
                text=f'O baú dropou o item:\n\n{markdown_item_sheet}',
                disable_notification=silent,
                reply_markup=reply_markup_drop,
                parse_mode=ParseMode.MARKDOWN_V2
            )
            message_id = response.message_id
            drops = context.chat_data.get('drop', None)
            if isinstance(drops, dict):
                drops[message_id] = True
            else:
                context.chat_data['drop'] = {message_id: True}
    else:
        raise TypeError(
            f'Variável items é do tipo "{type(items)}", mas precisar ser '
            f'do tipo "int" para dano de armadilhas ou do tipo "list" '
            f'para uma lista de itens que o jogador encontrou no baú.\n'
            f'Items: {items}.'
        )

    return ConversationHandler.END


async def activated_trap(
    damage: int,
    user_id: int,
    user_name: str,
    query: CallbackQuery
):
    damage_report = add_damage(damage, user_id=user_id)
    char = damage_report['char']
    text_find_trap_open = choice(REPLY_TEXTS_FIND_TRAP_OPEN)
    text_find_trap_damage = choice(REPLY_TEXTS_FIND_TRAP_DAMAGE).format(
        user_name=user_name
    )
    text = (
        f'{text_find_trap_open}\n\n'
        f'{text_find_trap_damage} "{damage}" pontos de dano.\n\n'
    )
    if damage_report['dead']:
        text += 'Seus pontos de vida chegaram a zero.\n'
        text += (
            f'Use o comando /{rest_commands[0]} '
            f'para descansar e poder continuar a sua jornada.\n\n'
        )
    text += f'HP: {char.combat_stats.show_hit_points}'
    await query.edit_message_text(text=text)

    return ConversationHandler.END


@print_basic_infos
@need_singup_group
@need_have_char
async def ignore_treasure(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Apaga a mensagem de busca de tesouro quando um jogador 
    clica em IGNORAR.
    '''
    query = update.callback_query
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
