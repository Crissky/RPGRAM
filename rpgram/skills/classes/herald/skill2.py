from typing import TYPE_CHECKING
from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.barrier import FlameMantillaCondition
from rpgram.conditions.self_skill import VigilFlameCondition
from rpgram.conditions.special_damage_skill import (
    SDIgneousHeartCondition,
    SDMantilledArmsCondition,
    SDVigilArmsCondition
)
from rpgram.constants.text import (
    CONSTITUTION_EMOJI_TEXT,
    HIT_POINT_FULL_EMOJI_TEXT,
    MAGICAL_DEFENSE_EMOJI_TEXT,
    PHYSICAL_DEFENSE_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.skill import (
    HeraldSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.classes.multiclasse.physical_defense import (
    GuardianShieldSkill
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class VigilFlameSkill(BaseSkill):
    NAME = HeraldSkillEnum.VIGIL_FLAME.value
    DESCRIPTION = (
        f'Canaliza uma *Aura de Fogo* que o envolve, '
        f'inflamando o seu espírito para aumentar a '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* e a '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* com base na '
        f'*{CONSTITUTION_EMOJI_TEXT}* (100% + 10% x Rank x Nível). '
        f'Além disso, adiciona dano de '
        f'*{get_damage_emoji_text(DamageEnum.FIRE)}* '
        f'baseado na '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.HERALD.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=VigilFlameSkill.NAME,
            description=VigilFlameSkill.DESCRIPTION,
            rank=VigilFlameSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=VigilFlameSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        char = self.char
        player_name = char.player_name
        level = self.level_rank
        condition = VigilFlameCondition(character=char, level=level)
        sd_power = char.cs.magical_defense
        sd_condition = SDVigilArmsCondition(power=sd_power, level=level)
        report_list = char.status.set_conditions(condition, sd_condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* se concentra para criar uma '
                f'*Aura de Fogo*, '
                f'aumentando a sua '
                f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* '
                f'em {condition.bonus_physical_defense} e a '
                f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* '
                f'em {condition.bonus_magical_defense} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class FlameMantillaSkill(BaseSkill):
    NAME = HeraldSkillEnum.FLAME_MANTILLA.value
    DESCRIPTION = (
        f'Libera *Energia Vigílica* que o envolve e '
        f'usa o calor liberado para criar uma *Mantilha de Chamas*, '
        f'se resguardando com uma barreira baseada na '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* (200% + 10% x Rank x Nível). '
        f'Além disso, adiciona dano de '
        f'*{get_damage_emoji_text(DamageEnum.FIRE)}* '
        f'baseado na '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.HERALD.value,
        'skill_list': [
            GuardianShieldSkill.NAME,
            VigilFlameSkill.NAME,
        ]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=FlameMantillaSkill.NAME,
            description=FlameMantillaSkill.DESCRIPTION,
            rank=FlameMantillaSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BARRIER,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=FlameMantillaSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        char = self.char
        player_name = char.player_name
        level = self.level_rank
        dice = self.dice
        barrier_power = dice.boosted_physical_defense
        barrier_condition = FlameMantillaCondition(
            power=barrier_power,
            level=level
        )
        sd_power = char.cs.magical_defense
        sd_condition = SDMantilledArmsCondition(power=sd_power, level=level)
        sd_report_list = char.status.set_conditions(
            barrier_condition, sd_condition
        )
        status_report_text = "\n".join(
            [report["text"] for report in sd_report_list]
        )
        report = {
            'text': (
                f'*{player_name}* se concentra para criar uma '
                f'*Mantilha de Chamas*, que o protege com uma barreira '
                f'*{barrier_condition.barrier_points_text}*({dice.text}).\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class IgneousStrikeSkill(BaseSkill):
    NAME = HeraldSkillEnum.IGNEOUS_STRIKE.value
    DESCRIPTION = (
        f'Envolve a própria arma em chamas e desfere um poderoso ataque '
        f'que causa dano de '
        f'*{get_damage_emoji_text(DamageEnum.FIRE)}* com base na '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* (125% + 5% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.HERALD.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_DEFENSE: 1.25,
        }
        damage_types = [DamageEnum.FIRE]

        super().__init__(
            name=IgneousStrikeSkill.NAME,
            description=IgneousStrikeSkill.DESCRIPTION,
            rank=IgneousStrikeSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=IgneousStrikeSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class PurifyingFlameSkill(BaseSkill):
    NAME = HeraldSkillEnum.IGNEOUS_STRIKE.value
    DESCRIPTION = (
        f'Envolve a própria arma em *Chamas Brancas* e '
        f'desfere ataque impetuoso '
        f'que causa dano de '
        f'*{get_damage_emoji_text(DamageEnum.FIRE)}* e '
        f'*{get_damage_emoji_text(DamageEnum.BLESSING)}* com base na '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* (150% + 5% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.HERALD.value,
        'skill_list': [
            IgneousStrikeSkill.NAME,
        ]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_DEFENSE: 1.50,
        }
        damage_types = [DamageEnum.FIRE, DamageEnum.BLESSING]

        super().__init__(
            name=PurifyingFlameSkill.NAME,
            description=PurifyingFlameSkill.DESCRIPTION,
            rank=PurifyingFlameSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=PurifyingFlameSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class IgneousHeartSkill(BaseSkill):
    NAME = HeraldSkillEnum.IGNEOUS_HEART.value
    DESCRIPTION = (
        f'Guiado por um Coração enfartado de *Ímpeto por Justiça*, '
        f'libera uma *Explosão Vigorosa* que cura seu '
        f'*{HIT_POINT_FULL_EMOJI_TEXT}* com base no '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* (100% + 10% x Rank x Nível). '
        f'Além disso, adiciona dano de '
        f'*{get_damage_emoji_text(DamageEnum.FIRE)}* '
        f'baseado na '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.HERALD.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=IgneousHeartSkill.NAME,
            description=IgneousHeartSkill.DESCRIPTION,
            rank=IgneousHeartSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.HEALING,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=IgneousHeartSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        char = self.char
        player_name = char.player_name
        dice = self.dice
        level = self.level_rank
        power_multiplier = 1 + (level / 10)
        power = dice.boosted_physical_attack * power_multiplier
        power = round(power)

        cure_report = char.cs.cure_hit_points(power)
        report_text = cure_report["text"]

        sd_power = char.cs.magical_defense
        sd_condition = SDIgneousHeartCondition(power=sd_power, level=level)
        report_list = char.status.set_conditions(sd_condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* é envolvido por um *Ímpeto por Justiça* '
                f'que cura suas feridas.\n'
                f'*{report_text}*({dice.text}).\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


SKILL_WAY_DESCRIPTION = {
    'name': 'Vigia das Chamas',
    'description': (
        'Um bastião ardente que utiliza o fogo como símbolo de proteção, '
        'purificação e justiça. '
        'Neste caminho, o Arauto manipula chamas sagradas para proteger '
        'seus aliados e devastar aqueles que ameaçam o equilíbrio. '
        'Suas habilidades mesclam ofensiva e defensiva, '
        'transformando o fogo em um aliado fiel que incinera o mal e aquece '
        'o coração dos justos.'
    ),
    'skill_list': [
        GuardianShieldSkill,
        VigilFlameSkill,
        FlameMantillaSkill,
        IgneousStrikeSkill,
        PurifyingFlameSkill,
        IgneousHeartSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import HERALD_CHARACTER

    skill = VigilFlameSkill(HERALD_CHARACTER)
    print(skill)
    print(HERALD_CHARACTER.cs.constitution,
          HERALD_CHARACTER.cs.physical_defense,
          HERALD_CHARACTER.cs.magical_defense)
    print(skill.function(HERALD_CHARACTER))
    print(HERALD_CHARACTER.cs.physical_defense,
          HERALD_CHARACTER.cs.magical_defense)
    HERALD_CHARACTER.skill_tree.learn_skill(VigilFlameSkill)

    skill = GuardianShieldSkill(HERALD_CHARACTER)
    print(skill)
    print(skill.function(HERALD_CHARACTER))
    HERALD_CHARACTER.skill_tree.learn_skill(GuardianShieldSkill)

    skill = FlameMantillaSkill(HERALD_CHARACTER)
    print(skill)
    print(skill.function(HERALD_CHARACTER))
    HERALD_CHARACTER.skill_tree.learn_skill(FlameMantillaSkill)

    skill = IgneousStrikeSkill(HERALD_CHARACTER)
    print(skill)
    print(HERALD_CHARACTER.cs.magical_attack)
    print(HERALD_CHARACTER.to_attack(
        defender_char=HERALD_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    HERALD_CHARACTER.skill_tree.learn_skill(IgneousStrikeSkill)

    skill = PurifyingFlameSkill(HERALD_CHARACTER)
    print(skill)
    print(HERALD_CHARACTER.cs.magical_attack)
    print(HERALD_CHARACTER.to_attack(
        defender_char=HERALD_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    HERALD_CHARACTER.skill_tree.learn_skill(PurifyingFlameSkill)

    skill = IgneousHeartSkill(HERALD_CHARACTER)
    print(skill)
    HERALD_CHARACTER.cs.damage_hit_points(5000, ignore_barrier=True)
    print(HERALD_CHARACTER.cs.magical_defense)
    print(skill.function(HERALD_CHARACTER))
    HERALD_CHARACTER.skill_tree.learn_skill(IgneousHeartSkill)
