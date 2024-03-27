from random import choice

from bot.functions.char import (
    choice_char,
    get_player_ids_from_group,
    save_char
)
from bot.functions.chat import get_close_keyboard
from bot.functions.config import get_attribute_group
from bot.functions.general import activated_condition
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

from bot.constants.create_char import COMMANDS
from bot.constants.rest import COMMANDS as REST_COMMANDS
from bot.functions.status import confusion_status, immobilized_status
from constant.text import (
    SECTION_HEAD_CONFUSION_END,
    SECTION_HEAD_CONFUSION_START
)
from function.text import create_text_in_box, escape_basic_markdown_v2
from repository.mongo import CharacterModel
from rpgram.enums.debuff import IMMOBILIZED_DEBUFFS_NAMES
from rpgram import Dice
from rpgram.enums.debuff import DEBUFF_FULL_NAMES

CONFUSION_TEXT = [
    (
        '{personagem} olha confuso para {aliado} e, em um momento de '
        'desorientação, desfere um golpe contra ele.\n\n'
    ),
    (
        'Com a mente confusa, {personagem} vê {aliado} como um inimigo e '
        'lança um ataque surpreendente.\n\n'
    ),
    (
        'Em meio à confusão, {personagem} se vira rapidamente e atinge '
        '{aliado}, pensando que era um oponente.\n\n'
    ),
    (
        'Os olhos de {personagem} se nublam momentaneamente, e ele ataca '
        '{aliado} por engano, em meio à sua confusão.\n\n'
    ),
    (
        '{personagem}, confundido, se vira para {aliado} e lança um ataque '
        'repentino, sem perceber sua identidade.\n\n'
    ),
    (
        'Diante da confusão momentânea, {personagem} ataca {aliado}, '
        'acreditando que era um inimigo se aproximando.\n\n'
    ),
    (
        'Em um momento de confusão, {personagem} se prepara para atacar um '
        'suposto inimigo, que na verdade era {aliado}.\n\n'
    ),
    (
        'Os sentidos de {personagem} falham momentaneamente, resultando em um '
        'ataque contra {aliado} por engano.\n\n'
    ),
    (
        'Com a mente embaralhada, {personagem} interpreta {aliado} como um '
        'oponente e lança um ataque desajeitado.\n\n'
    ),
    (
        'Diante da confusão repentina, {personagem} reage rapidamente, '
        'atacando {aliado} sem perceber sua identidade.\n\n'
    ),
]
DODGE_TEXT = [
    (
        '{aliado} se movimenta ágilmente, escapando do golpe com uma '
        'rápida esquiva.'
    ),
    (
        'Com reflexos afiados, {aliado} se esquiva habilmente do ataque, '
        'desviando no último momento.'
    ),
    (
        '{aliado} antecipa o ataque e realiza uma esquiva elegante, '
        'evitando o golpe por um triz.'
    ),
    (
        'Com destreza, {aliado} se esquiva do ataque, deslizando para '
        'fora do alcance do golpe inimigo.'
    ),
    (
        'Antes mesmo do golpe se concretizar, {aliado} se esquiva '
        'com um movimento ágil e preciso.'
    ),
    (
        '{aliado} percebe o ataque iminente e se esquiva com uma '
        'cambalhota, escapando ileso.'
    ),
    (
        'Com agilidade impressionante, {aliado} desvia do golpe inimigo, '
        'mostrando sua destreza em combate.'
    ),
    (
        'Os olhos atentos de {aliado} permitem que ele antecipe o '
        'ataque e se esquive com destreza.'
    ),
    (
        'Em um movimento fluído, {aliado} se esquiva do ataque, '
        'deslizando para um lugar seguro.'
    ),
    (
        'Com um salto habilidoso, {aliado} se esquiva do golpe, '
        'mostrando sua agilidade excepcional.'
    ),
]
ATTACK_TEXT = [
    (
        '{aliado} é atingido pelo golpe, sofrendo o impacto do ataque.\n\n'
    ),
    (
        'Infelizmente, {aliado} recebe o golpe em cheio, '
        'suportando o dano do ataque.\n\n'
    ),
    (
        'O ataque acerta em cheio {aliado}, que sente '
        'o impacto do golpe.\n\n'
    ),
    (
        'Com pesar, {aliado} é atingido pelo ataque, suportando '
        'o impacto do golpe.\n\n'
    ),
    (
        'O golpe encontra seu alvo em {aliado}, que recebe '
        'o dano do ataque.\n\n'
    ),
    (
        '{aliado} é pego desprevenido pelo ataque, sofrendo '
        'o impacto do golpe.\n\n'
    ),
    (
        'O ataque atinge {aliado}, que suporta o golpe e sente '
        'o impacto do dano.\n\n'
    ),
    (
        'Com frustração, {aliado} é atingido pelo golpe, suportando '
        'o impacto do ataque.\n\n'
    ),
    (
        '{aliado} sofre o impacto do ataque, recebendo '
        'o dano direto do golpe.\n\n'
    ),
    (
        'O golpe não falha em atingir {aliado}, que sente '
        'o impacto do ataque.\n\n'
    ),
]


def need_have_char(callback):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        print('@NEED_HAVE_CHAR')
        char_model = CharacterModel()
        user_id = update.effective_user.id

        if char_model.exists(user_id):
            print('\tAUTORIZADO - USUÁRIO POSSUI PERSONAGEM.')
            return await callback(update, context)
        else:
            await update.effective_message.reply_text(
                f'Você ainda não criou um personagem!\n'
                f'Crie o seu personagem com o comando /{COMMANDS[0]}.',
                allow_sending_without_reply=True
            )
            return ConversationHandler.END
    return wrapper


