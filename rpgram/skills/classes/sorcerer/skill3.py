from random import sample
from typing import TYPE_CHECKING, List
from rpgram.conditions.barrier import ChaosWeaverCondition
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
from rpgram.skills.skill_base import BaseSkill

if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


SKILL_WAY_DESCRIPTION = {
    'name': 'Tecelão do Caos',
    'description': (
        'O Tecelão do Caos manipula as energias arcanas de forma '
        'imprevisível e caótica para gerar efeitos devastadores e '
        'desorientar seus inimigos. '
        'Através de feitiços que combinam elementos de diferentes, '
        'o Feiticeiro se torna um agente da imprevisibilidade, '
        'capaz de lançar rajadas de energia caótica, '
        'conjurar criaturas de outras dimensões e distorcer o '
        'próprio tecido da realidade.'
    )
}


class ChaosOrbSkill(BaseSkill):
    NAME = SorcererSkillEnum.CHAOS_ORB.value
    DESCRIPTION = (
        f'Manipulando a essência da magia caótica, conjura um orbe '
        f'instável que transborda energia imprevisível, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.CHAOS)}* e '
        f'*❓❓❓* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (95% + 5% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.SORCERER.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 0.95,
        }
        damage_types = [DamageEnum.CHAOS, *random_damage_type()]

        super().__init__(
            name=ChaosOrbSkill.NAME,
            description=ChaosOrbSkill.DESCRIPTION,
            rank=ChaosOrbSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=ChaosOrbSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class ChaosVampirismSkill(BaseSkill):
    NAME = SorcererSkillEnum.CHAOS_VAMPIRISM.value
    DESCRIPTION = (
        f'Utiliza a energia do caos para gerar um *Vínculo Caótico* '
        f'com o inimigo e drenar a sua força vital, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.CHAOS)}* e '
        f'*❓❓❓* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (90% + 5% x Rank x Nível) e '
        f'curando a si em 20% do dano causado.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.SORCERER.value,
        'skill_list': [ChaosOrbSkill.NAME],
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 0.90,
        }
        damage_types = [DamageEnum.CHAOS, *random_damage_type(2)]

        super().__init__(
            name=ChaosVampirismSkill.NAME,
            description=ChaosVampirismSkill.DESCRIPTION,
            rank=ChaosVampirismSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=ChaosVampirismSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def hit_function(
        self,
        target: 'BaseCharacter',
        damage: int,
        total_damage: int,
    ) -> dict:
        heal_points = int(total_damage * 0.20)
        heal_report = self.char.cs.cure_hit_points(heal_points)
        player_name = self.char.player_name
        heal_report['text'] = f'*{player_name}* - {heal_report["text"]}'

        return heal_report


class ChaosWeaverSkill(BaseSkill):
    NAME = SorcererSkillEnum.CHAOS_WEAVER.value
    DESCRIPTION = (
        f'Por meio da energia caótica, drena a força vital do inimigo, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.CHAOS)}* e '
        f'*❓❓❓* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (90% + 5% x Rank x Nível) e '
        f'tece um *Véu Caótico* que o protege com uma '
        f'barreira baseada no dano causado (100% + 10% x Rank x Nível)'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.SORCERER.value,
        'skill_list': [ChaosOrbSkill.NAME],
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 0.90,
        }
        damage_types = [DamageEnum.CHAOS, *random_damage_type(2)]

        super().__init__(
            name=ChaosWeaverSkill.NAME,
            description=ChaosWeaverSkill.DESCRIPTION,
            rank=ChaosWeaverSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=ChaosWeaverSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def hit_function(
        self,
        target: 'BaseCharacter',
        damage: int,
        total_damage: int,
    ) -> dict:
        player_name = self.char.player_name
        power = total_damage
        level = self.level_rank
        condition = ChaosWeaverCondition(power=power, level=level)
        report_list = self.char.status.set_conditions(condition)
        status_report_text = f'*{player_name}*: '
        status_report_text += "\n".join(
            [report["text"] for report in report_list]
        )
        report = {'text': status_report_text}

        return report


def random_damage_type(quantity: int = 1) -> List[DamageEnum]:
    damage_enum_list = list(DamageEnum)
    damage_enum_list.remove(DamageEnum.CHAOS)

    return sample(damage_enum_list, quantity)


if __name__ == '__main__':
    from rpgram.constants.test import SORCERER_CHARACTER
    skill = ChaosOrbSkill(SORCERER_CHARACTER)
    print(skill)
    print(SORCERER_CHARACTER.cs.magical_attack)
    SORCERER_CHARACTER.skill_tree.learn_skill(ChaosOrbSkill)

    skill = ChaosVampirismSkill(SORCERER_CHARACTER)
    print(skill)
    print(SORCERER_CHARACTER.cs.magical_attack)
    # print(skill.hit_function(SORCERER_CHARACTER, 1000, 1500))
    print(SORCERER_CHARACTER.to_attack(
        defender_char=SORCERER_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    SORCERER_CHARACTER.skill_tree.learn_skill(ChaosVampirismSkill)

    skill = ChaosWeaverSkill(SORCERER_CHARACTER)
    print(skill)
    print(SORCERER_CHARACTER.cs.magical_attack)
    # print(skill.hit_function(SORCERER_CHARACTER, 1000, 1500))
    print(SORCERER_CHARACTER.to_attack(
        defender_char=SORCERER_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    SORCERER_CHARACTER.skill_tree.learn_skill(ChaosWeaverSkill)
