from random import choice
from typing import TYPE_CHECKING
from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.special_damage_skill import (
    SDWildAcidCondition,
    SDWildFireCondition,
    SDWildGroundCondition,
    SDWildLightningCondition,
    SDWildPoisonCondition,
    SDWildRockCondition,
    SDWildWindCondition
)
from rpgram.constants.text import (
    PHYSICAL_ATTACK_EMOJI_TEXT
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


class WildForgeSkill(BaseSkill):
    NAME = BarbarianSkillEnum.FURIOUS_FURY.value
    DESCRIPTION = (
        f'Imbui a própria arma com algum *Elemento Selvagem* aleatório '
        f'com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
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
            name=WildForgeSkill.NAME,
            description=WildForgeSkill.DESCRIPTION,
            rank=WildForgeSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=WildForgeSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        power = char.cs.physical_attack
        level = self.level_rank
        condition_class_list = [
            SDWildFireCondition,
            SDWildLightningCondition,
            SDWildWindCondition,
            SDWildRockCondition,
            SDWildGroundCondition,
            SDWildAcidCondition,
            SDWildPoisonCondition,
        ]
        condition_class = choice(condition_class_list)
        condition = condition_class(power=power, level=level)
        report_list = self.char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* forja o *Elemento {condition.name}* '
                f' e embebeda sua(s) arma(s), recebendo '
                f'o tipo de dano *{condition.damage_emoji_name}*.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


if __name__ == '__main__':
    from rpgram.constants.test import BARBARIAN_CHARACTER

    skill = WildForgeSkill(BARBARIAN_CHARACTER)
    print(skill)
    print(skill.function())
    print(BARBARIAN_CHARACTER.status)
    BARBARIAN_CHARACTER.skill_tree.learn_skill(WildForgeSkill)
