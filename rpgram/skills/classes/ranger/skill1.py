

from typing import TYPE_CHECKING

from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.self_skill import AlertCondition, SniffCondition
from rpgram.constants.text import DEXTERITY_EMOJI_TEXT, HIT_EMOJI_TEXT, MAGICAL_ATTACK_EMOJI_TEXT, PRECISION_ATTACK_EMOJI_TEXT
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.skill import (
    RangerSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class K9AttackSkill(BaseSkill):
    NAME = RangerSkillEnum.K9_STRIKE.value
    DESCRIPTION = (
        f'Realiza um comando sutil que faz com que seu '
        f'*Companheiro de Guarda* inicie um ataque feroz, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.PIERCING)}* com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.RANGER.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.25,
        }
        damage_types = [DamageEnum.PIERCING]

        super().__init__(
            name=K9AttackSkill.NAME,
            description=K9AttackSkill.DESCRIPTION,
            rank=K9AttackSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=K9AttackSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class DoubleAmbushSkill(BaseSkill):
    NAME = RangerSkillEnum.DOUBLE_AMBUSH.value
    DESCRIPTION = (
        f'Realiza um ataque em conjunto com o seu *Companheiro de Guarda*, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.PIERCING)}* com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (150% + 5% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.RANGER.value,
        'skill_list': [K9AttackSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.50,
        }
        damage_types = [DamageEnum.PIERCING]

        super().__init__(
            name=DoubleAmbushSkill.NAME,
            description=DoubleAmbushSkill.DESCRIPTION,
            rank=DoubleAmbushSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=DoubleAmbushSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class ThePackSkill(BaseSkill):
    NAME = RangerSkillEnum.THE_PACK.value
    DESCRIPTION = (
        f'Convoca *{RangerSkillEnum.THE_PACK.value}* e '
        f'realiza um ataque em conjunto contra os inimigos, juntamente com '
        f'o seu *Companheiro de Guarda*, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.PIERCING)}* com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (75% + 2.5% x Rank x Nível).'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.RANGER.value,
        'skill_list': [K9AttackSkill.NAME, DoubleAmbushSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 0.75,
        }
        damage_types = [
            DamageEnum.PIERCING,
            DamageEnum.PIERCING,
            DamageEnum.PIERCING,
        ]

        super().__init__(
            name=ThePackSkill.NAME,
            description=ThePackSkill.DESCRIPTION,
            rank=ThePackSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.TEAM,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=ThePackSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class SniffSkill(BaseSkill):
    NAME = RangerSkillEnum.SNIFF.value
    DESCRIPTION = (
        f'Realiza um comando para o *Companheiro de Guarda* iniciar o '
        f'ratreio de inimigos com o seu *Faro*, '
        f'aumentando o '
        f'*{HIT_EMOJI_TEXT}* com base na '
        f'*{DEXTERITY_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.RANGER.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=SniffSkill.NAME,
            description=SniffSkill.DESCRIPTION,
            rank=SniffSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=SniffSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        condition = SniffCondition(character=char, level=level)
        report_list = self.char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* realiza um comando para o '
                f'*Companheiro de Guarda* farejar, '
                f'aumentando o seu '
                f'*{HIT_EMOJI_TEXT}* '
                f'em {condition.bonus_hit} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class AlertSkill(BaseSkill):
    NAME = RangerSkillEnum.ALERT.value
    DESCRIPTION = (
        f'Realiza um comando para o *Companheiro de Guarda* entrar em '
        f'*Estado de Alerta*, '
        f'aumentando o '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* e '
        f'*{HIT_EMOJI_TEXT}* com base na '
        f'*{DEXTERITY_EMOJI_TEXT}* (200% + 10% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.RANGER.value,
        'skill_list': [SniffSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=AlertSkill.NAME,
            description=AlertSkill.DESCRIPTION,
            rank=AlertSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=AlertSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        condition = AlertCondition(character=char, level=level)
        report_list = self.char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* realiza um comando para o '
                f'*Companheiro de Guarda* entrar em *Estado de Alerta*, '
                f'aumentando o '
                f'*{PRECISION_ATTACK_EMOJI_TEXT}* '
                f'em {condition.bonus_precision_attack} pontos e o '
                f'*{HIT_EMOJI_TEXT}* '
                f'em {condition.bonus_hit} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


SKILL_WAY_DESCRIPTION = {
    'name': 'Guardião Selvagem',
    'description': (
        'O Guardião Selvagem é um guardião ancestral da natureza, '
        'profundamente conectado ao território que patrulha. '
        'Ele possui uma profunda compreensão dos ciclos da natureza e '
        'uma habilidade única de se comunicar com os animais.'
    ),
    'skill_list': [
        K9AttackSkill,
        DoubleAmbushSkill,
        ThePackSkill,
        SniffSkill,
        AlertSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import RANGER_CHARACTER

    skill = K9AttackSkill(RANGER_CHARACTER)
    print(skill)
    print(RANGER_CHARACTER.cs.physical_attack)
    print(RANGER_CHARACTER.to_attack(
        defender_char=RANGER_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    RANGER_CHARACTER.skill_tree.learn_skill(K9AttackSkill)

    skill = DoubleAmbushSkill(RANGER_CHARACTER)
    print(skill)
    print(RANGER_CHARACTER.cs.physical_attack)
    print(RANGER_CHARACTER.to_attack(
        defender_char=RANGER_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    RANGER_CHARACTER.skill_tree.learn_skill(DoubleAmbushSkill)

    skill = ThePackSkill(RANGER_CHARACTER)
    print(skill)
    print(RANGER_CHARACTER.cs.physical_attack)
    print(RANGER_CHARACTER.to_attack(
        defender_char=RANGER_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    RANGER_CHARACTER.skill_tree.learn_skill(ThePackSkill)

    skill = SniffSkill(RANGER_CHARACTER)
    print(skill)
    print(RANGER_CHARACTER.cs.dexterity)
    print(RANGER_CHARACTER.cs.hit)
    print(skill.function())
    print(RANGER_CHARACTER.cs.hit)
    RANGER_CHARACTER.skill_tree.learn_skill(SniffSkill)

    skill = AlertSkill(RANGER_CHARACTER)
    print(skill)
    print(RANGER_CHARACTER.cs.dexterity)
    print(RANGER_CHARACTER.cs.precision_attack)
    print(skill.function())
    print(RANGER_CHARACTER.cs.precision_attack)
    RANGER_CHARACTER.skill_tree.learn_skill(AlertSkill)
