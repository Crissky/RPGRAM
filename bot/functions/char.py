from operator import attrgetter
from random import choice, randint, random, sample, triangular
from typing import Any, List

from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot.constants.puzzle import SECTION_TEXT_PUZZLE_XP
from bot.functions.chat import (
    MIN_AUTODELETE_TIME,
    call_telegram_message_function,
    get_close_keyboard,
    reply_text_and_forward
)
from bot.functions.config import get_attribute_group
from bot.functions.player import get_player_ids_from_group
from constant.text import (
    ALERT_SECTION_HEAD,
    SECTION_HEAD_FAIL_PUNISHMENT_END,
    SECTION_HEAD_FAIL_PUNISHMENT_START,
    SECTION_HEAD_XP_END,
    SECTION_HEAD_XP_START
)
from function.text import create_text_in_box
from repository.mongo import (
    CharacterModel,
    EquipsModel,
    GroupModel,
)
from rpgram import Group
from rpgram.characters import BaseCharacter, NPCharacter, PlayerCharacter
from rpgram.conditions.condition import Condition
from rpgram.conditions.factory import condition_factory
from rpgram.enums.damage import (
    DamageEnum,
    MAGICAL_DAMAGE_TYPES,
    PHYSICAL_DAMAGE_TYPES
)
from rpgram.enums.debuff import DEBUFF_FULL_NAMES


SECTION_TEXT_PUZZLE_PUNISHMENT = 'PUNIÇÃO'


def add_xp(
    chat_id: int = None,
    user_id: int = None,
    group: Group = None,
    char: BaseCharacter = None,
    min_xp: int = 1,
    max_xp: int = 10,
    base_xp: int = 0,
    to_add_level_bonus: bool = True,
    save_equips: bool = False,
    save_status: bool = False,
) -> dict:
    '''Função que adiciona xp ao personagem.
    Retorna um dicionário com as informações do novo nível do personagem.
    returns: {
        level_up: boleano, True se passou de nível e False caso contrário.
        level: nível do personagem após ser adicionado XP.
        char: Personagem que recebeu XP.
        group: Grupo que o personagem recebeu XP.
        xp: Valor de XP adicionado.
    }
    '''

    if all((chat_id is None, user_id is None, group is None, char is None)):
        raise ValueError(
            'Todos os atributos não podem ser None.'
            'Forneça um "chat_id" ou "group" e um "user_id" ou "char".'
        )
    elif all((chat_id is None, group is None)):
        raise ValueError(
            'Forneça um "chat_id" ou "group". '
            'Ao menos um dos dois não podem ser None.'
        )
    elif all((user_id is None, char is None)):
        raise ValueError(
            'Forneça um "user_id" ou "char". '
            'Ao menos um dos dois não podem ser None.'
        )

    if chat_id and group is None:
        group_model = GroupModel()
        group: Group = group_model.get(chat_id)

    if user_id and char is None:
        char_model = CharacterModel()
        char: BaseCharacter = char_model.get(user_id)

    user_name = char.player_name
    level = char.base_stats.level
    multiplier_xp = group.multiplier_xp
    character_multiplier_xp = group.character_multiplier_xp
    group_level = group.group_level
    base_xp += randint(min_xp, max_xp)
    level_bonus = (
        character_multiplier_xp * level
        if to_add_level_bonus is True
        else 0
    )

    xp = int((base_xp + level_bonus) * multiplier_xp)

    if group_level > level:
        handicap = randint(150, 200) / 100
        xp = int(xp * handicap)

    report_xp = char.base_stats.add_xp(xp, user_name)
    save_char(char=char, equips=save_equips)
    new_level = char.base_stats.level

    if report_xp['level_up']:
        player_id = char.player_id
        group.add_tier(player_id, new_level)
        group_model = GroupModel()
        group_model.save(group)

    report_xp['char'] = char
    report_xp['group'] = group

    return report_xp


async def add_xp_group(
    chat_id: int,
    context: ContextTypes.DEFAULT_TYPE,
    silent: bool,
    message_id: int = None,
    section_name: str = SECTION_TEXT_PUZZLE_XP,
    section_start=SECTION_HEAD_XP_START,
    section_end=SECTION_HEAD_XP_END,
):
    '''Adiciona XP aos jogadores vivos de um grupo.
    '''

    full_text = ''
    char_list = get_player_chars_from_group(chat_id=chat_id, is_alive=True)
    sorted_char_list = sorted(
        char_list,
        key=attrgetter('level', 'xp'),
        reverse=True
    )
    for char in sorted_char_list:
        level = (char.level * 2)
        base_xp = int(max(level, 10))
        report_xp = add_xp(
            chat_id=chat_id,
            char=char,
            base_xp=base_xp,
        )
        full_text += f'{report_xp["text"]}\n'

    full_text = create_text_in_box(
        text=full_text,
        section_name=section_name,
        section_start=section_start,
        section_end=section_end
    )
    send_message_kwargs = dict(
        chat_id=chat_id,
        text=full_text,
        disable_notification=silent,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_to_message_id=message_id,
        allow_sending_without_reply=True,
        reply_markup=get_close_keyboard(None),
    )

    await call_telegram_message_function(
        function_caller='ADD_XP_GROUP()',
        function=context.bot.send_message,
        context=context,
        need_response=False,
        **send_message_kwargs
    )


