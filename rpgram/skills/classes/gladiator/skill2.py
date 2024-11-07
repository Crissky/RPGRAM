from typing import TYPE_CHECKING

from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.barrier import AjaxShieldCondition
from rpgram.conditions.self_skill import (
    ArenaDomainCondition,
    TurtleStanceCondition,
    UnicornStanceCondition
)
from rpgram.conditions.special_damage_skill import SDAresBladeCondition
from rpgram.conditions.target_skill_buff import (
    MartialBannerCondition,
    WarBannerCondition
)
from rpgram.constants.text import (
    CHARISMA_EMOJI_TEXT,
    CONSTITUTION_EMOJI_TEXT,
    EVASION_EMOJI_TEXT,
    HIT_EMOJI_TEXT,
    HIT_POINT_FULL_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT,
    PHYSICAL_DEFENSE_EMOJI_TEXT,
    STRENGTH_EMOJI_TEXT,
    WISDOM_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.skill import (
    GladiatorSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class MartialBannerSkill(BaseSkill):
    NAME = GladiatorSkillEnum.MARTIAL_BANNER.value
    DESCRIPTION = (
        f'Usa a própria força e ira para evocar o '
        f'*Sinal do Senhor da Guerra* e conceder à equipe '
        f'uma inspiração de combate que aumenta o '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* com base na '
        f'*{STRENGTH_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.GLADIATOR.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=MartialBannerSkill.NAME,
            description=MartialBannerSkill.DESCRIPTION,
            rank=MartialBannerSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.TEAM,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=MartialBannerSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        target_name = char.player_name
        if char.is_alive:
            power = self.char.bs.strength
            level = self.level_rank
            condition = MartialBannerCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{target_name}* recebe o *Sinal do Senhor da Guerra*, '
                    f'aumentando o '
                    f'{PHYSICAL_ATTACK_EMOJI_TEXT} em '
                    f'*{condition.power}* pontos.\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


SKILL_WAY_DESCRIPTION = {
    'name': 'Filho da Guerra',
    'description': (
        'Nascido e criado no calor da batalha, '
        'o Filho da Guerra é um guerreiro moldado pela violência. '
        'Seu destino é a batalha, onde ele encontra seu verdadeiro lar. '
        'Com cada combate, ele se fortalece, '
        'tanto física quanto espiritualmente, '
        'tornando-se uma força imparável.'
    ),
    'skill_list': [
        MartialBannerSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import GLADIATOR_CHARACTER

    skill = MartialBannerSkill(GLADIATOR_CHARACTER)
    print(skill)
    print(GLADIATOR_CHARACTER.cs.strength,
          GLADIATOR_CHARACTER.cs.physical_attack)
    print(skill.function(GLADIATOR_CHARACTER))
    print(GLADIATOR_CHARACTER.cs.physical_attack)
    GLADIATOR_CHARACTER.skill_tree.learn_skill(MartialBannerSkill)
