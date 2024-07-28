from typing import TYPE_CHECKING
from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.self_skill import (
    FrenzyCondition,
    FuriousFuryCondition,
    FuriousInstinctCondition
)
from rpgram.constants.text import (
    DEXTERITY_EMOJI_TEXT,
    HIT_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT,
    STRENGTH_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.skill import (
    BarbarianSkillEnum,
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
    'name': 'Fúria Implacável',
    'description': (
        'Caminho da fúria incontrolável do Bárbaro, a força bruta e a '
        'ferocidade que o definem em combate. '
        'As habilidades desse grupo se concentram em aumentar o dano do '
        'Bárbaro, sua resistência e sua capacidade de entrar em fúrias '
        'cada vez mais poderosas.'
    )
}


class FuriousFurySkill(BaseSkill):
    NAME = BarbarianSkillEnum.FURIOUS_FURY.value
    DESCRIPTION = (
        f'Entra em um estado de *Fúria* que o leva a agir *Furiosamente*, '
        f'aumentando o *{PHYSICAL_ATTACK_EMOJI_TEXT}* com base na '
        f'*{STRENGTH_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.BARBARIAN.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=FuriousFurySkill.NAME,
            description=FuriousFurySkill.DESCRIPTION,
            rank=FuriousFurySkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=FuriousFurySkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        condition = FuriousFuryCondition(character=char, level=level)
        report_list = self.char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* perde a concentração e entra em um estado '
                f'de *Fúria*, aumentando o seu '
                f'*{PHYSICAL_ATTACK_EMOJI_TEXT}*.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class FuriousInstinctSkill(BaseSkill):
    NAME = BarbarianSkillEnum.FURIOUS_INSTINCT.value
    DESCRIPTION = (
        f'Desperta *Furiosamente* um *Instinto* que amplifica seus sentidos e '
        f'afia suas habilidades de combate, aumentando a '
        f'*{DEXTERITY_EMOJI_TEXT}* (20% + 5% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.BARBARIAN.value,
        'skill_list': [FuriousFurySkill.NAME],
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=FuriousInstinctSkill.NAME,
            description=FuriousInstinctSkill.DESCRIPTION,
            rank=FuriousInstinctSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=FuriousInstinctSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        level = self.level_rank
        char = self.char
        condition = FuriousInstinctCondition(character=char, level=level)
        report_list = self.char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* desperta um instinto que amplifica seus '
                f'sentidos e afia suas habilidades de combate '
                f'aumentando a sua '
                f'*{DEXTERITY_EMOJI_TEXT}*.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class FrenzySkill(BaseSkill):
    NAME = BarbarianSkillEnum.FRENZY.value
    DESCRIPTION = (
        f'Entra em um estado de *Frenesi* que o leva a agir '
        f'como uma *Criatura Selvagem*, '
        f'afiando suas habilidades de combate, aprimorando a '
        f'*{STRENGTH_EMOJI_TEXT}* e a *{DEXTERITY_EMOJI_TEXT}* '
        f'(50% + 5% x Nível), mas pode, em um momento de insanidade, '
        f'atacar aliados ou a si mesmo.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.BARBARIAN.value,
        'skill_list': [FuriousFurySkill.NAME],
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=FrenzySkill.NAME,
            description=FrenzySkill.DESCRIPTION,
            rank=FrenzySkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=FrenzySkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        level = self.level_rank
        char = self.char
        condition = FrenzyCondition(character=char, level=level)
        report_list = self.char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* acessa um estado de *Frenesi*, '
                f'afiando suas habilidades de combate '
                f'aumentando a sua '
                f'*{STRENGTH_EMOJI_TEXT}* e *{DEXTERITY_EMOJI_TEXT}*.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class FuriousRoarSkill(BaseSkill):
    NAME = BarbarianSkillEnum.FURIOUS_ROAR.value
    DESCRIPTION = (
        f'Libera um *Rugido Aterrorizante* que despedaça a alma dos inimigos '
        f'com uma onda de terror que causa dano de '
        f'*{get_damage_emoji_text(DamageEnum.ROAR)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (87% + 2.5% x Rank x Nível), '
        f'mas possui uma baixa taxa de {HIT_EMOJI_TEXT}.'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.BARBARIAN.value,
        'skill_list': [
            FuriousFurySkill.NAME,
            FuriousInstinctSkill.NAME
        ],
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 0.87,
        }
        damage_types = [DamageEnum.ROAR]

        super().__init__(
            name=FuriousRoarSkill.NAME,
            description=FuriousRoarSkill.DESCRIPTION,
            rank=FuriousRoarSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.TEAM,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=FuriousRoarSkill.REQUIREMENTS,
            damage_types=damage_types
        )


if __name__ == '__main__':
    from rpgram.constants.test import BARBARIAN_CHARACTER
    skill = FuriousFurySkill(BARBARIAN_CHARACTER)
    print(skill)
    print(BARBARIAN_CHARACTER.bs.strength)
    print(BARBARIAN_CHARACTER.cs.physical_attack)
    print(skill.function())
    print(BARBARIAN_CHARACTER.cs.physical_attack)
    BARBARIAN_CHARACTER.skill_tree.learn_skill(FuriousFurySkill)

    skill = FuriousInstinctSkill(BARBARIAN_CHARACTER)
    print(skill)
    print(BARBARIAN_CHARACTER.bs.dexterity)
    print(BARBARIAN_CHARACTER.bs.multiplier_dexterity)
    print(skill.function())
    print(BARBARIAN_CHARACTER.bs.dexterity)
    print(BARBARIAN_CHARACTER.bs.multiplier_dexterity)
    BARBARIAN_CHARACTER.skill_tree.learn_skill(FuriousInstinctSkill)
    
    skill = FrenzySkill(BARBARIAN_CHARACTER)
    print(skill)
    print(BARBARIAN_CHARACTER.bs.strength)
    print(BARBARIAN_CHARACTER.bs.multiplier_strength)
    print(BARBARIAN_CHARACTER.bs.dexterity)
    print(BARBARIAN_CHARACTER.bs.multiplier_dexterity)
    print(skill.function())
    print(BARBARIAN_CHARACTER.bs.strength)
    print(BARBARIAN_CHARACTER.bs.multiplier_strength)
    print(BARBARIAN_CHARACTER.bs.dexterity)
    print(BARBARIAN_CHARACTER.bs.multiplier_dexterity)
    BARBARIAN_CHARACTER.skill_tree.learn_skill(FrenzySkill)

    skill = FuriousRoarSkill(BARBARIAN_CHARACTER)
    print(skill)
    print(BARBARIAN_CHARACTER.cs.physical_attack)
    BARBARIAN_CHARACTER.skill_tree.learn_skill(FuriousRoarSkill)
