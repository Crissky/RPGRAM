from typing import TYPE_CHECKING
from rpgram.conditions.self_skill import RobustBlockCondition
from rpgram.constants.text import (
    CONSTITUTION_EMOJI_TEXT,
    PHYSICAL_DEFENSE_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.skill import SkillDefenseEnum, SkillTypeEnum, TargetEnum
from rpgram.skills.skill_base import BaseSkill

if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


SKILL_WAY_DESCRIPTION = {
    'name': 'Fortaleza Inabalável',
    'description': (
        'O caminho da Fortaleza Inabalável transforma o Guardião '
        'em um bastião inabalável, pronto para enfrentar qualquer desafio. '
        'Através dessas habilidades, o Guardião se torna um escudo '
        'impenetrável para seus aliados, capaz de suportar os golpes '
        'mais devastadores e proteger seus companheiros de batalha. '
        'Sua resistência inquebrantável inspira confiança e serve como um '
        'farol de esperança em meio ao caos. '
        'Cada investida inimiga é repelida com força redobrada, '
        'demonstrando a força inabalável do Guardião e garantindo a '
        'vitória final.'
    )
}


class RobustBlockSkill(BaseSkill):
    NAME = 'Bloqueio Robusto'
    DESCRIPTION = (
        f'Assume uma postura defensiva aumentando a '
        f'{PHYSICAL_DEFENSE_EMOJI_TEXT} com base na {CONSTITUTION_EMOJI_TEXT}.'
    )
    RANK = 1

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 2
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        requirements = {
            'classe_name': ClasseEnum.GUARDIAN.value,
        }
        damage_types = None

        super().__init__(
            name=RobustBlockSkill.NAME,
            description=RobustBlockSkill.DESCRIPTION,
            rank=RobustBlockSkill.RANK,
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

    def function(self) -> dict:
        rbc = RobustBlockCondition(character=self.char)
        report_list = self.char.status.set_conditions(rbc)
        report = {
            'text': '\n'.join([report['text'] for report in report_list])
        }

        return report


if __name__ == '__main__':
    from rpgram.constants.test import BASE_CHARACTER
    skill = RobustBlockSkill(BASE_CHARACTER)
    print(skill)
    print(BASE_CHARACTER.cs.physical_defense)
    print(skill.function())
    print(BASE_CHARACTER.cs.physical_defense)
