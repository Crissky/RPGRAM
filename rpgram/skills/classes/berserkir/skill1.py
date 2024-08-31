from typing import TYPE_CHECKING

from rpgram.conditions.debuff import BerserkerCondition
from rpgram.constants.text import (
    HIT_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT
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


class IndomitableAttackSkill(BaseSkill):
    NAME = BerserkirSkillEnum.INDOMITABLE_ATTACK.value
    DESCRIPTION = (
        f'Entra em um estado de *Fúria Incontrolável*, recebendo a condição '
        f'*{get_debuff_emoji_text(DebuffEnum.BERSERKER)}* '
        f'com nível igual ao (Rank x Nível), '
        f'após isso, realiza uma série de ataques rápidos e brutais, '
        f'causando dano ao inimigo com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (300% + 5% x Rank x Nível), '
        f'mas possui uma baixa taxa de {HIT_EMOJI_TEXT}.'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.BERSERKIR.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 3.00,
        }
        damage_types = None

        super().__init__(
            name=IndomitableAttackSkill.NAME,
            description=IndomitableAttackSkill.DESCRIPTION,
            rank=IndomitableAttackSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=IndomitableAttackSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def pre_hit_function(self, target: 'BaseCharacter') -> dict:
        report = {'text': ''}
        char = self.char
        level = self.level_rank
        berserker_condition = BerserkerCondition(level=level)
        status_report = char.status.add_condition(berserker_condition)
        if status_report['text']:
            report['text'] = status_report["text"]

        return report

    @property
    def hit_multiplier(self) -> float:
        return 0.75


class ImpetuousStrikeSkill(BaseSkill):
    NAME = BerserkirSkillEnum.IMPETUOUS_STRIKE.value
    DESCRIPTION = (
        f'Entra em um estado de *Fúria Incontrolável*, recebendo a condição '
        f'*{get_debuff_emoji_text(DebuffEnum.BERSERKER)}* '
        f'com nível igual ao (Rank x Nível), '
        f'e desfere um ataque com força bruta, '
        f'causando dano com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (400% + 5% x Rank x Nível), '
        f'mas possui uma baixa taxa de {HIT_EMOJI_TEXT}.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.BERSERKIR.value,
        'skill_list': [IndomitableAttackSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 4.00,
        }
        damage_types = None

        super().__init__(
            name=ImpetuousStrikeSkill.NAME,
            description=ImpetuousStrikeSkill.DESCRIPTION,
            rank=ImpetuousStrikeSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=ImpetuousStrikeSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def pre_hit_function(self, target: 'BaseCharacter') -> dict:
        report = {'text': ''}
        char = self.char
        level = self.level_rank
        berserker_condition = BerserkerCondition(level=level)
        status_report = char.status.add_condition(berserker_condition)
        if status_report['text']:
            report['text'] = status_report["text"]

        return report

    @property
    def hit_multiplier(self) -> float:
        return 0.75


class DevastatingRushSkill(BaseSkill):
    NAME = BerserkirSkillEnum.DEVASTATING_RUSH.value
    DESCRIPTION = (
        f'Entra em um estado de *Fúria Incontrolável*, recebendo a condição '
        f'*{get_debuff_emoji_text(DebuffEnum.BERSERKER)}* '
        f'com nível igual ao (Rank x Nível), '
        f'e lança-se contra o alvo em uma corrida implacável, '
        f'causando dano com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (500% + 5% x Rank x Nível), '
        f'mas possui uma baixa taxa de {HIT_EMOJI_TEXT}.'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.BERSERKIR.value,
        'skill_list': [IndomitableAttackSkill.NAME, ImpetuousStrikeSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 5.00,
        }
        damage_types = None

        super().__init__(
            name=DevastatingRushSkill.NAME,
            description=DevastatingRushSkill.DESCRIPTION,
            rank=DevastatingRushSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=DevastatingRushSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def pre_hit_function(self, target: 'BaseCharacter') -> dict:
        report = {'text': ''}
        char = self.char
        level = self.level_rank
        berserker_condition = BerserkerCondition(level=level)
        status_report = char.status.add_condition(berserker_condition)
        if status_report['text']:
            report['text'] = status_report["text"]

        return report

    @property
    def hit_multiplier(self) -> float:
        return 0.75


SKILL_WAY_DESCRIPTION = {
    'name': 'Fúria Indomável',
    'description': (
        'Um tornado de raiva e destruição que usa a sua fúria cegante e '
        'sua força descomunal como arma e motivação. '
        'Ele se alimenta do caos da batalha, '
        'encontrando satisfação em cada golpe desferido e em cada grito '
        'de dor de seus inimigos, se fortalecendo a cada ataque.'
    ),
    'skill_list': [
        IndomitableAttackSkill,
        ImpetuousStrikeSkill,
        DevastatingRushSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import BERSERKIR_CHARACTER

    skill = IndomitableAttackSkill(BERSERKIR_CHARACTER)
    print(skill)
    print(BERSERKIR_CHARACTER.cs.physical_attack)
    print(BERSERKIR_CHARACTER.to_attack(
        defender_char=BERSERKIR_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    BERSERKIR_CHARACTER.skill_tree.learn_skill(IndomitableAttackSkill)

    skill = ImpetuousStrikeSkill(BERSERKIR_CHARACTER)
    print(skill)
    print(BERSERKIR_CHARACTER.cs.physical_attack)
    print(BERSERKIR_CHARACTER.to_attack(
        defender_char=BERSERKIR_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    BERSERKIR_CHARACTER.skill_tree.learn_skill(ImpetuousStrikeSkill)

    skill = DevastatingRushSkill(BERSERKIR_CHARACTER)
    print(skill)
    print(BERSERKIR_CHARACTER.cs.physical_attack)
    print(BERSERKIR_CHARACTER.to_attack(
        defender_char=BERSERKIR_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    BERSERKIR_CHARACTER.skill_tree.learn_skill(DevastatingRushSkill)

    print('\n'.join([
        report['text']
        for report in BERSERKIR_CHARACTER.activate_status()
    ]))
