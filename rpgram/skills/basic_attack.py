
from typing import TYPE_CHECKING
from rpgram.enums.skill import SkillDefenseEnum, SkillTypeEnum, TargetEnum
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.skills.skill_base import BaseSkill

if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class PhysicalAttack(BaseSkill):
    def __init__(self, char: 'BaseCharacter'):
        name = 'Physical Attack'
        description = 'Ataque Físico baseado em "FOR" e "DES".'
        level = 0
        cost = 1

        super().__init__(
            name=name,
            description=description,
            level=level,
            cost=cost,
            base_stats_multiplier={},
            combat_stats_multiplier={CombatStatsEnum.PHYSICAL_ATTACK: 1.0},
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements={},
            damage_types=None
        )


class PrecisionAttack(BaseSkill):
    def __init__(self, char: 'BaseCharacter'):
        name = 'Precision Attack'
        description = 'Ataque rápido baseado em "DES".'
        level = 0
        cost = 1

        super().__init__(
            name=name,
            description=description,
            level=level,
            cost=cost,
            base_stats_multiplier={},
            combat_stats_multiplier={CombatStatsEnum.PRECISION_ATTACK: 1.0},
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements={},
            damage_types=None
        )


class MagicalAttack(BaseSkill):
    def __init__(self, char: 'BaseCharacter'):
        name = 'Magical Attack'
        description = 'Ataque Mágico baseado em "INT" e "WIS".'
        level = 0
        cost = 1

        super().__init__(
            name=name,
            description=description,
            level=level,
            cost=cost,
            base_stats_multiplier={},
            combat_stats_multiplier={CombatStatsEnum.MAGICAL_ATTACK: 1.0},
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=True,
            requirements={},
            damage_types='MAGIC'
        )


if __name__ == '__main__':
    from rpgram.constants.test import BASE_CHARACTER
    pha = PhysicalAttack(BASE_CHARACTER)
    pra = PrecisionAttack(BASE_CHARACTER)
    maa = MagicalAttack(BASE_CHARACTER)
    print(f'\n{pha.description_text}\nPower: {pha.power}')
    print(f'CHARACTER.Physical Attack: {BASE_CHARACTER.cs.physical_attack}')
    print('#'*79)
    print(f'\n{pra.description_text}\nPower: {pra.power}')
    print(f'CHARACTER.Precision Attack: {BASE_CHARACTER.cs.precision_attack}')
    print('#'*79)
    print(f'\n{maa.description_text}\nPower: {maa.power}')
    print(f'CHARACTER.Magical Attack: {BASE_CHARACTER.cs.magical_attack}')
    print('#'*79)
