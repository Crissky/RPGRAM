from typing import TYPE_CHECKING

from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.target_skill_buff import (
    BoneArmorCondition,
    BoneBucklerCondition,
    BoneSpaulderCondition
)
from rpgram.constants.text import (
    INTELLIGENCE_EMOJI_TEXT,
    PHYSICAL_DEFENSE_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.skill import (
    NecromancerSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class BoneBucklerSkill(BaseSkill):
    NAME = NecromancerSkillEnum.BONE_BUCKLER.value
    DESCRIPTION = (
        'Constrói um *Escudo Esquelético* feito de '
        '*Ossos* e *Névoa Necromântica*, '
        'aumentando a '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* com base na '
        f'*{INTELLIGENCE_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.NECROMANCER.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=BoneBucklerSkill.NAME,
            description=BoneBucklerSkill.DESCRIPTION,
            rank=BoneBucklerSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=BoneBucklerSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        power = char.cs.intelligence
        condition = BoneBucklerCondition(power=power, level=level)
        report_list = char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* cria e equipa um *{self.name}*, '
                'aumentando a '
                f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* '
                f'em {condition.bonus_physical_defense} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class BoneSpaulderSkill(BaseSkill):
    NAME = NecromancerSkillEnum.BONE_SPAULDER.value
    DESCRIPTION = (
        'Forja uma *Espaldeira Esquelética* feita de '
        '*Ossos* e *Névoa Necromântica* e que '
        'aumenta a '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* com base na '
        f'*{INTELLIGENCE_EMOJI_TEXT}* (200% + 10% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.NECROMANCER.value,
        'skill_list': [BoneBucklerSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=BoneSpaulderSkill.NAME,
            description=BoneSpaulderSkill.DESCRIPTION,
            rank=BoneSpaulderSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=BoneSpaulderSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        power = char.cs.intelligence
        condition = BoneSpaulderCondition(power=power, level=level)
        report_list = char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* cria e equipa uma *{self.name}*, '
                'aumentando a '
                f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* '
                f'em {condition.bonus_physical_defense} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class BoneArmorSkill(BaseSkill):
    NAME = NecromancerSkillEnum.BONE_ARMOR.value
    DESCRIPTION = (
        'Forja uma *Armadura Esquelética* com placas feitas de '
        '*Ossos* e *Névoa Necromântica* e que '
        'aumenta a '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* com base na '
        f'*{INTELLIGENCE_EMOJI_TEXT}* (300% + 10% x Rank x Nível).'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.NECROMANCER.value,
        'skill_list': [BoneBucklerSkill.NAME, BoneSpaulderSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=BoneArmorSkill.NAME,
            description=BoneArmorSkill.DESCRIPTION,
            rank=BoneArmorSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=BoneArmorSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        power = char.cs.intelligence
        condition = BoneArmorCondition(power=power, level=level)
        report_list = char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* cria e equipa uma *{self.name}*, '
                'aumentando a '
                f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* '
                f'em {condition.bonus_physical_defense} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


SKILL_WAY_DESCRIPTION = {
    'name': 'Ossífice',
    'description': (
        'Um mestre da necromancia que se especializa na manipulação de '
        'ossos e esqueletos. '
        'Ele vê a morte não como um fim, mas como um novo começo, '
        'uma oportunidade para criar algo belo e terrível a partir '
        'daquilo que foi deixado para trás. '
        'Ele possui um profundo entendimento da estrutura óssea e '
        'da magia necromântica, '
        'permitindo-lhe manipular ossos de forma quase orgânica. '
        'Com isso, pode criar armas e armaduras ósseas ou até '
        'erguer construtos ósseos gigantescos.'
    ),
    'skill_list': [
        BoneBucklerSkill,
        BoneSpaulderSkill,
        BoneArmorSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import NECROMANCER_CHARACTER

    skill = BoneBucklerSkill(NECROMANCER_CHARACTER)
    print(skill)
    print(NECROMANCER_CHARACTER.cs.intelligence)
    print(NECROMANCER_CHARACTER.cs.physical_defense)
    print(skill.function())
    print(NECROMANCER_CHARACTER.cs.physical_defense)
    NECROMANCER_CHARACTER.skill_tree.learn_skill(BoneBucklerSkill)

    skill = BoneSpaulderSkill(NECROMANCER_CHARACTER)
    print(skill)
    print(NECROMANCER_CHARACTER.cs.intelligence)
    print(NECROMANCER_CHARACTER.cs.physical_defense)
    print(skill.function())
    print(NECROMANCER_CHARACTER.cs.physical_defense)
    NECROMANCER_CHARACTER.skill_tree.learn_skill(BoneSpaulderSkill)

    skill = BoneArmorSkill(NECROMANCER_CHARACTER)
    print(skill)
    print(NECROMANCER_CHARACTER.cs.intelligence)
    print(NECROMANCER_CHARACTER.cs.physical_defense)
    print(skill.function())
    print(NECROMANCER_CHARACTER.cs.physical_defense)
    NECROMANCER_CHARACTER.skill_tree.learn_skill(BoneArmorSkill)
