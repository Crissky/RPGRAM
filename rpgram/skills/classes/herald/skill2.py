from typing import TYPE_CHECKING
from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.self_skill import VigilFlameCondition
from rpgram.conditions.special_damage_skill import SDVigilArmsCondition
from rpgram.constants.text import (
    CONSTITUTION_EMOJI_TEXT,
    MAGICAL_DEFENSE_EMOJI_TEXT,
    PHYSICAL_DEFENSE_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.skill import (
    HeraldSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class VigilFlameSkill(BaseSkill):
    NAME = HeraldSkillEnum.VIGIL_FLAME.value
    DESCRIPTION = (
        f'Canaliza uma aura de fogo que o envolve, '
        f'inflamando o seu espírito para aumentar a '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* e a '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* com base na '
        f'*{CONSTITUTION_EMOJI_TEXT}* (100% + 10% x Rank x Nível). '
        f'Além disso, adiciona dano de '
        f'*{get_damage_emoji_text(DamageEnum.FIRE)}* '
        f'baseado no '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.HERALD.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=VigilFlameSkill.NAME,
            description=VigilFlameSkill.DESCRIPTION,
            rank=VigilFlameSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=VigilFlameSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        char = self.char
        player_name = char.player_name
        level = self.level_rank
        condition = VigilFlameCondition(character=char, level=level)
        report_list = char.status.set_conditions(condition)
        sd_power = char.cs.magical_defense
        sd_condition = SDVigilArmsCondition(power=sd_power, level=level)
        sd_report_list = char.status.set_conditions(sd_condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list + sd_report_list]
        )
        report = {
            'text': (
                f'*{player_name}* se concentra para criar uma '
                f'*Aura de Fogo*, '
                f'aumentando a sua '
                f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* '
                f'em {condition.bonus_physical_defense} e a '
                f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* '
                f'em {condition.bonus_magical_defense} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


SKILL_WAY_DESCRIPTION = {
    'name': 'Vigia das Chamas',
    'description': (
        'Um bastião ardente que utiliza o fogo como símbolo de proteção, '
        'purificação e justiça. '
        'Neste caminho, o Arauto manipula chamas sagradas para proteger '
        'seus aliados e devastar aqueles que ameaçam o equilíbrio. '
        'Suas habilidades mesclam ofensiva e defensiva, '
        'transformando o fogo em um aliado fiel que incinera o mal e aquece '
        'o coração dos justos.'
    ),
    'skill_list': [
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import HERALD_CHARACTER

    skill = VigilFlameSkill(HERALD_CHARACTER)
    print(skill)
    print(HERALD_CHARACTER.cs.constitution,
          HERALD_CHARACTER.cs.physical_defense,
          HERALD_CHARACTER.cs.magical_defense)
    print(skill.function(HERALD_CHARACTER))
    print(HERALD_CHARACTER.cs.physical_defense,
          HERALD_CHARACTER.cs.magical_defense)
    HERALD_CHARACTER.skill_tree.learn_skill(VigilFlameSkill)
