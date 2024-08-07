from typing import TYPE_CHECKING
from rpgram.conditions.debuff import BlindnessCondition
from rpgram.conditions.target_skill_debuff import MuddyCondition
from rpgram.constants.text import EVASION_EMOJI_TEXT, MAGICAL_ATTACK_EMOJI_TEXT
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.debuff import DebuffEnum, get_debuff_emoji_text
from rpgram.enums.skill import (
    ArcanistSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.classes.multiclasse.magical_attack import (
    EarthBreakSkill,
    FireBallSkill,
    WaterBubbleSkill,
    WindGustSkill
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class FireRaySkill(BaseSkill):
    NAME = ArcanistSkillEnum.FIRE_RAY.value
    DESCRIPTION = (
        f'Usa as mãos para conjurar um feixe concentrado de *Energia Ígnea*, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.FIRE)}* e '
        f'*{get_damage_emoji_text(DamageEnum.LIGHTNING)}* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (150% + 5% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.ARCANIST.value,
        'skill_list': [
            FireBallSkill.NAME,
            WindGustSkill.NAME,
        ]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 1.50,
        }
        damage_types = [
            DamageEnum.FIRE,
            DamageEnum.LIGHTNING,
        ]

        super().__init__(
            name=FireRaySkill.NAME,
            description=FireRaySkill.DESCRIPTION,
            rank=FireRaySkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=FireRaySkill.REQUIREMENTS,
            damage_types=damage_types
        )


class FireWaveSkill(BaseSkill):
    NAME = ArcanistSkillEnum.FIRE_WAVE.value
    DESCRIPTION = (
        f'Com um levantar das mãos, conjura uma poderosa *Parede de Chamas* '
        f'que se espalha rapidamente, incinerando tudo em seu caminho e '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.FIRE)}* e '
        f'*{get_damage_emoji_text(DamageEnum.WATER)}* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (75% + 2.5% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.ARCANIST.value,
        'skill_list': [
            FireBallSkill.NAME,
            WaterBubbleSkill.NAME,
        ]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 0.75,
        }
        damage_types = [
            DamageEnum.FIRE,
            DamageEnum.WATER,
        ]

        super().__init__(
            name=FireWaveSkill.NAME,
            description=FireWaveSkill.DESCRIPTION,
            rank=FireWaveSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.TEAM,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=FireWaveSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class MagmaGeyserSkill(BaseSkill):
    NAME = ArcanistSkillEnum.MAGMA_GEYSER.value
    DESCRIPTION = (
        f'Toca o chão com a ponta do dedo para canalizar a energia da '
        f'*Terra* e do *Fogo*, criando uma *Erupção de Magma* em um ponto '
        f'específico, lançando jatos de magma incandescente que incineram '
        f'o alvo e '
        f'causam dano de '
        f'*{get_damage_emoji_text(DamageEnum.FIRE)}* e '
        f'*{get_damage_emoji_text(DamageEnum.GROUND)}* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (150% + 5% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.ARCANIST.value,
        'skill_list': [
            FireBallSkill.NAME,
            EarthBreakSkill.NAME,
        ]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 1.50,
        }
        damage_types = [
            DamageEnum.FIRE,
            DamageEnum.GROUND,
        ]

        super().__init__(
            name=MagmaGeyserSkill.NAME,
            description=MagmaGeyserSkill.DESCRIPTION,
            rank=MagmaGeyserSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=MagmaGeyserSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class SwirlSkill(BaseSkill):
    NAME = ArcanistSkillEnum.SWIRL.value
    DESCRIPTION = (
        f'Canaliza a energia arcana e cria um *Redemoinho Voraz* que '
        f'suga o alvo, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.WIND)}* e '
        f'*{get_damage_emoji_text(DamageEnum.WATER)}* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (150% + 5% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.ARCANIST.value,
        'skill_list': [
            WindGustSkill.NAME,
            WaterBubbleSkill.NAME,
        ]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 1.50,
        }
        damage_types = [
            DamageEnum.WIND,
            DamageEnum.WATER,
        ]

        super().__init__(
            name=SwirlSkill.NAME,
            description=SwirlSkill.DESCRIPTION,
            rank=SwirlSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=SwirlSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class SandGustSkill(BaseSkill):
    NAME = ArcanistSkillEnum.SAND_GUST.value
    DESCRIPTION = (
        f'Manipula a *Terra* e o *Vento* para criar um poderoso '
        f'*Turbilhão de Areia* que se move rapidamente, '
        f'arrastando o alvo e '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.WIND)}* e '
        f'*{get_damage_emoji_text(DamageEnum.GROUND)}* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (150% + 5% x Rank x Nível) e '
        f'adicionando a condição '
        f'*{get_debuff_emoji_text(DebuffEnum.BLINDNESS)}* com nível igual ao '
        f'(Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.ARCANIST.value,
        'skill_list': [
            WindGustSkill.NAME,
            EarthBreakSkill.NAME,
        ]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 1.50,
        }
        damage_types = [
            DamageEnum.WIND,
            DamageEnum.GROUND,
        ]

        super().__init__(
            name=SandGustSkill.NAME,
            description=SandGustSkill.DESCRIPTION,
            rank=SandGustSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=SandGustSkill.REQUIREMENTS,
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
            blindness_condition = BlindnessCondition(level=level)
            status_report = target.status.add_condition(blindness_condition)
            report['status_text'] = status_report['text']

        return report


class MudTrapSkill(BaseSkill):
    NAME = ArcanistSkillEnum.MUD_TRAP.value
    DESCRIPTION = (
        f'Pisa e arrasta o pé suavemente pelo chão, liquefazendo o solo para '
        f'criar um *Poço de Lama Viscoso* sob os pés do alvo, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.WATER)}* e '
        f'*{get_damage_emoji_text(DamageEnum.GROUND)}* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível) e '
        f'diminuindo a *{EVASION_EMOJI_TEXT}* '
        f'com base no dano causado (8% + 2% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.ARCANIST.value,
        'skill_list': [
            WaterBubbleSkill.NAME,
            EarthBreakSkill.NAME,
        ]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 1.25,
        }
        damage_types = [
            DamageEnum.WATER,
            DamageEnum.GROUND,
        ]

        super().__init__(
            name=MudTrapSkill.NAME,
            description=MudTrapSkill.DESCRIPTION,
            rank=MudTrapSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=MudTrapSkill.REQUIREMENTS,
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
            power = int(total_damage)
            level = self.level_rank
            condition = MuddyCondition(power=power, level=level)
            status_report_list = target.status.set_powerful_conditions(
                condition
            )
            status_report_text = "\n".join(
                [report["text"] for report in status_report_list]
            )
            report['status_text'] = status_report_text

        return report


class TetragramShotSkill(BaseSkill):
    NAME = ArcanistSkillEnum.TETRAGRAM_SHOT.value
    DESCRIPTION = (
        f'Realiza quatro movimentos concisos e suaves, '
        f'invocando a energia dos quatro elementos fundamentais para lançar '
        f'contra o inimigo quatro raios devastadores que se mesclam em um '
        f'único disparo '
        f'que causa dano de '
        f'*{get_damage_emoji_text(DamageEnum.GROUND)}*, '
        f'*{get_damage_emoji_text(DamageEnum.FIRE)}*, '
        f'*{get_damage_emoji_text(DamageEnum.WATER)}* e '
        f'*{get_damage_emoji_text(DamageEnum.WIND)}* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (175% + 5% x Rank x Nível).'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.ARCANIST.value,
        'skill_list': [
            EarthBreakSkill.NAME,
            FireBallSkill.NAME,
            WaterBubbleSkill.NAME,
            WindGustSkill.NAME,
        ]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 1.75,
        }
        damage_types = [
            DamageEnum.GROUND,
            DamageEnum.FIRE,
            DamageEnum.WATER,
            DamageEnum.WIND,
        ]

        super().__init__(
            name=TetragramShotSkill.NAME,
            description=TetragramShotSkill.DESCRIPTION,
            rank=TetragramShotSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=TetragramShotSkill.REQUIREMENTS,
            damage_types=damage_types
        )


SKILL_WAY_DESCRIPTION = {
    'name': 'Arcano Elemental',
    'description': (
        'O Arcano Elemental possui uma alma intrinsecamente ligada aos '
        'elementos primordiais da natureza. '
        'Ele é um canal, um condutor de forças essenciais que '
        'moldam o mundo. '
        'Sua compreensão dos elementos não se limita a simples '
        'manipulação; ele os sente, os compreende e os respeita.'
    ),
    'skill_list': [
        FireBallSkill,
        WaterBubbleSkill,
        WindGustSkill,
        EarthBreakSkill,
        FireRaySkill,
        FireWaveSkill,
        MagmaGeyserSkill,
        SwirlSkill,
        SandGustSkill,
        MudTrapSkill,
        TetragramShotSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import ARCANIST_CHARACTER

    skill = FireBallSkill(ARCANIST_CHARACTER)
    print(skill)
    print(ARCANIST_CHARACTER.cs.magical_attack)
    print(ARCANIST_CHARACTER.to_attack(
        defender_char=ARCANIST_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    ARCANIST_CHARACTER.skill_tree.learn_skill(FireBallSkill)

    skill = WaterBubbleSkill(ARCANIST_CHARACTER)
    print(skill)
    print(ARCANIST_CHARACTER.cs.magical_attack)
    print(ARCANIST_CHARACTER.to_attack(
        defender_char=ARCANIST_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    ARCANIST_CHARACTER.skill_tree.learn_skill(WaterBubbleSkill)

    skill = WindGustSkill(ARCANIST_CHARACTER)
    print(skill)
    print(ARCANIST_CHARACTER.cs.magical_attack)
    print(ARCANIST_CHARACTER.to_attack(
        defender_char=ARCANIST_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    ARCANIST_CHARACTER.skill_tree.learn_skill(WindGustSkill)

    skill = EarthBreakSkill(ARCANIST_CHARACTER)
    print(skill)
    print(ARCANIST_CHARACTER.cs.magical_attack)
    print(ARCANIST_CHARACTER.to_attack(
        defender_char=ARCANIST_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    ARCANIST_CHARACTER.skill_tree.learn_skill(EarthBreakSkill)

    ARCANIST_CHARACTER.cs.cure_hit_points(10000)

    skill = FireRaySkill(ARCANIST_CHARACTER)
    print(skill)
    print(ARCANIST_CHARACTER.cs.magical_attack)
    print(ARCANIST_CHARACTER.to_attack(
        defender_char=ARCANIST_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    ARCANIST_CHARACTER.skill_tree.learn_skill(FireRaySkill)

    skill = FireWaveSkill(ARCANIST_CHARACTER)
    print(skill)
    print(ARCANIST_CHARACTER.cs.magical_attack)
    print(ARCANIST_CHARACTER.to_attack(
        defender_char=ARCANIST_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    ARCANIST_CHARACTER.skill_tree.learn_skill(FireWaveSkill)

    skill = MagmaGeyserSkill(ARCANIST_CHARACTER)
    print(skill)
    print(ARCANIST_CHARACTER.cs.magical_attack)
    print(ARCANIST_CHARACTER.to_attack(
        defender_char=ARCANIST_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    ARCANIST_CHARACTER.skill_tree.learn_skill(MagmaGeyserSkill)

    skill = SwirlSkill(ARCANIST_CHARACTER)
    print(skill)
    print(ARCANIST_CHARACTER.cs.magical_attack)
    print(ARCANIST_CHARACTER.to_attack(
        defender_char=ARCANIST_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    ARCANIST_CHARACTER.skill_tree.learn_skill(SwirlSkill)

    skill = SandGustSkill(ARCANIST_CHARACTER)
    print(skill)
    print(ARCANIST_CHARACTER.cs.magical_attack)
    print(ARCANIST_CHARACTER.to_attack(
        defender_char=ARCANIST_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    ARCANIST_CHARACTER.skill_tree.learn_skill(SandGustSkill)

    skill = MudTrapSkill(ARCANIST_CHARACTER)
    print(skill)
    print(ARCANIST_CHARACTER.cs.magical_attack)
    print(ARCANIST_CHARACTER.to_attack(
        defender_char=ARCANIST_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    ARCANIST_CHARACTER.skill_tree.learn_skill(MudTrapSkill)

    ARCANIST_CHARACTER.cs.cure_hit_points(10000)

    skill = TetragramShotSkill(ARCANIST_CHARACTER)
    print(skill)
    print(ARCANIST_CHARACTER.cs.magical_attack)
    print(ARCANIST_CHARACTER.to_attack(
        defender_char=ARCANIST_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    ARCANIST_CHARACTER.skill_tree.learn_skill(TetragramShotSkill)
