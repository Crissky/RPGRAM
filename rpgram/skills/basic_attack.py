
from rpgram.enums.skill import SkillTypeEnum, TargetEnum
from rpgram.equips import Equips
from rpgram.skills.skill_base import BaseSkill
from rpgram.stats.stats_base import BaseStats
from rpgram.stats.stats_combat import CombatStats


class PhysicalAttack(BaseSkill):
    def __init__(
        self,
        base_stats: BaseStats,
        combat_stats: CombatStats,
        equips: Equips
    ):
        name = 'Physical Attack'
        description = 'Ataque Físico baseado em "FOR" e "DES".'
        power = 0
        level = 1
        cost = 0

        super().__init__(
            name=name,
            description=description,
            power=power,
            level=level,
            cost=cost,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            base_stats=base_stats,
            combat_stats=combat_stats,
            equips=equips,
            requirements={},
            damage_types=None
        )

    @property
    def power(self) -> int:
        return self.combat_stats.physical_attack


class PrecisionAttack(BaseSkill):
    def __init__(
        self,
        base_stats: BaseStats,
        combat_stats: CombatStats,
        equips: Equips
    ):
        name = 'Precision Attack'
        description = 'Ataque rápido baseado em "DES".'
        power = 0
        level = 1
        cost = 0

        super().__init__(
            name=name,
            description=description,
            power=power,
            level=level,
            cost=cost,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            base_stats=base_stats,
            combat_stats=combat_stats,
            equips=equips,
            requirements={},
            damage_types=None
        )

    @property
    def power(self) -> int:
        return self.combat_stats.precision_attack


class MagicalAttack(BaseSkill):
    def __init__(
        self,
        base_stats: BaseStats,
        combat_stats: CombatStats,
        equips: Equips
    ):
        name = 'Magical Attack'
        description = 'Ataque Mágico baseado em "INT" e "WIS".'
        power = 0
        level = 1
        cost = 0

        super().__init__(
            name=name,
            description=description,
            power=power,
            level=level,
            cost=cost,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            base_stats=base_stats,
            combat_stats=combat_stats,
            equips=equips,
            requirements={},
            damage_types=None
        )

    @property
    def power(self) -> int:
        return self.combat_stats.magical_attack
