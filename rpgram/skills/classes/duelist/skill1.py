from typing import TYPE_CHECKING
from rpgram.constants.text import HIT_EMOJI_TEXT, PRECISION_ATTACK_EMOJI_TEXT
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.skill import (
    DuelistSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.classes.multiclasse.precision_attack import QuickAttackSkill
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class WindBladeSkill(BaseSkill):
    NAME = DuelistSkillEnum.WIND_BLADE.value
    DESCRIPTION = (
        f'Brande a arma com um único movimento rápido e imprevisível, '
        f'cortando o ar violentamente e '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.WIND)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.SLASHING)}* com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (100% + 5% x Rank x Nível). '
        f'Essa habilidade possui *{HIT_EMOJI_TEXT}* acima do normal.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.DUELIST.value,
        'skill_list': [QuickAttackSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.00
        }
        damage_types = [DamageEnum.WIND]

        super().__init__(
            name=WindBladeSkill.NAME,
            description=WindBladeSkill.DESCRIPTION,
            rank=WindBladeSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=WindBladeSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    @property
    def hit_multiplier(self) -> float:
        return 1.50


class SplashFountSkill(BaseSkill):
    NAME = DuelistSkillEnum.SPLASH_FOUNT.value
    DESCRIPTION = (
        f'Saca a arma com celeridade e desfere múltiplos ataques rápidos, '
        f'causando dano com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível). '
        f'Pode acertar o alvo diversas até 5 vezes '
        f'(cada acerto subsequente causa metade do dano).'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.DUELIST.value,
        'skill_list': [QuickAttackSkill.NAME, WindBladeSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.25
        }
        damage_types = None

        super().__init__(
            name=SplashFountSkill.NAME,
            description=SplashFountSkill.DESCRIPTION,
            rank=SplashFountSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=SplashFountSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def hit_function(
        self,
        target: 'BaseCharacter',
        damage: int,
        total_damage: int,
    ) -> dict:
        report = {'text': ''}
        total_attacks = int(self.dice.value / 5)
        report_text_list = []
        for i in range(total_attacks):
            if target.is_dead:
                break

            total_damage = int(total_damage / 2)
            damage_report = target.cs.damage_hit_points(value=total_damage)
            report_text_list.append(
                f'Ataque {i+2:02}: ' + damage_report['text']
            )
        report['text'] = '\n'.join(report_text_list)

        return report


SKILL_WAY_DESCRIPTION = {
    'name': 'Pés Ligeiros',
    'description': (
        ''
    ),
    'skill_list': [
        QuickAttackSkill,
        WindBladeSkill,
        SplashFountSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import DUELIST_CHARACTER

    skill = QuickAttackSkill(DUELIST_CHARACTER)
    print(skill)
    print(DUELIST_CHARACTER.cs.precision_attack)
    print(DUELIST_CHARACTER.to_attack(
        defender_char=DUELIST_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    DUELIST_CHARACTER.skill_tree.learn_skill(QuickAttackSkill)

    skill = WindBladeSkill(DUELIST_CHARACTER)
    print(skill)
    print(DUELIST_CHARACTER.cs.precision_attack)
    print(DUELIST_CHARACTER.to_attack(
        defender_char=DUELIST_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    DUELIST_CHARACTER.skill_tree.learn_skill(WindBladeSkill)

    skill = SplashFountSkill(DUELIST_CHARACTER)
    print(skill)
    print(DUELIST_CHARACTER.cs.precision_attack)
    print(DUELIST_CHARACTER.to_attack(
        defender_char=DUELIST_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    DUELIST_CHARACTER.skill_tree.learn_skill(SplashFountSkill)
