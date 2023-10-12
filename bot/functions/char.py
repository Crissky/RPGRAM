from random import randint

from repository.mongo import CharacterModel, GroupModel
from rpgram import Group
from rpgram.characters import BaseCharacter
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
    max_xp: int = 10
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

    char_model = CharacterModel()
    if user_id and char is None:
        char = char_model.get(user_id)

    level = char.base_stats.level
    level_bonus = group.character_multiplier_xp * level
    multiplier_xp = group.multiplier_xp
    group_level = group.group_level

    xp = int((randint(min_xp, max_xp) + level_bonus) * multiplier_xp)

    if group_level > level:
        handicap = randint(110, 125) / 100
        xp = int(xp + (group_level * handicap))

    char.base_stats.xp = xp
    char_model.save(char)
    new_level = char.base_stats.level

    if new_level > level:
        player_id = char.player_id
        group.add_tier(player_id, new_level)
        group_model = GroupModel()
        group_model.save(group)

    return dict(
        level_up=new_level > level,
        level=new_level,
        char=char,
        group=group,
        xp=xp
    )


def add_damage(
    damage: int,
    user_id: int = None,
    char: BaseCharacter = None,
    type_damage: DamageEnum = None,
):
    '''Função que adiciona dano ao personagem.
    '''
    if all((user_id is None, char is None)):
        raise ValueError(
            'Forneça um "user_id" ou "char". '
            'Ao menos um dos dois não podem ser None.'
        )

    char_model = CharacterModel()
    if user_id and char is None:
        char = char_model.get(user_id)

    if type_damage in PHYSICAL_DAMAGE_TYPES:
        damage_report = char.combat_stats.physical_damage_hit_points(damage)
    elif type_damage in MAGICAL_DAMAGE_TYPES:
        damage_report = char.combat_stats.magical_damage_hit_points(damage)
    else:
        damage_report = char.combat_stats.damage_hit_points(damage)
    char_model.save(char)

    return dict(
        char=char,
        type_damage=type_damage,
        dead=char.is_dead(),
        **damage_report,
    )
