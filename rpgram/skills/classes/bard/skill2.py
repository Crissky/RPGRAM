from typing import TYPE_CHECKING

from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.target_skill_buff import (
    CrescentMoonBalladCondition,
    TricksterTrovaCondition,
    WarSongCondition
)
from rpgram.constants.text import (
    CHARISMA_EMOJI_TEXT,
    EVASION_EMOJI_TEXT,
    HIT_EMOJI_TEXT,
    HIT_POINT_FULL_EMOJI_TEXT,
    MAGICAL_ATTACK_EMOJI_TEXT,
    MAGICAL_DEFENSE_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT,
    PHYSICAL_DEFENSE_EMOJI_TEXT,
    PRECISION_ATTACK_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.skill import (
    BardSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class WarSongSkill(BaseSkill):
    NAME = BardSkillEnum.WAR_SONG.value
    DESCRIPTION = (
        'Entoa uma *Antiga Canção de Batalha* para inspirar um companheiro, '
        'aumentando o '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}*, '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}*, '
        f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* e o '
        f'*{HIT_POINT_FULL_EMOJI_TEXT}* de ambos com base no '
        f'*{CHARISMA_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.BARD.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=WarSongSkill.NAME,
            description=WarSongSkill.DESCRIPTION,
            rank=WarSongSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=WarSongSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        player_name = self.char.player_name
        target_name = char.player_name
        level = self.level_rank
        power = self.char.cs.charisma
        self_condition = WarSongCondition(power=power, level=level)
        report_list = self.char.status.set_conditions(self_condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* se inspira pela *{self.name}*, '
                'que aumenta o '
                f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* '
                f'em {self_condition.bonus_physical_attack} pontos, '
                f'*{PRECISION_ATTACK_EMOJI_TEXT}* '
                f'em {self_condition.bonus_precision_attack} pontos, '
                f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* '
                f'em {self_condition.bonus_physical_defense} pontos e o '
                f'*{HIT_POINT_FULL_EMOJI_TEXT}* '
                f'em {self_condition.bonus_hit_points} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }
        if char.is_alive and self.char.player_id != char.player_id:
            condition = WarSongCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report['text'] += (
                '\n\n'
                f'*{target_name}* também é inspirado pela *{self.name}*, '
                'que aumenta o '
                f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* '
                f'em {condition.bonus_physical_attack} pontos, '
                f'*{PRECISION_ATTACK_EMOJI_TEXT}* '
                f'em {condition.bonus_precision_attack} pontos, '
                f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* '
                f'em {condition.bonus_physical_defense} pontos e o '
                f'*{HIT_POINT_FULL_EMOJI_TEXT}* '
                f'em {condition.bonus_hit_points} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        elif char.is_dead:
            report['text'] += f'\n\n*{target_name}* está morto.'

        return report


class CrescentMoonBalladSkill(BaseSkill):
    NAME = BardSkillEnum.CRESCENT_MOON_BALLAD.value
    DESCRIPTION = (
        'Solfea uma *Balada Élfica* que inspira um companheiro, '
        'aumentando o '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}*, '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* e o '
        f'*{HIT_POINT_FULL_EMOJI_TEXT}* de ambos com base no '
        f'*{CHARISMA_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.BARD.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=CrescentMoonBalladSkill.NAME,
            description=CrescentMoonBalladSkill.DESCRIPTION,
            rank=CrescentMoonBalladSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=CrescentMoonBalladSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        player_name = self.char.player_name
        target_name = char.player_name
        level = self.level_rank
        power = self.char.cs.charisma
        self_condition = CrescentMoonBalladCondition(power=power, level=level)
        report_list = self.char.status.set_conditions(self_condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* se inspira pela *{self.name}*, '
                'que aumenta o '
                f'*{MAGICAL_ATTACK_EMOJI_TEXT}* '
                f'em {self_condition.bonus_magical_attack} pontos, '
                f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* '
                f'em {self_condition.bonus_magical_defense} pontos e o '
                f'*{HIT_POINT_FULL_EMOJI_TEXT}* '
                f'em {self_condition.bonus_hit_points} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }
        if char.is_alive and self.char.player_id != char.player_id:
            condition = CrescentMoonBalladCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report['text'] += (
                '\n\n'
                f'*{target_name}* também é inspirado pela *{self.name}*, '
                'que aumenta o '
                f'*{MAGICAL_ATTACK_EMOJI_TEXT}* '
                f'em {condition.bonus_magical_attack} pontos, '
                f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* '
                f'em {condition.bonus_magical_defense} pontos e o '
                f'*{HIT_POINT_FULL_EMOJI_TEXT}* '
                f'em {condition.bonus_hit_points} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        elif char.is_dead:
            report['text'] += f'\n\n*{target_name}* está morto.'

        return report


class TricksterTrovaSkill(BaseSkill):
    NAME = BardSkillEnum.TRICKSTER_TROVA.value
    DESCRIPTION = (
        'Surrura, como que contando um secredo, uma *Trova dos Halfling* '
        'que inspira um companheiro, '
        'aumentando o '
        f'*{HIT_EMOJI_TEXT}*, '
        f'*{EVASION_EMOJI_TEXT}* e o '
        f'*{HIT_POINT_FULL_EMOJI_TEXT}* de ambos com base no '
        f'*{CHARISMA_EMOJI_TEXT}* (100% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.BARD.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=TricksterTrovaSkill.NAME,
            description=TricksterTrovaSkill.DESCRIPTION,
            rank=TricksterTrovaSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=TricksterTrovaSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        player_name = self.char.player_name
        target_name = char.player_name
        level = self.level_rank
        power = self.char.cs.charisma
        self_condition = TricksterTrovaCondition(power=power, level=level)
        report_list = self.char.status.set_conditions(self_condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* se inspira pela *{self.name}*, '
                'que aumenta o '
                f'*{HIT_EMOJI_TEXT}* '
                f'em {self_condition.bonus_hit} pontos, '
                f'*{EVASION_EMOJI_TEXT}* '
                f'em {self_condition.bonus_evasion} pontos e o '
                f'*{HIT_POINT_FULL_EMOJI_TEXT}* '
                f'em {self_condition.bonus_hit_points} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }
        if char.is_alive and self.char.player_id != char.player_id:
            condition = TricksterTrovaCondition(power=power, level=level)
            report_list = char.status.set_conditions(condition)
            status_report_text = "\n".join(
                [report["text"] for report in report_list]
            )
            report['text'] += (
                '\n\n'
                f'*{target_name}* também é inspirado pela *{self.name}*, '
                'que aumenta o '
                f'*{HIT_EMOJI_TEXT}* '
                f'em {self_condition.bonus_hit} pontos, '
                f'*{EVASION_EMOJI_TEXT}* '
                f'em {self_condition.bonus_evasion} pontos e o '
                f'*{HIT_POINT_FULL_EMOJI_TEXT}* '
                f'em {self_condition.bonus_hit_points} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        elif char.is_dead:
            report['text'] += f'\n\n*{target_name}* está morto.'

        return report


class InvigoratingSongSkill(BaseSkill):
    NAME = BardSkillEnum.INVIGORATING_SONG.value
    DESCRIPTION = (
        'Executa uma melodia suave e calmante que transmite energia vital '
        'ao companheiro ferido, '
        f'curando o *{HIT_POINT_FULL_EMOJI_TEXT}* de ambos com base na '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* (100% + 10% x Rank x Nível) e no '
        f'*{CHARISMA_EMOJI_TEXT}* (750% + 10% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.BARD.value,
        'skill_list': [
            WarSongSkill.NAME,
            CrescentMoonBalladSkill.NAME,
            TricksterTrovaSkill.NAME,
        ]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=InvigoratingSongSkill.NAME,
            description=InvigoratingSongSkill.DESCRIPTION,
            rank=InvigoratingSongSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.HEALING,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=InvigoratingSongSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        player_name = self.char.player_name
        target_name = char.player_name
        dice = self.dice
        level = self.level_rank
        magical_attack_power_multiplier = 1 + (level / 10)
        charisma_power_multiplier = 7.5 + (level / 10)
        power = sum([
            dice.boosted_magical_attack * magical_attack_power_multiplier,
            self.char.cs.charisma * charisma_power_multiplier
        ])
        power = round(power)
        cure_report = self.char.cs.cure_hit_points(power)
        report_text = cure_report["text"]
        report = {
            'text': (
                f'*{player_name}* é rodeado por uma melodia suave e '
                'calmante que cura suas feridas.\n'
                f'*{report_text}*({dice.text}).'
            )
        }
        if char.is_alive and self.char.player_id != char.player_id:
            cure_report = char.cs.cure_hit_points(power)
            report_text = cure_report["text"]
            report['text'] += (
                '\n\n'
                f'*{target_name}* é rodeado por uma melodia suave e '
                'calmante que cura suas feridas.\n'
                f'*{report_text}*({dice.text}).'
            )
        elif char.is_dead:
            report['text'] += f'\n\n*{target_name}* está morto.'

        return report


SKILL_WAY_DESCRIPTION = {
    'name': 'Inspirador',
    'description': (
        'O Inspirador utiliza a força da música e da palavra para elevar '
        'a moral de seus aliados e inspirá-los a grandes feitos, '
        'inflamando os seus corações e fortalecendo os seus espíritos. '
        'Sua voz é como um bálsamo para a alma, capaz de curar feridas, '
        'fortalecer a determinação e unir a equipe.'
    ),
    'skill_list': [
        WarSongSkill,
        CrescentMoonBalladSkill,
        TricksterTrovaSkill,
        InvigoratingSongSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import BARD_CHARACTER, BARBARIAN_CHARACTER

    skill = WarSongSkill(BARD_CHARACTER)
    print(skill)
    print(BARD_CHARACTER.bs.charisma)
    print(
        BARD_CHARACTER.cs.physical_attack,
        BARD_CHARACTER.cs.precision_attack,
        BARD_CHARACTER.cs.physical_defense,
        BARD_CHARACTER.cs.hp
    )
    print(skill.function(BARBARIAN_CHARACTER))
    print(
        BARD_CHARACTER.cs.physical_attack,
        BARD_CHARACTER.cs.precision_attack,
        BARD_CHARACTER.cs.physical_defense,
        BARD_CHARACTER.cs.hp
    )
    BARD_CHARACTER.skill_tree.learn_skill(WarSongSkill)

    skill = CrescentMoonBalladSkill(BARD_CHARACTER)
    print(skill)
    print(BARD_CHARACTER.bs.charisma)
    print(
        BARD_CHARACTER.cs.magical_attack,
        BARD_CHARACTER.cs.magical_defense,
        BARD_CHARACTER.cs.hp
    )
    print(skill.function(BARBARIAN_CHARACTER))
    print(
        BARD_CHARACTER.cs.magical_attack,
        BARD_CHARACTER.cs.magical_defense,
        BARD_CHARACTER.cs.hp
    )
    BARD_CHARACTER.skill_tree.learn_skill(CrescentMoonBalladSkill)

    skill = TricksterTrovaSkill(BARD_CHARACTER)
    print(skill)
    print(BARD_CHARACTER.bs.charisma)
    print(
        BARD_CHARACTER.cs.magical_attack,
        BARD_CHARACTER.cs.magical_defense,
        BARD_CHARACTER.cs.hp
    )
    print(skill.function(BARBARIAN_CHARACTER))
    print(
        BARD_CHARACTER.cs.magical_attack,
        BARD_CHARACTER.cs.magical_defense,
        BARD_CHARACTER.cs.hp
    )
    BARD_CHARACTER.skill_tree.learn_skill(TricksterTrovaSkill)

    BARBARIAN_CHARACTER.cs.damage_hit_points(10000)
    skill = InvigoratingSongSkill(BARD_CHARACTER)
    print(skill)
    print(BARD_CHARACTER.cs.magical_attack, BARD_CHARACTER.bs.charisma)
    print(skill.function(BARBARIAN_CHARACTER))
    BARD_CHARACTER.skill_tree.learn_skill(InvigoratingSongSkill)

    print('\n'.join([
        report['text']
        for report in BARD_CHARACTER.activate_status()
    ]))
