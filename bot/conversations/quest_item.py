from datetime import timedelta
from random import choice, randint

from telegram import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update
)
from telegram.constants import ParseMode
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
)

from bot.constants.job import BASE_JOB_KWARGS
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
    print_basic_infos,
    skip_if_dead_char,
    skip_if_immobilized,
    skip_if_no_singup_player,
)
from bot.decorators.job import skip_if_spawn_timeout
from bot.functions.bag import get_item_from_bag_by_id
from bot.functions.char import add_xp
from bot.functions.chat import (
    answer,
    call_telegram_message_function,
    callback_data_to_dict,
    callback_data_to_string,
    delete_message,
    edit_message_text_and_forward,
    get_close_keyboard
)
from bot.functions.config import get_attribute_group
from bot.functions.general import (
    get_attribute_group_or_player
)

from constant.text import (
    SECTION_HEAD_QUEST_COMPLETE_END,
    SECTION_HEAD_QUEST_COMPLETE_START,
    SECTION_HEAD_QUEST_END,
    SECTION_HEAD_QUEST_FAIL_END,
    SECTION_HEAD_QUEST_FAIL_START,
    SECTION_HEAD_QUEST_START
)

from function.text import create_text_in_box, escape_for_citation_markdown_v2
from repository.mongo import BagModel, PlayerModel
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
from rpgram import Item, Player
from rpgram.enums import EmojiEnum, TrocadoEnum


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

    if isinstance(consumable_item, GemstoneConsumable):
        sub_quantity = int(consumable_item.quantity / 2)
        if consumable_item.quantity > sub_quantity and sub_quantity > 0:
            consumable_item.sub(quantity=sub_quantity)

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

    call_telegram_kwargs = dict(
        chat_id=chat_id,
        text=text,
        disable_notification=silent,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=reply_markup,
    )
    response = await call_telegram_message_function(
        function_caller='JOB_START_ITEM_QUEST()',
        function=context.bot.send_message,
        context=context,
        auto_delete_message=3,
        **call_telegram_kwargs
    )
    job_data['response'] = response
    context.job_queue.run_once(
        callback=job_fail_item_quest,
        when=timedelta(minutes=randint(60, 120)),
        data=job_data,
        chat_id=chat_id,
        name=job_name,
        job_kwargs=BASE_JOB_KWARGS,
    )


async def job_fail_item_quest(context: ContextTypes.DEFAULT_TYPE):
    '''Encerra a quest de pedido de ajuda por falta de ajuda.
    '''

    job = context.job
    data = job.data
    response = data['response']
    helped_name = data['helped_name']

    narration_text = choice(DISAPPOINTED_NARRATION)
    narration_text = narration_text.format(helped_name=helped_name)

    narration_text = create_text_in_box(
        text=narration_text,
        section_name=SECTION_TEXT_QUEST_FAIL,
        section_start=SECTION_HEAD_QUEST_FAIL_START,
        section_end=SECTION_HEAD_QUEST_FAIL_END,
    )

    send_message_kwargs = dict(
        text=narration_text,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=get_close_keyboard(None),
    )

    await call_telegram_message_function(
        function_caller='JOB_FAIL_ITEM_QUEST()',
        function=response.edit_text,
        context=context,
        need_response=False,
        **send_message_kwargs
    )


@skip_if_no_singup_player
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
    query = update.callback_query
    data = callback_data_to_dict(query.data)

    job_name = data['item_quest_job_name']
    current_jobs = context.job_queue.get_jobs_by_name(job_name)
    if not current_jobs:
        query_text = 'Essa quest não existe mais.'
        await answer(query=query, text=query_text, show_alert=True)
        await delete_message(
            function_caller='COMPLETE_ITEM_QUEST()',
            context=context,
            query=query,
        )

        return ConversationHandler.END

    job = current_jobs[0]
    job_data = job.data
    quest_item = job_data['item']
    helped_name = job_data['helped_name']
    user_item = get_item_from_bag_by_id(
        user_id=user_id,
        item_id=quest_item._id
    )

    if isinstance(quest_item.item, TrocadoPouchConsumable):
        is_complete = await complete_trocado_pouch_quest(
            trocado_pouch_item=quest_item,
            user_id=user_id,
            query=query
        )
        if is_complete is True:
            await send_item_quest_reward(
                job_name=job_name,
                helped_name=helped_name,
                quest_item=quest_item,
                update=update,
                context=context
            )
    elif user_item and user_item.quantity >= quest_item.quantity:
        bag_model = BagModel()
        bag_model.sub(
            item=user_item,
            player_id=user_id,
            quantity=quest_item.quantity
        )
        await send_item_quest_reward(
            job_name=job_name,
            helped_name=helped_name,
            quest_item=quest_item,
            update=update,
            context=context
        )
    else:
        text = f'Você não tem "{quest_item.quantity}x {quest_item.name}".'
        await answer(query=query, text=text, show_alert=True)
        return ConversationHandler.END


async def complete_trocado_pouch_quest(
    trocado_pouch_item: Item,
    user_id: int,
    query: CallbackQuery
):
    '''Verifica se o Jogador possui o dinheiro suficiente para completar a
    quest. Se sim, subtrai o dinheiro do Jogador e retorna True. Se não,
    retorna False e exibe uma mensagem de erro.
    '''

    player_model = PlayerModel()
    player: Player = player_model.get(user_id)
    quest_trocado = trocado_pouch_item.full_price
    is_complete = False
    if player.trocado >= quest_trocado:
        player.sub_trocado(quest_trocado)
        player_model.save(player)
        is_complete = True
    else:
        text = (
            f'Você não tem {TrocadoEnum.TROCADOS.value} suficiente.\n'
            f'Possui apenas {player.trocado}{EmojiEnum.TROCADO.value}.\n'
            f'Precisa de {quest_trocado}{EmojiEnum.TROCADO.value}.'
        )
        await answer(query=query, text=text, show_alert=True)

    return is_complete


async def send_item_quest_reward(
    job_name: str,
    helped_name: str,
    quest_item: Item,
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    '''Edita a mensagem da quest para narrar o agradecimento e envia um
    Equipamento como recompensa.
    '''

    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    message_id = update.effective_message.message_id
    group_level = get_attribute_group(chat_id, 'group_level')
    silent = get_attribute_group_or_player(chat_id, 'silent')
    base_xp = int(quest_item.full_price // 10)
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
    await edit_message_text_and_forward(
        function_caller='SEND_ITEM_QUEST_REWARD()',
        new_text=text,
        user_ids=user_id,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        need_response=False,
        markdown=True,
    )
    job_item_rarity = quest_item.rarity.name
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
    remove_quest_item_job(context, job_name)
    return ConversationHandler.END


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
        add_quantity = randint(5, 50)
        item.add(add_quantity)
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
