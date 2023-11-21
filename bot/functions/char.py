from random import randint, random
from typing import List

from repository.mongo import (
    CharacterModel,
    EquipsModel,
    GroupModel,
    StatusModel,
)
from rpgram import Group
from rpgram.characters import BaseCharacter
from rpgram.conditions.factory import factory_condition
from rpgram.enums.damage import (
    DamageEnum,
    MAGICAL_DAMAGE_TYPES,
    PHYSICAL_DAMAGE_TYPES
)


def add_xp(
    chat_id: int = None,
    user_id: int = None,
    group: Group = None,
    char: BaseCharacter = None,
    min_xp: int = 1,
    max_xp: int = 10,
    base_xp: int = 0,
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
        group = group_model.get(chat_id)

    if user_id and char is None:
        char_model = CharacterModel()
        char = char_model.get(user_id)

    user_name = char.player_name
    level = char.base_stats.level
    level_bonus = group.character_multiplier_xp * level
    multiplier_xp = group.multiplier_xp
    group_level = group.group_level
    base_xp += randint(min_xp, max_xp)

    xp = int((base_xp + level_bonus) * multiplier_xp)

    if group_level > level:
        handicap = randint(110, 125) / 100
        xp = int(xp + (group_level * handicap))

    report_xp = char.base_stats.add_xp(xp, user_name)
    save_char(char)
    new_level = char.base_stats.level

    if report_xp['level_up']:
        player_id = char.player_id
        group.add_tier(player_id, new_level)
        group_model = GroupModel()
        group_model.save(group)

    report_xp['char'] = char
    report_xp['group'] = group

    return report_xp


def add_damage(
    damage: int,
    user_id: int = None,
    char: BaseCharacter = None,
    type_damage: DamageEnum = None,
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
        char = char_model.get(user_id)

    if type_damage in PHYSICAL_DAMAGE_TYPES:
        damage_report = char.combat_stats.physical_damage_hit_points(damage)
    elif type_damage in MAGICAL_DAMAGE_TYPES:
        damage_report = char.combat_stats.magical_damage_hit_points(damage)
    else:
        damage_report = char.combat_stats.damage_hit_points(damage)
    save_char(char)

    return dict(
        char=char,
        type_damage=type_damage,
        **damage_report,
    )


def add_conditions(
    *conditions: List[dict],
    user_id: int = None,
    char: BaseCharacter = None,
):
    '''Função que adiciona condições ao personagem
    '''
    if all((user_id is None, char is None)):
        raise ValueError(
            'Forneça um "user_id" ou "char". '
            'Ao menos um dos dois não podem ser None.'
        )

    if user_id and char is None:
        char_model = CharacterModel()
        char = char_model.get(user_id)

    condition_report = {'text': '', 'char': char}
    for condition in conditions:
        report = char.status.add(condition)
        condition_report['text'] += report['text'] + '\n'

    if condition_report['text']:
        condition_report['text'] += '\n'
    save_char(char, status=True)

    return condition_report


def add_conditions_trap(
    conditions_trap: List[dict],
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
        char = char_model.get(user_id)

    condition_trap_report = {'text': '', 'char': char}
    for condition_trap in conditions_trap:
        debuff_resistance = random()
        effectiveness = condition_trap['effectiveness']
        condition_name = condition_trap['condition']
        if debuff_resistance <= effectiveness:
            condition = factory_condition(condition_name)
            report = char.status.add(condition)
            condition_trap_report['text'] += report['text'] + '\n'

    if condition_trap_report['text']:
        condition_trap_report['text'] += '\n'
    save_char(char, status=True)

    return condition_trap_report


def activate_conditions(
    user_id: int = None,
    char: BaseCharacter = None,
) -> dict:
    '''Função que adiciona ativa as condições no Status do personagem.
    '''
    if all((user_id is None, char is None)):
        raise ValueError(
            'Forneça um "user_id" ou "char". '
            'Ao menos um dos dois não podem ser None.'
        )

    if user_id and char is None:
        char_model = CharacterModel()
        char = char_model.get(user_id)

    activate_report = {'text': '', 'char': char}
    reports = char.activate_status()
    for report in reports:
        activate_report['text'] += report['text'] + '\n'

    if activate_report['text']:
        activate_report['text'] += '\n'
    save_char(char, status=True)

    return activate_report


def save_char(
    char: BaseCharacter,
    equips: bool = False,
    status: bool = False,
):
    char_model = CharacterModel()
    char_model.save(char)

    if equips and char.equips:
        equips_model = EquipsModel()
        equips_model.save(char.equips)

    if status and char.status:
        status_model = StatusModel()
        status_model.save(char.status)
