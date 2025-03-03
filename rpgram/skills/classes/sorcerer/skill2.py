from typing import TYPE_CHECKING
from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.barrier import PrismaticShieldCondition
from rpgram.constants.text import (
    MAGICAL_ATTACK_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.skill import (
    SkillDefenseEnum,
    SkillTypeEnum,
    SorcererSkillEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.classes.multiclasse.magical_attack import PrismaticShotSkill
from rpgram.skills.skill_base import BaseSkill

if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class PrismaticScintillationSkill(BaseSkill):
    NAME = SorcererSkillEnum.PRISMATIC_SCINTILLATION.value
    DESCRIPTION = (
        f'Canaliza a *Energia Mágica*, criando e lançando um *Artefato '
        f'Prismático* que causa dano de '
        f'*{get_damage_emoji_text(DamageEnum.LIGHT)}* '
        f'a *TODES os inimigos* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (75% + 2.5% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.SORCERER.value,
        'skill_list': [PrismaticShotSkill.NAME],
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 0.75,
        }
        damage_types = [DamageEnum.LIGHT]

        super().__init__(
            name=PrismaticScintillationSkill.NAME,
            description=PrismaticScintillationSkill.DESCRIPTION,
            rank=PrismaticScintillationSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.TEAM,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=PrismaticScintillationSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class PrismaticShieldSkill(BaseSkill):
    NAME = SorcererSkillEnum.PRISMATIC_SHIELD.value
    DESCRIPTION = (
        f'Canaliza a *Energia Mágica* para envolver um aliado em um círculo '
        f'prismático que o salvaguardar com uma barreira baseada no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (200% + 10% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.SORCERER.value,
        'skill_list': [PrismaticShotSkill.NAME],
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=PrismaticShieldSkill.NAME,
            description=PrismaticShieldSkill.DESCRIPTION,
            rank=PrismaticShieldSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BARRIER,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=PrismaticShieldSkill.REQUIREMENTS,
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
            power = dice.boosted_magical_attack
            level = self.level_rank
            condition = PrismaticShieldCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report = {
                'text': (
                    f'*{player_name}* canaliza um *Círculo Cintilante* '
                    f'para salvaguardar '
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
    'name': 'Domínio Anímico',
    'description': (
        'Área da mágia que visa controlar os elementos não naturais. '
        'As habilidades desse grupo se concentram em conceder ao Feiticeiro '
        'acesso a magias sobrenaturais, permitindo que ele combine e '
        'explore seus diferentes efeitos em combate.'
    ),
    'skill_list': [
        PrismaticShotSkill,
        PrismaticScintillationSkill,
        PrismaticShieldSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import SORCERER_CHARACTER
    skill = PrismaticShotSkill(SORCERER_CHARACTER)
    print(skill)
    print(SORCERER_CHARACTER.cs.magical_attack)
    SORCERER_CHARACTER.skill_tree.learn_skill(PrismaticShotSkill)

    skill = PrismaticScintillationSkill(SORCERER_CHARACTER)
    print(skill)
    print(SORCERER_CHARACTER.cs.magical_attack)
    SORCERER_CHARACTER.skill_tree.learn_skill(PrismaticScintillationSkill)

    skill = PrismaticShieldSkill(SORCERER_CHARACTER)
    print(skill)
    print(SORCERER_CHARACTER.cs.magical_attack)
    print(skill.function(SORCERER_CHARACTER))
    SORCERER_CHARACTER.skill_tree.learn_skill(PrismaticShieldSkill)
