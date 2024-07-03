from typing import TYPE_CHECKING
from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.barrier import AegisShadowCondition
from rpgram.conditions.target_skill import WarBannerCondition
from rpgram.constants.text import (
    HIT_POINT_FULL_EMOJI_TEXT,
    MAGICAL_ATTACK_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT,
    PRECISION_ATTACK_EMOJI_TEXT,
    STRENGTH_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.skill import (
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum,
    WarriorSkillEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill

if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


SKILL_WAY_DESCRIPTION = {
    'name': 'Liderança',
    'description': (
        'O caminho da Liderança transforma o Guerreiro em um '
        'líder inspirador e comandante implacável, '
        'capaz de unir seus aliados e guiá-los à vitória através de '
        'sua força, bravura e carisma. '
        'Através de habilidades que inspiram coragem, '
        'fortalecem o grupo e amplificam a presença do Guerreiro no '
        'campo de batalha, ele se torna um farol de esperança e um '
        'símbolo de resistência.'
    )
}


class AegisShadowSkill(BaseSkill):
    NAME = WarriorSkillEnum.AEGIS_SHADOW.value
    DESCRIPTION = (
        f'Canaliza a sua determinação para ser imbuído pelas '
        f'*Sombras do Lendário Escudo*, recebendo uma barreira com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (100% + 5% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.WARRIOR.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 2
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=AegisShadowSkill.NAME,
            description=AegisShadowSkill.DESCRIPTION,
            rank=AegisShadowSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BARRIER,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=AegisShadowSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        dice = self.dice
        power = dice.boosted_physical_attack
        level = self.level_rank
        condition = AegisShadowCondition(power=power, level=level)
        report_list = self.char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* é imbuído pela *Sombra do Escudo Lendário* '
                f'que o protege com uma barreira '
                f'*{condition.barrier_points_text}*({dice.text}).\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class WarBannerSkill(BaseSkill):
    NAME = WarriorSkillEnum.WAR_BANNER.value
    DESCRIPTION = (
        f'Usa a própria força e determinação para evocar a '
        f'*Marca do Senhor da Guerra* e receber a inspiração de combate '
        f'aumentando o '
        f'{PHYSICAL_ATTACK_EMOJI_TEXT}, '
        f'{PRECISION_ATTACK_EMOJI_TEXT} e '
        f'{MAGICAL_ATTACK_EMOJI_TEXT} com base na '
        f'*{STRENGTH_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.WARRIOR.value,
        'skill_list': [AegisShadowSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 3
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=WarBannerSkill.NAME,
            description=WarBannerSkill.DESCRIPTION,
            rank=WarBannerSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.TEAM,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=WarBannerSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        player_name = self.char.player_name
        power = self.char.bs.strength
        level = self.level_rank
        condition = WarBannerCondition(power=power, level=level)
        report_list = char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* recebe a *Marca do Senhor da Guerra* '
                f'aumentando o '
                f'{PHYSICAL_ATTACK_EMOJI_TEXT}, '
                f'{PRECISION_ATTACK_EMOJI_TEXT} e '
                f'{MAGICAL_ATTACK_EMOJI_TEXT} em '
                f'*{condition.power}* pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class HeroicInspirationSkill(BaseSkill):
    NAME = WarriorSkillEnum.HEROIC_INSPIRATION.value
    DESCRIPTION = (
        f'Libera uma explosão de '
        f'energia inspiradora, revigorando seu espírito e curando seu'
        f'{HIT_POINT_FULL_EMOJI_TEXT} com base em '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (200% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.WARRIOR.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 2
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=HeroicInspirationSkill.NAME,
            description=HeroicInspirationSkill.DESCRIPTION,
            rank=HeroicInspirationSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.HEALING,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=HeroicInspirationSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        dice = self.dice
        level = self.level_rank
        power_multiplier = 2 + (level / 10)
        power = dice.boosted_physical_attack * power_multiplier
        power = (round(power))

        cure_report = self.char.cs.cure_hit_points(power)
        report_text = cure_report["text"]
        report = {
            'text': (
                f'*{player_name}* respira fundo se concentrando em acalmar a'
                f'sua mente, curando suas feridas.\n'
                f'*{report_text}*({dice.text}).'
            )
        }

        return report


class WarCrySkill(BaseSkill):
    NAME = WarriorSkillEnum.WAR_CRY.value
    DESCRIPTION = (
        f'Libera um grito que ecoa no campo de batalha, elevando os espíritos '
        f'dos aliados e curando seus '
        f'{HIT_POINT_FULL_EMOJI_TEXT} com base em '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.WARRIOR.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 3
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=WarCrySkill.NAME,
            description=WarCrySkill.DESCRIPTION,
            rank=WarCrySkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.TEAM,
            skill_type=SkillTypeEnum.HEALING,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=WarCrySkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        player_name = self.char.player_name
        target_name = char.player_name
        dice = self.dice
        level = self.level_rank
        power_multiplier = 1 + (level / 10)
        power = dice.boosted_physical_attack * power_multiplier
        power = (round(power))

        cure_report = char.cs.cure_hit_points(power)
        report_text = cure_report["text"]
        report = {
            'text': (
                f'*{player_name}* liberta o *{self.name}*, '
                f'curando as feridas de *{target_name}*.\n'
                f'*{report_text}*({dice.text}).'
            )
        }

        return report


if __name__ == '__main__':
    from rpgram.constants.test import WARRIOR_CHARACTER
    skill = AegisShadowSkill(WARRIOR_CHARACTER)
    print(skill)
    print(WARRIOR_CHARACTER.cs.physical_attack)
    print(skill.function())
    WARRIOR_CHARACTER.skill_tree.learn_skill(AegisShadowSkill)

    skill = HeroicInspirationSkill(WARRIOR_CHARACTER)
    print(skill)
    WARRIOR_CHARACTER.cs.damage_hit_points(3000)
    print(WARRIOR_CHARACTER.cs.physical_attack)
    print(WARRIOR_CHARACTER.cs.show_hit_points)
    print(skill.function(WARRIOR_CHARACTER))
    WARRIOR_CHARACTER.skill_tree.learn_skill(HeroicInspirationSkill)
    
    skill = WarCrySkill(WARRIOR_CHARACTER)
    print(skill)
    WARRIOR_CHARACTER.cs.damage_hit_points(3000)
    print(WARRIOR_CHARACTER.cs.physical_attack)
    print(WARRIOR_CHARACTER.cs.show_hit_points)
    print(skill.function(WARRIOR_CHARACTER))
    WARRIOR_CHARACTER.skill_tree.learn_skill(WarCrySkill)

    skill = WarBannerSkill(WARRIOR_CHARACTER)
    print(skill)
    print(WARRIOR_CHARACTER.bs.strength)
    print(
        WARRIOR_CHARACTER.cs.physical_attack,
        WARRIOR_CHARACTER.cs.precision_attack,
        WARRIOR_CHARACTER.cs.magical_attack,
    )
    print(skill.function(WARRIOR_CHARACTER))
    print(
        WARRIOR_CHARACTER.cs.physical_attack,
        WARRIOR_CHARACTER.cs.precision_attack,
        WARRIOR_CHARACTER.cs.magical_attack,
    )
    WARRIOR_CHARACTER.skill_tree.learn_skill(WarBannerSkill)
