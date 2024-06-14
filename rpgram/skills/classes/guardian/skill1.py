from typing import TYPE_CHECKING
from rpgram.enums.skill import SkillDefenseEnum, SkillTypeEnum, TargetEnum
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.skills.skill_base import BaseSkill

if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class TestGuardianSkill(BaseSkill):
    def __init__(self, char: 'BaseCharacter'):
        name = 'Test Guardian Skill'
        description = 'Uma skill de teste.'
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