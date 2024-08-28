from typing import TYPE_CHECKING

from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.special_damage_skill import (
    SDFellowPandinusCondition,
    SDFellowTurtleCondition,
    SDFellowWolfCondition,
    SDFellowYetiCondition
)
from rpgram.conditions.target_skill_buff import (
    ClairvoyantWolfCondition,
    FighterPandinusCondition,
    LookouterYetiCondition,
    ProtectorTurtleCondition
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
    ShamanSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class FighterPandinusSkill(BaseSkill):
    NAME = ShamanSkillEnum.FIGHTER_PANDINUS.value
    DESCRIPTION = (
        f'Convoca um companheiro *{ShamanSkillEnum.FIGHTER_PANDINUS.value}* '
        f'que guarda o Xamã e o auxilia nos combates, '
        f'aumentando o '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* e o '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (100% + 10% x Rank x Nível). '
        f'Além disso, o *{ShamanSkillEnum.FELLOW_PANDINUS.value}* '
        f'ataca em conjunto com o *Xamã*, adicionando dano de '
        f'*{get_damage_emoji_text(DamageEnum.PIERCING)}*, de '
        f'*{get_damage_emoji_text(DamageEnum.ROCK)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.POISON)}* '
        f'baseado no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.SHAMAN.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=FighterPandinusSkill.NAME,
            description=FighterPandinusSkill.DESCRIPTION,
            rank=FighterPandinusSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=FighterPandinusSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        power = char.cs.wisdom
        sd_power = char.cs.magical_attack
        condition = FighterPandinusCondition(power=power, level=level)
        sd_condition = SDFellowPandinusCondition(power=sd_power, level=level)
        report_list = char.status.set_conditions(condition)
        sd_report_list = char.status.set_conditions(sd_condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list + sd_report_list]
        )
        report = {
            'text': (
                f'*{player_name}* convoca um companheiro *{self.name}* '
                f'para batalhar ao seu lado, '
                f'aumentando o '
                f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* em '
                f'{condition.bonus_physical_attack} pontos e o '
                f'*{PRECISION_ATTACK_EMOJI_TEXT}* em '
                f'{condition.bonus_precision_attack} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class ProtectorTurtleSkill(BaseSkill):
    NAME = ShamanSkillEnum.PROTECTOR_TURTLE.value
    DESCRIPTION = (
        f'Convoca uma companheira *{ShamanSkillEnum.PROTECTOR_TURTLE.value}* '
        f'que o defende e o auxilia nos combates, '
        f'aumentando a '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* e a '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (100% + 10% x Rank x Nível). '
        f'Além disso, a *{ShamanSkillEnum.FELLOW_TURTLE.value}* '
        f'ataca em conjunto com o *Xamã*, adicionando dano de '
        f'*{get_damage_emoji_text(DamageEnum.BLUDGEONING)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.WATER)}* '
        f'baseado no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.SHAMAN.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=ProtectorTurtleSkill.NAME,
            description=ProtectorTurtleSkill.DESCRIPTION,
            rank=ProtectorTurtleSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=ProtectorTurtleSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        power = char.cs.wisdom
        sd_power = char.cs.magical_attack
        condition = ProtectorTurtleCondition(power=power, level=level)
        sd_condition = SDFellowTurtleCondition(power=sd_power, level=level)
        report_list = char.status.set_conditions(condition)
        sd_report_list = char.status.set_conditions(sd_condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list + sd_report_list]
        )
        report = {
            'text': (
                f'*{player_name}* convoca um companheiro *{self.name}* '
                f'para o proteger e batalhar ao seu lado, '
                f'aumentando a '
                f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* em '
                f'{condition.bonus_physical_defense} pontos e a '
                f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* em '
                f'{condition.bonus_magical_defense} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class ClairvoyantWolfSkill(BaseSkill):
    NAME = ShamanSkillEnum.CLAIRVOYANT_WOLF.value
    DESCRIPTION = (
        f'Convoca um companheiro *{ShamanSkillEnum.CLAIRVOYANT_WOLF.value}* '
        f'que fareja o futuro e o auxilia nos combates, '
        f'aumentando o '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* e a '
        f'*{EVASION_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (100% + 10% x Rank x Nível). '
        f'Além disso, o *{ShamanSkillEnum.FELLOW_WOLF.value}* '
        f'ataca em conjunto com o *Xamã*, adicionando dano de '
        f'*{get_damage_emoji_text(DamageEnum.SLASHING)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.LIGHT)}* '
        f'baseado no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.SHAMAN.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=ClairvoyantWolfSkill.NAME,
            description=ClairvoyantWolfSkill.DESCRIPTION,
            rank=ClairvoyantWolfSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=ClairvoyantWolfSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        power = char.cs.wisdom
        sd_power = char.cs.magical_attack
        condition = ClairvoyantWolfCondition(power=power, level=level)
        sd_condition = SDFellowWolfCondition(power=sd_power, level=level)
        report_list = char.status.set_conditions(condition)
        sd_report_list = char.status.set_conditions(sd_condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list + sd_report_list]
        )
        report = {
            'text': (
                f'*{player_name}* convoca um companheiro *{self.name}* '
                f'para fareja o futuro e batalhar ao seu lado, '
                f'aumentando o '
                f'*{MAGICAL_ATTACK_EMOJI_TEXT}* em '
                f'{condition.bonus_magical_attack} pontos e a '
                f'*{EVASION_EMOJI_TEXT}* em '
                f'{condition.bonus_evasion} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class LookouterYetiSkill(BaseSkill):
    NAME = ShamanSkillEnum.LOOKOUTER_YETI.value
    DESCRIPTION = (
        f'Convoca um companheiro *{ShamanSkillEnum.LOOKOUTER_YETI.value}* '
        f'que o observa e o auxilia nos combates, '
        f'aumentando o '
        f'*{HIT_POINT_FULL_EMOJI_TEXT}* e o '
        f'*{HIT_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (100% + 10% x Rank x Nível). '
        f'Além disso, o *{ShamanSkillEnum.FELLOW_YETI.value}* '
        f'ataca em conjunto com o *Xamã*, adicionando dano '
        f'*{get_damage_emoji_text(DamageEnum.ROAR)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.COLD)}* '
        f'baseado no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.SHAMAN.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=LookouterYetiSkill.NAME,
            description=LookouterYetiSkill.DESCRIPTION,
            rank=LookouterYetiSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=LookouterYetiSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        power = char.cs.wisdom
        sd_power = char.cs.magical_attack
        condition = LookouterYetiCondition(power=power, level=level)
        sd_condition = SDFellowYetiCondition(power=sd_power, level=level)
        report_list = char.status.set_conditions(condition)
        sd_report_list = char.status.set_conditions(sd_condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list + sd_report_list]
        )
        report = {
            'text': (
                f'*{player_name}* convoca um companheiro *{self.name}* '
                f'para observar e batalhar ao seu lado, '
                f'aumentando o '
                f'*{HIT_POINT_FULL_EMOJI_TEXT}* em '
                f'{condition.bonus_hit_points} pontos e o '
                f'*{HIT_EMOJI_TEXT}* em '
                f'{condition.bonus_hit} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


SKILL_WAY_DESCRIPTION = {
    'name': 'Aliança Selvagem',
    'description': (
        'A Aliança Selvagem representa a conexão intrínseca do Xamã '
        'com os animais da floresta. '
        'Através desta aliança, o Xamã cultiva um vínculo profundo com a '
        'natureza, tornando-o capaz de convocar criaturas selvagens para '
        'auxiliá-lo em suas jornadas.'
    ),
    'skill_list': [
        FighterPandinusSkill,
        ProtectorTurtleSkill,
        ClairvoyantWolfSkill,
        LookouterYetiSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import SHAMAN_CHARACTER

    skill = FighterPandinusSkill(SHAMAN_CHARACTER)
    print(skill)
    print(SHAMAN_CHARACTER.cs.wisdom)
    print(SHAMAN_CHARACTER.cs.physical_attack,
          SHAMAN_CHARACTER.cs.precision_attack)
    print(skill.function())
    print(SHAMAN_CHARACTER.cs.physical_attack,
          SHAMAN_CHARACTER.cs.precision_attack)
    SHAMAN_CHARACTER.skill_tree.learn_skill(FighterPandinusSkill)

    skill = ProtectorTurtleSkill(SHAMAN_CHARACTER)
    print(skill)
    print(SHAMAN_CHARACTER.cs.wisdom)
    print(SHAMAN_CHARACTER.cs.physical_defense,
          SHAMAN_CHARACTER.cs.magical_defense)
    print(skill.function())
    print(SHAMAN_CHARACTER.cs.physical_defense,
          SHAMAN_CHARACTER.cs.magical_defense)
    SHAMAN_CHARACTER.skill_tree.learn_skill(ProtectorTurtleSkill)

    skill = ClairvoyantWolfSkill(SHAMAN_CHARACTER)
    print(skill)
    print(SHAMAN_CHARACTER.cs.wisdom)
    print(SHAMAN_CHARACTER.cs.magical_attack,
          SHAMAN_CHARACTER.cs.evasion)
    print(skill.function())
    print(SHAMAN_CHARACTER.cs.magical_attack,
          SHAMAN_CHARACTER.cs.evasion)
    SHAMAN_CHARACTER.skill_tree.learn_skill(ClairvoyantWolfSkill)

    skill = LookouterYetiSkill(SHAMAN_CHARACTER)
    print(skill)
    print(SHAMAN_CHARACTER.cs.wisdom)
    print(SHAMAN_CHARACTER.cs.hit_points,
          SHAMAN_CHARACTER.cs.hit)
    print(skill.function())
    print(SHAMAN_CHARACTER.cs.hit_points,
          SHAMAN_CHARACTER.cs.hit)
    SHAMAN_CHARACTER.skill_tree.learn_skill(LookouterYetiSkill)

    # print('\n'.join([
    #     report['text']
    #     for report in SHAMAN_CHARACTER.activate_status()
    # ]))
