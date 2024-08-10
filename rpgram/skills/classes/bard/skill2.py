from typing import TYPE_CHECKING

from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.target_skill_buff import (
    CrescentMoonSongCondition,
    WarSongCondition
)
from rpgram.constants.text import (
    CHARISMA_EMOJI_TEXT,
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
        f'Entoa uma antiga canção de batalha para inspirar um companheiro, '
        f'aumentando o '
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
                f'que aumenta o '
                f'*{PHYSICAL_ATTACK_EMOJI_TEXT}*, '
                f'*{PRECISION_ATTACK_EMOJI_TEXT}*, '
                f'*{PHYSICAL_DEFENSE_EMOJI_TEXT}* e o '
                f'*{HIT_POINT_FULL_EMOJI_TEXT}*.\n\n'
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
                f'*\n\n{target_name}* também é inspirado pela '
                f'*{self.name}*.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        elif char.is_dead:
            report['text'] += f'\n\n*{target_name}* está morto.'

        return report


class CrescentMoonSongSkill(BaseSkill):
    NAME = BardSkillEnum.CRESCENT_MOON_SONG.value
    DESCRIPTION = (
        f'Solfea uma canção élfica que inspira um companheiro, '
        f'aumentando o '
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
            name=CrescentMoonSongSkill.NAME,
            description=CrescentMoonSongSkill.DESCRIPTION,
            rank=CrescentMoonSongSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=CrescentMoonSongSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        player_name = self.char.player_name
        target_name = char.player_name
        level = self.level_rank
        power = self.char.cs.charisma
        self_condition = CrescentMoonSongCondition(power=power, level=level)
        report_list = self.char.status.set_conditions(self_condition)
        status_report_text = "\n".join(
            [report["text"] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* se inspira pela *{self.name}*, '
                f'que aumenta o '
                f'*{MAGICAL_ATTACK_EMOJI_TEXT}*, '
                f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* e o '
                f'*{HIT_POINT_FULL_EMOJI_TEXT}*.\n\n'
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
                f'*\n\n{target_name}* também é inspirado pela '
                f'*{self.name}*.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
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
        CrescentMoonSongSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import BARD_CHARACTER, BARBARIAN_CHARACTER

    skill = WarSongSkill(BARD_CHARACTER)
    print(skill)
    print(BARD_CHARACTER.bs.charisma)
    print(BARD_CHARACTER.cs.physical_attack, BARD_CHARACTER.cs.precision_attack,
          BARD_CHARACTER.cs.physical_defense, BARD_CHARACTER.cs.hp)
    print(skill.function(BARBARIAN_CHARACTER))
    print(BARD_CHARACTER.cs.physical_attack, BARD_CHARACTER.cs.precision_attack,
          BARD_CHARACTER.cs.physical_defense, BARD_CHARACTER.cs.hp)
    BARD_CHARACTER.skill_tree.learn_skill(WarSongSkill)

    skill = CrescentMoonSongSkill(BARD_CHARACTER)
    print(skill)
    print(BARD_CHARACTER.bs.charisma)
    print(BARD_CHARACTER.cs.magical_attack,
          BARD_CHARACTER.cs.magical_defense, BARD_CHARACTER.cs.hp)
    print(skill.function(BARBARIAN_CHARACTER))
    print(BARD_CHARACTER.cs.magical_attack,
          BARD_CHARACTER.cs.magical_defense, BARD_CHARACTER.cs.hp)
    BARD_CHARACTER.skill_tree.learn_skill(CrescentMoonSongSkill)

    print('\n'.join([
        report['text']
        for report in BARD_CHARACTER.activate_status()
    ]))
