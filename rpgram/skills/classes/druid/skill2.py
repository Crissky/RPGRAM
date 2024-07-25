
from typing import TYPE_CHECKING
from constant.text import (
    ALERT_SECTION_HEAD_ADD_STATUS
)
from rpgram.conditions.special_damage_skill import (
    SDVineThornySpaulderCondition
)
from rpgram.conditions.target_skill_buff import (
    VineArmorCondition,
    VineBucklerCondition,
    VineSpikedSpaulderCondition
)
from rpgram.constants.text import (
    MAGICAL_DEFENSE_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT,
    PHYSICAL_DEFENSE_EMOJI_TEXT,
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
from rpgram.enums.stats_combat import CombatStatsEnum
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


class VineWhipSkill(BaseSkill):
    NAME = DruidSkillEnum.VINE_WHIP.value
    DESCRIPTION = (
        f'Com um movimento rápido, germina instantaneamente um '
        f'*Chicote de Vinha* para atacar o oponente, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.PLANTY)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.DRUID.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 2
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.25,
        }
        damage_types = [DamageEnum.PLANTY]

        super().__init__(
            name=VineWhipSkill.NAME,
            description=VineWhipSkill.DESCRIPTION,
            rank=VineWhipSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=VineWhipSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class VineBucklerSkill(BaseSkill):
    NAME = DruidSkillEnum.VINE_BUCKLER.value
    DESCRIPTION = (
        f'Brota um *Broquel* feito de um emaranhado de *Vinhas* ou, '
        f'caso possua um escudo, o reveste com *Vinhas*, '
        f'aumentando a '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (100% + 10% x Rank x Nível) e a '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (50% + 5% x Rank x Nível).'
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
            name=VineBucklerSkill.NAME,
            description=VineBucklerSkill.DESCRIPTION,
            rank=VineBucklerSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=VineBucklerSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        power = char.cs.wisdom
        condition = VineBucklerCondition(power=power, level=level)
        report_list = char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* cria e equipa um *{self.name}*.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class VineSpikedSpaulderSkill(BaseSkill):
    NAME = DruidSkillEnum.VINE_SPIKED_SPAULDER.value
    DESCRIPTION = (
        f'Brolha uma *Espaldeira* constituida de um entrançado de '
        f'*Vinhas Espinhosas* que aumenta o '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (200% + 10% x Rank x Nível) e a '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (100% + 5% x Rank x Nível). '
        f'Além disso, adiciona dano de '
        f'*{get_damage_emoji_text(DamageEnum.PIERCING)}* '
        f'baseado no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.DRUID.value,
        'skill_list': [VineBucklerSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 3
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=VineSpikedSpaulderSkill.NAME,
            description=VineSpikedSpaulderSkill.DESCRIPTION,
            rank=VineSpikedSpaulderSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=VineSpikedSpaulderSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        power = char.cs.wisdom
        sd_power = char.cs.physical_attack
        condition = VineSpikedSpaulderCondition(power=power, level=level)
        sd_condition = SDVineThornySpaulderCondition(
            power=sd_power,
            level=level
        )
        report_list = char.status.set_conditions(condition)
        sd_report_list = char.status.set_conditions(sd_condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list + sd_report_list]
        )
        report = {
            'text': (
                f'*{player_name}* cria e equipa uma *{self.name}*.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class VineArmorSkill(BaseSkill):
    NAME = DruidSkillEnum.VINE_ARMOR.value
    DESCRIPTION = (
        f'Se reveste com um entrelaçado de *Vinhas* '
        f'que aumenta a '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (300% + 10% x Rank x Nível) e a '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (150% + 5% x Rank x Nível).'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.DRUID.value,
        'skill_list': [VineBucklerSkill.NAME, VineSpikedSpaulderSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 4
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=VineArmorSkill.NAME,
            description=VineArmorSkill.DESCRIPTION,
            rank=VineArmorSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=VineArmorSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        power = char.cs.wisdom
        condition = VineArmorCondition(power=power, level=level)
        report_list = char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* cria e equipa uma *{self.name}*.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


if __name__ == '__main__':
    from rpgram.constants.test import DRUID_CHARACTER

    skill = VineWhipSkill(DRUID_CHARACTER)
    print(skill)
    print(DRUID_CHARACTER.cs.physical_attack)
    print(DRUID_CHARACTER.to_attack(
        defender_char=DRUID_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    DRUID_CHARACTER.skill_tree.learn_skill(VineWhipSkill)

    skill = VineBucklerSkill(DRUID_CHARACTER)
    print(skill)
    print(DRUID_CHARACTER.cs.wisdom)
    print(DRUID_CHARACTER.cs.magical_defense,
          DRUID_CHARACTER.cs.physical_defense)
    print(skill.function())
    print(DRUID_CHARACTER.cs.magical_defense,
          DRUID_CHARACTER.cs.physical_defense)
    DRUID_CHARACTER.skill_tree.learn_skill(VineBucklerSkill)

    skill = VineSpikedSpaulderSkill(DRUID_CHARACTER)
    print(skill)
    print(DRUID_CHARACTER.cs.wisdom)
    print(DRUID_CHARACTER.cs.physical_attack,
          DRUID_CHARACTER.cs.magical_defense)
    print(skill.function())
    print(DRUID_CHARACTER.cs.physical_attack,
          DRUID_CHARACTER.cs.magical_defense)
    DRUID_CHARACTER.skill_tree.learn_skill(VineSpikedSpaulderSkill)

    skill = VineArmorSkill(DRUID_CHARACTER)
    print(skill)
    print(DRUID_CHARACTER.cs.wisdom)
    print(DRUID_CHARACTER.cs.magical_defense,
          DRUID_CHARACTER.cs.physical_defense)
    print(skill.function())
    print(DRUID_CHARACTER.cs.magical_defense,
          DRUID_CHARACTER.cs.physical_defense)
    DRUID_CHARACTER.skill_tree.learn_skill(VineArmorSkill)
