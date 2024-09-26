
from typing import TYPE_CHECKING
from constant.text import (
    ALERT_SECTION_HEAD_ADD_STATUS
)
from rpgram.conditions.special_damage_skill import (
    SDThornySpaulderCondition
)
from rpgram.conditions.target_skill_buff import (
    OakArmorCondition,
    VineBucklerCondition,
    SilkFlossSpaulderCondition
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


class VineWhipSkill(BaseSkill):
    NAME = DruidSkillEnum.VINE_WHIP.value
    DESCRIPTION = (
        f'Com um movimento rápido, germina instantaneamente sua arma em um '
        f'*Chicote de Vinha* para atacar o oponente, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.PLANTY)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.SLASHING)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.DRUID.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.25,
        }
        damage_types = [DamageEnum.PLANTY, DamageEnum.SLASHING]

        super().__init__(
            name=VineWhipSkill.NAME,
            description=VineWhipSkill.DESCRIPTION,
            rank=VineWhipSkill.RANK,
            level=level,
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


class SilkFlossSwordSkill(BaseSkill):
    NAME = DruidSkillEnum.SILK_FLOSS_SWORD.value
    DESCRIPTION = (
        f'Com maestria, desabrocha prontamente sua arma em uma '
        f'*Espada Espiheta* e ataca o oponente, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.PLANTY)}*, de '
        f'*{get_damage_emoji_text(DamageEnum.PIERCING)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.SLASHING)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (150% + 5% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.DRUID.value,
        'skill_list': [VineWhipSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.50,
        }
        damage_types = [
            DamageEnum.PLANTY,
            DamageEnum.PIERCING,
            DamageEnum.SLASHING
        ]

        super().__init__(
            name=SilkFlossSwordSkill.NAME,
            description=SilkFlossSwordSkill.DESCRIPTION,
            rank=SilkFlossSwordSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=SilkFlossSwordSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class OakWarhammerSkill(BaseSkill):
    NAME = DruidSkillEnum.OAK_WARHAMMER.value
    DESCRIPTION = (
        f'Desabrolha sua arma em um gigantesco '
        f'*{DruidSkillEnum.OAK_WARHAMMER.value}* para atacar o oponente, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.PLANTY)}*, de '
        f'*{get_damage_emoji_text(DamageEnum.GROUND)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.BLUDGEONING)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (175% + 5% x Rank x Nível).'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.DRUID.value,
        'skill_list': [VineWhipSkill.NAME, SilkFlossSwordSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.75,
        }
        damage_types = [
            DamageEnum.PLANTY,
            DamageEnum.GROUND,
            DamageEnum.BLUDGEONING,
        ]

        super().__init__(
            name=OakWarhammerSkill.NAME,
            description=OakWarhammerSkill.DESCRIPTION,
            rank=OakWarhammerSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=OakWarhammerSkill.REQUIREMENTS,
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
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=VineBucklerSkill.NAME,
            description=VineBucklerSkill.DESCRIPTION,
            rank=VineBucklerSkill.RANK,
            level=level,
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
                f'*{player_name}* cria e equipa um *{self.name}*, '
                f'aumentando a '
                f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* '
                f'em {condition.bonus_magical_defense} pontos e a '
                f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* '
                f'em {condition.bonus_physical_defense} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class SilkFlossSpaulderSkill(BaseSkill):
    NAME = DruidSkillEnum.SILK_FLOSS_SPAULDER.value
    DESCRIPTION = (
        f'Brolha uma *Espaldeira* constituida de um entrançado de '
        f'*Madeira Espinhosa* que aumenta o '
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
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=SilkFlossSpaulderSkill.NAME,
            description=SilkFlossSpaulderSkill.DESCRIPTION,
            rank=SilkFlossSpaulderSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=SilkFlossSpaulderSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        power = char.cs.wisdom
        sd_power = char.cs.physical_attack
        condition = SilkFlossSpaulderCondition(power=power, level=level)
        sd_condition = SDThornySpaulderCondition(
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
                f'*{player_name}* cria e equipa uma *{self.name}*, '
                f'aumentando o '
                f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* '
                f'em {condition.bonus_physical_attack} pontos e a '
                f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* '
                f'em {condition.bonus_magical_defense} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class OakArmorSkill(BaseSkill):
    NAME = DruidSkillEnum.OAK_ARMOR.value
    DESCRIPTION = (
        f'Se reveste com um entrelaçado de *Placas de Carvalho* '
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
        'skill_list': [VineBucklerSkill.NAME, SilkFlossSpaulderSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=OakArmorSkill.NAME,
            description=OakArmorSkill.DESCRIPTION,
            rank=OakArmorSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=OakArmorSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        power = char.cs.wisdom
        condition = OakArmorCondition(power=power, level=level)
        report_list = char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* cria e equipa uma *{self.name}*, '
                f'aumentando a '
                f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* '
                f'em {condition.bonus_magical_defense} pontos e a '
                f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* '
                f'em {condition.bonus_physical_defense} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


SKILL_WAY_DESCRIPTION = {
    'name': 'Forja Verde',
    'description': (
        'A Forja Verde representa o domínio do Druida sobre a '
        'a vida e a matéria Verde da natureza, moldando-a para criar '
        'armas e armaduras imbuídas de vida. '
        'O Druida transforma a matéria prima da floresta em '
        'ferramentas poderosas, dando-lhe a capacidade de defender '
        'a natureza e seus aliados.'
    ),
    'skill_list': [
        VineWhipSkill,
        SilkFlossSwordSkill,
        OakWarhammerSkill,
        VineBucklerSkill,
        SilkFlossSpaulderSkill,
        OakArmorSkill,
    ]
}


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

    skill = SilkFlossSwordSkill(DRUID_CHARACTER)
    print(skill)
    print(DRUID_CHARACTER.cs.physical_attack)
    print(DRUID_CHARACTER.to_attack(
        defender_char=DRUID_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    DRUID_CHARACTER.skill_tree.learn_skill(SilkFlossSwordSkill)

    skill = OakWarhammerSkill(DRUID_CHARACTER)
    print(skill)
    print(DRUID_CHARACTER.cs.physical_attack)
    print(DRUID_CHARACTER.to_attack(
        defender_char=DRUID_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    DRUID_CHARACTER.skill_tree.learn_skill(OakWarhammerSkill)

    skill = VineBucklerSkill(DRUID_CHARACTER)
    print(skill)
    print(DRUID_CHARACTER.cs.wisdom)
    print(DRUID_CHARACTER.cs.magical_defense,
          DRUID_CHARACTER.cs.physical_defense)
    print(skill.function())
    print(DRUID_CHARACTER.cs.magical_defense,
          DRUID_CHARACTER.cs.physical_defense)
    DRUID_CHARACTER.skill_tree.learn_skill(VineBucklerSkill)

    skill = SilkFlossSpaulderSkill(DRUID_CHARACTER)
    print(skill)
    print(DRUID_CHARACTER.cs.wisdom)
    print(DRUID_CHARACTER.cs.physical_attack,
          DRUID_CHARACTER.cs.magical_defense)
    print(skill.function())
    print(DRUID_CHARACTER.cs.physical_attack,
          DRUID_CHARACTER.cs.magical_defense)
    DRUID_CHARACTER.skill_tree.learn_skill(SilkFlossSpaulderSkill)

    skill = OakArmorSkill(DRUID_CHARACTER)
    print(skill)
    print(DRUID_CHARACTER.cs.wisdom)
    print(DRUID_CHARACTER.cs.magical_defense,
          DRUID_CHARACTER.cs.physical_defense)
    print(skill.function())
    print(DRUID_CHARACTER.cs.magical_defense,
          DRUID_CHARACTER.cs.physical_defense)
    DRUID_CHARACTER.skill_tree.learn_skill(OakArmorSkill)
