from datetime import timedelta
from random import choice, randint

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
)

from bot.constants.quest_item import (
    ARRIVAL_NARRATION,
    CALLBACK_QUEST_PREFIX,
    DISAPPOINTED_NARRATION,
    LEAVE_NARRATION,
    PATTERN_ITEM_QUEST,
    QUEST_BUTTON_TEXT,
    REPLY_TEXT_GEMSTONE_ITEM,
    REPLY_TEXT_HEAL_CURE_ITEM,
    REPLY_TEXT_IDENTIFY_ITEM,
    REPLY_TEXT_REVIVE_ITEM,
    REPLY_TEXT_THANKS,
    REPLY_TEXT_TROCADO_ITEM,
    REPLY_TEXT_XP_ITEM,
    SECTION_TEXT_QUEST,
    SECTION_TEXT_QUEST_COMPLETE,
    SECTION_TEXT_QUEST_FAIL
)
from bot.conversations.bag import send_drop_message
from bot.decorators import (
    confusion,
    need_not_in_battle,
    print_basic_infos,
    skip_if_dead_char,
    skip_if_immobilized,
    skip_if_no_singup_player,
)
from bot.decorators.job import skip_if_spawn_timeout
from bot.functions.bag import get_item_from_bag_by_id
from bot.functions.char import add_xp
from bot.functions.chat import callback_data_to_dict, callback_data_to_string
from bot.functions.config import get_attribute_group
from bot.functions.date_time import is_boosted_day
from bot.functions.general import get_attribute_group_or_player

from constant.text import (
    SECTION_HEAD_QUEST_COMPLETE_END,
    SECTION_HEAD_QUEST_COMPLETE_START,
    SECTION_HEAD_QUEST_END,
    SECTION_HEAD_QUEST_FAIL_END,
    SECTION_HEAD_QUEST_FAIL_START,
    SECTION_HEAD_QUEST_START
)

from function.date_time import get_brazil_time_now
from function.text import create_text_in_box, escape_for_citation_markdown_v2
from repository.mongo.models.bag import BagModel
from repository.mongo.populate.enemy import (
    choice_enemy_name,
    choice_enemy_race_name
)

from repository.mongo.populate.item import (
    create_random_consumable,
    create_random_equipment
)

from rpgram.consumables import (
    CureConsumable,
    HealingConsumable,
    ReviveConsumable,
    GemstoneConsumable,
    IdentifyingConsumable,
    TrocadoPouchConsumable,
    XPConsumable
)
from rpgram import Item


async def job_create_item_quest(context: ContextTypes.DEFAULT_TYPE):
    '''Cria job da quest de pedido de items
    '''

    job = context.job
    chat_id = job.chat_id
    now = get_brazil_time_now()
    times = randint(1, 2) if is_boosted_day(now) else 1
    for i in range(times):
        minutes_in_seconds = randint(1, 60) * 60
        print(
            f'JOB_CREATE_ITEM_QUEST() - {now}: '
            f'Evento de item inicia em {minutes_in_seconds // 60} minutos.'
        )
        context.job_queue.run_once(
            callback=job_start_item_quest,
            when=minutes_in_seconds,
            name=f'JOB_CREATE_ITEM_QUEST_{i}',
            chat_id=chat_id,
        )


@skip_if_spawn_timeout
async def job_start_item_quest(context: ContextTypes.DEFAULT_TYPE):
    '''Envia a mensagem de pedido de ajuda para o grupo.
    '''

    job = context.job
    chat_id = job.chat_id
    group_level = get_attribute_group(chat_id, 'group_level')
    silent = get_attribute_group_or_player(chat_id, 'silent')
    consumable_item = create_random_consumable(
        group_level=group_level,
        random_level=True,
    )
    name = choice_enemy_name()
    race = choice_enemy_race_name()
    helped_name = f'{name} ({race})'
    quest_text = get_quest_text(consumable_item)
    narration_text = choice(ARRIVAL_NARRATION)
    text = (
        f'{narration_text}\n\n'
        f'>{helped_name}: {quest_text}'
    )
    text = create_text_in_box(
        text=text,
        section_name=SECTION_TEXT_QUEST,
        section_start=SECTION_HEAD_QUEST_START,
        section_end=SECTION_HEAD_QUEST_END,
        clean_func=escape_for_citation_markdown_v2
    )
    job_data = {
        'helped_name': helped_name,
        'item': consumable_item,
        'name': name,
        'race': race,
    }
    job_name = get_job_quest_name(job_data)
    quest_button = get_quest_button(job_name)
    reply_markup = InlineKeyboardMarkup([quest_button])

    response = await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        disable_notification=silent,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=reply_markup,
    )
    job_data['response'] = response
    context.job_queue.run_once(
        callback=job_fail_item_quest,
        when=timedelta(minutes=randint(60, 120)),
        data=job_data,
        name=job_name,
        chat_id=chat_id,
    )


