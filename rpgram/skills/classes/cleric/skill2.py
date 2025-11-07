
from typing import TYPE_CHECKING
from constant.text import (
    ALERT_SECTION_HEAD
)
from rpgram.constants.text import (
    HIT_POINT_FULL_EMOJI_TEXT,
    MAGICAL_ATTACK_EMOJI_TEXT,
    MAGICAL_DEFENSE_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.debuff import (
    CURSED_DEBUFFS_NAMES,
    get_debuffs_emoji_text
)
from rpgram.enums.race import MALEGNE_RACES
from rpgram.enums.skill import (
    ClericSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class IxChelsAmphoraSkill(BaseSkill):
    NAME = ClericSkillEnum.IXCHELÇÇÇS_AMPHORA.value
    DESCRIPTION = (
        'Um ritual de restauração que conjura uma *Amphora Mística* '
        f'que cura o *{HIT_POINT_FULL_EMOJI_TEXT}* de um aliado '
        f'com base na *{MAGICAL_DEFENSE_EMOJI_TEXT}* '
        '(200% + 10% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.CLERIC.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=IxChelsAmphoraSkill.NAME,
            description=IxChelsAmphoraSkill.DESCRIPTION,
            rank=IxChelsAmphoraSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.HEALING,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=IxChelsAmphoraSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        target_name = char.player_name
        if char.is_alive:
            dice = self.dice
            level = self.level_rank
            power_multiplier = 2 + (level / 10)
            power = dice.boosted_magical_defense * power_multiplier
            power = round(power)

            cure_report = char.cs.cure_hit_points(power)
            report_text = cure_report["text"]
            report = {
                'text': (
                    f'*{target_name}* é banhado pela águas de uma '
                    '*Amphora Mística* que cura suas feridas.\n'
                    f'*{report_text}*({dice.text}).'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


class DhanvantarisAmritaSkill(BaseSkill):
    NAME = ClericSkillEnum.DHANVANTARIÇÇÇS_AMRITA.value
    DESCRIPTION = (
        'Um ritual de purificação que conjura uma *Amrita* '
        'para curar até (5 x Rank x Nível) níveis de condições aleatórias '
        'de um aliado.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.CLERIC.value,
        'skill_list': [IxChelsAmphoraSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=DhanvantarisAmritaSkill.NAME,
            description=DhanvantarisAmritaSkill.DESCRIPTION,
            rank=DhanvantarisAmritaSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.HEALING,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=DhanvantarisAmritaSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter') -> dict:
        target_name = char.player_name
        if char.is_alive:
            level = self.level_rank
            quantity = int(5 * level)
            status_report = char.status.remove_random_debuff_conditions(
                quantity=quantity
            )
            report_text = status_report["text"]
            if report_text:
                alert_section_head_status = ALERT_SECTION_HEAD.format(
                    f'*STATUS ({quantity})*'
                )
                report_text = f'\n\n{alert_section_head_status}{report_text}'
            report = {
                'text': (
                    f'*{target_name}* é coberto pela *Amrita*.'
                    f'{report_text}'
                )
            }
        else:
            report = {'text': f'*{target_name}* está morto.'}

        return report


class ConcealmentSkill(BaseSkill):
    NAME = ClericSkillEnum.CONCEALMENT.value
    DESCRIPTION = (
        'Declara uma palavra de poder que oprime a alma do alvo, '
        'causando dano '
        f'*{get_damage_emoji_text(DamageEnum.BLESSING)}* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (100% + 5% x Rank x Nível). '
        'O dano é setuplicado se o alvo for uma *Criatura Malégna* '
        f'({", ".join(r.title() for r in MALEGNE_RACES)}) ou se estiver '
        'com uma *Condição Amaldiçoante* '
        f'({get_debuffs_emoji_text(*CURSED_DEBUFFS_NAMES)}), '
        'além disso, cura todas as *Condições Amaldiçoantes*.'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.CLERIC.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 1.00,
        }
        damage_types = [DamageEnum.BLESSING]

        super().__init__(
            name=ConcealmentSkill.NAME,
            description=ConcealmentSkill.DESCRIPTION,
            rank=ConcealmentSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=ConcealmentSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def hit_function(
        self,
        target: 'BaseCharacter',
        damage: int,
        total_damage: int,
    ) -> dict:
        report = {'text': ''}

        if target.is_alive and target.is_malegne:
            purge_damage = int(total_damage * 6)
            damage_report = target.cs.damage_hit_points(
                value=purge_damage,
                markdown=True,
            )
            report['text'] = damage_report['text']
            for condition_name in CURSED_DEBUFFS_NAMES:
                status_report = target.status.cure_condition(condition_name)
                if not status_report['is_fail']:
                    report['text'] += "\n" + status_report['text']

        return report


class HolyFireSkill(BaseSkill):
    NAME = ClericSkillEnum.HOLY_FIRE.value
    DESCRIPTION = (
        'Usa o poder da Fé para criar *Chamas Brancas* que incendeiam '
        'o espírito do alvo, causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.FIRE)}* e '
        f'*{get_damage_emoji_text(DamageEnum.BLESSING)}* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível). '
        'O dano é decuplicado se o alvo for uma *Criatura Malégna* '
        f'({", ".join(r.title() for r in MALEGNE_RACES)}) ou se estiver '
        'com uma *Condição Amaldiçoante* '
        f'({get_debuffs_emoji_text(*CURSED_DEBUFFS_NAMES)}), '
        'além disso, cura todas as *Condições Amaldiçoantes*.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.CLERIC.value,
        'skill_list': [ConcealmentSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 1.25,
        }
        damage_types = [DamageEnum.FIRE, DamageEnum.BLESSING]

        super().__init__(
            name=HolyFireSkill.NAME,
            description=HolyFireSkill.DESCRIPTION,
            rank=HolyFireSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=HolyFireSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def hit_function(
        self,
        target: 'BaseCharacter',
        damage: int,
        total_damage: int,
    ) -> dict:
        report = {'text': ''}

        if target.is_alive and target.is_malegne:
            purge_damage = int(total_damage * 9)
            damage_report = target.cs.damage_hit_points(
                value=purge_damage,
                markdown=True,
            )
            report['text'] = damage_report['text']
            for condition_name in CURSED_DEBUFFS_NAMES:
                status_report = target.status.cure_condition(condition_name)
                if not status_report['is_fail']:
                    report['text'] += "\n" + status_report['text']

        return report


class DivinePunishmentSkill(BaseSkill):
    NAME = ClericSkillEnum.DIVINE_PUNISHMENT.value
    DESCRIPTION = (
        'Clama pela punição dos deuses que acenam gentilmente em favor do '
        'rogador, causando dano '
        f'*{get_damage_emoji_text(DamageEnum.DIVINE)}* com base no '
        f'*{MAGICAL_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível). '
        'O dano é centuplicado se o alvo for uma *Criatura Malégna* '
        f'({", ".join(r.title() for r in MALEGNE_RACES)}) ou se estiver '
        'com uma *Condição Amaldiçoante* '
        f'({get_debuffs_emoji_text(*CURSED_DEBUFFS_NAMES)}), '
        'além disso, cura todas as *Condições Amaldiçoantes*.'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.CLERIC.value,
        'skill_list': [ConcealmentSkill.NAME, HolyFireSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_ATTACK: 1.50,
        }
        damage_types = [DamageEnum.DIVINE]

        super().__init__(
            name=DivinePunishmentSkill.NAME,
            description=DivinePunishmentSkill.DESCRIPTION,
            rank=DivinePunishmentSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=DivinePunishmentSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def hit_function(
        self,
        target: 'BaseCharacter',
        damage: int,
        total_damage: int,
    ) -> dict:
        report = {'text': ''}

        if target.is_alive and target.is_malegne:
            purge_damage = int(total_damage * 99)
            damage_report = target.cs.damage_hit_points(
                value=purge_damage,
                markdown=True,
            )
            report['text'] = damage_report['text']
            for condition_name in CURSED_DEBUFFS_NAMES:
                status_report = target.status.cure_condition(condition_name)
                if not status_report['is_fail']:
                    report['text'] += "\n" + status_report['text']

        return report


SKILL_WAY_DESCRIPTION = {
    'name': 'Misericórdia',
    'description': (
        'Movidos por compaixão e devoção à justiça, '
        'os Clérigos do Caminho da Misericórdia dedicam seus poderes '
        'à cura dos aflitos e à redenção dos corrompidos. '
        'Através de magias restauradoras e ataques sagrados purificadores, '
        'eles combatem o mal em todas as suas formas, '
        'aliviando o sofrimento e restaurando a esperança nos corações '
        'dos inocentes.'
    ),
    'skill_list': [
        IxChelsAmphoraSkill,
        DhanvantarisAmritaSkill,
        ConcealmentSkill,
        HolyFireSkill,
        DivinePunishmentSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.conditions.debuff import CurseCondition
    from rpgram.constants.test import CLERIC_CHARACTER

    skill = IxChelsAmphoraSkill(CLERIC_CHARACTER)
    print(skill)
    print(CLERIC_CHARACTER.cs.show_hit_points)
    print(skill.function(CLERIC_CHARACTER))
    print(CLERIC_CHARACTER.cs.show_hit_points)
    CLERIC_CHARACTER.skill_tree.learn_skill(IxChelsAmphoraSkill)

    condition = CurseCondition(level=11)
    CLERIC_CHARACTER.status.add_condition(condition)
    skill = DhanvantarisAmritaSkill(CLERIC_CHARACTER)
    print(skill)
    print(skill.function(CLERIC_CHARACTER))
    CLERIC_CHARACTER.skill_tree.learn_skill(DhanvantarisAmritaSkill)

    skill = ConcealmentSkill(CLERIC_CHARACTER)
    print(skill)
    print(CLERIC_CHARACTER.cs.magical_attack)
    print(CLERIC_CHARACTER.to_attack(
        defender_char=CLERIC_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    CLERIC_CHARACTER.skill_tree.learn_skill(ConcealmentSkill)

    condition = CurseCondition(level=11)
    CLERIC_CHARACTER.status.add_condition(condition)
    skill = HolyFireSkill(CLERIC_CHARACTER)
    print(skill)
    print(CLERIC_CHARACTER.cs.magical_attack)
    print(CLERIC_CHARACTER.to_attack(
        defender_char=CLERIC_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    CLERIC_CHARACTER.skill_tree.learn_skill(HolyFireSkill)

    condition = CurseCondition(level=11)
    CLERIC_CHARACTER.status.add_condition(condition)
    skill = DivinePunishmentSkill(CLERIC_CHARACTER)
    print(skill)
    print(CLERIC_CHARACTER.cs.magical_attack)
    print(CLERIC_CHARACTER.to_attack(
        defender_char=CLERIC_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    CLERIC_CHARACTER.skill_tree.learn_skill(DivinePunishmentSkill)