def skip_if_no_have_char(callback):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(f'@SKIP_IF_NO_HAVE_CHAR')
        char_model = CharacterModel()
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id

        if char_model.exists(user_id):
            return await callback(update, context)
        else:
            print(f'\tUSER: {user_id} SKIPPED in CHAT: {chat_id} - NO CHAR')
            return ConversationHandler.END
    return wrapper


def skip_if_dead_char(callback):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(f'@SKIP_IF_DEAD_CHAR')
        char_model = CharacterModel()
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id
        char = char_model.get(user_id)

        if char and char.is_alive:
            return await callback(update, context)
        else:
            print(f'\tUSER: {user_id} SKIPPED in CHAT: {chat_id} - DEAD CHAR')
            query = update.callback_query
            char_hit_points = ''
            if char:
                char_hit_points = f'HP: {char.combat_stats.show_hit_points}'

            text = (
                f'Essa ação não pode ser realizada, pois seu personagem '
                f'está morto.\n\n'
                f'{char_hit_points}'
            )

            if query:
                await query.answer(
                    text,
                    show_alert=True
                )
            else:
                silent = get_attribute_group(chat_id, 'silent')
                await update.effective_message.reply_text(
                    text=text,
                    disable_notification=silent,
                    allow_sending_without_reply=True
                )

            return ConversationHandler.END
    return wrapper


def skip_if_dead_char_silent(callback):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(f'@SKIP_IF_DEAD_CHAR_SILENT')
        char_model = CharacterModel()
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id
        char = char_model.get(user_id)

        if char and char.is_alive:
            return await callback(update, context)
        else:
            print(f'\tUSER: {user_id} SKIPPED in CHAT: {chat_id} - DEAD CHAR')
            query = update.callback_query
            char_hit_points = ''
            if char:
                char_hit_points = f'HP: {char.combat_stats.show_hit_points}'

            text = (
                f'Essa ação não pode ser realizada, pois seu personagem '
                f'está morto.\n\n'
                f'{char_hit_points}'
            )

            if query:
                await query.answer(
                    text,
                    show_alert=True
                )

            return ConversationHandler.END
    return wrapper


def skip_if_immobilized(callback):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        print('@SKIP_IF_IMMOBILIZED')
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id
        status = immobilized_status(user_id)

        if not status:
            return await callback(update, context)
        else:
            print(
                f'\tUSER: {user_id} SKIPPED in '
                f'CHAT: {chat_id} - IMMOBILIZED CHAR'
            )
            query = update.callback_query
            conditions = status['condition_args']
            text = (
                f'Essa ação não pode ser realizada, pois seu personagem '
                f'está '
            )
            conditions_names = [
                DEBUFF_FULL_NAMES[condition['name'].upper()]
                for condition in conditions
                if condition['name'] in IMMOBILIZED_DEBUFFS_NAMES
            ]
            text += ', '.join(conditions_names)
            if query:
                await query.answer(text, show_alert=True)
            else:
                await update.effective_message.reply_text(
                    text,
                    allow_sending_without_reply=True
                )
            return ConversationHandler.END
    return wrapper


def confusion(retry_state=ConversationHandler.END):
    def decorator(callback):
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            print('@CONFUSION')
            char_model = CharacterModel()
            chat_id = update.effective_chat.id
            user_id = update.effective_user.id
            query = update.callback_query
            status = confusion_status(user_id)
            activated_confusion = activated_condition()
            if not status or not activated_confusion:
                return await callback(update, context)
            else:
                player_ids = get_player_ids_from_group(chat_id)
                player_ids.append(user_id)

                confuse_char = char_model.get(user_id)
                target_char = choice_char(
                    player_id_list=player_ids,
                    is_alive=True
                )
                confuse_player_name = confuse_char.player_name
                target_player_name = target_char.player_name
                if confuse_char.player_id == target_char.player_id:
                    target_player_name = 'a si mesmo'
                    target_char_dice = Dice(1)
                else:
                    target_char_dice = Dice(20)

                confuse_char_dice = Dice(20)
                confuse_action = confuse_char.weighted_choice_action_attack()

                attack_report = confuse_char.to_attack(
                    defender_char=target_char,
                    attacker_dice=confuse_char_dice,
                    defender_dice=target_char_dice,
                    attacker_action_name=confuse_action,
                    to_dodge=True,
                    to_defend=True,
                    rest_command=REST_COMMANDS[0],
                    verbose=True,
                    markdown=True,
                )

                text = choice(CONFUSION_TEXT).format(
                    personagem=confuse_player_name,
                    aliado=target_player_name
                )
                target_player_name = target_char.player_name

                if attack_report['defense']['is_miss']:
                    text += choice(DODGE_TEXT).format(
                        aliado=target_player_name
                    )
                else:
                    text += choice(ATTACK_TEXT).format(
                        aliado=target_player_name
                    )

                    text += attack_report['text']
                    if attack_report['dead']:
                        text += (
                            f'\n\n{target_player_name} morreu! '
                            f'Use o comando /{REST_COMMANDS[0]} '
                            f'para descansar.'
                        )
                    save_char(target_char)
                text = escape_basic_markdown_v2(text)
                text = create_text_in_box(
                    text=text,
                    section_name='CONFUSÃO',
                    section_start=SECTION_HEAD_CONFUSION_START,
                    section_end=SECTION_HEAD_CONFUSION_END
                )

                await update.effective_message.reply_text(
                    text,
                    parse_mode=ParseMode.MARKDOWN_V2,
                    allow_sending_without_reply=True,
                    reply_markup=get_close_keyboard(None),
                )
                return retry_state
        return wrapper
    return decorator
