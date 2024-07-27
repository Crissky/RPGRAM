from typing import TYPE_CHECKING

from rpgram.constants.text import (
    HIT_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT
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
    'name': 'Combate Primal',
    'description': (
        'A maestria do Bárbaro em combate corpo a corpo selvagem e brutal. '
        'As habilidades desse grupo se concentram em conceder ao Bárbaro '
        'ataques poderosos, manobras brutais e habilidades de '
        'combate instintivas.'
    )
}


class PrimalAttackSkill(BaseSkill):
    NAME = BarbarianSkillEnum.PRIMAL_ATTACK.value
    DESCRIPTION = (
        f'Realiza uma série de ataques rápidos e brutais, causando dano ao '
        f'inimigo com base no '
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
            name=PrimalAttackSkill.NAME,
            description=PrimalAttackSkill.DESCRIPTION,
            rank=PrimalAttackSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=PrimalAttackSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    @property
    def hit_multiplier(self) -> float:
        return 0.75


class PrimalStrikeSkill(BaseSkill):
    NAME = BarbarianSkillEnum.PRIMAL_STRIKE.value
    DESCRIPTION = (
        f'Desfere um ataque com força bruta, causando dano ao '
        f'alvo com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (210% + 5% x Rank x Nível), '
        f'mas possui uma baixa taxa de {HIT_EMOJI_TEXT}.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.BARBARIAN.value,
        'skill_list': [PrimalAttackSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 3
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 2.10,
        }
        damage_types = None

        super().__init__(
            name=PrimalStrikeSkill.NAME,
            description=PrimalStrikeSkill.DESCRIPTION,
            rank=PrimalStrikeSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=PrimalStrikeSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    @property
    def hit_multiplier(self) -> float:
        return 0.90


class PrimalRamSkill(BaseSkill):
    NAME = BarbarianSkillEnum.PRIMAL_RAM.value
    DESCRIPTION = (
        f'Abaixa a cabeça e investe contra o inimigo como um '
        f'*Ariete de Guerra*, destruindo qualquer barreira antes de aplicar '
        f'o dano de '
        f'*{get_damage_emoji_text(DamageEnum.BLUDGEONING)}* baseado em '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (160% + 5% x Rank x Nível), '
        f'mas possui uma baixa taxa de {HIT_EMOJI_TEXT}.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.BARBARIAN.value,
        'skill_list': [PrimalAttackSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 3
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.60,
        }
        damage_types = [DamageEnum.BLUDGEONING]

        super().__init__(
            name=PrimalRamSkill.NAME,
            description=PrimalRamSkill.DESCRIPTION,
            rank=PrimalRamSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=PrimalRamSkill.REQUIREMENTS,
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
        f'tremer e se despedaçar ao redor, causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.GROUND)}* baseado em '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (132% + 2.5% x Rank x Nível), '
        f'mas possui uma baixa taxa de {HIT_EMOJI_TEXT}.'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.BARBARIAN.value,
        'skill_list': [PrimalAttackSkill.NAME, PrimalStrikeSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 4
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
    skill = PrimalAttackSkill(BARBARIAN_CHARACTER)
    print(skill)
    print(BARBARIAN_CHARACTER.cs.physical_attack)
    BARBARIAN_CHARACTER.skill_tree.learn_skill(PrimalAttackSkill)

    skill = PrimalStrikeSkill(BARBARIAN_CHARACTER)
    print(skill)
    print(BARBARIAN_CHARACTER.cs.physical_attack)
    BARBARIAN_CHARACTER.skill_tree.learn_skill(PrimalStrikeSkill)

    skill = PrimalRamSkill(BARBARIAN_CHARACTER)
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
    BARBARIAN_CHARACTER.skill_tree.learn_skill(PrimalRamSkill)

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
