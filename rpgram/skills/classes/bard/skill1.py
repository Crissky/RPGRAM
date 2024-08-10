
from typing import TYPE_CHECKING

from rpgram.conditions.debuff import DeathSentenceCondition
from rpgram.constants.text import (
    CHARISMA_EMOJI_TEXT,
    MAGICAL_ATTACK_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.skill import (
    BardSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_base import BaseStatsEnum
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class DissonanceSkill(BaseSkill):
    NAME = BardSkillEnum.DISSONANCE.value
    DESCRIPTION = (
        f'Manipula o som para causar *Caos* e *Desorientação* no alvo, '
        f'canalizando sua energia musical para criar uma cacofonia '
        f'ensurdecedora que atinge a mente do adversário, '
        f'causando dano '
        f'*{get_damage_emoji_text(DamageEnum.SONIC)}* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (100% + 5% x Rank x Nível) e no '
        f'*{CHARISMA_EMOJI_TEXT}* (500% + 5% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.BARD.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {
            BaseStatsEnum.CHARISMA: 5.00,
        }
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 1.00,
        }
        damage_types = [
            DamageEnum.SONIC
        ]

        super().__init__(
            name=DissonanceSkill.NAME,
            description=DissonanceSkill.DESCRIPTION,
            rank=DissonanceSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=DissonanceSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class ResonanceSkill(BaseSkill):
    NAME = BardSkillEnum.RESONANCE.value
    DESCRIPTION = (
        f'Canaliza a energia musical para criar ondas sonoras poderosas '
        f'e destrutivas por meio de uma vibração intensa que ressoa '
        f'no corpo do inimigo, '
        f'causando dano '
        f'*{get_damage_emoji_text(DamageEnum.SONIC)}* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (100% + 5% x Rank x Nível) e no '
        f'*{CHARISMA_EMOJI_TEXT}* (750% + 5% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.BARD.value,
        'skill_list': [DissonanceSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {
            BaseStatsEnum.CHARISMA: 7.50,
        }
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 1.00,
        }
        damage_types = [
            DamageEnum.SONIC
        ]

        super().__init__(
            name=ResonanceSkill.NAME,
            description=ResonanceSkill.DESCRIPTION,
            rank=ResonanceSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=ResonanceSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class FatalChordSkill(BaseSkill):
    NAME = BardSkillEnum.FATAL_CHORD.value
    DESCRIPTION = (
        f'Toca uma *Melodia Sombria* e intensa, '
        f'canalizando uma energia de morte em uma única nota que '
        f'causa dano de '
        f'*{get_damage_emoji_text(DamageEnum.CHAOS)}*, '
        f'*{get_damage_emoji_text(DamageEnum.DARK)}* e '
        f'*{get_damage_emoji_text(DamageEnum.SONIC)}* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (100% + 5% x Rank x Nível) e no '
        f'*{CHARISMA_EMOJI_TEXT}* (1000% + 5% x Rank x Nível).'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.BARD.value,
        'skill_list': [DissonanceSkill.NAME, ResonanceSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {
            BaseStatsEnum.CHARISMA: 10.00,
        }
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 1.00,
        }
        damage_types = [
            DamageEnum.CHAOS,
            DamageEnum.DARK,
            DamageEnum.SONIC,
        ]

        super().__init__(
            name=FatalChordSkill.NAME,
            description=FatalChordSkill.DESCRIPTION,
            rank=FatalChordSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=FatalChordSkill.REQUIREMENTS,
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
            blindness_condition = DeathSentenceCondition(level=level)
            status_report = target.status.add_condition(blindness_condition)
            report['status_text'] = status_report['text']

        return report


class SupersonicSkill(BaseSkill):
    NAME = BardSkillEnum.SUPERSONIC.value
    DESCRIPTION = (
        f'Canaliza a energia sonora para criar uma *Onda Supersônica*, '
        f'ao tocar uma nota aguda e intensa, '
        f'disparando uma sinuosidade de som concentrado que viaja em '
        f'alta velocidade por todo o campo de batalha e '
        f'causa dano '
        f'*{get_damage_emoji_text(DamageEnum.SONIC)}* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (50% + 2.5% x Rank x Nível) e no '
        f'*{CHARISMA_EMOJI_TEXT}* (500% + 2.5% x Rank x Nível).'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.BARD.value,
        'skill_list': [DissonanceSkill.NAME, ResonanceSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {
            BaseStatsEnum.CHARISMA: 5.00,
        }
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 0.50,
        }
        damage_types = [
            DamageEnum.SONIC,
            DamageEnum.SONIC,
            DamageEnum.SONIC,
        ]

        super().__init__(
            name=SupersonicSkill.NAME,
            description=SupersonicSkill.DESCRIPTION,
            rank=SupersonicSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.TEAM,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=SupersonicSkill.REQUIREMENTS,
            damage_types=damage_types
        )


SKILL_WAY_DESCRIPTION = {
    'name': 'Sonomante',
    'description': (
        'O Sonomante transcende a mera música. '
        'Ele é um manipulador de sons, capaz de moldar as melodias e '
        'harmonias como ferramentas de combate. '
        'Seus instrumentos não são apenas apetrechos de entretenimento, '
        'mas armas feitas para batalha.'
    ),
    'skill_list': [
        DissonanceSkill,
        ResonanceSkill,
        FatalChordSkill,
        SupersonicSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import BARD_CHARACTER

    skill = DissonanceSkill(BARD_CHARACTER)
    print(skill)
    print(BARD_CHARACTER.cs.magical_attack)
    print(BARD_CHARACTER.to_attack(
        defender_char=BARD_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    BARD_CHARACTER.skill_tree.learn_skill(DissonanceSkill)

    BARD_CHARACTER.cs.cure_hit_points(10_000)
    skill = ResonanceSkill(BARD_CHARACTER)
    print(skill)
    print(BARD_CHARACTER.cs.magical_attack)
    print(BARD_CHARACTER.to_attack(
        defender_char=BARD_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    BARD_CHARACTER.skill_tree.learn_skill(ResonanceSkill)

    BARD_CHARACTER.cs.cure_hit_points(10_000)
    skill = FatalChordSkill(BARD_CHARACTER)
    print(skill)
    print(BARD_CHARACTER.cs.magical_attack)
    print(BARD_CHARACTER.to_attack(
        defender_char=BARD_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    BARD_CHARACTER.skill_tree.learn_skill(FatalChordSkill)

    BARD_CHARACTER.cs.cure_hit_points(10_000)
    skill = SupersonicSkill(BARD_CHARACTER)
    print(skill)
    print(BARD_CHARACTER.cs.magical_attack)
    print(BARD_CHARACTER.to_attack(
        defender_char=BARD_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    BARD_CHARACTER.skill_tree.learn_skill(SupersonicSkill)

    for i in range(10):
        print(
            i,
            '\n'.join(
                report['text']
                for report in BARD_CHARACTER.activate_status()
            )
        )