def add_damage(
    damage: int,
    user_id: int = None,
    char: BaseCharacter = None,
    type_damage: DamageEnum = None,
    ignore_barrier: bool = False,
) -> dict:
    '''Função que adiciona dano ao personagem.
    '''

    if all((user_id is None, char is None)):
        raise ValueError(
            'Forneça um "user_id" ou "char". '
            'Ao menos um dos dois não podem ser None.'
        )

    if user_id and char is None:
        char_model = CharacterModel()
        char: BaseCharacter = char_model.get(user_id)

    if type_damage in PHYSICAL_DAMAGE_TYPES:
        damage_report = char.combat_stats.physical_damage_hit_points(damage)
    elif type_damage in MAGICAL_DAMAGE_TYPES:
        damage_report = char.combat_stats.magical_damage_hit_points(damage)
    else:
        damage_report = char.combat_stats.damage_hit_points(
            value=damage,
            ignore_barrier=ignore_barrier
        )

    save_char(char=char)

    return dict(
        char=char,
        type_damage=type_damage,
        **damage_report,
    )


def add_trap_damage(
    min_ratio_damage: float,
    user_id: int = None,
    char: BaseCharacter = None,
    damage_type: DamageEnum = None,
) -> dict:
    '''Função que adiciona dano ao personagem.
    '''

    if all((user_id is None, char is None)):
        raise ValueError(
            'Forneça um "user_id" ou "char". '
            'Ao menos um dos dois não podem ser None.'
        )

    if user_id and char is None:
        char_model = CharacterModel()
        char: BaseCharacter = char_model.get(user_id)

    boosted_ratio = triangular(min_ratio_damage, min_ratio_damage * 1.5)
    boosted_ratio = round(boosted_ratio, 2)
    boosted_ratio = min(0.99, boosted_ratio)
    base_damage = int(char.combat_stats.hit_points * boosted_ratio)

    if damage_type in PHYSICAL_DAMAGE_TYPES:
        defense = char.combat_stats.physical_defense
        damage = int(base_damage + defense)
        damage_report = char.combat_stats.physical_damage_hit_points(damage)
    elif damage_type in MAGICAL_DAMAGE_TYPES:
        defense = char.combat_stats.magical_defense
        damage = int(base_damage + defense)
        damage_report = char.combat_stats.magical_damage_hit_points(damage)
    else:
        damage = base_damage
        damage_report = char.combat_stats.damage_hit_points(damage)

    save_char(char=char)

    return dict(
        char=char,
        type_damage=damage_type,
        min_ratio_damage=min_ratio_damage,
        boosted_ratio=boosted_ratio,
        **damage_report,
    )


def add_conditions(
    *conditions: List[Condition],
    user_id: int = None,
    char: BaseCharacter = None,
) -> dict:
    '''Função que adiciona condições ao personagem
    '''

    if all((user_id is None, char is None)):
        raise ValueError(
            'Forneça um "user_id" ou "char". '
            'Ao menos um dos dois não podem ser None.'
        )

    if user_id and char is None:
        char_model = CharacterModel()
        char: BaseCharacter = char_model.get(user_id)

    condition_report = {'text': '', 'char': char}
    for condition in conditions:
        report = char.status.add(condition)
        condition_report['text'] += report['text'] + '\n'

    if condition_report['text']:
        condition_report['text'] += '\n'
    save_char(char=char)

    return condition_report


