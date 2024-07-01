from typing import TYPE_CHECKING
from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.self_skill import (
    FuriousFuryCondition
)
from rpgram.constants.text import (
    PHYSICAL_ATTACK_EMOJI_TEXT,
    STRENGTH_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.skill import (
    BarbarianSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill

if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


SKILL_WAY_DESCRIPTION = {
    'name': 'Fúria Selvagem',
    'description': (
        'Caminho da fúria incontrolável do Bárbaro, a força bruta e a '
        'ferocidade que o definem em combate. '
        'As habilidades desse grupo se concentram em aumentar o dano do '
        'Bárbaro, sua resistência e sua capacidade de entrar em fúrias '
        'cada vez mais poderosas.'
    )
}


class FuriousFurySkill(BaseSkill):
    NAME = BarbarianSkillEnum.FURIOUS_FURY.value
    DESCRIPTION = (
        f'Entra em um estado de *Fúria* que o leva a agir Furiosamente, '
        f'aumentando o *{PHYSICAL_ATTACK_EMOJI_TEXT}* com base na '
        f'*{STRENGTH_EMOJI_TEXT}*.'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.BARBARIAN.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 2
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=FuriousFurySkill.NAME,
            description=FuriousFurySkill.DESCRIPTION,
            rank=FuriousFurySkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.DEFENSE,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=FuriousFurySkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        condition = FuriousFuryCondition(character=self.char, level=self.level)
        report_list = self.char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'Você perde a concentração e entra em um estado de *Fúria*, '
                f'aumentando o seu '
                f'*{PHYSICAL_ATTACK_EMOJI_TEXT}*.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


if __name__ == '__main__':
    from rpgram.constants.test import BARBARIAN_CHARACTER
    skill = FuriousFurySkill(BARBARIAN_CHARACTER)
    print(skill)
    print(BARBARIAN_CHARACTER.bs.strength)
    print(BARBARIAN_CHARACTER.cs.physical_attack)
    print(skill.function())
    print(BARBARIAN_CHARACTER.cs.physical_attack)
    BARBARIAN_CHARACTER.skill_tree.learn_skill(FuriousFurySkill)
