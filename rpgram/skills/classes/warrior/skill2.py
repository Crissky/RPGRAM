from typing import TYPE_CHECKING
from rpgram.constants.text import (
    PHYSICAL_ATTACK_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.skill import (
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum,
    WarriorSkillEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
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
    NAME = WarriorSkillEnum.QUICK_ATTACK.value
    DESCRIPTION = (
        f'Executa uma sequência de golpes precisos '
        f'como um vendaval contra seu inimigo, '
        f'dificultando as chances de esquiva do oponente e '
        f'causando dano com base em '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (115% + 5% x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.WARRIOR.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 2
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.15
        }
        damage_types = None

        super().__init__(
            name=QuickAttackSkill.NAME,
            description=QuickAttackSkill.DESCRIPTION,
            rank=QuickAttackSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=QuickAttackSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    @property
    def hit_multiplier(self) -> float:
        return 1.50


class LethalAttackSkill(BaseSkill):
    NAME = WarriorSkillEnum.LETHAL_ATTACK.value
    DESCRIPTION = (
        f'Desfere um ataque preciso focando pontos vitais do inimigo, '
        f'causando dano com base em '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (165% + 5% x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.WARRIOR.value,
        'skill_list': [QuickAttackSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 3
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.65
        }
        damage_types = None

        super().__init__(
            name=LethalAttackSkill.NAME,
            description=LethalAttackSkill.DESCRIPTION,
            rank=LethalAttackSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=LethalAttackSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    @property
    def hit_multiplier(self) -> float:
        return 2.00


if __name__ == '__main__':
    from rpgram.constants.test import WARRIOR_CHARACTER
    skill = QuickAttackSkill(WARRIOR_CHARACTER)
    print(skill)
    print(WARRIOR_CHARACTER.cs.precision_attack)
    WARRIOR_CHARACTER.skill_tree.learn_skill(QuickAttackSkill)

    skill = LethalAttackSkill(WARRIOR_CHARACTER)
    print(skill)
    print(WARRIOR_CHARACTER.cs.precision_attack)
    WARRIOR_CHARACTER.skill_tree.learn_skill(LethalAttackSkill)
