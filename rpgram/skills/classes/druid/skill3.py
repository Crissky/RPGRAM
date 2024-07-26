
from typing import TYPE_CHECKING
from constant.text import (
    ALERT_SECTION_HEAD_ADD_STATUS
)
from rpgram.conditions.special_damage_skill import (
    SDEscarchaSapCondition,
    SDIgneousSapCondition,
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
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


SKILL_WAY_DESCRIPTION = {
    'name': 'Bruxo Verde',
    'description': (
        'O Bruxo Verde domina a alquimia da Seiva para criar '
        'aprimoramentos e feitiços. '
        'Através de um profundo conhecimento das plantas e de '
        'seus poderes, o Druida manipula a Seiva para '
        'imbuir seus equipamentos com propriedades mágicas e '
        'para manipulá-la como um instrumento de ataque.'
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
            power = self.char.cs.physical_attack
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


class IgneousSapSkill(BaseSkill):
    NAME = DruidSkillEnum.IGNEOUS_SAP.value
    DESCRIPTION = (
        f'Imbui os equipamentos com uma '
        f'*{DruidSkillEnum.IGNEOUS_SAP.value}* que '
        f'adiciona dano de '
        f'*{get_damage_emoji_text(DamageEnum.FIRE)}* '
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
            name=IgneousSapSkill.NAME,
            description=IgneousSapSkill.DESCRIPTION,
            rank=IgneousSapSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=IgneousSapSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        player_name = self.char.player_name
        target_name = char.player_name
        if char.is_alive:
            level = self.level_rank
            power = self.char.cs.physical_attack
            condition = SDIgneousSapCondition(power=power, level=level)
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


class EscarchaSapSkill(BaseSkill):
    NAME = DruidSkillEnum.ESCARCHA_SAP.value
    DESCRIPTION = (
        f'Imbui os equipamentos com uma '
        f'*{DruidSkillEnum.ESCARCHA_SAP.value}* que '
        f'adiciona dano de '
        f'*{get_damage_emoji_text(DamageEnum.COLD)}* '
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
            name=EscarchaSapSkill.NAME,
            description=EscarchaSapSkill.DESCRIPTION,
            rank=EscarchaSapSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=EscarchaSapSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        player_name = self.char.player_name
        target_name = char.player_name
        if char.is_alive:
            level = self.level_rank
            power = self.char.cs.physical_attack
            condition = SDEscarchaSapCondition(power=power, level=level)
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


class SapiousCubeSkill(BaseSkill):
    NAME = DruidSkillEnum.SAPIOUS_CUBE.value
    DESCRIPTION = (
        f'Conjura os poderes da natureza para materializar um '
        f'*Cubo Gelatinoso*, composto por diversos tipos de *Seivas*, '
        f'ao redor do alvo, causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.POISON)}*, de '
        f'*{get_damage_emoji_text(DamageEnum.FIRE)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.COLD)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (150% + 5% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.DRUID.value,
        'skill_list': [
            PoisonousSapSkill.NAME,
            IgneousSapSkill.NAME,
            EscarchaSapSkill.NAME,
        ]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 3
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.50,
        }
        damage_types = [
            DamageEnum.POISON,
            DamageEnum.FIRE,
            DamageEnum.COLD,
        ]

        super().__init__(
            name=SapiousCubeSkill.NAME,
            description=SapiousCubeSkill.DESCRIPTION,
            rank=SapiousCubeSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=SapiousCubeSkill.REQUIREMENTS,
            damage_types=damage_types
        )


if __name__ == '__main__':
    from rpgram.constants.test import DRUID_CHARACTER

    skill = PoisonousSapSkill(DRUID_CHARACTER)
    print(skill)
    print(DRUID_CHARACTER.cs.physical_attack)
    print(skill.function(DRUID_CHARACTER))
    DRUID_CHARACTER.skill_tree.learn_skill(PoisonousSapSkill)

    skill = IgneousSapSkill(DRUID_CHARACTER)
    print(skill)
    print(DRUID_CHARACTER.cs.physical_attack)
    print(skill.function(DRUID_CHARACTER))
    DRUID_CHARACTER.skill_tree.learn_skill(IgneousSapSkill)

    skill = EscarchaSapSkill(DRUID_CHARACTER)
    print(skill)
    print(DRUID_CHARACTER.cs.physical_attack)
    print(skill.function(DRUID_CHARACTER))
    DRUID_CHARACTER.skill_tree.learn_skill(EscarchaSapSkill)

    skill = SapiousCubeSkill(DRUID_CHARACTER)
    print(skill)
    print(DRUID_CHARACTER.cs.physical_attack)
    print(DRUID_CHARACTER.to_attack(
        defender_char=DRUID_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    DRUID_CHARACTER.skill_tree.learn_skill(SapiousCubeSkill)
