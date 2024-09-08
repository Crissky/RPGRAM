
from typing import TYPE_CHECKING
from rpgram.conditions.debuff import DeathSentenceCondition, SilenceCondition
from rpgram.constants.text import (
    HIT_EMOJI_TEXT,
    PRECISION_ATTACK_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.debuff import DebuffEnum, get_debuff_emoji_text
from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.skill import (
    LordOfTheRoguesSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.classes.multiclasse.precision_attack import (
    QuickAttackSkill
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class SilentAssassinSkill(BaseSkill):
    NAME = LordOfTheRoguesSkillEnum.SILENT_ASSASSIN.value
    DESCRIPTION = (
        f'Move-se com a agilidade de uma sombra e desfere um golpe lôbrego, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.DARK)}* com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (100% + 5% x Rank x Nível) e '
        f'adicionando a condição '
        f'*{get_debuff_emoji_text(DebuffEnum.SILENCE)}* com nível igual ao '
        f'(Rank x Nível) se tirar 15{EmojiEnum.DICE.value} ou mais. '
        f'Essa habilidade possui *{HIT_EMOJI_TEXT}* acima do normal.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.LORD_OF_THE_ROGUES.value,
        'skill_list': [QuickAttackSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.00
        }
        damage_types = [DamageEnum.DARK]

        super().__init__(
            name=SilentAssassinSkill.NAME,
            description=SilentAssassinSkill.DESCRIPTION,
            rank=SilentAssassinSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=SilentAssassinSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def hit_function(
        self,
        target: 'BaseCharacter',
        damage: int,
        total_damage: int,
    ) -> dict:
        report = {'text': ''}
        if target.is_alive and self.dice.value >= 15:
            level = self.level_rank
            silence_condition = SilenceCondition(level=level)
            status_report = target.status.add_condition(silence_condition)
            report['status_text'] = status_report['text']

        return report

    @property
    def hit_multiplier(self) -> float:
        return 1.50


class DeadlyBladeSkill(BaseSkill):
    NAME = LordOfTheRoguesSkillEnum.DEADLY_BLADE.value
    DESCRIPTION = (
        f'Desfere um golpe fatal em um ponto vital do inimigo, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.DARK)}* com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível) e '
        f'adicionando a condição '
        f'*{get_debuff_emoji_text(DebuffEnum.DEATH_SENTENCE)}* '
        f'com nível igual ao (Rank x Nível). '
        f'Mata o oponente se for *Acerto Crítico*{EmojiEnum.DICE.value}. '
        f'Essa habilidade possui *{HIT_EMOJI_TEXT}* acima do normal.'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.LORD_OF_THE_ROGUES.value,
        'skill_list': [QuickAttackSkill.NAME, SilentAssassinSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.25
        }
        damage_types = [DamageEnum.DARK]

        super().__init__(
            name=DeadlyBladeSkill.NAME,
            description=DeadlyBladeSkill.DESCRIPTION,
            rank=DeadlyBladeSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=DeadlyBladeSkill.REQUIREMENTS,
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
        elif target.is_alive:
            level = self.level_rank
            silence_condition = DeathSentenceCondition(level=level)
            status_report = target.status.add_condition(silence_condition)
            report['status_text'] = status_report['text']

        return report

    @property
    def hit_multiplier(self) -> float:
        return 1.50


SKILL_WAY_DESCRIPTION = {
    'name': 'Mestre dos Assassinos',
    'description': (
        'Mestre na morte, um predador que opera nas sombras. '
        'Sua vida é dedicada à perfeição da arte do assassinato, '
        'desenvolvendo uma habilidade inigualável para eliminar seus alvos '
        'de forma silenciosa e eficiente.'
        'O Mestre dos Assassinos é um artífice da morte, '
        'capaz de eliminar seus inimigos, utilizando o fio da lâmina e '
        'venenos letais para infligir feridas fatais.'
    ),
    'skill_list': [
        QuickAttackSkill,
        SilentAssassinSkill,
        DeadlyBladeSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import LORD_OF_THE_ROGUES_CHARACTER

    skill = QuickAttackSkill(LORD_OF_THE_ROGUES_CHARACTER)
    print(skill)
    print(LORD_OF_THE_ROGUES_CHARACTER.cs.precision_attack)
    print(LORD_OF_THE_ROGUES_CHARACTER.to_attack(
        defender_char=LORD_OF_THE_ROGUES_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    LORD_OF_THE_ROGUES_CHARACTER.skill_tree.learn_skill(QuickAttackSkill)

    skill = SilentAssassinSkill(LORD_OF_THE_ROGUES_CHARACTER)
    print(skill)
    print(LORD_OF_THE_ROGUES_CHARACTER.cs.precision_attack)
    print(LORD_OF_THE_ROGUES_CHARACTER.to_attack(
        defender_char=LORD_OF_THE_ROGUES_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    LORD_OF_THE_ROGUES_CHARACTER.skill_tree.learn_skill(SilentAssassinSkill)

    skill = DeadlyBladeSkill(LORD_OF_THE_ROGUES_CHARACTER)
    print(skill)
    print(LORD_OF_THE_ROGUES_CHARACTER.cs.precision_attack)
    print(LORD_OF_THE_ROGUES_CHARACTER.to_attack(
        defender_char=LORD_OF_THE_ROGUES_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    LORD_OF_THE_ROGUES_CHARACTER.skill_tree.learn_skill(DeadlyBladeSkill)
