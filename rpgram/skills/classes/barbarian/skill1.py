from typing import TYPE_CHECKING
from rpgram.constants.text import (
    HIT_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
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


if __name__ == '__main__':
    from rpgram.constants.test import BARBARIAN_CHARACTER
    skill = FuriousAttackSkill(BARBARIAN_CHARACTER)
    print(skill)
    print(BARBARIAN_CHARACTER.cs.physical_attack)
    BARBARIAN_CHARACTER.skill_tree.learn_skill(FuriousAttackSkill)

    skill = WildStrikeSkill(BARBARIAN_CHARACTER)
    print(skill)
    print(BARBARIAN_CHARACTER.cs.physical_attack)
    BARBARIAN_CHARACTER.skill_tree.learn_skill(WildStrikeSkill)
