from typing import TYPE_CHECKING

from rpgram.constants.text import HIT_EMOJI_TEXT, PRECISION_ATTACK_EMOJI_TEXT
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.skill import KnightSkillEnum, SkillDefenseEnum, SkillTypeEnum, TargetEnum
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter



class RoyalFurySkill(BaseSkill):
    NAME = KnightSkillEnum.ROYAL_FURY.value
    DESCRIPTION = (
        f'Em nome do Rei, desfere uma série de golpes rápidos e devastadores, '
        f'causando dano '
        f'*{get_damage_emoji_text(DamageEnum.BLESSING)}* com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (100% + 5% x Rank x Nível). '
        f'Essa habilidade possui *{HIT_EMOJI_TEXT}* acima do normal.'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.KNIGHT.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.00,
        }
        damage_types = None

        super().__init__(
            name=RoyalFurySkill.NAME,
            description=RoyalFurySkill.DESCRIPTION,
            rank=RoyalFurySkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=RoyalFurySkill.REQUIREMENTS,
            damage_types=damage_types
        )

    @property
    def hit_multiplier(self) -> float:
        return 1.25


SKILL_WAY_DESCRIPTION = {
    # Sugestão para nomes do caminho:
    # Sentinela da Planície, Lâmina dos Reis, Lança Celeste, 
    # Arauto da Tempestade, Juramento de Aço, Guardião da Honra, 
    # Marechal de Guerra, Vanguarda da Justiça
    'name': 'Lâmina dos Reis',
    'description': (
        'Entre os Cavaleiros, há aqueles que transcendem a mera maestria '
        'no combate e se tornam a personificação da realeza guerreira. '
        'Os que trilham o caminho da Lâmina dos Reis não são apenas '
        'guerreiros habilidosos, mas símbolos vivos da honra, '
        'da liderança e do poder absoluto. '

        'Eles combinam técnica refinada com uma presença inspiradora no '
        'campo de batalha. Seus golpes são rápidos e letais, '
        'repletos da precisão de um duelista e da força bruta de uma '
        'investida real. A cada estocada ou arco de sua espada, '
        'eles ditam o ritmo da guerra, derrubando adversários e '
        'erguendo aliados com sua coragem inabalável.'
    ),
    'skill_list': [
        RoyalFurySkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import KNIGHT_CHARACTER

    skill = RoyalFurySkill(KNIGHT_CHARACTER)
    print(skill)
    print(KNIGHT_CHARACTER.cs.precision_attack)
    print(KNIGHT_CHARACTER.to_attack(
        defender_char=KNIGHT_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    KNIGHT_CHARACTER.skill_tree.learn_skill(RoyalFurySkill)
