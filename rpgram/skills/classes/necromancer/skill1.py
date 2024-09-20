from typing import TYPE_CHECKING

from rpgram.conditions.debuff import DeathSentenceCondition
from rpgram.constants.text import (
    HIT_EMOJI_TEXT,
    MAGICAL_ATTACK_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.debuff import DebuffEnum, get_debuff_emoji_text
from rpgram.enums.skill import (
    NecromancerSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class BannedSoulSkill(BaseSkill):
    NAME = NecromancerSkillEnum.BANNED_SOUL.value
    DESCRIPTION = (
        f'Convoca um *Espírito Espectral* do além-vida que '
        f'avança sobre um inimigo, '
        f'causando dano '
        f'*{get_damage_emoji_text(DamageEnum.GHOSTLY)}* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.NECROMANCER.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 1.25,
        }
        damage_types = [DamageEnum.GHOSTLY]

        super().__init__(
            name=BannedSoulSkill.NAME,
            description=BannedSoulSkill.DESCRIPTION,
            rank=BannedSoulSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=BannedSoulSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class VengefulSpiritSkill(BaseSkill):
    NAME = NecromancerSkillEnum.VENGEFUL_SPIRIT.value
    DESCRIPTION = (
        f'Convoca um *Espírito de Vingaça* provindo do *Cárcere das Almas* '
        f'que avança sobre um inimigo, '
        f'causando dano '
        f'*{get_damage_emoji_text(DamageEnum.GHOSTLY)}* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (150% + 5% x Rank x Nível) e '
        f'adicionando a condição '
        f'*{get_debuff_emoji_text(DebuffEnum.DEATH_SENTENCE)}* '
        f'com nível igual ao (Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.NECROMANCER.value,
        'skill_list': [BannedSoulSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 1.50,
        }
        damage_types = [DamageEnum.GHOSTLY]

        super().__init__(
            name=VengefulSpiritSkill.NAME,
            description=VengefulSpiritSkill.DESCRIPTION,
            rank=VengefulSpiritSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=VengefulSpiritSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def hit_function(
        self,
        target: 'BaseCharacter',
        damage: int,
        total_damage: int,
    ) -> dict:
        report = {'text': ''}
        if target.is_alive:
            level = self.level_rank
            death_stc_condition = DeathSentenceCondition(level=level)
            status_report = target.status.add_condition(death_stc_condition)
            report['status_text'] = status_report['text']

        return report


class UndeadEmbraceSkill(BaseSkill):
    NAME = NecromancerSkillEnum.UNDEAD_EMBRACE.value
    DESCRIPTION = (
        f'Ergue do solo e reanima um *Cadáver Putrefato* '
        f'que avança lentamente sobre o inimigo, atacando e '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.POISON)}* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (200% + 5% x Rank x Nível), '
        f'mas possui uma baixa taxa de {HIT_EMOJI_TEXT}.'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.NECROMANCER.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 2.00,
        }
        damage_types = [DamageEnum.POISON]

        super().__init__(
            name=UndeadEmbraceSkill.NAME,
            description=UndeadEmbraceSkill.DESCRIPTION,
            rank=UndeadEmbraceSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=UndeadEmbraceSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    @property
    def hit_multiplier(self) -> float:
        return 0.75


class AbyssalCreatureSkill(BaseSkill):
    NAME = NecromancerSkillEnum.ABYSSAL_CREATURE.value
    DESCRIPTION = (
        f'Ergue do solo um cadáver reaimado de uma *Criatura Colossal* '
        f'que avança lentamente sobre o inimigo, atacando e '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.POISON)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.BLUDGEONING)}* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (300% + 5% x Rank x Nível), '
        f'mas possui uma baixa taxa de {HIT_EMOJI_TEXT}.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.NECROMANCER.value,
        'skill_list': [UndeadEmbraceSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 3.00,
        }
        damage_types = [
            DamageEnum.POISON,
            DamageEnum.BLUDGEONING,
        ]

        super().__init__(
            name=AbyssalCreatureSkill.NAME,
            description=AbyssalCreatureSkill.DESCRIPTION,
            rank=AbyssalCreatureSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=AbyssalCreatureSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    @property
    def hit_multiplier(self) -> float:
        return 0.75


class TheHordeSkill(BaseSkill):
    NAME = NecromancerSkillEnum.THE_HORDE.value
    DESCRIPTION = (
        f'Ergue do solo uma *Horda* de *Cadáveres Putrefatos Reanimados* '
        f'que avança lentamente sobre os inimigos, atacando e '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.POISON)}* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (200% + 2.5% x Rank x Nível), '
        f'mas possui uma baixa taxa de {HIT_EMOJI_TEXT}.'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.NECROMANCER.value,
        'skill_list': [UndeadEmbraceSkill.NAME, AbyssalCreatureSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 2.00,
        }
        damage_types = [
            DamageEnum.POISON,
            DamageEnum.POISON,
            DamageEnum.POISON,
            DamageEnum.POISON,
            DamageEnum.POISON,
        ]

        super().__init__(
            name=TheHordeSkill.NAME,
            description=TheHordeSkill.DESCRIPTION,
            rank=TheHordeSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.TEAM,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=TheHordeSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    @property
    def hit_multiplier(self) -> float:
        return 0.75


SKILL_WAY_DESCRIPTION = {
    'name': 'Senhor da Morte',
    'description': (
        'Um governante do além, um mestre da vida e da morte. '
        'Seus poderes sobre a morte são vastos e profundos, '
        'permitindo-lhe manipular cadáveres, invocar espíritos e '
        'controlar as forças do pós-vida.'
    ),
    'skill_list': [
        BannedSoulSkill,
        VengefulSpiritSkill,
        UndeadEmbraceSkill,
        AbyssalCreatureSkill,
        TheHordeSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import NECROMANCER_CHARACTER

    skill = BannedSoulSkill(NECROMANCER_CHARACTER)
    print(skill)
    print(NECROMANCER_CHARACTER.cs.magical_attack)
    print(NECROMANCER_CHARACTER.to_attack(
        defender_char=NECROMANCER_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    NECROMANCER_CHARACTER.skill_tree.learn_skill(BannedSoulSkill)

    skill = VengefulSpiritSkill(NECROMANCER_CHARACTER)
    print(skill)
    print(NECROMANCER_CHARACTER.cs.magical_attack)
    print(NECROMANCER_CHARACTER.to_attack(
        defender_char=NECROMANCER_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    NECROMANCER_CHARACTER.skill_tree.learn_skill(VengefulSpiritSkill)

    skill = UndeadEmbraceSkill(NECROMANCER_CHARACTER)
    print(skill)
    print(NECROMANCER_CHARACTER.cs.magical_attack)
    print(NECROMANCER_CHARACTER.to_attack(
        defender_char=NECROMANCER_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    NECROMANCER_CHARACTER.skill_tree.learn_skill(UndeadEmbraceSkill)

    skill = AbyssalCreatureSkill(NECROMANCER_CHARACTER)
    print(skill)
    print(NECROMANCER_CHARACTER.cs.magical_attack)
    print(NECROMANCER_CHARACTER.to_attack(
        defender_char=NECROMANCER_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    NECROMANCER_CHARACTER.skill_tree.learn_skill(AbyssalCreatureSkill)

    skill = TheHordeSkill(NECROMANCER_CHARACTER)
    print(skill)
    print(NECROMANCER_CHARACTER.cs.magical_attack)
    print(NECROMANCER_CHARACTER.to_attack(
        defender_char=NECROMANCER_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    NECROMANCER_CHARACTER.skill_tree.learn_skill(TheHordeSkill)
