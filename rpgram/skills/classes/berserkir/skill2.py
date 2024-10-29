from typing import TYPE_CHECKING

from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.debuff import BerserkerCondition
from rpgram.conditions.self_skill import (
    FenrirsInstinctCondition,
    HrungnirsSovereigntyCondition,
    YmirsResilienceCondition
)
from rpgram.constants.text import (
    EVASION_EMOJI_TEXT,
    HIT_EMOJI_TEXT,
    HIT_POINT_FULL_EMOJI_TEXT,
    MAGICAL_DEFENSE_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT,
    PHYSICAL_DEFENSE_EMOJI_TEXT,
    STRENGTH_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.debuff import DebuffEnum, get_debuff_emoji_text
from rpgram.enums.skill import (
    BerserkirSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class HrungnirsSovereigntySkill(BaseSkill):
    NAME = BerserkirSkillEnum.HRUNGNIRÇÇÇS_SOVEREIGNTY.value
    DESCRIPTION = (
        f'Entra em um estado de *Fúria Desenfreada* ao ser envolto pelo '
        f'espírito do *Gigante Hrungnir*, '
        f'recebendo a condição '
        f'*{get_debuff_emoji_text(DebuffEnum.BERSERKER)}* '
        f'com nível igual ao (Rank x Nível) e '
        f'aumentando o *{HIT_POINT_FULL_EMOJI_TEXT}* e o '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* com base na '
        f'*{STRENGTH_EMOJI_TEXT}* (200% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.BERSERKIR.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=HrungnirsSovereigntySkill.NAME,
            description=HrungnirsSovereigntySkill.DESCRIPTION,
            rank=HrungnirsSovereigntySkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=HrungnirsSovereigntySkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank

        condition = HrungnirsSovereigntyCondition(character=char, level=level)
        report_list = self.char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )

        berserker_condition = BerserkerCondition(level=level)
        status_report = char.status.add_condition(berserker_condition)

        report = {
            'text': (
                f'*{player_name}* é envolto pelo espírito do '
                f'*Gigante Hrungnir*, entrando em um estado '
                f'de *Fúria Desenfreada* que aumenta o seu '
                f'*{HIT_POINT_FULL_EMOJI_TEXT}* '
                f'em {condition.bonus_hit_points} pontos e o '
                f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* '
                f'em {condition.bonus_physical_attack} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}\n'
                f'{status_report["text"]}'
            )
        }

        return report


class FenrirsInstinctSkill(BaseSkill):
    NAME = BerserkirSkillEnum.FENRIRÇÇÇS_INSTINCT.value
    DESCRIPTION = (
        f'Entra em um estado de *Fúria Desenfreada* ao ser envolto pelo '
        f'espírito do lobo gigante, *Fenrir*, '
        f'recebendo a condição '
        f'*{get_debuff_emoji_text(DebuffEnum.BERSERKER)}* '
        f'com nível igual ao (Rank x Nível) e '
        f'aumentando o *{HIT_POINT_FULL_EMOJI_TEXT}*, '
        f'o *{HIT_EMOJI_TEXT}* e a '
        f'*{EVASION_EMOJI_TEXT}* com base na '
        f'*{STRENGTH_EMOJI_TEXT}* (200% + 10% x Rank x Nível), '
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.BERSERKIR.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=FenrirsInstinctSkill.NAME,
            description=FenrirsInstinctSkill.DESCRIPTION,
            rank=FenrirsInstinctSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=FenrirsInstinctSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank

        condition = FenrirsInstinctCondition(character=char, level=level)
        report_list = self.char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )

        berserker_condition = BerserkerCondition(level=level)
        status_report = char.status.add_condition(berserker_condition)

        report = {
            'text': (
                f'*{player_name}* é envolto pelo espírito de '
                f'*Fenrir*, o lobo gigante, entrando em um estado '
                f'de *Fúria Desenfreada* que aumenta o seu '
                f'*{HIT_POINT_FULL_EMOJI_TEXT}* '
                f'em {condition.bonus_hit_points} pontos, '
                f'o *{HIT_EMOJI_TEXT}* '
                f'em {condition.bonus_hit} pontos e a '
                f'*{EVASION_EMOJI_TEXT}* '
                f'em {condition.bonus_evasion} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}\n'
                f'{status_report["text"]}'
            )
        }

        return report


class YmirsResilienceSkill(BaseSkill):
    NAME = BerserkirSkillEnum.YMIRÇÇÇS_RESILIENCE.value
    DESCRIPTION = (
        f'Entra em um estado de *Fúria Desenfreada* ao ser envolto pelo '
        f'espírito do gigante de gelo, *Ymir*, '
        f'recebendo a condição '
        f'*{get_debuff_emoji_text(DebuffEnum.BERSERKER)}* '
        f'com nível igual ao (Rank x Nível) e '
        f'aumentando o *{HIT_POINT_FULL_EMOJI_TEXT}*, '
        f'a *{PHYSICAL_DEFENSE_EMOJI_TEXT}* e a '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* com base na '
        f'*{STRENGTH_EMOJI_TEXT}* (200% + 10% x Rank x Nível), '
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.BERSERKIR.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=YmirsResilienceSkill.NAME,
            description=YmirsResilienceSkill.DESCRIPTION,
            rank=YmirsResilienceSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=YmirsResilienceSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank

        condition = YmirsResilienceCondition(character=char, level=level)
        report_list = self.char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )

        berserker_condition = BerserkerCondition(level=level)
        status_report = char.status.add_condition(berserker_condition)

        report = {
            'text': (
                f'*{player_name}* é envolto pelo espírito de '
                f'*Ymir*, o gigante de gelo, entrando em um estado '
                f'de *Fúria Desenfreada* que aumenta o seu '
                f'*{HIT_POINT_FULL_EMOJI_TEXT}* '
                f'em {condition.bonus_hit_points} pontos, '
                f'o *{PHYSICAL_DEFENSE_EMOJI_TEXT}* '
                f'em {condition.bonus_physical_defense} pontos e a '
                f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* '
                f'em {condition.bonus_magical_defense} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}\n'
                f'{status_report["text"]}'
            )
        }

        return report


class StoneStrikeSkill(BaseSkill):
    NAME = BerserkirSkillEnum.STONE_STRIKE.value
    DESCRIPTION = (
        f'Entra em um estado de *Fúria Incontrolável*, '
        f'contraindo os músculos dos braços até transformá-los em pedra, '
        f'recebendo a condição '
        f'*{get_debuff_emoji_text(DebuffEnum.BERSERKER)}* '
        f'com nível igual ao (Rank x Nível) '
        f'e desferindo um ataque com força bruta, '
        f'que causa dano de '
        f'*{get_damage_emoji_text(DamageEnum.ROCK)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (250% + 5% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.BERSERKIR.value,
        'skill_list': [HrungnirsSovereigntySkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 2.50,
        }
        damage_types = [DamageEnum.ROCK]

        super().__init__(
            name=StoneStrikeSkill.NAME,
            description=StoneStrikeSkill.DESCRIPTION,
            rank=StoneStrikeSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=StoneStrikeSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def pre_hit_function(self, target: 'BaseCharacter') -> dict:
        report = {'text': ''}
        char = self.char
        level = self.level_rank
        berserker_condition = BerserkerCondition(level=level)
        status_report = char.status.add_condition(berserker_condition)
        if status_report['text']:
            report['text'] = status_report["text"]

        return report


SKILL_WAY_DESCRIPTION = {
    'name': 'Espírito Bestial',
    'description': (
        'O caminho do Espírito Bestial transforma o Berserkir '
        'em um receptáculo das forças das Criaturas Mitológicas, utilizando '
        'habilidades ancestrais para manipular os Poderes Bestiais e '
        'liberar a fúria indomável da fera interior. '
        'Através de rituais ancestrais e conexão profunda com esses seres, '
        'o Berserkir se torna um agente da destruição da ancianidade.'
    ),
    'skill_list': [
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import BERSERKIR_CHARACTER

    skill = HrungnirsSovereigntySkill(BERSERKIR_CHARACTER)
    print(skill)
    print(BERSERKIR_CHARACTER.bs.strength,
          BERSERKIR_CHARACTER.cs.hit_points,
          BERSERKIR_CHARACTER.cs.physical_attack)
    print(skill.function())
    print(BERSERKIR_CHARACTER.bs.strength,
          BERSERKIR_CHARACTER.cs.hit_points,
          BERSERKIR_CHARACTER.cs.physical_attack)
    BERSERKIR_CHARACTER.skill_tree.learn_skill(HrungnirsSovereigntySkill)

    skill = FenrirsInstinctSkill(BERSERKIR_CHARACTER)
    print(skill)
    print(BERSERKIR_CHARACTER.bs.strength,
          BERSERKIR_CHARACTER.cs.hit_points,
          BERSERKIR_CHARACTER.cs.hit,
          BERSERKIR_CHARACTER.cs.evasion)
    print(skill.function())
    print(BERSERKIR_CHARACTER.bs.strength,
          BERSERKIR_CHARACTER.cs.hit_points,
          BERSERKIR_CHARACTER.cs.hit,
          BERSERKIR_CHARACTER.cs.evasion)
    BERSERKIR_CHARACTER.skill_tree.learn_skill(FenrirsInstinctSkill)

    skill = YmirsResilienceSkill(BERSERKIR_CHARACTER)
    print(skill)
    print(BERSERKIR_CHARACTER.bs.strength,
          BERSERKIR_CHARACTER.cs.hit_points,
          BERSERKIR_CHARACTER.cs.physical_defense,
          BERSERKIR_CHARACTER.cs.magical_defense)
    print(skill.function())
    print(BERSERKIR_CHARACTER.bs.strength,
          BERSERKIR_CHARACTER.cs.hit_points,
          BERSERKIR_CHARACTER.cs.physical_defense,
          BERSERKIR_CHARACTER.cs.magical_defense)
    BERSERKIR_CHARACTER.skill_tree.learn_skill(YmirsResilienceSkill)

    skill = StoneStrikeSkill(BERSERKIR_CHARACTER)
    print(skill)
    print(BERSERKIR_CHARACTER.cs.magical_attack)
    print(BERSERKIR_CHARACTER.to_attack(
        defender_char=BERSERKIR_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    BERSERKIR_CHARACTER.skill_tree.learn_skill(StoneStrikeSkill)
