from typing import TYPE_CHECKING
from rpgram.constants.text import (
    PHYSICAL_ATTACK_EMOJI_TEXT,
    PHYSICAL_DEFENSE_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum
from rpgram.enums.skill import SkillDefenseEnum, SkillTypeEnum, TargetEnum
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.skills.skill_base import BaseSkill

if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


SKILL_WAY_DESCRIPTION = {
    'name': 'Titã Implacável',
    'description': (
        'O Titã Implacável encarna a força bruta do Guardião, '
        'utilizando seu corpo como arma devastadora para esmagar '
        'seus inimigos. '
        'Através desse caminho de habilidades, '
        'o Guardião se torna um mestre do combate corpo a corpo, '
        'capaz de infligir danos colossais e dominar o campo de batalha '
        'com pura ferocidade. '
        'Cada golpe carrega a fúria titânica, '
        'impulsionando o Guardião a superar qualquer obstáculo e conquistar '
        'a vitória a qualquer custo.'
    )
}


class HeavyChargeSkill(BaseSkill):
    NAME = 'Investida Pesada'
    DESCRIPTION = (
        f'Assume uma postura ofensiva, avançando contra o inimigo '
        f'usando seu corpo massivo como arma, causando dano com base em '
        f'{PHYSICAL_DEFENSE_EMOJI_TEXT} e {PHYSICAL_ATTACK_EMOJI_TEXT}.'
    )
    RANK = 1

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 2
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 0.45,
            CombatStatsEnum.PHYSICAL_DEFENSE: 0.90,
        }
        requirements = {
            'classe_name': ClasseEnum.GUARDIAN.value,
        }
        damage_types = [DamageEnum.BLUDGEONING]

        super().__init__(
            name=HeavyChargeSkill.NAME,
            description=HeavyChargeSkill.DESCRIPTION,
            rank=HeavyChargeSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.DEFENSE,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=requirements,
            damage_types=damage_types
        )


if __name__ == '__main__':
    from rpgram.constants.test import BASE_CHARACTER
    skill = HeavyChargeSkill(BASE_CHARACTER)
    print(skill)
    print(BASE_CHARACTER.cs.physical_attack)
    print(BASE_CHARACTER.cs.physical_defense)
