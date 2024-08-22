from typing import TYPE_CHECKING

from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.self_skill import ImproviseCondition
from rpgram.constants.text import (
    DEXTERITY_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.skill import (
    MercenarySkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class NosebreakerSkill(BaseSkill):
    NAME = MercenarySkillEnum.NOSEBREAKER.value
    DESCRIPTION = (
        f'Concentra sua força em um golpe direto focando a face do inimigo, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.BLUDGEONING)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.MERCENARY.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.25,
        }
        damage_types = [DamageEnum.BLUDGEONING]

        super().__init__(
            name=NosebreakerSkill.NAME,
            description=NosebreakerSkill.DESCRIPTION,
            rank=NosebreakerSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=NosebreakerSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class SkullbreakerSkill(BaseSkill):
    NAME = MercenarySkillEnum.SKULLBREAKER.value
    DESCRIPTION = (
        f'Realiza um ataque físico brutal focando a cabeça do inimigo, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.BLUDGEONING)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (150% + 5% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.MERCENARY.value,
        'skill_list': [NosebreakerSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.50,
        }
        damage_types = [DamageEnum.BLUDGEONING]

        super().__init__(
            name=SkullbreakerSkill.NAME,
            description=SkullbreakerSkill.DESCRIPTION,
            rank=SkullbreakerSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=SkullbreakerSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class ImproviseSkill(BaseSkill):
    NAME = MercenarySkillEnum.IMPROVISE.value
    DESCRIPTION = (
        f'*Improvisa* melhorias temporárias para suas armas, '
        f'aumentando o *{PHYSICAL_ATTACK_EMOJI_TEXT}* com base na '
        f'*{DEXTERITY_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.MERCENARY.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=ImproviseSkill.NAME,
            description=ImproviseSkill.DESCRIPTION,
            rank=ImproviseSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=ImproviseSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        condition = ImproviseCondition(character=char, level=level)
        report_list = self.char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* *Improvisa* melhorias em sua(s) arma(s), '
                f'aumentando o seu '
                f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* '
                f'em {condition.bonus_physical_attack} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


SKILL_WAY_DESCRIPTION = {
    'name': 'Combate Desleal',
    'description': (
        'O mercenário que segue esse caminho não se prende a '
        'regras ou códigos de honra. '
        'Para ele, a vitória é tudo, e qualquer meio é justificado '
        'para alcançá-la. '
        'A trapaça, a manipulação e a surpresa são suas '
        'ferramentas mais valiosas.'
    ),
    'skill_list': [
        NosebreakerSkill,
        SkullbreakerSkill,
        ImproviseSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import MERCENARY_CHARACTER

    skill = NosebreakerSkill(MERCENARY_CHARACTER)
    print(skill)
    print(MERCENARY_CHARACTER.cs.physical_attack)
    print(MERCENARY_CHARACTER.to_attack(
        defender_char=MERCENARY_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    MERCENARY_CHARACTER.skill_tree.learn_skill(NosebreakerSkill)

    skill = SkullbreakerSkill(MERCENARY_CHARACTER)
    print(skill)
    print(MERCENARY_CHARACTER.cs.physical_attack)
    print(MERCENARY_CHARACTER.to_attack(
        defender_char=MERCENARY_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    MERCENARY_CHARACTER.skill_tree.learn_skill(SkullbreakerSkill)

    skill = ImproviseSkill(MERCENARY_CHARACTER)
    print(skill)
    print(MERCENARY_CHARACTER.cs.physical_attack,
          MERCENARY_CHARACTER.cs.dexterity)
    print(skill.function())
    print(MERCENARY_CHARACTER.cs.physical_attack)
    MERCENARY_CHARACTER.skill_tree.learn_skill(ImproviseSkill)
