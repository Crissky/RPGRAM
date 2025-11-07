from typing import TYPE_CHECKING
from rpgram.conditions.debuff import BlindnessCondition
from rpgram.conditions.target_skill_debuff import (
    AchillesHeelCondition,
    DisarmorCondition
)
from rpgram.constants.text import (
    EVASION_EMOJI_TEXT,
    PHYSICAL_DEFENSE_EMOJI_TEXT,
    PRECISION_ATTACK_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.debuff import DebuffEnum, get_debuff_emoji_text
from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.skill import (
    DuelistSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class InverseSkill(BaseSkill):
    NAME = DuelistSkillEnum.INVERSE.value
    DESCRIPTION = (
        'Avança contra o inimigo e finge um ataque em uma direção, '
        'mas ataca na outra, '
        'causando dano com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.DUELIST.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.25
        }
        damage_types = None

        super().__init__(
            name=InverseSkill.NAME,
            description=InverseSkill.DESCRIPTION,
            rank=InverseSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=InverseSkill.REQUIREMENTS,
            damage_types=damage_types
        )


class DirtyBlowSkill(BaseSkill):
    NAME = DuelistSkillEnum.DIRTY_BLOW.value
    DESCRIPTION = (
        'Acomete contra o inimigo de maneira astuta e imprevisível, '
        'atirando algo em seus olhos para turvar a sua visão '
        'e, em seguida, desfere um golpe veloz, '
        'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.GROUND)}* com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível) e '
        'adicionando a condição '
        f'*{get_debuff_emoji_text(DebuffEnum.BLINDNESS)}* com nível igual ao '
        '(Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.DUELIST.value,
        'skill_list': [InverseSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.25,
        }
        damage_types = [DamageEnum.GROUND]

        super().__init__(
            name=DirtyBlowSkill.NAME,
            description=DirtyBlowSkill.DESCRIPTION,
            rank=DirtyBlowSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=DirtyBlowSkill.REQUIREMENTS,
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


class AchillesHeelSkill(BaseSkill):
    NAME = DuelistSkillEnum.ACHILLEÇÇÇS_HEEL.value
    DESCRIPTION = (
        'Detecta os pontos vulneráveis de seus inimigos, '
        'seja uma articulação frágil, uma postura desequilibrada ou '
        'um movimento previsível e ataca de modo a debilitar os movimentos '
        'do alvo, causando dano com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (150% + 5% x Rank x Nível) e '
        f'diminuindo a *{EVASION_EMOJI_TEXT}* em '
        '(5% do dano causado + 1% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.DUELIST.value,
        'skill_list': [InverseSkill.NAME],
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.50,
        }
        damage_types = None

        super().__init__(
            name=AchillesHeelSkill.NAME,
            description=AchillesHeelSkill.DESCRIPTION,
            rank=AchillesHeelSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=AchillesHeelSkill.REQUIREMENTS,
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
            condition = AchillesHeelCondition(power=power, level=level)
            status_report_list = target.status.set_powerful_conditions(
                condition
            )
            status_report_text = "\n".join(
                [report["text"] for report in status_report_list]
            )
            report['status_text'] = status_report_text

        return report


class DisarmorSkill(BaseSkill):
    NAME = DuelistSkillEnum.DISARMOR.value
    DESCRIPTION = (
        'Identifica uma abertura nas proteções do inimigo e '
        'executa um movimento rápido e preciso, '
        'fragilizando as proteções do oponente e '
        'causando dano com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (90% + 5% x Rank x Nível) e '
        f'diminuindo a *{PHYSICAL_DEFENSE_EMOJI_TEXT}* em '
        '(5% do dano causado + 1% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.DUELIST.value,
        'skill_list': [InverseSkill.NAME],
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 0.90,
        }
        damage_types = None

        super().__init__(
            name=DisarmorSkill.NAME,
            description=DisarmorSkill.DESCRIPTION,
            rank=DisarmorSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=DisarmorSkill.REQUIREMENTS,
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
            condition = DisarmorCondition(power=power, level=level)
            status_report_list = target.status.set_powerful_conditions(
                condition
            )
            status_report_text = "\n".join(
                [report["text"] for report in status_report_list]
            )
            report['status_text'] = status_report_text

        return report


class SiegfriedsShoulderBladeSkill(BaseSkill):
    NAME = DuelistSkillEnum.SIEGFRIEDÇÇÇS_SHOULDER_BLADE.value
    DESCRIPTION = (
        'Avança sobre o oponente e imobiliza-o, '
        'utilizando a sua força e tenacidade para aplicar uma pressão '
        'insuportável sobre o ombro e o pescoço do oponente, '
        'causando dano com base no '
        f'*{PRECISION_ATTACK_EMOJI_TEXT}* (150% + 5% x Rank x Nível). '
        'Caso o golpe seja aplicado com perfeição '
        f'(*Acerto Crítico*{EmojiEnum.DICE.value}) o dano é decuplicado.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.DUELIST.value,
        'skill_list': [InverseSkill.NAME],
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PRECISION_ATTACK: 1.50,
        }
        damage_types = None

        super().__init__(
            name=SiegfriedsShoulderBladeSkill.NAME,
            description=SiegfriedsShoulderBladeSkill.DESCRIPTION,
            rank=SiegfriedsShoulderBladeSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=SiegfriedsShoulderBladeSkill.REQUIREMENTS,
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
            critical_damage = int(total_damage * 9)
            damage_report = target.cs.damage_hit_points(
                value=critical_damage,
                markdown=True,
            )
            report['text'] = damage_report['text']

        return report


SKILL_WAY_DESCRIPTION = {
    'name': 'Jogo Sujo',
    'description': (
        'Com o Jogo Sujo o duelista transcende as regras '
        'tradicionais do combate. '
        'Ele é um mestre da trapaça e utiliza truques e subterfúgios para '
        'derrotar seus inimigos. '
        'Sua habilidade reside em explorar as fraquezas de seus oponentes e '
        'tirar proveito de qualquer vantagem, justa ou não.'
    ),
    'skill_list': [
        InverseSkill,
        DirtyBlowSkill,
        AchillesHeelSkill,
        DisarmorSkill,
        SiegfriedsShoulderBladeSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.constants.test import DUELIST_CHARACTER

    skill = InverseSkill(DUELIST_CHARACTER)
    print(skill)
    print(DUELIST_CHARACTER.cs.precision_attack)
    print(DUELIST_CHARACTER.to_attack(
        defender_char=DUELIST_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    DUELIST_CHARACTER.skill_tree.learn_skill(InverseSkill)

    skill = DirtyBlowSkill(DUELIST_CHARACTER)
    print(skill)
    print(DUELIST_CHARACTER.cs.precision_attack)
    print(DUELIST_CHARACTER.to_attack(
        defender_char=DUELIST_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    DUELIST_CHARACTER.skill_tree.learn_skill(DirtyBlowSkill)

    skill = AchillesHeelSkill(DUELIST_CHARACTER)
    print(skill)
    print(DUELIST_CHARACTER.cs.precision_attack, DUELIST_CHARACTER.cs.evasion)
    print(DUELIST_CHARACTER.to_attack(
        defender_char=DUELIST_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    print(DUELIST_CHARACTER.cs.precision_attack, DUELIST_CHARACTER.cs.evasion)
    DUELIST_CHARACTER.skill_tree.learn_skill(AchillesHeelSkill)

    skill = DisarmorSkill(DUELIST_CHARACTER)
    print(skill)
    print(DUELIST_CHARACTER.cs.precision_attack,
          DUELIST_CHARACTER.cs.physical_defense)
    print(DUELIST_CHARACTER.to_attack(
        defender_char=DUELIST_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    print(DUELIST_CHARACTER.cs.precision_attack,
          DUELIST_CHARACTER.cs.physical_defense)
    DUELIST_CHARACTER.skill_tree.learn_skill(DisarmorSkill)

    skill = SiegfriedsShoulderBladeSkill(DUELIST_CHARACTER)
    print(skill)
    print(DUELIST_CHARACTER.cs.precision_attack)
    print(DUELIST_CHARACTER.to_attack(
        defender_char=DUELIST_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    print(DUELIST_CHARACTER.cs.precision_attack)
    DUELIST_CHARACTER.skill_tree.learn_skill(SiegfriedsShoulderBladeSkill)
