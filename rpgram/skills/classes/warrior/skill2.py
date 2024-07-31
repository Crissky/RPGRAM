from typing import TYPE_CHECKING
from rpgram.constants.text import (
    HIT_EMOJI_TEXT,
    PRECISION_ATTACK_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.skill import (
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum,
    WarriorSkillEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.classes.multiclasse.precision_attack import (
    QuickAttackSkill
)
from rpgram.skills.skill_base import BaseSkill

if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class BlinkAttackSkill(BaseSkill):
    NAME = WarriorSkillEnum.BLINK_ATTACK.value
    DESCRIPTION = (
        f'Executa um único golpe rápido como um relâmpago, '
        f'imperceptível aos olhos destreinados, '
        f'dificultando as chances de esquiva do oponente e '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.LIGHTNING)}* com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (100% + 5% x Rank x Nível). '
        f'Essa habilidade possui *{HIT_EMOJI_TEXT}* acima do normal.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.WARRIOR.value,
        'skill_list': [QuickAttackSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.00
        }
        damage_types = [DamageEnum.LIGHTNING]

        super().__init__(
            name=BlinkAttackSkill.NAME,
            description=BlinkAttackSkill.DESCRIPTION,
            rank=BlinkAttackSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=BlinkAttackSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    @property
    def hit_multiplier(self) -> float:
        return 1.50


class LethalAttackSkill(BaseSkill):
    NAME = WarriorSkillEnum.LETHAL_ATTACK.value
    DESCRIPTION = (
        f'Desfere um ataque preciso focando pontos vitais do inimigo, '
        f'ignorando suas defesas e '
        f'causando dano com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (75% + 5% x Rank x Nível).'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.WARRIOR.value,
        'skill_list': [QuickAttackSkill.NAME, BlinkAttackSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 0.75
        }
        damage_types = None

        super().__init__(
            name=LethalAttackSkill.NAME,
            description=LethalAttackSkill.DESCRIPTION,
            rank=LethalAttackSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.TRUE,
            char=char,
            use_equips_damage_types=True,
            requirements=LethalAttackSkill.REQUIREMENTS,
            damage_types=damage_types
        )


SKILL_WAY_DESCRIPTION = {
    'name': 'Maestria em Combate',
    'description': (
        'O caminho da Maestria em Combate transforma o Guerreiro '
        'em um virtuoso do combate, transcendendo a força bruta e '
        'empunhando as armas com precisão mortal. '
        'Através de um arsenal de técnicas elaboradas e movimentos precisos, '
        'o Guerreiro se torna um arauto da morte no campo de batalha, '
        'eliminando seus inimigos com golpes rápidos e letais.'
    ),
    'skill_list': [
        BlinkAttackSkill,
        LethalAttackSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import WARRIOR_CHARACTER

    skill = QuickAttackSkill(WARRIOR_CHARACTER)
    print(skill)
    print(WARRIOR_CHARACTER.cs.precision_attack)
    print(WARRIOR_CHARACTER.to_attack(
        defender_char=WARRIOR_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    WARRIOR_CHARACTER.skill_tree.learn_skill(QuickAttackSkill)

    skill = BlinkAttackSkill(WARRIOR_CHARACTER)
    print(skill)
    print(WARRIOR_CHARACTER.cs.precision_attack)
    print(WARRIOR_CHARACTER.to_attack(
        defender_char=WARRIOR_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    WARRIOR_CHARACTER.skill_tree.learn_skill(BlinkAttackSkill)

    skill = LethalAttackSkill(WARRIOR_CHARACTER)
    print(skill)
    print(WARRIOR_CHARACTER.cs.precision_attack)
    print(WARRIOR_CHARACTER.to_attack(
        defender_char=WARRIOR_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    WARRIOR_CHARACTER.skill_tree.learn_skill(LethalAttackSkill)
