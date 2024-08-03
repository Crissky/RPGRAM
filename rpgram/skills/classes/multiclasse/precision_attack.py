from typing import TYPE_CHECKING
from rpgram.constants.text import HIT_EMOJI_TEXT, PRECISION_ATTACK_EMOJI_TEXT
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.skill import (
    MultiClasseSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class QuickAttackSkill(BaseSkill):
    NAME = MultiClasseSkillEnum.QUICK_ATTACK.value
    DESCRIPTION = (
        f'Executa uma sequência de golpes precisos '
        f'como um vendaval contra o inimigo, '
        f'dificultando as chances de esquiva do oponente e '
        f'causando dano com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (100% + 5% x Rank x Nível). '
        f'Essa habilidade possui *{HIT_EMOJI_TEXT}* acima do normal.'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name_list': [
            ClasseEnum.DUELIST.value,
            ClasseEnum.ROGUE.value,
            ClasseEnum.WARRIOR.value,
        ],
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.00
        }
        damage_types = None

        super().__init__(
            name=QuickAttackSkill.NAME,
            description=QuickAttackSkill.DESCRIPTION,
            rank=QuickAttackSkill.RANK,
            level=level,
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
        return 1.25
