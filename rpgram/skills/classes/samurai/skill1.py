from typing import TYPE_CHECKING
from rpgram.conditions.debuff import StunnedCondition
from rpgram.conditions.target_skill_debuff import (
    DoUchiCondition,
    KoteUchiCondition
)
from rpgram.constants.text import (
    PHYSICAL_ATTACK_EMOJI_TEXT,
    PHYSICAL_DEFENSE_EMOJI_TEXT,
    PRECISION_ATTACK_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.debuff import DebuffEnum, get_debuff_emoji_text
from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.skill import (
    SamuraiSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class KoteUchiSkill(BaseSkill):
    NAME = SamuraiSkillEnum.KOTE_UCHI.value
    DESCRIPTION = (
        f'Primeiro movimento: ataque que *Desestabiliza os Braços* '
        f'do oponente, '
        f'causa dano com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível) e '
        f'reduz o '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* e o '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* '
        f'com base no dano causado (10% + 1% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.SAMURAI.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.25
        }
        damage_types = None

        super().__init__(
            name=KoteUchiSkill.NAME,
            description=KoteUchiSkill.DESCRIPTION,
            rank=KoteUchiSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=KoteUchiSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def hit_function(
        self,
        target: 'BaseCharacter',
        damage: int,
        total_damage: int,
    ) -> dict:
        report = {'text': ''}
        if target.is_alive:
            power = int(total_damage)
            level = self.level_rank
            condition = KoteUchiCondition(power=power, level=level)
            status_report_list = target.status.set_powerful_conditions(
                condition
            )
            status_report_text = "\n".join(
                [report["text"] for report in status_report_list]
            )
            report['status_text'] = status_report_text

        return report


class DoUchiSkill(BaseSkill):
    NAME = SamuraiSkillEnum.DO_UCHI.value
    DESCRIPTION = (
        f'Segundo movimento: ataque que *Desestabiliza o Tronco* '
        f'do oponente, '
        f'causa dano com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (150% + 5% x Rank x Nível) e '
        f'reduz a '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* '
        f'com base no dano causado (10% + 1% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.SAMURAI.value,
        'skill_list': [KoteUchiSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.50
        }
        damage_types = None

        super().__init__(
            name=DoUchiSkill.NAME,
            description=DoUchiSkill.DESCRIPTION,
            rank=DoUchiSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=DoUchiSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def hit_function(
        self,
        target: 'BaseCharacter',
        damage: int,
        total_damage: int,
    ) -> dict:
        report = {'text': ''}
        if target.is_alive:
            power = int(total_damage)
            level = self.level_rank
            condition = DoUchiCondition(power=power, level=level)
            status_report_list = target.status.set_powerful_conditions(
                condition
            )
            status_report_text = "\n".join(
                [report["text"] for report in status_report_list]
            )
            report['status_text'] = status_report_text

        return report


class MenUchiSkill(BaseSkill):
    NAME = SamuraiSkillEnum.MEN_UCHI.value
    DESCRIPTION = (
        f'Terceiro movimento: ataque que visa a cabeça '
        f'do oponente, '
        f'causa dano com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (175% + 5% x Rank x Nível) e '
        f'adiciona a condição '
        f'*{get_debuff_emoji_text(DebuffEnum.STUNNED)}* com nível igual ao '
        f'(Rank x Nível) se tirar 10{EmojiEnum.DICE.value} ou mais. '
        f'Mata o oponente se for *Acerto Crítico*{EmojiEnum.DICE.value}. '
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.SAMURAI.value,
        'skill_list': [KoteUchiSkill.NAME, DoUchiSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.75
        }
        damage_types = None

        super().__init__(
            name=MenUchiSkill.NAME,
            description=MenUchiSkill.DESCRIPTION,
            rank=MenUchiSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=MenUchiSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def hit_function(
        self,
        target: 'BaseCharacter',
        damage: int,
        total_damage: int,
    ) -> dict:
        report = {'text': ''}
        if target.is_alive and self.dice.is_critical:
            extra_damage = target.cs.hit_points
            damage_report = target.cs.damage_hit_points(
                value=extra_damage,
                ignore_barrier=True
            )
            report['text'] = damage_report['text']
        elif target.is_alive and self.dice.value >= 10:
            level = self.level_rank
            stunned_condition = StunnedCondition(level=level)
            status_report = target.status.add_condition(stunned_condition)
            report['status_text'] = status_report['text']

        return report


SKILL_WAY_DESCRIPTION = {
    'name': '',
    'description': (
        ''
    ),
    'skill_list': []
}


if __name__ == '__main__':
    from rpgram.constants.test import SAMURAI_CHARACTER

    skill = KoteUchiSkill(SAMURAI_CHARACTER)
    print(skill)
    print(SAMURAI_CHARACTER.cs.precision_attack)
    print(SAMURAI_CHARACTER.to_attack(
        defender_char=SAMURAI_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    SAMURAI_CHARACTER.skill_tree.learn_skill(KoteUchiSkill)

    skill = DoUchiSkill(SAMURAI_CHARACTER)
    print(skill)
    print(SAMURAI_CHARACTER.cs.precision_attack)
    print(SAMURAI_CHARACTER.to_attack(
        defender_char=SAMURAI_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    SAMURAI_CHARACTER.skill_tree.learn_skill(DoUchiSkill)

    skill = MenUchiSkill(SAMURAI_CHARACTER)
    print(skill)
    print(SAMURAI_CHARACTER.cs.precision_attack)
    print(SAMURAI_CHARACTER.to_attack(
        defender_char=SAMURAI_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    SAMURAI_CHARACTER.skill_tree.learn_skill(MenUchiSkill)
