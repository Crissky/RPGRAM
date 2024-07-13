from typing import TYPE_CHECKING

from rpgram.constants.text import (
    HIT_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum
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
    'name': 'Combate Primal',
    'description': (
        'A maestria do Bárbaro em combate corpo a corpo selvagem e brutal. '
        'As habilidades desse grupo se concentram em conceder ao Bárbaro '
        'ataques poderosos, manobras brutais e habilidades de '
        'combate instintivas.'
    )
}


class FuriousAttackSkill(BaseSkill):
    NAME = BarbarianSkillEnum.FURIOUS_ATTACK.value
    DESCRIPTION = (
        f'Realiza uma série de ataques rápidos e brutais, causando dano ao '
        f'inimigo com base em '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (200% + 5% x Rank x Nível), '
        f'mas possui uma baixa taxa de {HIT_EMOJI_TEXT}.'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.BARBARIAN.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 2
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 2.00,
        }
        damage_types = None

        super().__init__(
            name=FuriousAttackSkill.NAME,
            description=FuriousAttackSkill.DESCRIPTION,
            rank=FuriousAttackSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=FuriousAttackSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    @property
    def hit_multiplier(self) -> float:
        return 0.75


class WildStrikeSkill(BaseSkill):
    NAME = BarbarianSkillEnum.WILD_STRIKE.value
    DESCRIPTION = (
        f'Desfere um ataque com força bruta, causando dano ao '
        f'alvo com base em '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (210% + 5% x Rank x Nível), '
        f'mas possui uma baixa taxa de {HIT_EMOJI_TEXT}.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.BARBARIAN.value,
        'skill_list': [FuriousAttackSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 3
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 2.10,
        }
        damage_types = None

        super().__init__(
            name=WildStrikeSkill.NAME,
            description=WildStrikeSkill.DESCRIPTION,
            rank=WildStrikeSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=WildStrikeSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    @property
    def hit_multiplier(self) -> float:
        return 0.90


class WildRamSkill(BaseSkill):
    NAME = BarbarianSkillEnum.WILD_RAM.value
    DESCRIPTION = (
        f'Abaixa a cabeça e investe contra o inimigo como um '
        f'*Ariete de Guerra*, destruindo qualquer barreira antes de aplicar '
        f'o dano baseado em '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (160% + 5% x Rank x Nível), '
        f'mas possui uma baixa taxa de {HIT_EMOJI_TEXT}.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.BARBARIAN.value,
        'skill_list': [FuriousAttackSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 3
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.60,
        }
        damage_types = [DamageEnum.BLUDGEONING]

        super().__init__(
            name=WildRamSkill.NAME,
            description=WildRamSkill.DESCRIPTION,
            rank=WildRamSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=WildRamSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    @property
    def hit_multiplier(self) -> float:
        return 0.90

    def pre_hit_function(self, target: 'BaseCharacter') -> dict:
        report = {'text': ''}
        status_report = target.status.broken_all_barriers()
        if status_report['text']:
            report['text'] = status_report["text"]

        return report


class SeismicImpactSkill(BaseSkill):
    NAME = BarbarianSkillEnum.SEISMIC_IMPACT.value
    DESCRIPTION = (
        f'Com uma força descomunal, ergue sua arma e a golpeia violentamente '
        f'contra o chão, liberando uma onda de choque que faz a terra '
        f'tremer e se despedaçar ao redor, causando dano baseado em '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (132% + 2.5% x Rank x Nível), '
        f'mas possui uma baixa taxa de {HIT_EMOJI_TEXT}.'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.BARBARIAN.value,
        'skill_list': [FuriousAttackSkill.NAME, WildStrikeSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 3
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.32,
        }
        damage_types = [DamageEnum.GROUND, DamageEnum.GROUND]

        super().__init__(
            name=SeismicImpactSkill.NAME,
            description=SeismicImpactSkill.DESCRIPTION,
            rank=SeismicImpactSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.TEAM,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=SeismicImpactSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    @property
    def hit_multiplier(self) -> float:
        return 0.90


if __name__ == '__main__':
    from rpgram.constants.test import BARBARIAN_CHARACTER
    from rpgram.conditions.barrier import GuardianShieldCondition
    skill = FuriousAttackSkill(BARBARIAN_CHARACTER)
    print(skill)
    print(BARBARIAN_CHARACTER.cs.physical_attack)
    BARBARIAN_CHARACTER.skill_tree.learn_skill(FuriousAttackSkill)

    skill = WildStrikeSkill(BARBARIAN_CHARACTER)
    print(skill)
    print(BARBARIAN_CHARACTER.cs.physical_attack)
    BARBARIAN_CHARACTER.skill_tree.learn_skill(WildStrikeSkill)

    skill = WildRamSkill(BARBARIAN_CHARACTER)
    print(skill)
    print(BARBARIAN_CHARACTER.cs.physical_attack)
    barrier_condition = GuardianShieldCondition(power=50_000)
    BARBARIAN_CHARACTER.status.add_condition(barrier_condition)
    # print(skill.pre_hit_function(BARBARIAN_CHARACTER))
    print(BARBARIAN_CHARACTER.to_attack(
        defender_char=BARBARIAN_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    print(BARBARIAN_CHARACTER.status)
    BARBARIAN_CHARACTER.skill_tree.learn_skill(WildRamSkill)

    skill = SeismicImpactSkill(BARBARIAN_CHARACTER)
    print(skill)
    print(BARBARIAN_CHARACTER.cs.physical_attack)
    print(BARBARIAN_CHARACTER.to_attack(
        defender_char=BARBARIAN_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    print(BARBARIAN_CHARACTER.status)
    BARBARIAN_CHARACTER.skill_tree.learn_skill(SeismicImpactSkill)
