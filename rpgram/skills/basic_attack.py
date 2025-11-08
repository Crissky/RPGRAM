
from typing import TYPE_CHECKING
from rpgram.enums.skill import SkillDefenseEnum, SkillTypeEnum, TargetEnum
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.skills.skill_base import BaseSkill

if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class PhysicalAttackSkill(BaseSkill):
    NAME = 'Physical Attack'
    DESCRIPTION = 'Ataque Físico baseado em "FOR" e "DES".'

    def __init__(self, char: 'BaseCharacter'):
        rank = 0
        level = 0
        cost = 1

        super().__init__(
            name=PhysicalAttackSkill.NAME,
            description=PhysicalAttackSkill.DESCRIPTION,
            rank=rank,
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


class PrecisionAttackSkill(BaseSkill):
    NAME = 'Precision Attack'
    DESCRIPTION = 'Ataque rápido baseado em "DES".'

    def __init__(self, char: 'BaseCharacter'):
        rank = 0
        level = 0
        cost = 1

        super().__init__(
            name=PrecisionAttackSkill.NAME,
            description=PrecisionAttackSkill.DESCRIPTION,
            rank=rank,
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


class MagicalAttackSkill(BaseSkill):
    NAME = 'Magical Attack'
    DESCRIPTION = 'Ataque Mágico baseado em "INT" e "WIS".'

    def __init__(self, char: 'BaseCharacter'):
        rank = 0
        level = 0
        cost = 1

        super().__init__(
            name=MagicalAttackSkill.NAME,
            description=MagicalAttackSkill.DESCRIPTION,
            rank=rank,
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
            damage_types=None
        )


if __name__ == '__main__':
    from rpgram.constants.test import BASE_CHARACTER
    pha = PhysicalAttackSkill(BASE_CHARACTER)
    pra = PrecisionAttackSkill(BASE_CHARACTER)
    maa = MagicalAttackSkill(BASE_CHARACTER)
    print(f'\n{pha.description_text}\nPower: {pha.power}')
    print(f'CHARACTER.Physical Attack: {BASE_CHARACTER.cs.physical_attack}')
    print('#'*79)
    print(f'\n{pra.description_text}\nPower: {pra.power}')
    print(f'CHARACTER.Precision Attack: {BASE_CHARACTER.cs.precision_attack}')
    print('#'*79)
    print(f'\n{maa.description_text}\nPower: {maa.power}')
    print(f'CHARACTER.Magical Attack: {BASE_CHARACTER.cs.magical_attack}')
    print('#'*79)
    print(pha)
