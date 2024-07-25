
from typing import TYPE_CHECKING
from constant.text import (
    ALERT_SECTION_HEAD_ADD_STATUS
)
from rpgram.conditions.special_damage_skill import (
    SDPoisonousSapCondition
)
from rpgram.constants.text import (
    PHYSICAL_ATTACK_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.skill import (
    DruidSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


SKILL_WAY_DESCRIPTION = {
    'name': '',
    'description': (
        ''
    )
}


class PoisonousSapSkill(BaseSkill):
    NAME = DruidSkillEnum.POISONOUS_SAP.value
    DESCRIPTION = (
        f'Imbui os equipamentos com uma '
        f'*{DruidSkillEnum.POISONOUS_SAP.value}* que '
        f'adiciona dano de '
        f'*{get_damage_emoji_text(DamageEnum.POISON)}* '
        f'baseado no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.DRUID.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 2
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=PoisonousSapSkill.NAME,
            description=PoisonousSapSkill.DESCRIPTION,
            rank=PoisonousSapSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=PoisonousSapSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        player_name = self.char.player_name
        target_name = char.player_name
        if char.is_alive:
            level = self.level_rank
            power = char.cs.physical_attack
            condition = SDPoisonousSapCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            if player_name == target_name:
                weapon_text = 'as suas armas'
            else:
                weapon_text = f'as arma de {target_name}'
            report = {
                'text': (
                    f'*{player_name}* imbui {weapon_text} com '
                    f'*{self.name}*.\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


if __name__ == '__main__':
    from rpgram.constants.test import DRUID_CHARACTER

    skill = PoisonousSapSkill(DRUID_CHARACTER)
    print(skill)
    print(DRUID_CHARACTER.cs.physical_attack)
    print(skill.function(DRUID_CHARACTER))
    DRUID_CHARACTER.skill_tree.learn_skill(PoisonousSapSkill)
