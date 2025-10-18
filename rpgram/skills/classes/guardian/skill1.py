from typing import TYPE_CHECKING
from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.barrier import GuardianShieldCondition
from rpgram.constants.text import (
    PHYSICAL_DEFENSE_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.skill import (
    GuardianSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.requirement import Requirement
from rpgram.skills.classes.multiclasse.physical_defense import (
    RobustBlockSkill
)
from rpgram.skills.classes.multiclasse.physical_defense import (
    GuardianShieldSkill
)
from rpgram.skills.skill_base import BaseSkill

if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class ShieldWallSkill(BaseSkill):
    NAME = GuardianSkillEnum.SHIELD_WALL.value
    DESCRIPTION = (
        'Erguendo o escudo com *Determinação* e *Fé Inabalável*, '
        'evoca uma miríade de *Escudo Familiar Protetivo* '
        'que resguardam os aliados com barreiras baseada na '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.GUARDIAN.value,
        'skill_list': [GuardianShieldSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=ShieldWallSkill.NAME,
            description=ShieldWallSkill.DESCRIPTION,
            rank=ShieldWallSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.TEAM,
            skill_type=SkillTypeEnum.BARRIER,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=ShieldWallSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        player_name = self.char.player_name
        target_name = char.player_name
        if char.is_alive:
            target_name = (
                'a si mesmo'
                if target_name == player_name
                else target_name
            )
            dice = self.dice
            power = dice.boosted_physical_defense
            level = self.level_rank
            condition = GuardianShieldCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{player_name}* se impõe contra o perigo, evocando um '
                    '*Escudo Familiar Protetivo* para resguardar '
                    f'*{target_name}* com uma barreira '
                    f'*{condition.barrier_points_text}*({dice.text}).\n\n'
                    f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                    f'{status_report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


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
    ),
    'skill_list': [
        RobustBlockSkill,
        GuardianShieldSkill,
        ShieldWallSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import GUARDIAN_CHARACTER
    skill = RobustBlockSkill(GUARDIAN_CHARACTER)
    print(skill)
    print(GUARDIAN_CHARACTER.bs.constitution)
    print(GUARDIAN_CHARACTER.cs.physical_defense)
    print(skill.function())
    print(GUARDIAN_CHARACTER.cs.physical_defense)
    GUARDIAN_CHARACTER.skill_tree.learn_skill(RobustBlockSkill)

    skill = GuardianShieldSkill(GUARDIAN_CHARACTER)
    print(skill)
    print(GUARDIAN_CHARACTER.cs.physical_defense)
    print(skill.function(GUARDIAN_CHARACTER))
    GUARDIAN_CHARACTER.skill_tree.learn_skill(GuardianShieldSkill)

    skill = ShieldWallSkill(GUARDIAN_CHARACTER)
    print(skill)
    print(GUARDIAN_CHARACTER.cs.physical_defense)
    print(skill.function(GUARDIAN_CHARACTER))
    GUARDIAN_CHARACTER.skill_tree.learn_skill(ShieldWallSkill)
