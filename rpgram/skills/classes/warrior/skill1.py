from typing import TYPE_CHECKING
from rpgram.constants.text import (
    PHYSICAL_ATTACK_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.skill import SkillDefenseEnum, SkillTypeEnum, TargetEnum
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.skills.skill_base import BaseSkill

if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


SKILL_WAY_DESCRIPTION = {
    'name': 'Combate Brutal',
    'description': (
        'O caminho do Combate Brutal molda o Guerreiro em um agente de '
        'destruição implacável, utilizando força bruta e '
        'ferocidade inigualável para esmagar seus oponentes. '
        'Dominando a arte do combate, o Guerreiro se torna um '
        'mestre da violência, capaz de infligir danos devastadores '
        'com cada golpe. '
        'Habilidades brutais como Ataques Múltiplos, Golpes Poderosos '
        'e Ataques Implacáveis transformam o Guerreiro em um redemoinho '
        'de fúria, dizimando inimigos em um turbilhão de aço e sangue.'
    )
}


class PowerfulAttackSkill(BaseSkill):
    NAME = 'Ataque Poderoso'
    DESCRIPTION = (
        f'Tenciona os músculos ao máximo e desfere um golpe devastador, '
        f'causando dano com base em {PHYSICAL_ATTACK_EMOJI_TEXT}.'
    )
    RANK = 1

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 2
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.50,
        }
        requirements = {
            'classe_name': ClasseEnum.WARRIOR.value,
        }
        damage_types = None

        super().__init__(
            name=PowerfulAttackSkill.NAME,
            description=PowerfulAttackSkill.DESCRIPTION,
            rank=PowerfulAttackSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=requirements,
            damage_types=damage_types
        )


if __name__ == '__main__':
    from rpgram.constants.test import BASE_CHARACTER
    skill = PowerfulAttackSkill(BASE_CHARACTER)
    print(skill)
    print(BASE_CHARACTER.cs.physical_attack)
