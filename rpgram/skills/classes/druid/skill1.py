
from typing import TYPE_CHECKING
from constant.text import (
    ALERT_SECTION_HEAD_ADD_STATUS
)
from rpgram.conditions.special_damage_skill import (
    SDFellowBearCondition,
    SDFellowFalconCondition,
    SDFellowOwlCondition,
    SDFellowTigerCondition
)
from rpgram.conditions.target_skill_buff import (
    BodyguardBearCondition,
    HunterTigerCondition,
    RangerFalconCondition,
    WatcherOwlCondition
)
from rpgram.constants.text import (
    EVASION_EMOJI_TEXT,
    HIT_EMOJI_TEXT,
    HIT_POINT_FULL_EMOJI_TEXT,
    MAGICAL_ATTACK_EMOJI_TEXT,
    MAGICAL_DEFENSE_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT,
    PHYSICAL_DEFENSE_EMOJI_TEXT,
    PRECISION_ATTACK_EMOJI_TEXT,
    WISDOM_EMOJI_TEXT
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


class RangerFalconSkill(BaseSkill):
    NAME = DruidSkillEnum.RANGER_FALCON.value
    DESCRIPTION = (
        f'Convoca um companheiro *{DruidSkillEnum.RANGER_FALCON.value}* '
        f'que ronda as proximidades e o auxilia nos combates, '
        f'aumentando o '
        f'*{HIT_EMOJI_TEXT}* e a *{EVASION_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (100% + 10% x Rank x Nível). '
        f'Além disso, o *{DruidSkillEnum.FELLOW_FALCON.value}* '
        f'ataca em conjunto com o *Druida*, adicionando dano de '
        f'*{get_damage_emoji_text(DamageEnum.PIERCING)}* e de '
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
            name=RangerFalconSkill.NAME,
            description=RangerFalconSkill.DESCRIPTION,
            rank=RangerFalconSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=RangerFalconSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        power = self.char.cs.wisdom
        sd_power = self.char.cs.physical_attack
        condition = RangerFalconCondition(power=power, level=level)
        sd_condition = SDFellowFalconCondition(power=sd_power, level=level)
        report_list = char.status.set_conditions(condition)
        sd_report_list = char.status.set_conditions(sd_condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list + sd_report_list]
        )
        report = {
            'text': (
                f'*{player_name}* convoca um companheiro *{self.name}* '
                f'para vigiar e batalhar ao seu lado.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class GuardianBearSkill(BaseSkill):
    NAME = DruidSkillEnum.GUARDIAN_BEAR.value
    DESCRIPTION = (
        f'Convoca um companheiro *{DruidSkillEnum.GUARDIAN_BEAR.value}* '
        f'que o protege e o auxilia nos combates, '
        f'aumentando o '
        f'*{HIT_POINT_FULL_EMOJI_TEXT}* e a '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (100% + 10% x Rank x Nível). '
        f'Além disso, o *{DruidSkillEnum.FELLOW_BEAR.value}* '
        f'ataca em conjunto com o *Druida*, adicionando dano de '
        f'*{get_damage_emoji_text(DamageEnum.BLUDGEONING)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.GROUND)}* '
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
            name=GuardianBearSkill.NAME,
            description=GuardianBearSkill.DESCRIPTION,
            rank=GuardianBearSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=GuardianBearSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        power = self.char.cs.wisdom
        sd_power = self.char.cs.physical_attack
        condition = BodyguardBearCondition(power=power, level=level)
        sd_condition = SDFellowBearCondition(power=sd_power, level=level)
        report_list = char.status.set_conditions(condition)
        sd_report_list = char.status.set_conditions(sd_condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list + sd_report_list]
        )
        report = {
            'text': (
                f'*{player_name}* convoca um companheiro *{self.name}* '
                f'para o proteger e batalhar ao seu lado.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class HunterTigerSkill(BaseSkill):
    NAME = DruidSkillEnum.HUNTER_TIGER.value
    DESCRIPTION = (
        f'Convoca um companheiro *{DruidSkillEnum.HUNTER_TIGER.value}* '
        f'que persegue presas e o auxilia nos combates, '
        f'aumentando o '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* e o '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (100% + 10% x Rank x Nível). '
        f'Além disso, o *{DruidSkillEnum.FELLOW_TIGER.value}* '
        f'ataca em conjunto com o *Druida*, adicionando dano de '
        f'*{get_damage_emoji_text(DamageEnum.SLASHING)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.LIGHTNING)}* '
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
            name=HunterTigerSkill.NAME,
            description=HunterTigerSkill.DESCRIPTION,
            rank=HunterTigerSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=HunterTigerSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        power = self.char.cs.wisdom
        sd_power = self.char.cs.physical_attack
        condition = HunterTigerCondition(power=power, level=level)
        sd_condition = SDFellowTigerCondition(power=sd_power, level=level)
        report_list = char.status.set_conditions(condition)
        sd_report_list = char.status.set_conditions(sd_condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list + sd_report_list]
        )
        report = {
            'text': (
                f'*{player_name}* convoca um companheiro *{self.name}* '
                f'para caçar e batalhar ao seu lado.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class WatcherOwlSkill(BaseSkill):
    NAME = DruidSkillEnum.WATCHER_OWL.value
    DESCRIPTION = (
        f'Convoca um companheiro *{DruidSkillEnum.WATCHER_OWL.value}* '
        f'que observa o plano místico e o auxilia nos combates, '
        f'aumentando o '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* e a '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (100% + 10% x Rank x Nível). '
        f'Além disso, a *{DruidSkillEnum.FELLOW_OWL.value}* '
        f'ataca em conjunto com o *Druida*, adicionando dano '
        f'*{get_damage_emoji_text(DamageEnum.MAGIC)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.WIND)}* '
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
            name=WatcherOwlSkill.NAME,
            description=WatcherOwlSkill.DESCRIPTION,
            rank=WatcherOwlSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=WatcherOwlSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        power = self.char.cs.wisdom
        sd_power = self.char.cs.physical_attack
        condition = WatcherOwlCondition(power=power, level=level)
        sd_condition = SDFellowOwlCondition(power=sd_power, level=level)
        report_list = char.status.set_conditions(condition)
        sd_report_list = char.status.set_conditions(sd_condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list + sd_report_list]
        )
        report = {
            'text': (
                f'*{player_name}* convoca um companheiro *{self.name}* '
                f'para observar o plano místico e batalhar ao seu lado.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


if __name__ == '__main__':
    from rpgram.constants.test import DRUID_CHARACTER

    skill = RangerFalconSkill(DRUID_CHARACTER)
    print(skill)
    print(DRUID_CHARACTER.cs.wisdom)
    print(DRUID_CHARACTER.cs.hit, DRUID_CHARACTER.cs.evasion)
    print(skill.function(DRUID_CHARACTER))
    print(DRUID_CHARACTER.cs.hit, DRUID_CHARACTER.cs.evasion)
    DRUID_CHARACTER.skill_tree.learn_skill(RangerFalconSkill)

    skill = GuardianBearSkill(DRUID_CHARACTER)
    print(skill)
    print(DRUID_CHARACTER.cs.wisdom)
    print(DRUID_CHARACTER.cs.hit_points, DRUID_CHARACTER.cs.physical_defense)
    print(skill.function(DRUID_CHARACTER))
    print(DRUID_CHARACTER.cs.hit_points, DRUID_CHARACTER.cs.physical_defense)
    DRUID_CHARACTER.skill_tree.learn_skill(GuardianBearSkill)

    skill = HunterTigerSkill(DRUID_CHARACTER)
    print(skill)
    print(DRUID_CHARACTER.cs.wisdom)
    print(DRUID_CHARACTER.cs.physical_attack,
          DRUID_CHARACTER.cs.precision_attack)
    print(skill.function(DRUID_CHARACTER))
    print(DRUID_CHARACTER.cs.physical_attack,
          DRUID_CHARACTER.cs.precision_attack)
    DRUID_CHARACTER.skill_tree.learn_skill(HunterTigerSkill)

    skill = WatcherOwlSkill(DRUID_CHARACTER)
    print(skill)
    print(DRUID_CHARACTER.cs.wisdom)
    print(DRUID_CHARACTER.cs.magical_attack,
          DRUID_CHARACTER.cs.magical_defense)
    print(skill.function(DRUID_CHARACTER))
    print(DRUID_CHARACTER.cs.magical_attack,
          DRUID_CHARACTER.cs.magical_defense)
    DRUID_CHARACTER.skill_tree.learn_skill(WatcherOwlSkill)

    print('\n'.join(
        report['text']
        for report in DRUID_CHARACTER.activate_status()
    ))