def add_conditions_from_trap(
    condition_list: List[dict],
    group_level: int,
    user_id: int = None,
    char: BaseCharacter = None,
) -> dict:
    '''Função que adiciona condições ao personagem oriundas de armadilhas.
    '''

    if all((user_id is None, char is None)):
        raise ValueError(
            'Forneça um "user_id" ou "char". '
            'Ao menos um dos dois não podem ser None.'
        )

    if user_id and char is None:
        char_model = CharacterModel()
        char: BaseCharacter = char_model.get(user_id)

    condition_level_base = (group_level // 10) + 1
    condition_trap_report = {'text': '', 'char': char}
    for condition_trap in condition_list:
        condition_level = randint(
            condition_level_base // 2,
            condition_level_base
        )
        debuff_resistance = random()
        effectiveness = condition_trap['effectiveness']
        condition_name = condition_trap['condition']
        if debuff_resistance <= effectiveness:
            condition = condition_factory(
                name=condition_name,
                level=condition_level
            )
            report = char.status.add(condition)
            condition_trap_report['text'] += report['text'] + '\n'

    if condition_trap_report['text']:
        condition_trap_report['text'] += '\n'
    save_char(char=char)

    return condition_trap_report


def get_base_xp_from_enemy_attack(
    enemy_char: NPCharacter,
    defender_char: PlayerCharacter
) -> int:
    '''Retorna o XP base para o personagem que sobreviveu a um ataque.
    '''

    base_xp = int(
        enemy_char.points_multiplier *
        max(enemy_char.level - defender_char.level, 10)
    )

    return base_xp


def get_base_xp_from_player_attack(
    enemy_char: NPCharacter,
    attacker_char: PlayerCharacter,
    is_miss: bool
) -> int:
    '''Retorna o XP base para o personagem que atacou um inimigo.
    '''

    level_divisor = 2 if enemy_char.is_alive else 0.5
    level_divisor *= 2 if is_miss else 1
    base_xp = int(
        enemy_char.points_multiplier *
        max(
            (enemy_char.level / level_divisor) - attacker_char.level,
            10
        )
    )

    return base_xp


def activate_conditions(
    user_id: int = None,
    char: BaseCharacter = None,
) -> dict:
    '''Função que ativa as condições no Status do personagem.
    '''

    if all((user_id is None, char is None)):
        raise ValueError(
            'Forneça um "user_id" ou "char". '
            'Ao menos um dos dois não podem ser None.'
        )

    if user_id and char is None:
        char_model = CharacterModel()
        char: BaseCharacter = char_model.get(user_id)

    activate_report = {'text': '', 'char': char, 'have_debuff': False}
    reports = char.activate_status()
    for report in reports:
        activate_report['text'] += report['text'] + '\n'
        if not activate_report['have_debuff'] and report['is_debuff']:
            activate_report['have_debuff'] = True

    activate_report['status'] = char.status.get_sheet()
    activate_report['status_verbose'] = char.status.get_sheet(verbose=True)
    activate_report['all_status'] = char.status.get_all_sheets()
    activate_report['all_status_verbose'] = char.status.get_all_sheets(
        verbose=True
    )
    if activate_report['text']:
        activate_report['text'] += '\n'
    save_char(char=char)

    return activate_report


def get_player_chars_from_group(
    chat_id: int,
    is_alive: bool = False
) -> List[BaseCharacter]:
    '''Retorna os Personagens de todos os jogadores do grupo.
    '''

    char_model = CharacterModel()
    player_id_list = get_player_ids_from_group(chat_id)
    query = {'player_id': {'$in': player_id_list}}
    char_list = char_model.get_all(query=query)

    if is_alive:
        char_list = [char for char in char_list if char.is_alive]

    return char_list


def get_chars_level_from_group(chat_id: int) -> List[int]:
    '''Retorna o level de todos os personagens do grupo.
    '''

    char_model = CharacterModel()
    player_id_list = get_player_ids_from_group(chat_id)
    query = {'player_id': {'$in': player_id_list}}
    fields = ['level']
    level_char_list = char_model.get_all(query=query, fields=fields)

    return level_char_list


def get_char_attribute(user_id: int, attribute: str) -> Any:
    '''Retorna o atributo de um personagem.
    '''

    char_model = CharacterModel()
    query = {'player_id': user_id}
    fields = [attribute]
    attribute_dict = char_model.get(query=query, fields=fields)

    return attribute_dict[attribute]


def choice_char(
    player_id_list: List[int] = None,
    chat_id: int = None,
    is_alive: bool = False,
) -> PlayerCharacter:
    '''Retorna um personagem aleatório do grupo ou de uma lista de player_ids
    '''

    if not player_id_list and not chat_id:
        raise ValueError('Forneça um "player_id_list" ou "chat_id". ')
    elif player_id_list and chat_id:
        raise ValueError(
            'Forneça apenas um dos atributos ("player_id_list" ou "chat_id"). '
            'Ao menos um dos dois não podem ser None.'
        )

    if chat_id:
        player_id_list = get_player_ids_from_group(chat_id)

    if not player_id_list:
        raise ValueError(f'Não há player_id_list para o chat_id: "{chat_id}"')

    char = None
    char_model = CharacterModel()
    while char is None and player_id_list:
        player_id = choice(player_id_list)
        char: BaseCharacter = char_model.get(player_id)
        if is_alive:
            if char and char.is_alive:
                break
            else:
                player_id_list.remove(player_id)
                char = None

    if not isinstance(char, BaseCharacter):
        raise ValueError(
            f'Não há personagem válido para o chat_id: "{chat_id}"'
        )

    return char


def char_is_alive(user_id: int) -> bool:
    char_model = CharacterModel()
    char: BaseCharacter = char_model.get(user_id)

    return isinstance(char, BaseCharacter) and char.is_alive


def save_char(
    char: BaseCharacter,
    equips: bool = False,
):
    '''Salva o personagem e opcionais caso True
    '''

    char_model = CharacterModel()
    char_model.save(char)

    if equips and char.equips:
        equips_model = EquipsModel()
        equips_model.save(char.equips)


async def punishment(
    context: ContextTypes.DEFAULT_TYPE,
    message_id: int,
):
    '''Punição: adiciona dano e Status a todos os jogadores por falharem no 
    desafio.
    '''

    chat_id = context._chat_id
    group_level = get_attribute_group(chat_id, 'group_level')
    char_list = get_player_chars_from_group(chat_id=chat_id, is_alive=True)
    sorted_char_list = sorted(
        char_list,
        key=attrgetter('level', 'xp'),
        reverse=True
    )
    debuff_list = [
        debuff_name.title()
        for debuff_name in DEBUFF_FULL_NAMES.keys()
    ]
    min_debuff_quantity = 0
    max_debuff_quantity = len(debuff_list)
    min_condition_level = int(group_level // 10) + 1
    max_condition_level = min_condition_level * 2
    for char in sorted_char_list:
        if char.is_dead:
            text = (
                f'{char.player_name} está morto, por isso não vai receber '
                'a punição.'
            )
            text = create_text_in_box(
                text=text,
                section_name=SECTION_TEXT_PUZZLE_PUNISHMENT,
                section_start=SECTION_HEAD_FAIL_PUNISHMENT_START,
                section_end=SECTION_HEAD_FAIL_PUNISHMENT_END
            )
            await reply_text_and_forward(
                function_caller='PUNISHMENT()',
                text=text,
                context=context,
                user_ids=char.player_id,
                chat_id=chat_id,
                message_id=message_id,
                markdown=True,
                silent_forward=False,
                need_response=False,
                auto_delete_message=MIN_AUTODELETE_TIME,
            )
            continue

        quantity_sample = randint(min_debuff_quantity, max_debuff_quantity)
        debuff_sample = sample(debuff_list, quantity_sample)
        debuff_sample = [
            condition_factory(
                name=debuff_name,
                level=randint(min_condition_level, max_condition_level)
            )
            for debuff_name in debuff_sample
        ]
        report_condition = add_conditions(
            *debuff_sample,
            char=char,
        )
        report_damage = add_trap_damage(
            min_ratio_damage=0.35,
            char=char,
        )
        text = (
            f'{report_condition["text"]}\n'
            f'{char.player_name} - {report_damage["text"]}\n'
        )

        text = create_text_in_box(
            text=text,
            section_name=SECTION_TEXT_PUZZLE_PUNISHMENT,
            section_start=SECTION_HEAD_FAIL_PUNISHMENT_START,
            section_end=SECTION_HEAD_FAIL_PUNISHMENT_END
        )

        await reply_text_and_forward(
            function_caller='PUNISHMENT()',
            text=text,
            context=context,
            user_ids=char.player_id,
            chat_id=chat_id,
            message_id=message_id,
            markdown=True,
            silent_forward=False,
            need_response=False,
            auto_delete_message=MIN_AUTODELETE_TIME,
        )


def bad_move_damage(
    user_id: int,
    multiplier: float = 1,
) -> str:
    '''Causa dano ao jogador que fez uma jogada ruim.
    O dano é (5% * multiplier) * max_hp do jogador.
    '''

    print('WORDGAME_PUNISHMENT()')
    char_model = CharacterModel()
    char: BaseCharacter = char_model.get(user_id)
    max_hp = char.cs.hp
    multiplier = multiplier * 0.05
    percent = round(multiplier*100, 2)
    damage = int(max_hp * multiplier)
    report = add_damage(damage=damage, char=char)

    return (
        f"{ALERT_SECTION_HEAD.format('*DAMAGE REPORT*')}\n"
        f"{char.full_name}\n"
        f"{report['text']}[{percent}%]"
    )


if __name__ == '__main__':
    from decouple import config
    MY_GROUP_ID = config('MY_GROUP_ID', cast=int)
    print(MY_GROUP_ID)
    print(get_chars_level_from_group(MY_GROUP_ID))
