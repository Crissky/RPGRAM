from typing import TYPE_CHECKING
from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.barrier import GuardianShieldCondition
from rpgram.conditions.self_skill import RobustBlockCondition
from rpgram.constants.text import (
    CONSTITUTION_EMOJI_TEXT,
    PHYSICAL_DEFENSE_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.skill import (
    GuardianSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill

if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


SKILL_WAY_DESCRIPTION = {
    'name': 'Fortaleza Inabalável',
    'description': (
        'O caminho da Fortaleza Inabalável transforma o Guardião '
        'em um bastião inabalável, pronto para enfrentar qualquer desafio. '
        'Através dessas habilidades, o Guardião se torna um escudo '
        'impenetrável para seus aliados, capaz de suportar os golpes '
        'mais devastadores e proteger seus companheiros de batalha. '
        'Sua resistência inquebrantável inspira confiança e serve como um '
        'farol de esperança em meio ao caos. '
        'Cada investida inimiga é repelida com força redobrada, '
        'demonstrando a força inabalável do Guardião e garantindo a '
        'vitória final.'
    )
}


class RobustBlockSkill(BaseSkill):
    NAME = GuardianSkillEnum.ROBUST_BLOCK.value
    DESCRIPTION = (
        f'Assume uma postura defensiva aumentando a '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* com base na '
        f'*{CONSTITUTION_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.GUARDIAN.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 2
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=RobustBlockSkill.NAME,
            description=RobustBlockSkill.DESCRIPTION,
            rank=RobustBlockSkill.RANK,
            level=level,
            cost=cost,
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
                f'*{player_name}* se concentra em fortalecer a sua defesa '
                f'assumindo uma postura defensiva aumentando a sua '
                f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}*.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class GuardianShieldSkill(BaseSkill):
    NAME = GuardianSkillEnum.GUARDIAN_SHIELD.value
    DESCRIPTION = (
        f'Erguendo o escudo com fé inabalável, evoca um *Escudo Familiar '
        f'Protetivo* que resguarda um aliado com uma barreira baseada na '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.GUARDIAN.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 2
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=GuardianShieldSkill.NAME,
            description=GuardianShieldSkill.DESCRIPTION,
            rank=GuardianShieldSkill.RANK,
            level=level,
            cost=cost,
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

        return report


class ShieldWallSkill(BaseSkill):
    NAME = GuardianSkillEnum.SHIELD_WALL.value
    DESCRIPTION = (
        f'Erguendo o escudo com determinação e fé inabalável, '
        f'evoca uma miríade de *Escudo Familiar Protetivo* '
        f'que resguardam os aliados com barreiras baseada na '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.GUARDIAN.value,
        'skill_list': [GuardianShieldSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 2
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=ShieldWallSkill.NAME,
            description=ShieldWallSkill.DESCRIPTION,
            rank=ShieldWallSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.TEAM,
            skill_type=SkillTypeEnum.BARRIER,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=ShieldWallSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        player_name = self.char.player_name
        target_name = char.player_name
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

        return report

if __name__ == '__main__':
    from rpgram.constants.test import GUARDIAN_CHARACTER
    skill = RobustBlockSkill(GUARDIAN_CHARACTER)
    print(skill)
    print(GUARDIAN_CHARACTER.bs.constitution)
    print(GUARDIAN_CHARACTER.cs.physical_defense)
    print(skill.function())
    print(GUARDIAN_CHARACTER.cs.physical_defense)
    GUARDIAN_CHARACTER.skill_tree.learn_skill(RobustBlockSkill)

    skill = GuardianShieldSkill(GUARDIAN_CHARACTER)
    print(skill)
    print(GUARDIAN_CHARACTER.cs.physical_defense)
    print(skill.function(GUARDIAN_CHARACTER))
    GUARDIAN_CHARACTER.skill_tree.learn_skill(GuardianShieldSkill)

    skill = ShieldWallSkill(GUARDIAN_CHARACTER)
    print(skill)
    print(GUARDIAN_CHARACTER.cs.physical_defense)
    print(skill.function(GUARDIAN_CHARACTER))
    GUARDIAN_CHARACTER.skill_tree.learn_skill(ShieldWallSkill)
