from typing import TYPE_CHECKING

from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.debuff import BerserkerCondition
from rpgram.conditions.self_skill import HrungnirsSovereigntyCondition
from rpgram.constants.text import (
    HIT_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT,
    STRENGTH_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.debuff import DebuffEnum, get_debuff_emoji_text
from rpgram.enums.skill import (
    BerserkirSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class HrungnirsSovereigntySkill(BaseSkill):
    NAME = BerserkirSkillEnum.HRUNGNIRÇÇÇS_SOVEREIGNTY.value
    DESCRIPTION = (
        f'Entra em um estado de *Fúria Desenfreada* ao ser envolto pelo '
        f'espírito do *Gigante Hrungnir*, '
        f'recebendo a condição '
        f'*{get_debuff_emoji_text(DebuffEnum.BERSERKER)}* '
        f'com nível igual ao (Rank x Nível) e '
        f'aumentando o *{PHYSICAL_ATTACK_EMOJI_TEXT}* com base na '
        f'*{STRENGTH_EMOJI_TEXT}* (200% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.BERSERKIR.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=HrungnirsSovereigntySkill.NAME,
            description=HrungnirsSovereigntySkill.DESCRIPTION,
            rank=HrungnirsSovereigntySkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=HrungnirsSovereigntySkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank

        condition = HrungnirsSovereigntyCondition(character=char, level=level)
        report_list = self.char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )

        berserker_condition = BerserkerCondition(level=level)
        status_report = char.status.add_condition(berserker_condition)

        report = {
            'text': (
                f'*{player_name}* é envolto pelo espírito do '
                f'*Gigante Hrungnir*, entrando em um estado '
                f'de *Fúria Desenfreada* que aumenta o seu '
                f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* '
                f'em {condition.bonus_physical_attack} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}\n'
                f'{status_report["text"]}'
            )
        }

        return report


SKILL_WAY_DESCRIPTION = {
    'name': 'Espírito Bestial',
    'description': (
        'O caminho do Espírito Bestial transforma o Berserkir '
        'em um receptáculo das forças das Criaturas Mitológicas, utilizando '
        'habilidades ancestrais para manipular os Poderes Bestiais e '
        'liberar a fúria indomável da fera interior. '
        'Através de rituais ancestrais e conexão profunda com esses seres, '
        'o Berserkir se torna um agente da destruição da ancianidade.'
    ),
    'skill_list': [
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import BERSERKIR_CHARACTER

    skill = HrungnirsSovereigntySkill(BERSERKIR_CHARACTER)
    print(skill)
    print(BERSERKIR_CHARACTER.bs.strength,
          BERSERKIR_CHARACTER.cs.physical_attack)
    print(skill.function())
    print(BERSERKIR_CHARACTER.bs.strength,
          BERSERKIR_CHARACTER.cs.physical_attack)
    BERSERKIR_CHARACTER.skill_tree.learn_skill(HrungnirsSovereigntySkill)
