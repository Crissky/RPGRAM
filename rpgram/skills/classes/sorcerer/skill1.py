from typing import TYPE_CHECKING
from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.self_skill import (
    MysticalConfluenceCondition,
    MysticalProtectionCondition,
    MysticalVigorCondition
)
from rpgram.constants.text import (
    HIT_POINT_FULL_EMOJI_TEXT,
    INTELLIGENCE_EMOJI_TEXT,
    MAGICAL_ATTACK_EMOJI_TEXT,
    MAGICAL_DEFENSE_EMOJI_TEXT,
    WISDOM_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.skill import (
    SkillDefenseEnum,
    SkillTypeEnum,
    SorcererSkillEnum,
    TargetEnum
)
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill

if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class MysticalProtectionSkill(BaseSkill):
    NAME = SorcererSkillEnum.MYSTICAL_PROTECTION.value
    DESCRIPTION = (
        f'Tece uma *Trama de Energia Mística* que concede '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* com base na '
        f'*{WISDOM_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.SORCERER.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=MysticalProtectionSkill.NAME,
            description=MysticalProtectionSkill.DESCRIPTION,
            rank=MysticalProtectionSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=MysticalProtectionSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        level = self.level_rank
        char = self.char
        condition = MysticalProtectionCondition(character=char, level=level)
        report_list = self.char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* com movimentos simples, tece uma '
                f'*Trama de Energia Mística*, '
                f'aumentando a '
                f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* '
                f'em {condition.bonus_magical_defense} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class MysticalConfluenceSkill(BaseSkill):
    NAME = SorcererSkillEnum.MYSTICAL_CONFLUENCE.value
    DESCRIPTION = (
        f'Manipulando os fluxos da magia, entrelaça diferentes tipos de '
        f'*Energias Místicas* para amplificar seu '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* com base na '
        f'*{INTELLIGENCE_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.SORCERER.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=MysticalConfluenceSkill.NAME,
            description=MysticalConfluenceSkill.DESCRIPTION,
            rank=MysticalConfluenceSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=MysticalConfluenceSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        condition = MysticalConfluenceCondition(character=char, level=level)
        report_list = self.char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* com movimentos precisos, '
                f'entrelaça diferentes tipos de '
                f'*Energias Místicas*, '
                f'aumentando o '
                f'*{MAGICAL_ATTACK_EMOJI_TEXT}* '
                f'em {condition.bonus_magical_attack} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class MysticalVigorSkill(BaseSkill):
    NAME = SorcererSkillEnum.MYSTICAL_VIGOR.value
    DESCRIPTION = (
        f'Evoca *Energias Místicas* para fortalecer o seu espírito '
        f'aumentando o *{HIT_POINT_FULL_EMOJI_TEXT}* com base na '
        f'*{INTELLIGENCE_EMOJI_TEXT}* (200% + 20% x Rank x Nível) '
        f'e na *{WISDOM_EMOJI_TEXT}* (200% + 20% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.SORCERER.value,
        'skill_list': [MysticalProtectionSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=MysticalVigorSkill.NAME,
            description=MysticalVigorSkill.DESCRIPTION,
            rank=MysticalVigorSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=MysticalVigorSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        condition = MysticalVigorCondition(character=char, level=level)
        report_list = self.char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* controlando a respiração, '
                f'evoca *Energias Místicas* para fortalecer o seu espírito, '
                f'aumentando o '
                f'*{HIT_POINT_FULL_EMOJI_TEXT}* '
                f'em {condition.bonus_hit_points} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


SKILL_WAY_DESCRIPTION = {
    'name': 'Poder Inato',
    'description': (
        'O caminho da conexão inata do Feiticeiro com a magia, '
        'sua capacidade de manipular energias místicas e '
        'moldá-las à sua vontade. '
        'As habilidades desse grupo se concentram em aprimorar o poder bruto '
        'das magias do Feiticeiro, sua capacidade de lançá-las com mais '
        'eficiência, e sua resistência a efeitos mágicos.'
    ),
    'skill_list': [
        MysticalProtectionSkill,
        MysticalConfluenceSkill,
        MysticalVigorSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import SORCERER_CHARACTER

    skill = MysticalProtectionSkill(SORCERER_CHARACTER)
    print(skill)
    print(SORCERER_CHARACTER.bs.wisdom)
    print(SORCERER_CHARACTER.cs.magical_defense)
    print(skill.function())
    print(SORCERER_CHARACTER.cs.magical_defense)
    SORCERER_CHARACTER.skill_tree.learn_skill(MysticalProtectionSkill)

    skill = MysticalConfluenceSkill(SORCERER_CHARACTER)
    print(skill)
    print(SORCERER_CHARACTER.bs.intelligence)
    print(SORCERER_CHARACTER.cs.magical_attack)
    print(skill.function())
    print(SORCERER_CHARACTER.cs.magical_attack)
    SORCERER_CHARACTER.skill_tree.learn_skill(MysticalConfluenceSkill)

    skill = MysticalVigorSkill(SORCERER_CHARACTER)
    print(skill)
    print(SORCERER_CHARACTER.bs.intelligence)
    print(SORCERER_CHARACTER.bs.wisdom)
    print(SORCERER_CHARACTER.cs.hit_points)
    print(skill.function())
    print(SORCERER_CHARACTER.cs.hit_points)
    SORCERER_CHARACTER.skill_tree.learn_skill(MysticalVigorSkill)
