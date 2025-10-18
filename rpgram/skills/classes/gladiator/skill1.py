from typing import TYPE_CHECKING

from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.barrier import AjaxShieldCondition
from rpgram.conditions.self_skill import (
    ArenaDomainCondition,
    TurtleStanceCondition,
    UnicornStanceCondition
)
from rpgram.conditions.special_damage_skill import SDAresBladeCondition
from rpgram.constants.text import (
    CHARISMA_EMOJI_TEXT,
    CONSTITUTION_EMOJI_TEXT,
    EVASION_EMOJI_TEXT,
    HIT_EMOJI_TEXT,
    HIT_POINT_FULL_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT,
    PHYSICAL_DEFENSE_EMOJI_TEXT,
    STRENGTH_EMOJI_TEXT,
    WISDOM_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.skill import (
    GladiatorSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class AchillesAttackSkill(BaseSkill):
    NAME = GladiatorSkillEnum.ACHILLES_ATTACK.value
    DESCRIPTION = (
        'Canaliza a *Força e a Fúria de Aquiles*, '
        'concentrando toda a sua energia em um único golpe poderoso, '
        'causando dano com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.GLADIATOR.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.25,
        }
        damage_types = None

        super().__init__(
            name=AchillesAttackSkill.NAME,
            description=AchillesAttackSkill.DESCRIPTION,
            rank=AchillesAttackSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=AchillesAttackSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class HerculesFurySkill(BaseSkill):
    NAME = GladiatorSkillEnum.HERCULES_FURY.value
    DESCRIPTION = (
        'Invoca a *Força Bruta* e a raiva do lendário herói grego, '
        'se transformando em um jugo da natureza para '
        'investir contra o inimigo e '
        'causar dano de '
        f'*{get_damage_emoji_text(DamageEnum.BLUDGEONING)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (150% + 5% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.GLADIATOR.value,
        'skill_list': [AchillesAttackSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.50,
        }
        damage_types = [
            DamageEnum.BLUDGEONING
        ]

        super().__init__(
            name=HerculesFurySkill.NAME,
            description=HerculesFurySkill.DESCRIPTION,
            rank=HerculesFurySkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=HerculesFurySkill.REQUIREMENTS,
            damage_types=damage_types
        )


class AresBladeSkill(BaseSkill):
    NAME = GladiatorSkillEnum.ARES_BLADE.value
    DESCRIPTION = (
        'Imbui sua arma com a *Ira de Ares*, '
        'concedendo dano de '
        f'*{get_damage_emoji_text(DamageEnum.SLASHING)}*, '
        f'*{get_damage_emoji_text(DamageEnum.FIRE)}*, '
        f'*{get_damage_emoji_text(DamageEnum.DIVINE)}* e '
        f'*{get_damage_emoji_text(DamageEnum.CHAOS)}* '
        'baseado no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (100% + 10% x Rank x Nível) '
        'e desfere um ataque poderoso, '
        'causando dano com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (175% + 5% x Rank x Nível).'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.GLADIATOR.value,
        'skill_list': [
            AchillesAttackSkill.NAME,
            HerculesFurySkill.NAME
        ]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.75,
        }
        damage_types = []

        super().__init__(
            name=AresBladeSkill.NAME,
            description=AresBladeSkill.DESCRIPTION,
            rank=AresBladeSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=AresBladeSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def pre_hit_function(self, target: 'BaseCharacter') -> dict:
        player_name = self.char.player_name
        power = self.char.cs.physical_attack
        level = self.level_rank
        condition = SDAresBladeCondition(power=power, level=level)
        report_list = self.char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* imbui sua arma com a *Ira de Ares*, '
                'concedendo dano '
                f'*{get_damage_emoji_text(DamageEnum.SLASHING)}*, '
                f'*{get_damage_emoji_text(DamageEnum.FIRE)}*, '
                f'*{get_damage_emoji_text(DamageEnum.DIVINE)}* e '
                f'*{get_damage_emoji_text(DamageEnum.CHAOS)}*.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class AjaxShieldSkill(BaseSkill):
    NAME = GladiatorSkillEnum.AJAX_SHIELD.value
    DESCRIPTION = (
        'Evoca a *Lendária Proteção* do guerreiro grego, '
        'criando um escudo de energia à sua frente, '
        'recebendo uma barreira com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (200% + 5% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.GLADIATOR.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=AjaxShieldSkill.NAME,
            description=AjaxShieldSkill.DESCRIPTION,
            rank=AjaxShieldSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BARRIER,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=AjaxShieldSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        dice = self.dice
        power = dice.boosted_physical_attack
        level = self.level_rank
        condition = AjaxShieldCondition(power=power, level=level)
        report_list = self.char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* é coberto pela *Lendária Proteção* '
                'que concede uma barreira '
                f'*{condition.barrier_points_text}*({dice.text}).\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class TurtleStanceSkill(BaseSkill):
    NAME = GladiatorSkillEnum.TURTLE_STANCE.value
    DESCRIPTION = (
        'Se curva sobre si mesmo, protegendo seu corpo '
        'com os braços e as pernas, assumindo uma postura defensiva '
        'que lembra o casco de uma tartaruga, '
        'aumentando a '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* com base na '
        f'*{CONSTITUTION_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.GLADIATOR.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=TurtleStanceSkill.NAME,
            description=TurtleStanceSkill.DESCRIPTION,
            rank=TurtleStanceSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=TurtleStanceSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        condition = TurtleStanceCondition(character=char, level=level)
        report_list = self.char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* se curva sobre si mesmo '
                'assumindo uma postura preventiva que aumenta a sua '
                f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* '
                f'em {condition.bonus_physical_defense} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class UnicornStanceSkill(BaseSkill):
    NAME = GladiatorSkillEnum.UNICORN_STANCE.value
    DESCRIPTION = (
        'Assume uma postura elegante e poderosa, '
        'canalizando a energia de um *Lendário Unicórnio*, '
        'aumentando o '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* com base na '
        f'*{STRENGTH_EMOJI_TEXT}* (200% + 10% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.GLADIATOR.value,
        'skill_list': [TurtleStanceSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=UnicornStanceSkill.NAME,
            description=UnicornStanceSkill.DESCRIPTION,
            rank=UnicornStanceSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=UnicornStanceSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        condition = UnicornStanceCondition(character=char, level=level)
        report_list = self.char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* assume a *{self.name}* '
                'assumindo uma postura agressiva quee aumenta o seu '
                f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* '
                f'em {condition.bonus_physical_attack} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class ArenaDomainSkill(BaseSkill):
    NAME = GladiatorSkillEnum.ARENA_DOMAIN.value
    DESCRIPTION = (
        'Entra em um *Estado de Fluxo*, onde seus sentidos se aguçam e '
        'sua compreensão do combate se aprofunda, '
        'aumentando o '
        f'*{HIT_POINT_FULL_EMOJI_TEXT}*, '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}*, '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}*, '
        f'*{HIT_EMOJI_TEXT}* e '
        f'*{EVASION_EMOJI_TEXT}* com base na '
        f'*{STRENGTH_EMOJI_TEXT}*, '
        f'*{CONSTITUTION_EMOJI_TEXT}*, '
        f'*{WISDOM_EMOJI_TEXT}* e '
        f'*{CHARISMA_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.GLADIATOR.value,
        'skill_list': [
            TurtleStanceSkill.NAME,
            UnicornStanceSkill.NAME
        ]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=ArenaDomainSkill.NAME,
            description=ArenaDomainSkill.DESCRIPTION,
            rank=ArenaDomainSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=ArenaDomainSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        char = self.char
        level = self.level_rank
        condition = ArenaDomainCondition(character=char, level=level)
        report_list = self.char.status.set_conditions(condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* entra em um *Estado de Fluxo* '
                'que aumenta o seu '
                f'*{HIT_POINT_FULL_EMOJI_TEXT}* '
                f'em {condition.bonus_hit_points} pontos, '
                f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* '
                f'em {condition.bonus_physical_attack} pontos, '
                f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* '
                f'em {condition.bonus_physical_defense} pontos, '
                f'*{HIT_EMOJI_TEXT}* '
                f'em {condition.bonus_hit} pontos e '
                f'*{EVASION_EMOJI_TEXT}* '
                f'em {condition.bonus_evasion} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


SKILL_WAY_DESCRIPTION = {
    'name': 'Mestre da Arena',
    'description': (
        'O Mestre da Arena é mais do que apenas um combatente; '
        'ele é um símbolo de poder, glória e superação. '
        'É um predador nato que caça seus '
        'adversários com a mesma '
        'implacabilidade que um leão caça sua presa. '
        'Sua existência gira em torno do combate, da competição e do triunfo. '
        'A arena é seu reino, e ele é o rei indiscutível.'
    ),
    'skill_list': [
        AchillesAttackSkill,
        HerculesFurySkill,
        AresBladeSkill,
        AjaxShieldSkill,
        TurtleStanceSkill,
        UnicornStanceSkill,
        ArenaDomainSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import GLADIATOR_CHARACTER

    skill = AchillesAttackSkill(GLADIATOR_CHARACTER)
    print(skill)
    print(GLADIATOR_CHARACTER.cs.physical_attack)
    print(GLADIATOR_CHARACTER.to_attack(
        defender_char=GLADIATOR_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    GLADIATOR_CHARACTER.skill_tree.learn_skill(AchillesAttackSkill)

    skill = HerculesFurySkill(GLADIATOR_CHARACTER)
    print(skill)
    print(GLADIATOR_CHARACTER.cs.physical_attack)
    print(GLADIATOR_CHARACTER.to_attack(
        defender_char=GLADIATOR_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    GLADIATOR_CHARACTER.skill_tree.learn_skill(HerculesFurySkill)

    skill = AresBladeSkill(GLADIATOR_CHARACTER)
    print(skill)
    print(GLADIATOR_CHARACTER.cs.physical_attack)
    print(GLADIATOR_CHARACTER.to_attack(
        defender_char=GLADIATOR_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    GLADIATOR_CHARACTER.skill_tree.learn_skill(AresBladeSkill)

    skill = AjaxShieldSkill(GLADIATOR_CHARACTER)
    print(skill)
    print(GLADIATOR_CHARACTER.cs.physical_attack)
    print(GLADIATOR_CHARACTER.cs.show_barrier_points)
    print(skill.function())
    print(GLADIATOR_CHARACTER.cs.show_barrier_points)
    GLADIATOR_CHARACTER.skill_tree.learn_skill(AjaxShieldSkill)

    skill = TurtleStanceSkill(GLADIATOR_CHARACTER)
    print(skill)
    print(GLADIATOR_CHARACTER.bs.constitution)
    print(GLADIATOR_CHARACTER.cs.physical_defense)
    print(skill.function())
    print(GLADIATOR_CHARACTER.cs.physical_defense)
    GLADIATOR_CHARACTER.skill_tree.learn_skill(TurtleStanceSkill)

    skill = UnicornStanceSkill(GLADIATOR_CHARACTER)
    print(skill)
    print(GLADIATOR_CHARACTER.bs.strength)
    print(GLADIATOR_CHARACTER.cs.physical_attack)
    print(skill.function())
    print(GLADIATOR_CHARACTER.cs.physical_attack)
    GLADIATOR_CHARACTER.skill_tree.learn_skill(UnicornStanceSkill)

    skill = ArenaDomainSkill(GLADIATOR_CHARACTER)
    print(skill)
    print(sum([
        GLADIATOR_CHARACTER.bs.strength,
        GLADIATOR_CHARACTER.bs.constitution,
        GLADIATOR_CHARACTER.bs.wisdom,
        GLADIATOR_CHARACTER.bs.charisma,
    ]))
    print(
        GLADIATOR_CHARACTER.cs.hit_points,
        GLADIATOR_CHARACTER.cs.physical_attack,
        GLADIATOR_CHARACTER.cs.physical_defense,
        GLADIATOR_CHARACTER.cs.hit,
        GLADIATOR_CHARACTER.cs.evasion,
    )
    print(skill.function())
    print(
        GLADIATOR_CHARACTER.cs.hit_points,
        GLADIATOR_CHARACTER.cs.physical_attack,
        GLADIATOR_CHARACTER.cs.physical_defense,
        GLADIATOR_CHARACTER.cs.hit,
        GLADIATOR_CHARACTER.cs.evasion,
    )
    GLADIATOR_CHARACTER.skill_tree.learn_skill(ArenaDomainSkill)
