from typing import TYPE_CHECKING
from rpgram.constants.text import (
    MAGICAL_DEFENSE_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT,
    PHYSICAL_DEFENSE_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.skill import (
    GuardianSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
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
    NAME = GuardianSkillEnum.HEAVY_CHARGE.value
    DESCRIPTION = (
        f'Assume uma postura ofensiva, avançando contra o inimigo '
        f'usando seu corpo massivo como arma, causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.BLUDGEONING)}* com base em '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* (75% + 5% x Rank x Nível) e '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (50% + 5% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.GUARDIAN.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 2
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_DEFENSE: 0.75,
            CombatStatsEnum.PHYSICAL_ATTACK: 0.50,
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
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=HeavyChargeSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class IronChargeSkill(BaseSkill):
    NAME = GuardianSkillEnum.IRON_CHARGE.value
    DESCRIPTION = (
        f'Avança através das linhas inimigas com uma força imparável '
        f'como um ariete implacável, envolto em uma aura metálica '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.BLUDGEONING)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.PIERCING)}* com base em '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* (50% + 5% x Rank x Nível), '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* (50% + 5% x Rank x Nível) e '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (50% + 5% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.GUARDIAN.value,
        'skill_list': [HeavyChargeSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 3
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_DEFENSE: 0.50,
            CombatStatsEnum.MAGICAL_DEFENSE: 0.50,
            CombatStatsEnum.PHYSICAL_ATTACK: 0.50,
        }
        damage_types = [
            DamageEnum.BLUDGEONING,
            DamageEnum.PIERCING,
        ]

        super().__init__(
            name=IronChargeSkill.NAME,
            description=IronChargeSkill.DESCRIPTION,
            rank=IronChargeSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=IronChargeSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    @property
    def hit_multiplier(self) -> float:
        return 1.25


class SteelStormSkill(BaseSkill):
    NAME = GuardianSkillEnum.STEEL_STORM.value
    DESCRIPTION = (
        f'Avança com um giro devastador revestido em uma energia metálica '
        f'que desencadeia uma *Tempestade*, '
        f'ceifando seus inimigos impiedosamente com '
        f'dano de '
        f'*{get_damage_emoji_text(DamageEnum.BLUDGEONING)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.SLASHING)}* baseado em '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* (9% + 2.5% x Rank x Nível), '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* (9% + 2.5% x Rank x Nível) e '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (9% + 2.5% x Rank x Nível).'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.GUARDIAN.value,
        'skill_list': [HeavyChargeSkill.NAME, IronChargeSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        cost = 4
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_DEFENSE: 0.09,
            CombatStatsEnum.MAGICAL_DEFENSE: 0.09,
            CombatStatsEnum.PHYSICAL_ATTACK: 0.09,
        }
        damage_types = [
            DamageEnum.BLUDGEONING,
            DamageEnum.BLUDGEONING,
            DamageEnum.SLASHING,
            DamageEnum.SLASHING,
        ]

        super().__init__(
            name=SteelStormSkill.NAME,
            description=SteelStormSkill.DESCRIPTION,
            rank=SteelStormSkill.RANK,
            level=level,
            cost=cost,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.TEAM,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=SteelStormSkill.REQUIREMENTS,
            damage_types=damage_types
        )


if __name__ == '__main__':
    from rpgram.constants.test import GUARDIAN_CHARACTER

    skill = HeavyChargeSkill(GUARDIAN_CHARACTER)
    print(skill)
    print(GUARDIAN_CHARACTER.cs.physical_attack)
    print(GUARDIAN_CHARACTER.cs.physical_defense)
    GUARDIAN_CHARACTER.skill_tree.learn_skill(HeavyChargeSkill)

    skill = IronChargeSkill(GUARDIAN_CHARACTER)
    print(skill)
    print(GUARDIAN_CHARACTER.cs.physical_attack)
    print(GUARDIAN_CHARACTER.cs.physical_defense)
    GUARDIAN_CHARACTER.skill_tree.learn_skill(IronChargeSkill)

    skill = SteelStormSkill(GUARDIAN_CHARACTER)
    print(skill)
    print(GUARDIAN_CHARACTER.cs.physical_defense)
    print(GUARDIAN_CHARACTER.cs.magical_defense)
    GUARDIAN_CHARACTER.skill_tree.learn_skill(SteelStormSkill)
