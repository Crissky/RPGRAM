from typing import TYPE_CHECKING
from rpgram.conditions.self_skill import RobustBlockCondition
from rpgram.constants.text import CONSTITUTION_ABB, PHYSICAL_DEFENSE_FULL
from rpgram.enums.skill import SkillDefenseEnum, SkillTypeEnum, TargetEnum
from rpgram.skills.skill_base import BaseSkill

if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class RobustBlockSkill(BaseSkill):
    NAME = 'Bloqueio Robusto'
    def __init__(self, char: 'BaseCharacter', level: int = 1):
        description = (
            f'Assume uma postura defensiva aumentando a '
            f'{PHYSICAL_DEFENSE_FULL} com base na {CONSTITUTION_ABB}.'
        )
        cost = 2

        super().__init__(
            name=RobustBlockSkill.NAME,
            description=description,
            level=level,
            cost=cost,
            base_stats_multiplier={},
            combat_stats_multiplier={},
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.DEFENSE,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements={},
            damage_types=None
        )

    def function(self) -> dict:
        rbc = RobustBlockCondition(character=self.char)
        report_list = self.char.status.set_conditions(rbc)
        report = {
            'text': '\n'.join([report['text'] for report in report_list])
        }

        return report


if __name__ == '__main__':
    from rpgram.constants.test import BASE_CHARACTER
    rbs = RobustBlockSkill(BASE_CHARACTER)
    print(rbs)
    print(BASE_CHARACTER.cs.physical_defense)
    print(rbs.function())
    print(BASE_CHARACTER.cs.physical_defense)
