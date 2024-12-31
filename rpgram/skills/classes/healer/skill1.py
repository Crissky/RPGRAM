from typing import TYPE_CHECKING

from constant.text import ALERT_SECTION_HEAD, ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.barrier import ProtectiveAuraCondition
from rpgram.conditions.target_skill_buff import (
    VitalityAuraCondition
)
from rpgram.constants.text import (
    HIT_POINT_FULL_EMOJI_TEXT,
    INTELLIGENCE_EMOJI_TEXT,
    MAGICAL_DEFENSE_EMOJI_TEXT,
    WISDOM_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.skill import (
    HealerSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class HealingTouchSkill(BaseSkill):
    NAME = HealerSkillEnum.HEALING_TOUCH.value
    DESCRIPTION = (
        f'Canaliza *Energia Vital* para, com um simples toque, '
        f'curar o *{HIT_POINT_FULL_EMOJI_TEXT}* de um aliado '
        f'com base na *{MAGICAL_DEFENSE_EMOJI_TEXT}* '
        f'(200% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.HEALER.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=HealingTouchSkill.NAME,
            description=HealingTouchSkill.DESCRIPTION,
            rank=HealingTouchSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.HEALING,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=HealingTouchSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        target_name = char.player_name
        if char.is_alive:
            dice = self.dice
            level = self.level_rank
            power_multiplier = 2 + (level / 10)
            power = dice.boosted_magical_defense * power_multiplier
            power = round(power)

            cure_report = char.cs.cure_hit_points(power)
            report_text = cure_report["text"]
            report = {
                'text': (
                    f'*{target_name}* é revigorado pelo *{self.name}*.\n'
                    f'*{report_text}*({dice.text}).'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


class HealingHerbSkill(BaseSkill):
    NAME = HealerSkillEnum.HEALING_HERB.value
    DESCRIPTION = (
        f'Imbui um punhado de ervas com *Energia Vital*, '
        f'atribuindo-lhe propriedades terapêuticas '
        f'para curar até (5 x Rank x Nível) níveis de condições aleatórias '
        f'de um aliado.'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.HEALER.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=HealingHerbSkill.NAME,
            description=HealingHerbSkill.DESCRIPTION,
            rank=HealingHerbSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.HEALING,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=HealingHerbSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        target_name = char.player_name
        if char.is_alive:
            level = self.level_rank
            quantity = int(5 * level)
            status_report = char.status.remove_random_debuff_conditions(
                quantity=quantity
            )
            report_text = status_report["text"]
            if report_text:
                alert_section_head_status = ALERT_SECTION_HEAD.format(
                    f'*STATUS ({quantity})*'
                )
                report_text = f'\n\n{alert_section_head_status}{report_text}'
            report = {
                'text': (
                    f'*{target_name}* é tratado pela *{self.name}*.'
                    f'{report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


class VitalityAuraSkill(BaseSkill):
    NAME = HealerSkillEnum.VITALITY_AURA.value
    DESCRIPTION = (
        f'Cria uma aura usando a *Energia Vital*, '
        f'melhorando a vitalidade de um aliado, '
        f'aumentando seu *{HIT_POINT_FULL_EMOJI_TEXT}* com base na '
        f'*{INTELLIGENCE_EMOJI_TEXT}* e na *{WISDOM_EMOJI_TEXT}* '
        f'(200% + 20% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.HEALER.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=VitalityAuraSkill.NAME,
            description=VitalityAuraSkill.DESCRIPTION,
            rank=VitalityAuraSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=VitalityAuraSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        target_name = char.player_name
        if char.is_alive:
            level = self.level_rank
            power = self.char.cs.intelligence + self.char.cs.wisdom
            condition = VitalityAuraCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{target_name}* é envolvido pela *{self.name}* '
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


class ReviveRitualSkill(BaseSkill):
    NAME = HealerSkillEnum.REVIVE_RITUAL.value
    DESCRIPTION = (
        f'Realiza um *Ritual Sagrado*, concentrando *Energia Vital* '
        f'que permite trazer um aliado caído de volta à vida, '
        f'desafiando as leis da morte, '
        f'curando o *{HIT_POINT_FULL_EMOJI_TEXT}* de um aliado '
        f'com base na *{MAGICAL_DEFENSE_EMOJI_TEXT}* '
        f'(200% + 10% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.HEALER.value,
        'skill_list': [
            HealingTouchSkill.NAME,
            HealingHerbSkill.NAME,
            VitalityAuraSkill.NAME
        ]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=ReviveRitualSkill.NAME,
            description=ReviveRitualSkill.DESCRIPTION,
            rank=ReviveRitualSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.HEALING,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=ReviveRitualSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        target_name = char.player_name
        if char.is_dead:
            dice = self.dice
            level = self.level_rank
            power_multiplier = 2 + (level / 10)
            power = dice.boosted_magical_defense * power_multiplier
            power = round(power)

            cure_report = char.cs.revive(power)
            report_text = cure_report["text"]
            report = {
                'text': (
                    f'*{target_name}* é revivido pelo *{self.name}*.\n'
                    f'*{report_text}*({dice.text}).'
                )
            }
        else:
            report = {'text': f'*{target_name}* está vivo.'}

        return report


SKILL_WAY_DESCRIPTION = {
    'name': 'Senhor da Vida',
    'description': (
        'O Senhor da Vida é um guardião da existência, '
        'um defensor da vida em todas as suas formas. '
        'Sua conexão com a força vital do universo é profunda, '
        'permitindo-lhe curar feridas, prolongar vidas e até mesmo '
        'trazer os mortos de volta à vida.'
    ),
    'skill_list': [
        HealingTouchSkill,
        HealingHerbSkill,
        VitalityAuraSkill,
        ReviveRitualSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.conditions.debuff import CurseCondition
    from rpgram.constants.test import HEALER_CHARACTER

    skill = HealingTouchSkill(HEALER_CHARACTER)
    print(skill)
    print(HEALER_CHARACTER.cs.show_hit_points)
    print(skill.function(HEALER_CHARACTER))
    print(HEALER_CHARACTER.cs.show_hit_points)
    HEALER_CHARACTER.skill_tree.learn_skill(HealingTouchSkill)

    HEALER_CHARACTER.status.add_condition(CurseCondition(level=10))
    skill = HealingHerbSkill(HEALER_CHARACTER)
    print(skill)
    print(HEALER_CHARACTER.cs.show_hit_points)
    print(skill.function(HEALER_CHARACTER))
    print(HEALER_CHARACTER.cs.show_hit_points)
    HEALER_CHARACTER.skill_tree.learn_skill(HealingHerbSkill)

    skill = VitalityAuraSkill(HEALER_CHARACTER)
    print(skill)
    print(HEALER_CHARACTER.cs.intelligence, HEALER_CHARACTER.cs.wisdom)
    print(HEALER_CHARACTER.cs.hit_points)
    print(skill.function(HEALER_CHARACTER))
    print(HEALER_CHARACTER.cs.hit_points)
    HEALER_CHARACTER.skill_tree.learn_skill(VitalityAuraSkill)

    HEALER_CHARACTER.cs.damage_hit_points(20_000)
    skill = ReviveRitualSkill(HEALER_CHARACTER)
    print(skill)
    print(HEALER_CHARACTER.cs.show_hit_points)
    print(skill.function(HEALER_CHARACTER))
    print(HEALER_CHARACTER.cs.show_hit_points)
    HEALER_CHARACTER.skill_tree.learn_skill(ReviveRitualSkill)
