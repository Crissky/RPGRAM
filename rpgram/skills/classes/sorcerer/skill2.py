from typing import TYPE_CHECKING
from rpgram.constants.text import (
    MAGICAL_ATTACK_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum
from rpgram.enums.skill import (
    SkillDefenseEnum,
    SkillTypeEnum,
    SorcererSkillEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill

if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


SKILL_WAY_DESCRIPTION = {
    'name': 'Domínio Anímico',
    'description': (
        'Área da mágia que visa controlar os elementos não naturais. '
        'As habilidades desse grupo se concentram em conceder ao Feiticeiro '
        'acesso a magias sobrenaturais, permitindo que ele combine e '
        'explore seus diferentes efeitos em combate.'
    )
}


class PrismaticShotSkill(BaseSkill):
    NAME = SorcererSkillEnum.PRISMATIC_SHOT.value
    DESCRIPTION = (
        f'Canalizando a energia mágica, dispara um feixe prismático '
        f'causando dano com base em *{MAGICAL_ATTACK_EMOJI_TEXT}*.'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.SORCERER.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 2
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 1.50,
        }
        damage_types = [DamageEnum.LIGHT]

        super().__init__(
            name=PrismaticShotSkill.NAME,
            description=PrismaticShotSkill.DESCRIPTION,
            rank=PrismaticShotSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=PrismaticShotSkill.REQUIREMENTS,
            damage_types=damage_types
        )


if __name__ == '__main__':
    from rpgram.constants.test import SORCERER_CHARACTER
    skill = PrismaticShotSkill(SORCERER_CHARACTER)
    print(skill)
    print(SORCERER_CHARACTER.cs.magical_attack)
    SORCERER_CHARACTER.skill_tree.learn_skill(PrismaticShotSkill)
