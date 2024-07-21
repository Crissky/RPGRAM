
from typing import TYPE_CHECKING
from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.target_skill_buff import (
    AnansisTrickeryCondition,
    HecatesFlamesCondition,
    IdunnsAppleCondition,
    IsissVeilCondition,
    KratossWrathCondition,
    OgunsCloakCondition,
    UllrsFocusCondition
)
from rpgram.constants.text import (
    EVASION_EMOJI_TEXT,
    HIT_EMOJI_TEXT,
    HIT_POINT_FULL_EMOJI_TEXT,
    MAGICAL_ATTACK_EMOJI_TEXT,
    MAGICAL_DEFENSE_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT,
    PHYSICAL_DEFENSE_EMOJI_TEXT,
    PRECISION_ATTACK_EMOJI_TEXT,
    WISDOM_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.skill import (
    ClericSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class IxChelsAmphoraSkill(BaseSkill):
    NAME = ClericSkillEnum.IXCHELÇÇÇS_AMPHORA.value
    DESCRIPTION = (
        f'Um ritual de purificação que conjura uma *Amphora Mística* '
        f'que cura o *{HIT_POINT_FULL_EMOJI_TEXT}* de um aliado '
        f'com base na *{MAGICAL_DEFENSE_EMOJI_TEXT}* '
        f'(200% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.CLERIC.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 2
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=IxChelsAmphoraSkill.NAME,
            description=IxChelsAmphoraSkill.DESCRIPTION,
            rank=IxChelsAmphoraSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=IxChelsAmphoraSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        target_name = char.player_name
        dice = self.dice
        level = self.level_rank
        power_multiplier = 2 + (level / 10)
        power = dice.boosted_magical_defense * power_multiplier
        power = round(power)

        cure_report = self.char.cs.cure_hit_points(power)
        report_text = cure_report["text"]
        report = {
            'text': (
                f'*{target_name}* é banhado pela águas de uma '
                f'*Amphora Mística* que cura suas feridas.\n'
                f'*{report_text}*({dice.text}).'
            )
        }

        return report


if __name__ == '__main__':
    from rpgram.constants.test import CLERIC_CHARACTER

    skill = IxChelsAmphoraSkill(CLERIC_CHARACTER)
    print(skill)
    print(CLERIC_CHARACTER.cs.show_hit_points)
    print(skill.function(CLERIC_CHARACTER))
    print(CLERIC_CHARACTER.cs.show_hit_points)
    CLERIC_CHARACTER.skill_tree.learn_skill(IxChelsAmphoraSkill)
