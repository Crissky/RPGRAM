import re

from random import choice, randint

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
from bot.constants.item import (
    REPLY_TEXTS_FIND_TRAP_DAMAGE,
    REPLY_TEXTS_FIND_TRAP_OPEN,
    REPLY_TEXTS_FIND_TREASURE_START,
    REPLY_TEXTS_FIND_TREASURE_MIDDLE,
    REPLY_TEXTS_FIND_TREASURE_END,
    REPLY_TEXTS_FIND_TREASURE_OPEN,
    REPLY_TEXTS_FIND_TREASURE_FINDING,
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
from constant.text import TEXT_SEPARATOR
from function.datetime import get_brazil_time_now

from repository.mongo import BagModel, GroupModel, ItemModel
from repository.mongo.populate.item import create_random_item
from rpgram import Bag, Consumable
from rpgram.boosters import Equipment


CALLBACK_TEXT_YES = '$get_item'
CALLBACK_TEXT_NO = '$drop_item'
ESCAPED_CALLBACK_TEXT_YES = re.escape(CALLBACK_TEXT_YES)
ESCAPED_CALLBACK_TEXT_NO = re.escape(CALLBACK_TEXT_NO)


async def job_create_find_treasure(context: ContextTypes.DEFAULT_TYPE):
    '''Cria um evento de busca de tesouro que ocorrerá entre 1 e 29 minutos.
    Está função é chamada em cada 00 e 30 minutos de cada hora.
    '''
    group_model = GroupModel()
    job = context.job
    chat_id = job.chat_id  # chat_id vem como string
    minutes_in_seconds = randint(1, 29) * 60
    group = group_model.get(int(chat_id))
    spawn_start_time = group.spawn_start_time
    spawn_end_time = group.spawn_end_time
    now = get_brazil_time_now()

    if now.hour >= spawn_start_time and now.hour < spawn_end_time:
        print(
            f'JOB_CREATE_FIND_TREASURE() - {now}: '
            f'Evento de item inicia em {minutes_in_seconds // 60} minutos.'
        )
        context.job_queue.run_once(
            callback=job_find_treasure,
            when=minutes_in_seconds,
            name='JOB_CREATE_EVENTE_TREASURE',
            chat_id=chat_id,
        )
    else:
        print(
            f'Evento skipado, pois está fora do horário de spawn do grupo\n'
            f'[{chat_id}] {group.name}: Hora: {now.hour}:{now.minute}\n'
            f'Horário de spawn: {spawn_start_time}H - {spawn_end_time}H.'
        )


async def job_find_treasure(context: ContextTypes.DEFAULT_TYPE):
    '''Envia uma mensagem para o grupo com as opções de INVESTIGAR ou IGNORAR 
    uma busca por tesouro. A mensagem é gerada de maneira aleatória.
    '''
    job = context.job
    chat_id = job.chat_id
    silent = get_attribute_group_or_player(chat_id, 'silent')
    print('job_find_treasure() - silent:', silent)
    text = choice(REPLY_TEXTS_FIND_TREASURE_START)
    text += choice(REPLY_TEXTS_FIND_TREASURE_MIDDLE)
    text += choice(REPLY_TEXTS_FIND_TREASURE_END)
    inline_keyboard = [[
        InlineKeyboardButton(
            'Investigar', callback_data=CALLBACK_TEXT_YES),
        InlineKeyboardButton('Ignorar', callback_data=CALLBACK_TEXT_NO),
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
    query = update.callback_query
    if query:
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id
        user_name = update.effective_user.name
        group_level = get_attribute_group_or_player(chat_id, 'higher_level')
        bag_model = BagModel()
        items_model = ItemModel()
        player_bag = bag_model.get(query={'player_id': user_id})

        if not player_bag:
            player_bag = Bag(
                items=[],
                player_id=user_id,
            )

        items = create_random_item(group_level)
        if isinstance(items, int):
            return await activated_trap(items, user_id, user_name, query)
        elif isinstance(items, list):
            markdown_item_sheet = ''
            for item in items:
                if isinstance(item.item, Equipment):
                    items_model.save(item.item)
                    markdown_item_sheet += item.get_all_sheets(
                        verbose=True, markdown=True
                    )
                elif isinstance(item.item, Consumable):
                    markdown_item_sheet += item.get_sheet(
                        verbose=True, markdown=True
                    )
                else:
                    raise TypeError(
                        f'Variável item é do tipo "{type(item)}", mas precisa '
                        f'ser do tipo "Equipment" ou "Consumable".\n'
                        f'Item: {item}'
                    )
                markdown_item_sheet += f'{TEXT_SEPARATOR}\n'
                player_bag.add(item)
        else:
            raise TypeError(
                f'Variável items é do tipo "{type(items)}", mas precisar ser '
                f'do tipo "int" para dano de armadilhas ou do tipo "list" '
                f'para uma lista de itens que o jogador encontrou no baú.\n'
                f'Items: {items}.'
            )

        bag_model.save(player_bag)

        text_find_treasure_open = choice(REPLY_TEXTS_FIND_TREASURE_OPEN)
        text_find_treasure_finding = choice(
            REPLY_TEXTS_FIND_TREASURE_FINDING
        ).format(user_name=user_name)

        text = f'{text_find_treasure_open}\n\n'
        text += f'{text_find_treasure_finding}\n'
        text += f'{markdown_item_sheet}\n\n'

        min_xp = group_level
        max_xp = int(group_level * 1.5)
        report_xp = add_xp(chat_id, user_id, min_xp=min_xp, max_xp=max_xp)
        level_up = report_xp['level_up']
        if level_up:
            new_level = report_xp['level']
            text += (
                f'Parabéns\!\!\!\n'
                f'Você passou de nível\! '
                f'Seu personagem agora está no nível {new_level}\.'
            )
        else:
            xp = report_xp['xp']
            player_char = report_xp['char']
            text += (
                f'Você ganhou {xp} de XP\.\n'
                f'Experiência: {player_char.bs.show_xp}'
            )

        await query.edit_message_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN_V2
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
        await query.edit_message_text(
            text=text
        )
    return ConversationHandler.END


TREASURE_HANDLERS = [
    CallbackQueryHandler(
        inspect_treasure,
        pattern=f'^{ESCAPED_CALLBACK_TEXT_YES}$',
    ),
    CallbackQueryHandler(
        ignore_treasure,
        pattern=f'^{ESCAPED_CALLBACK_TEXT_NO}$',
    ),
]
