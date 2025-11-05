from typing import TYPE_CHECKING
from rpgram.conditions.debuff import (
    BleedingCondition,
    BurnCondition,
    ParalysisCondition,
    PetrifiedCondition,
    StunnedCondition
)
from rpgram.constants.text import (
    PRECISION_ATTACK_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.debuff import DebuffEnum, get_debuff_emoji_text
from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.skill import (
    SamuraiSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class ZantetsusenSkill(BaseSkill):
    NAME = SamuraiSkillEnum.ZANTETSUSEN.value
    DESCRIPTION = (
        'Executa um poderoso golpe pesado acima da cabeça, '
        'recuando e avançando para um golpe lateral usando as duas mãos, '
        'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.SLASHING)}* com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.SAMURAI.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.25
        }
        damage_types = [DamageEnum.SLASHING]

        super().__init__(
            name=ZantetsusenSkill.NAME,
            description=ZantetsusenSkill.DESCRIPTION,
            rank=ZantetsusenSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=ZantetsusenSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class MizuKogekiSkill(BaseSkill):
    NAME = SamuraiSkillEnum.MIZU_KOGEKI.value
    DESCRIPTION = (
        'Executa movimentos giratórios para desferir um poderoso golpe '
        'usando as duas mãos, '
        'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.SLASHING)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.WATER)}* com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (150% + 5% x Rank x Nível) e '
        'adicionando a condição '
        f'*{get_debuff_emoji_text(DebuffEnum.STUNNED)}* com nível igual ao '
        f'(Rank x Nível) se tirar 15{EmojiEnum.DICE.value} ou mais.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.SAMURAI.value,
        'skill_list': [ZantetsusenSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.50
        }
        damage_types = [DamageEnum.SLASHING, DamageEnum.WATER]

        super().__init__(
            name=MizuKogekiSkill.NAME,
            description=MizuKogekiSkill.DESCRIPTION,
            rank=MizuKogekiSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=MizuKogekiSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def hit_function(
        self,
        target: 'BaseCharacter',
        damage: int,
        total_damage: int,
    ) -> dict:
        report = {'text': ''}
        if target.is_alive and self.dice.value >= 15:
            level = self.level_rank
            stunned_condition = StunnedCondition(level=level)
            status_report = target.status.add_condition(stunned_condition)
            report['status_text'] = status_report['text']

        return report


class HonoKogekiSkill(BaseSkill):
    NAME = SamuraiSkillEnum.HONO_KOGEKI.value
    DESCRIPTION = (
        'Executa um movimento concentrado para desferir um poderoso golpe '
        'usando as duas mãos, '
        'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.SLASHING)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.FIRE)}* com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (150% + 5% x Rank x Nível) e '
        'adicionando a condição '
        f'*{get_debuff_emoji_text(DebuffEnum.BURN)}* com nível igual ao '
        f'(Rank x Nível) se tirar 5{EmojiEnum.DICE.value} ou mais.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.SAMURAI.value,
        'skill_list': [ZantetsusenSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.50
        }
        damage_types = [DamageEnum.SLASHING, DamageEnum.FIRE]

        super().__init__(
            name=HonoKogekiSkill.NAME,
            description=HonoKogekiSkill.DESCRIPTION,
            rank=HonoKogekiSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=HonoKogekiSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def hit_function(
        self,
        target: 'BaseCharacter',
        damage: int,
        total_damage: int,
    ) -> dict:
        report = {'text': ''}
        if target.is_alive and self.dice.value >= 5:
            level = self.level_rank
            burn_condition = BurnCondition(level=level)
            status_report = target.status.add_condition(burn_condition)
            report['status_text'] = status_report['text']

        return report


class KosenKogekiSkill(BaseSkill):
    NAME = SamuraiSkillEnum.KOSEN_KOGEKI.value
    DESCRIPTION = (
        'Executa um movimento rápido para desferir um poderoso golpe '
        'usando as duas mãos, '
        'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.SLASHING)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.LIGHTNING)}* com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (150% + 5% x Rank x Nível) e '
        'adicionando a condição '
        f'*{get_debuff_emoji_text(DebuffEnum.PARALYSIS)}* com nível igual ao '
        f'(Rank x Nível) se tirar 15{EmojiEnum.DICE.value} ou mais.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.SAMURAI.value,
        'skill_list': [ZantetsusenSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.50
        }
        damage_types = [DamageEnum.SLASHING, DamageEnum.LIGHTNING]

        super().__init__(
            name=KosenKogekiSkill.NAME,
            description=KosenKogekiSkill.DESCRIPTION,
            rank=KosenKogekiSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=KosenKogekiSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def hit_function(
        self,
        target: 'BaseCharacter',
        damage: int,
        total_damage: int,
    ) -> dict:
        report = {'text': ''}
        if target.is_alive and self.dice.value >= 15:
            level = self.level_rank
            paralysis_condition = ParalysisCondition(level=level)
            status_report = target.status.add_condition(paralysis_condition)
            report['status_text'] = status_report['text']

        return report


class KazeKogekiSkill(BaseSkill):
    NAME = SamuraiSkillEnum.KAZE_KOGEKI.value
    DESCRIPTION = (
        'Executa um movimento direto para desferir um poderoso golpe '
        'usando as duas mãos, '
        'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.SLASHING)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.WIND)}* com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (150% + 5% x Rank x Nível) e '
        'adicionando a condição '
        f'*{get_debuff_emoji_text(DebuffEnum.BLEEDING)}* com nível igual ao '
        f'(Rank x Nível) se tirar 5{EmojiEnum.DICE.value} ou mais.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.SAMURAI.value,
        'skill_list': [ZantetsusenSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.50
        }
        damage_types = [DamageEnum.SLASHING, DamageEnum.WIND]

        super().__init__(
            name=KazeKogekiSkill.NAME,
            description=KazeKogekiSkill.DESCRIPTION,
            rank=KazeKogekiSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=KazeKogekiSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def hit_function(
        self,
        target: 'BaseCharacter',
        damage: int,
        total_damage: int,
    ) -> dict:
        report = {'text': ''}
        if target.is_alive and self.dice.value >= 5:
            level = self.level_rank
            bleeding_condition = BleedingCondition(level=level)
            status_report = target.status.add_condition(bleeding_condition)
            report['status_text'] = status_report['text']

        return report


class IwaKogekiSkill(BaseSkill):
    NAME = SamuraiSkillEnum.IWA_KOGEKI.value
    DESCRIPTION = (
        'Executa um movimento pesado para desferir um poderoso golpe '
        'usando as duas mãos, '
        'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.SLASHING)}* e de '
        f'*{get_damage_emoji_text(DamageEnum.ROCK)}* com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (150% + 5% x Rank x Nível) e '
        'adicionando a condição '
        f'*{get_debuff_emoji_text(DebuffEnum.PETRIFIED)}* com nível igual ao '
        f'(Rank x Nível) se for *Acerto Crítico*{EmojiEnum.DICE.value}.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.SAMURAI.value,
        'skill_list': [ZantetsusenSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.50
        }
        damage_types = [DamageEnum.SLASHING, DamageEnum.ROCK]

        super().__init__(
            name=IwaKogekiSkill.NAME,
            description=IwaKogekiSkill.DESCRIPTION,
            rank=IwaKogekiSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=IwaKogekiSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def hit_function(
        self,
        target: 'BaseCharacter',
        damage: int,
        total_damage: int,
    ) -> dict:
        report = {'text': ''}
        if target.is_alive and self.dice.is_critical:
            level = self.level_rank
            petrified_condition = PetrifiedCondition(level=level)
            status_report = target.status.add_condition(petrified_condition)
            report['status_text'] = status_report['text']

        return report


SKILL_WAY_DESCRIPTION = {
    'name': 'Gogyō no Ken (五行の剣)',
    'description': (
        'O Gogyō no Ken (Espada dos Cinco Elementos) '
        'transcende a mera proficiência com a espada; '
        'é uma filosofia de combate profundamente enraizada na natureza. '
        'O samurai que segue este caminho não apenas domina as '
        'técnicas de combate, mas busca a harmonia entre o '
        'homem e o universo, se tornando um mestre da manipulação '
        'dos cinco elementos (Água, Fogo, Raio, Vento e Rocha), '
        'canalizando-os através de sua arma.'
    ),
    'skill_list': [
        ZantetsusenSkill,
        MizuKogekiSkill,
        HonoKogekiSkill,
        KosenKogekiSkill,
        KazeKogekiSkill,
        IwaKogekiSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import SAMURAI_CHARACTER

    skill = ZantetsusenSkill(SAMURAI_CHARACTER)
    print(skill)
    print(SAMURAI_CHARACTER.cs.precision_attack)
    print(SAMURAI_CHARACTER.to_attack(
        defender_char=SAMURAI_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    SAMURAI_CHARACTER.skill_tree.learn_skill(ZantetsusenSkill)

    skill = MizuKogekiSkill(SAMURAI_CHARACTER)
    print(skill)
    print(SAMURAI_CHARACTER.cs.precision_attack)
    print(SAMURAI_CHARACTER.to_attack(
        defender_char=SAMURAI_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    SAMURAI_CHARACTER.skill_tree.learn_skill(MizuKogekiSkill)

    skill = HonoKogekiSkill(SAMURAI_CHARACTER)
    print(skill)
    print(SAMURAI_CHARACTER.cs.precision_attack)
    print(SAMURAI_CHARACTER.to_attack(
        defender_char=SAMURAI_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    SAMURAI_CHARACTER.skill_tree.learn_skill(HonoKogekiSkill)

    skill = KosenKogekiSkill(SAMURAI_CHARACTER)
    print(skill)
    print(SAMURAI_CHARACTER.cs.precision_attack)
    print(SAMURAI_CHARACTER.to_attack(
        defender_char=SAMURAI_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    SAMURAI_CHARACTER.skill_tree.learn_skill(KosenKogekiSkill)

    skill = KazeKogekiSkill(SAMURAI_CHARACTER)
    print(skill)
    print(SAMURAI_CHARACTER.cs.precision_attack)
    print(SAMURAI_CHARACTER.to_attack(
        defender_char=SAMURAI_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    SAMURAI_CHARACTER.skill_tree.learn_skill(KazeKogekiSkill)

    skill = IwaKogekiSkill(SAMURAI_CHARACTER)
    print(skill)
    print(SAMURAI_CHARACTER.cs.precision_attack)
    print(SAMURAI_CHARACTER.to_attack(
        defender_char=SAMURAI_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    SAMURAI_CHARACTER.skill_tree.learn_skill(IwaKogekiSkill)
