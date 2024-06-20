from typing import TYPE_CHECKING
from rpgram.conditions.self_skill import RobustBlockCondition
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
        f'usando seu corpo massivo como arma.'
    )

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 2
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 0.45,
            CombatStatsEnum.PHYSICAL_DEFENSE: 0.9
        }

        super().__init__(
            name=HeavyChargeSkill.NAME,
            description=HeavyChargeSkill.DESCRIPTION,
            level=level,
            cost=cost,
            base_stats_multiplier={},
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.DEFENSE,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements={},
            damage_types=None
        )

    def function(self) -> dict:
        rbc = RobustBlockCondition(character=self.char)
        report_list = self.char.status.set_conditions(rbc)
        report = {
            'text': '\n'.join([report['text'] for report in report_list])
        }

        return report


if __name__ == '__main__':
    from rpgram.constants.test import BASE_CHARACTER
    hcs = HeavyChargeSkill(BASE_CHARACTER)
    print(hcs)
    print(BASE_CHARACTER.cs.physical_defense)
    print(hcs.function())
    print(BASE_CHARACTER.cs.physical_defense)
