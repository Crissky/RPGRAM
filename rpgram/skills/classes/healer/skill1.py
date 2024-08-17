from typing import TYPE_CHECKING

from rpgram.constants.text import (
    HIT_POINT_FULL_EMOJI_TEXT,
    MAGICAL_DEFENSE_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.skill import (
    HealerSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class HealingTouchSkill(BaseSkill):
    NAME = HealerSkillEnum.HEALING_TOUCH.value
    DESCRIPTION = (
        f'Canaliza energia vital para, com um simples toque, '
        f'curar o *{HIT_POINT_FULL_EMOJI_TEXT}* de um aliado '
        f'com base na *{MAGICAL_DEFENSE_EMOJI_TEXT}* '
        f'(200% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.HEALER.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=HealingTouchSkill.NAME,
            description=HealingTouchSkill.DESCRIPTION,
            rank=HealingTouchSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.HEALING,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=HealingTouchSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        target_name = char.player_name
        if char.is_alive:
            dice = self.dice
            level = self.level_rank
            power_multiplier = 2 + (level / 10)
            power = dice.boosted_magical_defense * power_multiplier
            power = round(power)

            cure_report = char.cs.cure_hit_points(power)
            report_text = cure_report["text"]
            report = {
                'text': (
                    f'*{target_name}* é revigorado pelo *{self.name}*.\n'
                    f'*{report_text}*({dice.text}).'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


SKILL_WAY_DESCRIPTION = {
    'name': '',
    'description': (
        ''
    ),
    'skill_list': []
}


if __name__ == '__main__':
    from rpgram.conditions.debuff import CurseCondition, PoisoningCondition
    from rpgram.constants.test import HEALER_CHARACTER

    skill = HealingTouchSkill(HEALER_CHARACTER)
    print(skill)
    print(HEALER_CHARACTER.cs.show_hit_points)
    print(skill.function(HEALER_CHARACTER))
    print(HEALER_CHARACTER.cs.show_hit_points)
    HEALER_CHARACTER.skill_tree.learn_skill(HealingTouchSkill)
