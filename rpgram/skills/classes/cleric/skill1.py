
from typing import TYPE_CHECKING
from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.target_skill_buff import (
    AnansisTrickeryCondition,
    ArtemissArrowCondition,
    CeridwensMagicPotionCondition,
    GraceOfThePantheonCondition,
    HecatesFlamesCondition,
    IdunnsAppleCondition,
    IsissVeilCondition,
    KratossWrathCondition,
    OgunsCloakCondition,
    UllrsFocusCondition,
    VidarsBraveryCondition
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
from rpgram.enums.skill import (
    ClericSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class IdunnsAppleSkill(BaseSkill):
    NAME = ClericSkillEnum.IDUNNÇÇÇS_APPLE.value
    DESCRIPTION = (
        f'Recita cânticos antigos para materializar '
        f'uma *Maçã Mágica* que irradia uma luz suave e '
        f'amplifica a vitalidade de um aliado, '
        f'aumentando seu *{HIT_POINT_FULL_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (200% + 20% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.CLERIC.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=IdunnsAppleSkill.NAME,
            description=IdunnsAppleSkill.DESCRIPTION,
            rank=IdunnsAppleSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=IdunnsAppleSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        target_name = char.player_name
        if char.is_alive:
            level = self.level_rank
            power = self.char.cs.wisdom
            condition = IdunnsAppleCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{target_name}* é agraciado com uma *Maçã Mágica* '
                    f'que aumenta o '
                    f'*{HIT_POINT_FULL_EMOJI_TEXT}* '
                    f'em {condition.bonus_hit_points} pontos.\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


class KratossWrathSkill(BaseSkill):
    NAME = ClericSkillEnum.KRATOSÇÇÇS_WRATH.value
    DESCRIPTION = (
        f'Como o peso de um corpo, faz decair sobre um aliado a '
        f'*Ira do Deus Grego da Guerra*, '
        f'aumentando seu *{PHYSICAL_ATTACK_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.CLERIC.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=KratossWrathSkill.NAME,
            description=KratossWrathSkill.DESCRIPTION,
            rank=KratossWrathSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=KratossWrathSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        target_name = char.player_name
        if char.is_alive:
            level = self.level_rank
            power = self.char.cs.wisdom
            condition = KratossWrathCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{target_name}* é agraciado com a '
                    f'*Ira do Deus Grego da Guerra* '
                    f'que aumenta o '
                    f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* '
                    f'em {condition.bonus_physical_attack} pontos.\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


class UllrsFocusSkill(BaseSkill):
    NAME = ClericSkillEnum.ULLRÇÇÇS_FOCUS.value
    DESCRIPTION = (
        f'*Ullr* limpa a mente de um aliado, fazendo-o perceber '
        f'cada ponto vulnerável na defesa do oponente, '
        f'aumentando o *{PRECISION_ATTACK_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.CLERIC.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=UllrsFocusSkill.NAME,
            description=UllrsFocusSkill.DESCRIPTION,
            rank=UllrsFocusSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=UllrsFocusSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        target_name = char.player_name
        if char.is_alive:
            level = self.level_rank
            power = self.char.cs.wisdom
            condition = UllrsFocusCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{target_name}* é agraciado com o '
                    f'*Foco de Ullr* '
                    f'que aumenta o '
                    f'*{PRECISION_ATTACK_EMOJI_TEXT}* '
                    f'em {condition.bonus_precision_attack} pontos.\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


class HecatesFlamesSkill(BaseSkill):
    NAME = ClericSkillEnum.HECATEÇÇÇS_FLAMES.value
    DESCRIPTION = (
        f'*Chamas Mágicas* irrompem dos céus, banhando um aliado e '
        f'fazendo com que seu poder mágico entre em um estado de ebulição, '
        f'aumentando o *{MAGICAL_ATTACK_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.CLERIC.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=HecatesFlamesSkill.NAME,
            description=HecatesFlamesSkill.DESCRIPTION,
            rank=HecatesFlamesSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=HecatesFlamesSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        target_name = char.player_name
        if char.is_alive:
            level = self.level_rank
            power = self.char.cs.wisdom
            condition = HecatesFlamesCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{target_name}* é agraciado com as '
                    f'*Chamas Mágicas* '
                    f'que aumentam o '
                    f'*{MAGICAL_ATTACK_EMOJI_TEXT}* '
                    f'em {condition.bonus_magical_attack} pontos.\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


class OgunsCloakSkill(BaseSkill):
    NAME = ClericSkillEnum.OGUNÇÇÇS_CLOAK.value
    DESCRIPTION = (
        f'Conjura *Fragmentos de Metal dos Deuses* que envolvem um aliado, '
        f'formando uma espécie de manto escuro e reluzente que '
        f'aumentam a *{PHYSICAL_DEFENSE_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.CLERIC.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=OgunsCloakSkill.NAME,
            description=OgunsCloakSkill.DESCRIPTION,
            rank=OgunsCloakSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=OgunsCloakSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        target_name = char.player_name
        if char.is_alive:
            level = self.level_rank
            power = self.char.cs.wisdom
            condition = OgunsCloakCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{target_name}* é agraciado com os '
                    f'*Fragmentos de Metal dos Deuses* '
                    f'que aumentam a '
                    f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* '
                    f'em {condition.bonus_physical_defense} pontos.\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


class IsissVeilSkill(BaseSkill):
    NAME = ClericSkillEnum.ISISÇÇÇS_VEIL.value
    DESCRIPTION = (
        f'Evoca uma *Névoa Resplandecente de Energia Divina* '
        f'que cinge um aliado, '
        f'aumentando a *{MAGICAL_DEFENSE_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.CLERIC.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=IsissVeilSkill.NAME,
            description=IsissVeilSkill.DESCRIPTION,
            rank=IsissVeilSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=IsissVeilSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        target_name = char.player_name
        if char.is_alive:
            level = self.level_rank
            power = self.char.cs.wisdom
            condition = IsissVeilCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{target_name}* é agraciado com a '
                    f'*Névoa Resplandecente de Energia Divina* '
                    f'que aumenta a '
                    f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* '
                    f'em {condition.bonus_magical_defense} pontos.\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


class AnansisTrickerySkill(BaseSkill):
    NAME = ClericSkillEnum.ANANSIÇÇÇS_TRICKERY.value
    DESCRIPTION = (
        f'Invoca a *Astúcia e Engenhosidade de Anansi* e '
        f'tece uma *Teia de Ilusões*, '
        f'aumentando o '
        f'*{HIT_EMOJI_TEXT}* e a *{EVASION_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.CLERIC.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=AnansisTrickerySkill.NAME,
            description=AnansisTrickerySkill.DESCRIPTION,
            rank=AnansisTrickerySkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=AnansisTrickerySkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        target_name = char.player_name
        if char.is_alive:
            level = self.level_rank
            power = self.char.cs.wisdom
            condition = AnansisTrickeryCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{target_name}* recebe a '
                    f'*Teia de Ilusões* '
                    f'que aumenta o '
                    f'*{HIT_EMOJI_TEXT}* '
                    f'em {condition.bonus_hit} pontos e a '
                    f'*{EVASION_EMOJI_TEXT}* '
                    f'em {condition.bonus_evasion} pontos.\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


class VidarsBraverySkill(BaseSkill):
    NAME = ClericSkillEnum.VIDARÇÇÇS_BRAVERY.value
    DESCRIPTION = (
        f'Unge um aliado com a *Bravura Indomita de Vigar*, '
        f'aumentando o '
        f'*{HIT_POINT_FULL_EMOJI_TEXT}*, '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* e a '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.CLERIC.value,
        'skill_list': [
            IdunnsAppleSkill.NAME,
            KratossWrathSkill.NAME,
            OgunsCloakSkill.NAME,
        ]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=VidarsBraverySkill.NAME,
            description=VidarsBraverySkill.DESCRIPTION,
            rank=VidarsBraverySkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=VidarsBraverySkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        target_name = char.player_name
        if char.is_alive:
            level = self.level_rank
            power = self.char.cs.wisdom
            condition = VidarsBraveryCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{target_name}* é ungido com a *Bravura Indomita* '
                    f'que aumenta o '
                    f'*{HIT_POINT_FULL_EMOJI_TEXT}* '
                    f'em {condition.bonus_hit_points} pontos, '
                    f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* '
                    f'em {condition.bonus_physical_attack} pontos e a '
                    f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* '
                    f'em {condition.bonus_physical_defense} pontos.\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


class ArtemissArrowSkill(BaseSkill):
    NAME = ClericSkillEnum.ARTEMISÇÇÇS_ARROW.value
    DESCRIPTION = (
        f'Atira contra um aliado uma *Flecha Lunar* que desperta os '
        f'instintos de combate do alvo, '
        f'aumentando o '
        f'*{HIT_POINT_FULL_EMOJI_TEXT}*, '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}*, '
        f'*{HIT_EMOJI_TEXT}* e a '
        f'*{EVASION_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.CLERIC.value,
        'skill_list': [
            IdunnsAppleSkill.NAME,
            UllrsFocusSkill.NAME,
            AnansisTrickerySkill.NAME,
        ]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=ArtemissArrowSkill.NAME,
            description=ArtemissArrowSkill.DESCRIPTION,
            rank=ArtemissArrowSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=ArtemissArrowSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        target_name = char.player_name
        if char.is_alive:
            level = self.level_rank
            power = self.char.cs.wisdom
            condition = ArtemissArrowCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{target_name}* é atingido pela *Flecha Lunar* '
                    f'que aumenta o '
                    f'*{HIT_POINT_FULL_EMOJI_TEXT}* '
                    f'em {condition.bonus_hit_points} pontos, '
                    f'*{PRECISION_ATTACK_EMOJI_TEXT}* '
                    f'em {condition.bonus_precision_attack} pontos, '
                    f'*{HIT_EMOJI_TEXT}* '
                    f'em {condition.bonus_hit} pontos e a '
                    f'*{EVASION_EMOJI_TEXT}* '
                    f'em {condition.bonus_evasion} pontos.\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


class CeridwensMagicPotionSkill(BaseSkill):
    NAME = ClericSkillEnum.CERIDWENÇÇÇS_MAGIC_POTION.value
    DESCRIPTION = (
        f'Chama a realidade um antigo *Caldeirão Encantado* que derrama sobre '
        f'um aliado uma *Poção Mágica* que desperta os seus '
        f'poderes sobrenaturais, '
        f'aumentando o '
        f'*{HIT_POINT_FULL_EMOJI_TEXT}*, '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* e a '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.CLERIC.value,
        'skill_list': [
            IdunnsAppleSkill.NAME,
            HecatesFlamesSkill.NAME,
            IsissVeilSkill.NAME,
        ]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=CeridwensMagicPotionSkill.NAME,
            description=CeridwensMagicPotionSkill.DESCRIPTION,
            rank=CeridwensMagicPotionSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=CeridwensMagicPotionSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        target_name = char.player_name
        if char.is_alive:
            level = self.level_rank
            power = self.char.cs.wisdom
            condition = CeridwensMagicPotionCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{target_name}* é banhado pela *Poção Mágica* '
                    f'que aumenta o '
                    f'*{HIT_POINT_FULL_EMOJI_TEXT}* '
                    f'em {condition.bonus_hit_points} pontos, '
                    f'*{MAGICAL_ATTACK_EMOJI_TEXT}* '
                    f'em {condition.bonus_magical_attack} pontos e a '
                    f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* '
                    f'em {condition.bonus_magical_defense} pontos.\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


class GraceOfThePantheonSkill(BaseSkill):
    NAME = ClericSkillEnum.GRACE_OF_THE_PANTHEON.value
    DESCRIPTION = (
        f'Agraciado pelos deuses, sua fé inabalável concede a um aliado um '
        f'fragmento da *{ClericSkillEnum.GRACE_OF_THE_PANTHEON.value}*, '
        f'aumentando o '
        f'*{HIT_POINT_FULL_EMOJI_TEXT}*, '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}*, '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}*, '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}*, '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}*, '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}*, '
        f'*{HIT_EMOJI_TEXT}* e a '
        f'*{EVASION_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (200% + 10% x Rank x Nível).'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.CLERIC.value,
        'skill_list': [
            IdunnsAppleSkill.NAME,
            KratossWrathSkill.NAME,
            UllrsFocusSkill.NAME,
            HecatesFlamesSkill.NAME,
            OgunsCloakSkill.NAME,
            IsissVeilSkill.NAME,
            AnansisTrickerySkill.NAME,
            VidarsBraverySkill.NAME,
            ArtemissArrowSkill.NAME,
            CeridwensMagicPotionSkill.NAME,
        ]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=GraceOfThePantheonSkill.NAME,
            description=GraceOfThePantheonSkill.DESCRIPTION,
            rank=GraceOfThePantheonSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=GraceOfThePantheonSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        target_name = char.player_name
        if char.is_alive:
            level = self.level_rank
            power = self.char.cs.wisdom
            condition = GraceOfThePantheonCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{target_name}* é agraciado por um fragmentos da '
                    f'*{self.name}* '
                    f'que aumenta o '
                    f'*{HIT_POINT_FULL_EMOJI_TEXT}* '
                    f'em {condition.bonus_hit_points} pontos, '
                    f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* '
                    f'em {condition.bonus_physical_attack} pontos, '
                    f'*{PRECISION_ATTACK_EMOJI_TEXT}* '
                    f'em {condition.bonus_precision_attack} pontos, '
                    f'*{MAGICAL_ATTACK_EMOJI_TEXT}* '
                    f'em {condition.bonus_magical_attack} pontos, '
                    f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* '
                    f'em {condition.bonus_physical_defense} pontos, '
                    f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* '
                    f'em {condition.bonus_magical_defense} pontos, '
                    f'*{HIT_EMOJI_TEXT}* '
                    f'em {condition.bonus_hit} pontos e a '
                    f'*{EVASION_EMOJI_TEXT}* '
                    f'em {condition.bonus_evasion} pontos.\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


SKILL_WAY_DESCRIPTION = {
    'name': 'Benção do Panteão',
    'description': (
        'Imbuídos da fé inabalável nos deuses, '
        'os Clérigos do Caminho da Benção do Panteão canalizam a força '
        'divina para auxiliar seus aliados em combate. '
        'Através de invocações sagradas e bênçãos divinas, '
        'eles concedem aos seus companheiros melhorias nos '
        'Atributos de Combate, elevando-os a feitos grandiosos em nome das '
        'divindades que veneram.'
    ),
    'skill_list': [
        IdunnsAppleSkill,
        KratossWrathSkill,
        UllrsFocusSkill,
        HecatesFlamesSkill,
        OgunsCloakSkill,
        IsissVeilSkill,
        AnansisTrickerySkill,
        VidarsBraverySkill,
        ArtemissArrowSkill,
        CeridwensMagicPotionSkill,
        GraceOfThePantheonSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import CLERIC_CHARACTER

    skill = IdunnsAppleSkill(CLERIC_CHARACTER)
    print(skill)
    print(CLERIC_CHARACTER.bs.wisdom)
    print(CLERIC_CHARACTER.cs.hp)
    print(skill.function(CLERIC_CHARACTER))
    print(CLERIC_CHARACTER.cs.hp)
    CLERIC_CHARACTER.skill_tree.learn_skill(IdunnsAppleSkill)

    skill = KratossWrathSkill(CLERIC_CHARACTER)
    print(skill)
    print(CLERIC_CHARACTER.bs.wisdom)
    print(CLERIC_CHARACTER.cs.physical_attack)
    print(skill.function(CLERIC_CHARACTER))
    print(CLERIC_CHARACTER.cs.physical_attack)
    CLERIC_CHARACTER.skill_tree.learn_skill(KratossWrathSkill)

    skill = UllrsFocusSkill(CLERIC_CHARACTER)
    print(skill)
    print(CLERIC_CHARACTER.bs.wisdom)
    print(CLERIC_CHARACTER.cs.precision_attack)
    print(skill.function(CLERIC_CHARACTER))
    print(CLERIC_CHARACTER.cs.precision_attack)
    CLERIC_CHARACTER.skill_tree.learn_skill(UllrsFocusSkill)

    skill = HecatesFlamesSkill(CLERIC_CHARACTER)
    print(skill)
    print(CLERIC_CHARACTER.bs.wisdom)
    print(CLERIC_CHARACTER.cs.magical_attack)
    print(skill.function(CLERIC_CHARACTER))
    print(CLERIC_CHARACTER.cs.magical_attack)
    CLERIC_CHARACTER.skill_tree.learn_skill(HecatesFlamesSkill)

    skill = OgunsCloakSkill(CLERIC_CHARACTER)
    print(skill)
    print(CLERIC_CHARACTER.bs.wisdom)
    print(CLERIC_CHARACTER.cs.physical_defense)
    print(skill.function(CLERIC_CHARACTER))
    print(CLERIC_CHARACTER.cs.physical_defense)
    CLERIC_CHARACTER.skill_tree.learn_skill(OgunsCloakSkill)

    skill = IsissVeilSkill(CLERIC_CHARACTER)
    print(skill)
    print(CLERIC_CHARACTER.bs.wisdom)
    print(CLERIC_CHARACTER.cs.magical_defense)
    print(skill.function(CLERIC_CHARACTER))
    print(CLERIC_CHARACTER.cs.magical_defense)
    CLERIC_CHARACTER.skill_tree.learn_skill(IsissVeilSkill)

    skill = AnansisTrickerySkill(CLERIC_CHARACTER)
    print(skill)
    print(CLERIC_CHARACTER.bs.wisdom)
    print(CLERIC_CHARACTER.cs.hit, CLERIC_CHARACTER.cs.evasion)
    print(skill.function(CLERIC_CHARACTER))
    print(CLERIC_CHARACTER.cs.hit, CLERIC_CHARACTER.cs.evasion)
    CLERIC_CHARACTER.skill_tree.learn_skill(AnansisTrickerySkill)

    skill = VidarsBraverySkill(CLERIC_CHARACTER)
    print(skill)
    print(CLERIC_CHARACTER.bs.wisdom)
    print(CLERIC_CHARACTER.cs.hit_points, CLERIC_CHARACTER.cs.physical_attack,
          CLERIC_CHARACTER.cs.physical_defense)
    print(skill.function(CLERIC_CHARACTER))
    print(CLERIC_CHARACTER.cs.hit_points, CLERIC_CHARACTER.cs.physical_attack,
          CLERIC_CHARACTER.cs.physical_defense)
    CLERIC_CHARACTER.skill_tree.learn_skill(VidarsBraverySkill)

    skill = ArtemissArrowSkill(CLERIC_CHARACTER)
    print(skill)
    print(CLERIC_CHARACTER.bs.wisdom)
    print(CLERIC_CHARACTER.cs.hit_points, CLERIC_CHARACTER.cs.precision_attack,
          CLERIC_CHARACTER.cs.hit, CLERIC_CHARACTER.cs.evasion)
    print(skill.function(CLERIC_CHARACTER))
    print(CLERIC_CHARACTER.cs.hit_points, CLERIC_CHARACTER.cs.precision_attack,
          CLERIC_CHARACTER.cs.hit, CLERIC_CHARACTER.cs.evasion)
    CLERIC_CHARACTER.skill_tree.learn_skill(ArtemissArrowSkill)

    skill = CeridwensMagicPotionSkill(CLERIC_CHARACTER)
    print(skill)
    print(CLERIC_CHARACTER.bs.wisdom)
    print(CLERIC_CHARACTER.cs.hit_points, CLERIC_CHARACTER.cs.magical_attack,
          CLERIC_CHARACTER.cs.magical_defense)
    print(skill.function(CLERIC_CHARACTER))
    print(CLERIC_CHARACTER.cs.hit_points, CLERIC_CHARACTER.cs.magical_attack,
          CLERIC_CHARACTER.cs.magical_defense)
    CLERIC_CHARACTER.skill_tree.learn_skill(CeridwensMagicPotionSkill)

    skill = GraceOfThePantheonSkill(CLERIC_CHARACTER)
    print(skill)
    print(CLERIC_CHARACTER.bs.wisdom)
    print(CLERIC_CHARACTER.cs.hit_points, CLERIC_CHARACTER.cs.physical_attack,
          CLERIC_CHARACTER.cs.precision_attack, CLERIC_CHARACTER.cs.magical_attack,
          CLERIC_CHARACTER.cs.physical_defense, CLERIC_CHARACTER.cs.magical_defense,
          CLERIC_CHARACTER.cs.hit, CLERIC_CHARACTER.cs.evasion)
    print(skill.function(CLERIC_CHARACTER))
    print(CLERIC_CHARACTER.cs.hit_points, CLERIC_CHARACTER.cs.physical_attack,
          CLERIC_CHARACTER.cs.precision_attack, CLERIC_CHARACTER.cs.magical_attack,
          CLERIC_CHARACTER.cs.physical_defense, CLERIC_CHARACTER.cs.magical_defense,
          CLERIC_CHARACTER.cs.hit, CLERIC_CHARACTER.cs.evasion)
    CLERIC_CHARACTER.skill_tree.learn_skill(GraceOfThePantheonSkill)
