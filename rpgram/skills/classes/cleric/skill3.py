from typing import TYPE_CHECKING
from rpgram.constants.text import MAGICAL_ATTACK_EMOJI_TEXT
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.skill import (
    ClericSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class WillOTheWispSkill(BaseSkill):
    NAME = ClericSkillEnum.WILL_O_THE_WISP.value
    DESCRIPTION = (
        'Utiliza um artefato antigo para lançar *Chamas Fantasmagóricas* '
        'em um inimigo, causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.FIRE)}* e '
        f'*{get_damage_emoji_text(DamageEnum.GHOSTLY)}* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.CLERIC.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 1.25,
        }
        damage_types = [DamageEnum.FIRE, DamageEnum.GHOSTLY]

        super().__init__(
            name=WillOTheWispSkill.NAME,
            description=WillOTheWispSkill.DESCRIPTION,
            rank=WillOTheWispSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=WillOTheWispSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class GreekFireSkill(BaseSkill):
    NAME = ClericSkillEnum.GREEK_FIRE.value
    DESCRIPTION = (
        'Por meio de um engenhoso artefato antigo, invoca as '
        '*Chamas Negras das Fornalhas de Hefesto* para golpear o oponente, '
        'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.FIRE)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.DARK)}* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (150% + 5% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.CLERIC.value,
        'skill_list': [WillOTheWispSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 1.25,
        }
        damage_types = [DamageEnum.FIRE, DamageEnum.DARK]

        super().__init__(
            name=GreekFireSkill.NAME,
            description=GreekFireSkill.DESCRIPTION,
            rank=GreekFireSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=GreekFireSkill.REQUIREMENTS,
            damage_types=damage_types
        )


SKILL_WAY_DESCRIPTION = {
    'name': 'Artefatos Sagrados',
    'description': (
        'Mergulhando nos mistérios arcanos de relíquias sagradas e '
        'artefatos ancestrais, '
        'os Clérigos do Caminho dos Artefatos Sagrados canalizam o poder '
        'divino através desses objetos imbuídos de magia divina. '
        'Através de rituais sagrados e encantamentos poderosos, '
        'eles despertam os poderes adormecidos desses artefatos, '
        'conjurando magias devastadoras e concedendo bênçãos divinas '
        'aos seus aliados.'
    ),
    'skill_list': [
        WillOTheWispSkill,
        GreekFireSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import CLERIC_CHARACTER

    skill = WillOTheWispSkill(CLERIC_CHARACTER)
    print(skill)
    print(CLERIC_CHARACTER.cs.magical_attack)
    print(CLERIC_CHARACTER.to_attack(
        defender_char=CLERIC_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    CLERIC_CHARACTER.skill_tree.learn_skill(WillOTheWispSkill)

    skill = GreekFireSkill(CLERIC_CHARACTER)
    print(skill)
    print(CLERIC_CHARACTER.cs.magical_attack)
    print(CLERIC_CHARACTER.to_attack(
        defender_char=CLERIC_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    CLERIC_CHARACTER.skill_tree.learn_skill(GreekFireSkill)