async def job_fail_item_quest(context: ContextTypes.DEFAULT_TYPE):
    '''Encerra a quest de pedido de ajuda por falta de ajuda.
    '''

    job = context.job
    data = job.data
    response = data['response']
    helped_name = data['helped_name']

    narration_text = choice(DISAPPOINTED_NARRATION)
    narration_text.format(helped_name=helped_name)

    narration_text = create_text_in_box(
        text=narration_text,
        section_name=SECTION_TEXT_QUEST_FAIL,
        section_start=SECTION_HEAD_QUEST_FAIL_START,
        section_end=SECTION_HEAD_QUEST_FAIL_END,
    )

    await response.edit_text(
        text=narration_text,
        parse_mode=ParseMode.MARKDOWN_V2
    )


@skip_if_no_singup_player
@need_not_in_battle
@skip_if_dead_char
@skip_if_immobilized
@confusion()
@print_basic_infos
async def complete_item_quest(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    '''Checa se o objetivo da quest é satisfeito e dropa a recompensa.
    '''

    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    query = update.callback_query
    group_level = get_attribute_group(chat_id, 'group_level')
    silent = get_attribute_group_or_player(chat_id, 'silent')
    data = callback_data_to_dict(query.data)

    job_name = data['item_quest_job_name']
    current_jobs = context.job_queue.get_jobs_by_name(job_name)
    if not current_jobs:
        await query.answer('Essa quest não existe mais.', show_alert=True)
        await query.delete_message()
        return ConversationHandler.END

    job = current_jobs[0]
    job_data = job.data
    job_item = job_data['item']
    job_item_id = job_item._id
    job_item_name = job_item.name
    job_item_quantity = job_item.quantity
    user_item = get_item_from_bag_by_id(
        user_id=user_id,
        item_id=job_item_id
    )
    if user_item and user_item.quantity >= job_item_quantity:
        helped_name = job_data['helped_name']
        bag_model = BagModel()
        bag_model.sub(
            item=user_item,
            player_id=user_id,
            quantity=job_item_quantity
        )
        base_xp = int(job_item.full_price // 10)
        report_xp = add_xp(
            chat_id=chat_id,
            user_id=user_id,
            base_xp=base_xp,
        )
        text_xp = report_xp['text']
        thanks_text = choice(REPLY_TEXT_THANKS)
        narration_text = choice(LEAVE_NARRATION)
        narration_text = narration_text.format(helped_name=helped_name)
        text = (
            f'>{helped_name}: {thanks_text}\n\n'
            f'{narration_text}\n\n'
            f'{text_xp}'
        )
        text = create_text_in_box(
            text=text,
            section_name=SECTION_TEXT_QUEST_COMPLETE,
            section_start=SECTION_HEAD_QUEST_COMPLETE_START,
            section_end=SECTION_HEAD_QUEST_COMPLETE_END,
            clean_func=escape_for_citation_markdown_v2
        )
        await query.edit_message_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN_V2
        )
        job_item_rarity = job_item.rarity.name
        equipment = create_random_equipment(
            equip_type=None,
            group_level=group_level,
            rarity=job_item_rarity,
            random_level=True,
            save_in_database=True,
        )
        text = f'*{helped_name}* deixou'
        await send_drop_message(
            context=context,
            items=equipment,
            text=text,
            update=update,
            silent=silent,
        )
    else:
        text = f'Você não tem "{job_item_quantity}x {job_item_name}".'
        await query.answer(text, show_alert=True)

    remove_quest_item_job(context, job_name)


def get_quest_text(item: Item) -> str:
    if isinstance(item.item, (CureConsumable, HealingConsumable)):
        text = choice(REPLY_TEXT_HEAL_CURE_ITEM)
    elif isinstance(item.item, ReviveConsumable):
        text = choice(REPLY_TEXT_REVIVE_ITEM)
    elif isinstance(item.item, IdentifyingConsumable):
        text = choice(REPLY_TEXT_IDENTIFY_ITEM)
    elif isinstance(item.item, XPConsumable):
        text = choice(REPLY_TEXT_XP_ITEM)
    elif isinstance(item.item, TrocadoPouchConsumable):
        text = choice(REPLY_TEXT_TROCADO_ITEM)
    elif isinstance(item.item, GemstoneConsumable):
        text = choice(REPLY_TEXT_GEMSTONE_ITEM)

    item_name = item.name
    item_quantity = item.quantity
    item_text = f'{item_quantity}x {item_name}'
    text = text.format(item=item_text)

    return text


def get_quest_button(job_name: str):
    return [
        InlineKeyboardButton(
            text=QUEST_BUTTON_TEXT,
            callback_data=callback_data_to_string({
                'item_quest_job_name': job_name,
            })
        )
    ]


def get_job_quest_name(job_data: dict) -> str:
    name = job_data['name']

    return f'{CALLBACK_QUEST_PREFIX}{name}'.replace(' ', '_')


def remove_quest_item_job(
    context: ContextTypes.DEFAULT_TYPE,
    job_name: str
) -> bool:
    '''Remove o job de Quest de Item.
    '''

    current_jobs = context.job_queue.get_jobs_by_name(job_name)
    print('current_jobs', current_jobs)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()

    return True


ITEM_QUEST_HANDLER = CallbackQueryHandler(
    complete_item_quest,
    pattern=PATTERN_ITEM_QUEST
)
