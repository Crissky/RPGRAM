
from typing import TYPE_CHECKING

from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.barrier import GuardianShieldCondition
from rpgram.conditions.self_skill import RobustBlockCondition
from rpgram.constants.text import (
    CONSTITUTION_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT,
    PHYSICAL_DEFENSE_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.skill import (
    MultiClasseSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class RobustBlockSkill(BaseSkill):
    NAME = MultiClasseSkillEnum.ROBUST_BLOCK.value
    DESCRIPTION = (
        f'Assume uma postura defensiva aumentando a '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* com base na '
        f'*{CONSTITUTION_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name_list': [
            ClasseEnum.GUARDIAN.value,
            ClasseEnum.HERALD.value,
        ],
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=RobustBlockSkill.NAME,
            description=RobustBlockSkill.DESCRIPTION,
            rank=RobustBlockSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=RobustBlockSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        condition = RobustBlockCondition(character=char, level=level)
        report_list = self.char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* se concentra em fortalecer a sua guarda '
                f'assumindo uma postura preventiva que aumenta a sua '
                f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* '
                f'em {condition.bonus_physical_defense} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class GuardianShieldSkill(BaseSkill):
    NAME = MultiClasseSkillEnum.GUARDIAN_SHIELD.value
    DESCRIPTION = (
        f'Erguendo o escudo com fé inabalável, evoca um *Escudo Familiar '
        f'Protetivo* que resguarda um aliado com uma barreira baseada na '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name_list': [
            ClasseEnum.GUARDIAN.value,
            ClasseEnum.HERALD.value,
        ],
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=GuardianShieldSkill.NAME,
            description=GuardianShieldSkill.DESCRIPTION,
            rank=GuardianShieldSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BARRIER,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=GuardianShieldSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        player_name = self.char.player_name
        target_name = char.player_name
        if char.is_alive:
            target_name = (
                'a si mesmo'
                if target_name == player_name
                else target_name
            )
            dice = self.dice
            power = dice.boosted_physical_defense
            level = self.level_rank
            condition = GuardianShieldCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{player_name}* se impõe contra o perigo, evocando um '
                    f'*Escudo Familiar Protetivo* para resguardar '
                    f'*{target_name}* com uma barreira '
                    f'*{condition.barrier_points_text}*({dice.text}).\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


class HeavyChargeSkill(BaseSkill):
    NAME = MultiClasseSkillEnum.HEAVY_CHARGE.value
    DESCRIPTION = (
        f'Assume uma postura ofensiva, avançando contra o inimigo '
        f'usando seu corpo massivo como arma, causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.BLUDGEONING)}* com base em '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* (75% + 5% x Rank x Nível) e '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (50% + 5% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name_list': [
            ClasseEnum.GUARDIAN.value,
            ClasseEnum.HERALD.value,
        ],
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_DEFENSE: 0.75,
            CombatStatsEnum.PHYSICAL_ATTACK: 0.50,
        }
        damage_types = [DamageEnum.BLUDGEONING]

        super().__init__(
            name=HeavyChargeSkill.NAME,
            description=HeavyChargeSkill.DESCRIPTION,
            rank=HeavyChargeSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=HeavyChargeSkill.REQUIREMENTS,
            damage_types=damage_types
        )
