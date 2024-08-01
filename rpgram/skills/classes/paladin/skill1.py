
from typing import TYPE_CHECKING
from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.special_damage_skill import (
    SDBlueDjinnBalmCondition,
    SDGreenDragonBalmCondition,
    SDRedPhoenixBalmCondition,
    SDSacredBalmCondition
)
from rpgram.conditions.target_skill_buff import (
    CourtesanAnointingCondition,
    KnightAnointingCondition,
    LordAnointingCondition,
    MaidenAnointingCondition,
    SquireAnointingCondition,
    WarriorAnointingCondition
)
from rpgram.constants.text import (
    HIT_POINT_FULL_EMOJI_TEXT,
    MAGICAL_DEFENSE_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT,
    PHYSICAL_DEFENSE_EMOJI_TEXT,
    PRECISION_ATTACK_EMOJI_TEXT,
    WISDOM_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.skill import (
    PaladinSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class SacredBalmSkill(BaseSkill):
    NAME = PaladinSkillEnum.SACRED_BALM.value
    DESCRIPTION = (
        f'Um toque suave no alvo com a ponta dos dedos, sagramenta-o com o '
        f'*{PaladinSkillEnum.SACRED_BALM.value}*, '
        f'concedendo dano '
        f'*{get_damage_emoji_text(DamageEnum.BLESSING)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.LIGHT)}* '
        f'baseado na '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.PALADIN.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=SacredBalmSkill.NAME,
            description=SacredBalmSkill.DESCRIPTION,
            rank=SacredBalmSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=SacredBalmSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        player_name = self.char.player_name
        target_name = char.player_name
        if char.is_alive:
            target_name = (
                'si mesmo'
                if target_name == player_name
                else target_name
            )
            power = self.char.cs.magical_defense
            level = self.level_rank
            condition = SDSacredBalmCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{player_name}* toca as mãos de *{target_name}* '
                    f'com a *{self.name}*, concedendo dano '
                    f'*{get_damage_emoji_text(DamageEnum.BLESSING)}* e de '
                    f'*{get_damage_emoji_text(DamageEnum.LIGHT)}*.\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


class GreenDragonBalmSkill(BaseSkill):
    NAME = PaladinSkillEnum.GREENDRAGON_BALM.value
    DESCRIPTION = (
        f'Um toque suave no alvo com a ponta dos dedos, sagramenta-o com o '
        f'*{PaladinSkillEnum.GREENDRAGON_BALM.value}*, '
        f'concedendo dano '
        f'*{get_damage_emoji_text(DamageEnum.BLESSING)}*, de '
        f'*{get_damage_emoji_text(DamageEnum.POISON)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.ACID)}* '
        f'baseado na '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* (200% + 10% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.PALADIN.value,
        'skill_list': [SacredBalmSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=GreenDragonBalmSkill.NAME,
            description=GreenDragonBalmSkill.DESCRIPTION,
            rank=GreenDragonBalmSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=GreenDragonBalmSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        player_name = self.char.player_name
        target_name = char.player_name
        if char.is_alive:
            target_name = (
                'si mesmo'
                if target_name == player_name
                else target_name
            )
            power = self.char.cs.magical_defense
            level = self.level_rank
            condition = SDGreenDragonBalmCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{player_name}* toca as mãos de *{target_name}* '
                    f'com a *{self.name}*, concedendo dano '
                    f'*{get_damage_emoji_text(DamageEnum.BLESSING)}*, de '
                    f'*{get_damage_emoji_text(DamageEnum.POISON)}* e de '
                    f'*{get_damage_emoji_text(DamageEnum.ACID)}*.\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


class RedPhoenixBalmSkill(BaseSkill):
    NAME = PaladinSkillEnum.REDPHOENIX_BALM.value
    DESCRIPTION = (
        f'Um toque suave no alvo com a ponta dos dedos, sagramenta-o com o '
        f'*{PaladinSkillEnum.REDPHOENIX_BALM.value}*, '
        f'concedendo dano '
        f'*{get_damage_emoji_text(DamageEnum.BLESSING)}*, de '
        f'*{get_damage_emoji_text(DamageEnum.FIRE)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.WIND)}* '
        f'baseado na '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* (200% + 10% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.PALADIN.value,
        'skill_list': [SacredBalmSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=RedPhoenixBalmSkill.NAME,
            description=RedPhoenixBalmSkill.DESCRIPTION,
            rank=RedPhoenixBalmSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=RedPhoenixBalmSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        player_name = self.char.player_name
        target_name = char.player_name
        if char.is_alive:
            target_name = (
                'si mesmo'
                if target_name == player_name
                else target_name
            )
            power = self.char.cs.magical_defense
            level = self.level_rank
            condition = SDRedPhoenixBalmCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{player_name}* toca as mãos de *{target_name}* '
                    f'com a *{self.name}*, concedendo dano '
                    f'*{get_damage_emoji_text(DamageEnum.BLESSING)}*, de '
                    f'*{get_damage_emoji_text(DamageEnum.FIRE)}* e de '
                    f'*{get_damage_emoji_text(DamageEnum.WIND)}*.\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


class BlueDjinnBalmSkill(BaseSkill):
    NAME = PaladinSkillEnum.BLUEDJINN_BALM.value
    DESCRIPTION = (
        f'Um toque suave no alvo com a ponta dos dedos, sagramenta-o com o '
        f'*{PaladinSkillEnum.BLUEDJINN_BALM.value}*, '
        f'concedendo dano '
        f'*{get_damage_emoji_text(DamageEnum.BLESSING)}*, '
        f'*{get_damage_emoji_text(DamageEnum.MAGIC)}*, de '
        f'*{get_damage_emoji_text(DamageEnum.COLD)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.WATER)}* '
        f'baseado na '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* (200% + 10% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.PALADIN.value,
        'skill_list': [SacredBalmSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=BlueDjinnBalmSkill.NAME,
            description=BlueDjinnBalmSkill.DESCRIPTION,
            rank=BlueDjinnBalmSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=BlueDjinnBalmSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        player_name = self.char.player_name
        target_name = char.player_name
        if char.is_alive:
            target_name = (
                'si mesmo'
                if target_name == player_name
                else target_name
            )
            power = self.char.cs.magical_defense
            level = self.level_rank
            condition = SDBlueDjinnBalmCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{player_name}* toca as mãos de *{target_name}* '
                    f'com a *{self.name}*, concedendo dano '
                    f'*{get_damage_emoji_text(DamageEnum.BLESSING)}*, '
                    f'*{get_damage_emoji_text(DamageEnum.MAGIC)}*, de '
                    f'*{get_damage_emoji_text(DamageEnum.COLD)}* e de '
                    f'*{get_damage_emoji_text(DamageEnum.WATER)}*.\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


class SquireAnointingSkill(BaseSkill):
    NAME = PaladinSkillEnum.SQUIRE_ANOINTING.value
    DESCRIPTION = (
        f'Unge a armadura do alvo com a '
        f'*{PaladinSkillEnum.SQUIRE_ANOINTING.value}* que '
        f'aumenta a *{PHYSICAL_DEFENSE_EMOJI_TEXT}* e o '
        f'*{HIT_POINT_FULL_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.PALADIN.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=SquireAnointingSkill.NAME,
            description=SquireAnointingSkill.DESCRIPTION,
            rank=SquireAnointingSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=SquireAnointingSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        target_name = char.player_name
        if char.is_alive:
            level = self.level_rank
            power = self.char.cs.wisdom
            condition = SquireAnointingCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{target_name}* é ungido com a '
                    f'*{self.name}* '
                    f'que aumenta a '
                    f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* e o '
                    f'*{HIT_POINT_FULL_EMOJI_TEXT}*.\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


class WarriorAnointingSkill(BaseSkill):
    NAME = PaladinSkillEnum.WARRIOR_ANOINTING.value
    DESCRIPTION = (
        f'Unge a arma do alvo com a '
        f'*{PaladinSkillEnum.WARRIOR_ANOINTING.value}* que '
        f'aumenta o '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}*, o '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* e o '
        f'*{HIT_POINT_FULL_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.PALADIN.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=WarriorAnointingSkill.NAME,
            description=WarriorAnointingSkill.DESCRIPTION,
            rank=WarriorAnointingSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=WarriorAnointingSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        target_name = char.player_name
        if char.is_alive:
            level = self.level_rank
            power = self.char.cs.wisdom
            condition = WarriorAnointingCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{target_name}* é ungido com a '
                    f'*{self.name}* '
                    f'que aumenta o '
                    f'*{PHYSICAL_ATTACK_EMOJI_TEXT}*, o '
                    f'*{PRECISION_ATTACK_EMOJI_TEXT}* e o '
                    f'*{HIT_POINT_FULL_EMOJI_TEXT}*.\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


class MaidenAnointingSkill(BaseSkill):
    NAME = PaladinSkillEnum.MAIDEN_ANOINTING.value
    DESCRIPTION = (
        f'Unge as mãos do alvo com a '
        f'*{PaladinSkillEnum.MAIDEN_ANOINTING.value}* que '
        f'aumenta a '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* e o '
        f'*{HIT_POINT_FULL_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.PALADIN.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=MaidenAnointingSkill.NAME,
            description=MaidenAnointingSkill.DESCRIPTION,
            rank=MaidenAnointingSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=MaidenAnointingSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        target_name = char.player_name
        if char.is_alive:
            level = self.level_rank
            power = self.char.cs.wisdom
            condition = MaidenAnointingCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{target_name}* é ungido com a '
                    f'*{self.name}* '
                    f'que aumenta a '
                    f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* e o '
                    f'*{HIT_POINT_FULL_EMOJI_TEXT}*.\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


class KnightAnointingSkill(BaseSkill):
    NAME = PaladinSkillEnum.KNIGHT_ANOINTING.value
    DESCRIPTION = (
        f'Unge os ombros do alvo com a '
        f'*{PaladinSkillEnum.KNIGHT_ANOINTING.value}* que '
        f'aumenta o '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}*, o '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}*, a '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* e o '
        f'*{HIT_POINT_FULL_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (200% + 10% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.PALADIN.value,
        'skill_list': [SquireAnointingSkill.NAME, WarriorAnointingSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=KnightAnointingSkill.NAME,
            description=KnightAnointingSkill.DESCRIPTION,
            rank=KnightAnointingSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=KnightAnointingSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        target_name = char.player_name
        if char.is_alive:
            level = self.level_rank
            power = self.char.cs.wisdom
            condition = KnightAnointingCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{target_name}* é ungido com a '
                    f'*{self.name}* '
                    f'que aumenta o '
                    f'*{PHYSICAL_ATTACK_EMOJI_TEXT}*, o '
                    f'*{PRECISION_ATTACK_EMOJI_TEXT}*, a '
                    f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* e o '
                    f'*{HIT_POINT_FULL_EMOJI_TEXT}*.\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


class CourtesanAnointingSkill(BaseSkill):
    NAME = PaladinSkillEnum.COURTESAN_ANOINTING.value
    DESCRIPTION = (
        f'Unge os lábios do alvo com a '
        f'*{PaladinSkillEnum.COURTESAN_ANOINTING.value}* que '
        f'aumenta a '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}*, a '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* e o '
        f'*{HIT_POINT_FULL_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (200% + 10% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.PALADIN.value,
        'skill_list': [SquireAnointingSkill.NAME, MaidenAnointingSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=CourtesanAnointingSkill.NAME,
            description=CourtesanAnointingSkill.DESCRIPTION,
            rank=CourtesanAnointingSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=CourtesanAnointingSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        target_name = char.player_name
        if char.is_alive:
            level = self.level_rank
            power = self.char.cs.wisdom
            condition = CourtesanAnointingCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{target_name}* é ungido com a '
                    f'*{self.name}* '
                    f'que aumenta a '
                    f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}*, a '
                    f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* e o '
                    f'*{HIT_POINT_FULL_EMOJI_TEXT}*.\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


class LordAnointingSkill(BaseSkill):
    NAME = PaladinSkillEnum.LORD_ANOINTING.value
    DESCRIPTION = (
        f'Unge o coração do alvo com a '
        f'*{PaladinSkillEnum.LORD_ANOINTING.value}* que '
        f'aumenta o '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}*, o '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}*, a '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* e o '
        f'*{HIT_POINT_FULL_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (200% + 10% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.PALADIN.value,
        'skill_list': [WarriorAnointingSkill.NAME, MaidenAnointingSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=LordAnointingSkill.NAME,
            description=LordAnointingSkill.DESCRIPTION,
            rank=LordAnointingSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=LordAnointingSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        target_name = char.player_name
        if char.is_alive:
            level = self.level_rank
            power = self.char.cs.wisdom
            condition = LordAnointingCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{target_name}* é ungido com a '
                    f'*{self.name}* '
                    f'que aumenta o '
                    f'*{PHYSICAL_ATTACK_EMOJI_TEXT}*, o '
                    f'*{PRECISION_ATTACK_EMOJI_TEXT}*, a '
                    f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* e o '
                    f'*{HIT_POINT_FULL_EMOJI_TEXT}*.\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


SKILL_WAY_DESCRIPTION = {
    'name': 'Unção de Combate',
    'description': (
        'A Unção de Combate faz o Paladino canalizar a sua fé, '
        'por meio de uma profunda conexão com as forças divinas, '
        'para aprimorar suas habilidades de combate e '
        'de seus companheiros de batalha. '
        'Essa conexão lhe concede a capacidade de imbuir suas armas e '
        'corpo com poder sagrado e sua devoção lhe concede '
        'força sobre-humana e resistência, '
        'tornando-o uma potestade imparável no campo de batalha.'
    ),
    'skill_list': [
        SacredBalmSkill,
        GreenDragonBalmSkill,
        RedPhoenixBalmSkill,
        BlueDjinnBalmSkill,
        SquireAnointingSkill,
        WarriorAnointingSkill,
        MaidenAnointingSkill,
        KnightAnointingSkill,
        CourtesanAnointingSkill,
        LordAnointingSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import PALADIN_CHARACTER

    skill = SacredBalmSkill(PALADIN_CHARACTER)
    print(skill)
    print(skill.function(PALADIN_CHARACTER))
    PALADIN_CHARACTER.skill_tree.learn_skill(SacredBalmSkill)

    skill = GreenDragonBalmSkill(PALADIN_CHARACTER)
    print(skill)
    print(skill.function(PALADIN_CHARACTER))
    PALADIN_CHARACTER.skill_tree.learn_skill(GreenDragonBalmSkill)

    skill = RedPhoenixBalmSkill(PALADIN_CHARACTER)
    print(skill)
    print(skill.function(PALADIN_CHARACTER))
    PALADIN_CHARACTER.skill_tree.learn_skill(RedPhoenixBalmSkill)

    skill = BlueDjinnBalmSkill(PALADIN_CHARACTER)
    print(skill)
    print(skill.function(PALADIN_CHARACTER))
    PALADIN_CHARACTER.skill_tree.learn_skill(BlueDjinnBalmSkill)

    skill = SquireAnointingSkill(PALADIN_CHARACTER)
    print(skill)
    print(skill.function(PALADIN_CHARACTER))
    PALADIN_CHARACTER.skill_tree.learn_skill(SquireAnointingSkill)

    skill = WarriorAnointingSkill(PALADIN_CHARACTER)
    print(skill)
    print(skill.function(PALADIN_CHARACTER))
    PALADIN_CHARACTER.skill_tree.learn_skill(WarriorAnointingSkill)

    skill = MaidenAnointingSkill(PALADIN_CHARACTER)
    print(skill)
    print(skill.function(PALADIN_CHARACTER))
    PALADIN_CHARACTER.skill_tree.learn_skill(MaidenAnointingSkill)

    skill = KnightAnointingSkill(PALADIN_CHARACTER)
    print(skill)
    print(skill.function(PALADIN_CHARACTER))
    PALADIN_CHARACTER.skill_tree.learn_skill(KnightAnointingSkill)

    skill = CourtesanAnointingSkill(PALADIN_CHARACTER)
    print(skill)
    print(skill.function(PALADIN_CHARACTER))
    PALADIN_CHARACTER.skill_tree.learn_skill(CourtesanAnointingSkill)

    skill = LordAnointingSkill(PALADIN_CHARACTER)
    print(skill)
    print(skill.function(PALADIN_CHARACTER))
    PALADIN_CHARACTER.skill_tree.learn_skill(LordAnointingSkill)

    print('\n'.join([
        report['text']
        for report in PALADIN_CHARACTER.activate_status()
    ]))
