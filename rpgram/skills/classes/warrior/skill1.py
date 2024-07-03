from typing import TYPE_CHECKING
from rpgram.constants.text import (
    PHYSICAL_ATTACK_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.skill import (
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum,
    WarriorSkillEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill

if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


SKILL_WAY_DESCRIPTION = {
    'name': 'Combate Brutal',
    'description': (
        'O caminho do Combate Brutal molda o Guerreiro em um agente de '
        'destruição implacável, utilizando força bruta e '
        'ferocidade inigualável para esmagar seus oponentes. '
        'Dominando a arte do combate, o Guerreiro se torna um '
        'mestre da violência, capaz de infligir danos devastadores '
        'com cada golpe. '
        'Habilidades brutais como Ataques Múltiplos, Golpes Poderosos '
        'e Ataques Implacáveis transformam o Guerreiro em um redemoinho '
        'de fúria, dizimando inimigos em um turbilhão de aço e sangue.'
    )
}


class PowerfulAttackSkill(BaseSkill):
    NAME = WarriorSkillEnum.POWERFUL_ATTACK.value
    DESCRIPTION = (
        f'Tenciona os músculos ao máximo e desfere um golpe devastador, '
        f'causando dano com base em '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (150% + 5% x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.WARRIOR.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 2
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.50,
        }
        damage_types = None

        super().__init__(
            name=PowerfulAttackSkill.NAME,
            description=PowerfulAttackSkill.DESCRIPTION,
            rank=PowerfulAttackSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=PowerfulAttackSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class MoreThanPowerfulAttackSkill(BaseSkill):
    NAME = WarriorSkillEnum.MORE_THAN_POWERFUL_ATTACK.value
    DESCRIPTION = (
        f'Tenciona os músculos além do máximo e desfere um '
        f'golpe devastador, causando dano com base em '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (200% + 5% x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.WARRIOR.value,
        'skill_list': [PowerfulAttackSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 3
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 2.00,
        }
        damage_types = None

        super().__init__(
            name=MoreThanPowerfulAttackSkill.NAME,
            description=MoreThanPowerfulAttackSkill.DESCRIPTION,
            rank=MoreThanPowerfulAttackSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=MoreThanPowerfulAttackSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    @property
    def hit_multiplier(self) -> float:
        return 1.10


if __name__ == '__main__':
    from rpgram.constants.test import WARRIOR_CHARACTER
    skill = PowerfulAttackSkill(WARRIOR_CHARACTER)
    print(skill)
    print(WARRIOR_CHARACTER.cs.physical_attack)
    WARRIOR_CHARACTER.skill_tree.learn_skill(PowerfulAttackSkill)

    skill = MoreThanPowerfulAttackSkill(WARRIOR_CHARACTER)
    print(skill)
    print(WARRIOR_CHARACTER.cs.physical_attack)
    WARRIOR_CHARACTER.skill_tree.learn_skill(MoreThanPowerfulAttackSkill)
