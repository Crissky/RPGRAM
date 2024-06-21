from typing import TYPE_CHECKING
from rpgram.constants.text import (
    PHYSICAL_ATTACK_EMOJI_TEXT
)
from rpgram.enums.skill import SkillDefenseEnum, SkillTypeEnum, TargetEnum
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.skills.skill_base import BaseSkill

if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


SKILL_WAY_DESCRIPTION = {
    'name': 'Maestria em Combate',
    'description': (
        'O caminho da Maestria em Combate transforma o Guerreiro '
        'em um virtuoso do combate, transcendendo a força bruta e '
        'empunhando as armas com precisão mortal. '
        'Através de um arsenal de técnicas elaboradas e movimentos precisos, '
        'o Guerreiro se torna um arauto da morte no campo de batalha, '
        'eliminando seus inimigos com golpes rápidos e letais.'
    )
}


class QuickAttackSkill(BaseSkill):
    NAME = 'Ataque Rápido'
    DESCRIPTION = (
        f'Executa uma sequência de golpes precisos '
        f'como um vendaval contra seu inimigo, '
        f'dificultando as chances de esquiva do oponente e '
        f'causando dano com base em {PHYSICAL_ATTACK_EMOJI_TEXT}.'
    )

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 2
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.15001
        }
        requirements = {}
        damage_types = []

        super().__init__(
            name=QuickAttackSkill.NAME,
            description=QuickAttackSkill.DESCRIPTION,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.DEFENSE,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=True,
            requirements=requirements,
            damage_types=damage_types
        )
    
    @property
    def hit_multiplier(self) -> float:
        return 2.0


class LethalAttackSkill(BaseSkill):
    NAME = 'Ataque Letal'
    DESCRIPTION = (
        f'Desfere um ataque preciso focando pontos vitais do inimigo, '
        f'causando dano com base em {PHYSICAL_ATTACK_EMOJI_TEXT}.'
    )

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 3
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 2.50
        }
        requirements = {}
        damage_types = []

        super().__init__(
            name=LethalAttackSkill.NAME,
            description=LethalAttackSkill.DESCRIPTION,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.DEFENSE,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=True,
            requirements=requirements,
            damage_types=damage_types
        )


if __name__ == '__main__':
    from rpgram.constants.test import BASE_CHARACTER
    skill = QuickAttackSkill(BASE_CHARACTER)
    print(skill)
    print(BASE_CHARACTER.cs.precision_attack)
    skill = LethalAttackSkill(BASE_CHARACTER)
    print(skill)
    print(BASE_CHARACTER.cs.precision_attack)
