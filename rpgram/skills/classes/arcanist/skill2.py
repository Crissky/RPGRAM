from typing import TYPE_CHECKING
from rpgram.conditions.debuff import BlindnessCondition
from rpgram.constants.text import MAGICAL_ATTACK_EMOJI_TEXT
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.debuff import DebuffEnum, get_debuff_emoji_text
from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.skill import (
    ArcanistSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.classes.multiclasse.magical_attack import (
    PrismaticShotSkill
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class DarkShotSkill(BaseSkill):
    NAME = ArcanistSkillEnum.DARK_SHOT.value
    DESCRIPTION = (
        f'Canaliza a *Energia Mágica* e dispara um *Feixe Trevoso*, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.DARK)}* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (100% + 5% x Rank x Nível) e '
        f'adicionando a condição '
        f'*{get_debuff_emoji_text(DebuffEnum.BLINDNESS)}* com nível igual ao '
        f'(Rank x Nível) se for *Acerto Crítico*{EmojiEnum.DICE.value}.'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.ARCANIST.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 1.00,
        }
        damage_types = [DamageEnum.DARK]

        super().__init__(
            name=DarkShotSkill.NAME,
            description=DarkShotSkill.DESCRIPTION,
            rank=DarkShotSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=DarkShotSkill.REQUIREMENTS,
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
            level = self.level_rank
            blindness_condition = BlindnessCondition(level=level)
            status_report = target.status.add_condition(blindness_condition)
            report['status_text'] = status_report['text']

        return report


class PrismaticAbrumationSkill(BaseSkill):
    NAME = ArcanistSkillEnum.PRISMATIC_ABRUMATION.value
    DESCRIPTION = (
        f'Canaliza a *Energia Mágica*, criando e lançando um *Artefato '
        f'Trevoso* que causa dano de '
        f'*{get_damage_emoji_text(DamageEnum.DARK)}* '
        f'a *TODES os inimigos* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (62% + 2.5% x Rank x Nível) e '
        f'adicionando a condição '
        f'*{get_debuff_emoji_text(DebuffEnum.BLINDNESS)}* com nível igual ao '
        f'(Rank x Nível) se tirar 15{EmojiEnum.DICE.value} ou mais.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.ARCANIST.value,
        'skill_list': [DarkShotSkill.NAME],
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 0.75,
        }
        damage_types = [DamageEnum.DARK]

        super().__init__(
            name=PrismaticAbrumationSkill.NAME,
            description=PrismaticAbrumationSkill.DESCRIPTION,
            rank=PrismaticAbrumationSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.TEAM,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=PrismaticAbrumationSkill.REQUIREMENTS,
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
            blindness_condition = BlindnessCondition(level=level)
            status_report = target.status.add_condition(blindness_condition)
            report['status_text'] = status_report['text']

        return report


SKILL_WAY_DESCRIPTION = {
    'name': 'Arcano Crepúscular',
    'description': (
        'O Arcano Crepúscular possui uma alma intrinsecamente ligada aos '
        'elementos Luz e Trevas. '
        'Ele é um canal, um condutor de forças essenciais que '
        'moldam a realidade. '
        'Sua compreensão dos elementos não se limita a simples '
        'manipulação; ele os sente, os compreende e os respeita.'
    ),
    'skill_list': [
        PrismaticShotSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import ARCANIST_CHARACTER

    skill = PrismaticShotSkill(ARCANIST_CHARACTER)
    print(skill)
    print(ARCANIST_CHARACTER.cs.magical_attack)
    print(ARCANIST_CHARACTER.to_attack(
        defender_char=ARCANIST_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    ARCANIST_CHARACTER.skill_tree.learn_skill(PrismaticShotSkill)

    skill = DarkShotSkill(ARCANIST_CHARACTER)
    print(skill)
    print(ARCANIST_CHARACTER.cs.magical_attack)
    print(ARCANIST_CHARACTER.to_attack(
        defender_char=ARCANIST_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    ARCANIST_CHARACTER.skill_tree.learn_skill(DarkShotSkill)

    skill = PrismaticAbrumationSkill(ARCANIST_CHARACTER)
    print(skill)
    print(ARCANIST_CHARACTER.cs.magical_attack)
    print(ARCANIST_CHARACTER.to_attack(
        defender_char=ARCANIST_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    ARCANIST_CHARACTER.skill_tree.learn_skill(PrismaticAbrumationSkill)
