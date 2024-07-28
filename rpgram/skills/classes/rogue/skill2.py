from typing import TYPE_CHECKING
from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.self_skill import (
    ChaoticStepsCondition,
    ShadowStepsCondition
)
from rpgram.constants.text import (
    DEXTERITY_EMOJI_TEXT,
    EVASION_EMOJI_TEXT,
    HIT_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.skill import (
    RogueSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


SKILL_WAY_DESCRIPTION = {
    'name': 'Mestre das Sombras',
    'description': (
        ''
    )
}


class ShadowStepsSkill(BaseSkill):
    NAME = RogueSkillEnum.SHADOW_STEPS.value
    DESCRIPTION = (
        f'Torna-se um "Fantasma", movendo-se pelas *Sombras* e '
        f'aumentando o '
        f'*{HIT_EMOJI_TEXT}* com base na '
        f'*{DEXTERITY_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.ROGUE.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=ShadowStepsSkill.NAME,
            description=ShadowStepsSkill.DESCRIPTION,
            rank=ShadowStepsSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=ShadowStepsSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        condition = ShadowStepsCondition(character=char, level=level)
        report_list = self.char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* move-se pelas *Sombras*, '
                f' aumentando o '
                f'*{HIT_EMOJI_TEXT}*.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class ChaoticStepsSkill(BaseSkill):
    NAME = RogueSkillEnum.CHAOTIC_STEPS.value
    DESCRIPTION = (
        f'Assume um padrão errático e imprevisível de movimentos, '
        f'tornado sua locomoção ainda mais difícil de prever, '
        f'aumentando a '
        f'*{EVASION_EMOJI_TEXT}* com base na '
        f'*{DEXTERITY_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.ROGUE.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=ChaoticStepsSkill.NAME,
            description=ChaoticStepsSkill.DESCRIPTION,
            rank=ChaoticStepsSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=ChaoticStepsSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        condition = ChaoticStepsCondition(character=char, level=level)
        report_list = self.char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* começa a mover-se de maneira '
                f'errática e imprevisível, '
                f'aumentando a '
                f'*{EVASION_EMOJI_TEXT}*.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


if __name__ == '__main__':
    from rpgram.constants.test import ROGUE_CHARACTER

    skill = ShadowStepsSkill(ROGUE_CHARACTER)
    print(skill)
    print(ROGUE_CHARACTER.cs.dexterity)
    print(ROGUE_CHARACTER.cs.hit)
    print(skill.function())
    print(ROGUE_CHARACTER.cs.hit)
    ROGUE_CHARACTER.skill_tree.learn_skill(ShadowStepsSkill)

    skill = ChaoticStepsSkill(ROGUE_CHARACTER)
    print(skill)
    print(ROGUE_CHARACTER.cs.dexterity)
    print(ROGUE_CHARACTER.cs.evasion)
    print(skill.function())
    print(ROGUE_CHARACTER.cs.evasion)
    ROGUE_CHARACTER.skill_tree.learn_skill(ChaoticStepsSkill)

    print('\n'.join([
        report['text']
        for report in ROGUE_CHARACTER.activate_status()
    ]))
