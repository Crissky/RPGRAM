from random import choice
from typing import TYPE_CHECKING

from constant.text import ALERT_SECTION_HEAD_ADD_STATUS
from rpgram.conditions.debuff import BleedingCondition, ExhaustionCondition
from rpgram.conditions.factory import copy_condition
from rpgram.conditions.self_skill import PenitenceCondition
from rpgram.constants.text import (
    HIT_POINT_FULL_EMOJI_TEXT,
    MAGICAL_DEFENSE_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT
)
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum, get_damage_emoji_text
from rpgram.enums.debuff import (
    CURSED_DEBUFFS_NAMES,
    DebuffEnum,
    get_debuff_emoji_text,
    get_debuffs_emoji_text
)
from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.skill import (
    PaladinSkillEnum,
    SkillDefenseEnum,
    SkillTypeEnum,
    TargetEnum
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class FloggingsSkill(BaseSkill):
    NAME = PaladinSkillEnum.FLOGGINGS.value
    DESCRIPTION = (
        f'Entregue a *Sede de Justiça*, castiga a transgressão do alvo com um '
        f'*Flagelo* repleto de pontas cortantes, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.SLASHING)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (100% + 5% x Rank x Nível).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.PALADIN.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.00,
        }
        damage_types = [
            DamageEnum.SLASHING,
            DamageEnum.SLASHING,
            DamageEnum.SLASHING,
        ]

        super().__init__(
            name=FloggingsSkill.NAME,
            description=FloggingsSkill.DESCRIPTION,
            rank=FloggingsSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=FloggingsSkill.REQUIREMENTS,
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
            bleeding_condition = BleedingCondition(level=level)
            status_report = target.status.add_condition(bleeding_condition)
            report['status_text'] = status_report['text']

        return report


class CutThroatSkill(BaseSkill):
    NAME = PaladinSkillEnum.CUT_THROAT.value
    DESCRIPTION = (
        f'Imerso no *Ódio dos Deuses*, pune os pecados do oponente com um '
        f'*Corte em sua Garganta*, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.SLASHING)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (125% + 5% x Rank x Nível) e '
        f'adicionando a condição '
        f'*{get_debuff_emoji_text(DebuffEnum.BLEEDING)}* com nível igual ao '
        f'(Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.PALADIN.value,
        'skill_list': [FloggingsSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.25,
        }
        damage_types = [DamageEnum.SLASHING]

        super().__init__(
            name=CutThroatSkill.NAME,
            description=CutThroatSkill.DESCRIPTION,
            rank=CutThroatSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=CutThroatSkill.REQUIREMENTS,
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
            bleeding_condition = BleedingCondition(level=level)
            status_report = target.status.add_condition(bleeding_condition)
            report['status_text'] = status_report['text']

        return report


class VladsPunishmentSkill(BaseSkill):
    NAME = PaladinSkillEnum.VLADS_PUNISHMENT.value
    DESCRIPTION = (
        f'Envolto pela *Crueldade e Brutalidade dos Deuses*, '
        f'escarmenta os sacrilégios do inimigo com um '
        f'golpe empalador, '
        f'causando dano de '
        f'*{get_damage_emoji_text(DamageEnum.PIERCING)}* com base no '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* (150% + 5% x Rank x Nível) e '
        f'adicionando a condição '
        f'*{get_debuff_emoji_text(DebuffEnum.BLEEDING)}* com nível igual ao '
        f'(Rank x Nível + {EmojiEnum.DICE.value}).'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.PALADIN.value,
        'skill_list': [FloggingsSkill.NAME, CutThroatSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.PHYSICAL_ATTACK: 1.50,
        }
        damage_types = [DamageEnum.SLASHING]

        super().__init__(
            name=VladsPunishmentSkill.NAME,
            description=VladsPunishmentSkill.DESCRIPTION,
            rank=VladsPunishmentSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.PHYSICAL,
            char=char,
            use_equips_damage_types=True,
            requirements=VladsPunishmentSkill.REQUIREMENTS,
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
            level = self.level_rank + self.dice.value
            bleeding_condition = BleedingCondition(level=level)
            status_report = target.status.add_condition(bleeding_condition)
            report['status_text'] = status_report['text']

        return report


class ConfessionSkill(BaseSkill):
    NAME = PaladinSkillEnum.CONFESSION.value
    DESCRIPTION = (
        f'Combina a *Fé Inabalável* com a *Força da Justiça* '
        f'para se conecta com uma força superior, canalizando sua energia '
        f'para purificar a sua alma, '
        f'revigorando seu espírito e curando seu '
        f'{HIT_POINT_FULL_EMOJI_TEXT} com base na '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* (300% + 10% x Rank x Nível). '
        f'além disso, cura todas as *Condições Amaldiçoantes* '
        f'({get_debuffs_emoji_text(*CURSED_DEBUFFS_NAMES)}).'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.PALADIN.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=ConfessionSkill.NAME,
            description=ConfessionSkill.DESCRIPTION,
            rank=ConfessionSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.HEALING,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=ConfessionSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        player_name = self.char.player_name
        dice = self.dice
        level = self.level_rank
        power_multiplier = 3 + (level / 10)
        power = dice.boosted_magical_defense * power_multiplier
        power = round(power)

        cure_report = self.char.cs.cure_hit_points(power)
        report_text = cure_report["text"]
        report = {
            'text': (
                f'*{player_name}* respira fundo, clamando às '
                f'forças superiores que purificam a sua alma e '
                f'curam as suas feridas.\n'
                f'*{report_text}*({dice.text}).'
            )
        }
        for condition_name in CURSED_DEBUFFS_NAMES:
            status_report = self.char.status.cure_condition(condition_name)
            if not status_report['is_fail']:
                report['text'] += "\n" + status_report['text']

        return report


class PenitenceSkill(BaseSkill):
    NAME = PaladinSkillEnum.PENITENCE.value
    DESCRIPTION = (
        f'Constringe o *Cilício* em sua coxa, '
        f'submetendo-se a um julgamento interior para expurgar '
        f'os próprios pecados e fortalecer a sua fé, '
        f'diminuindo o '
        f'*{HIT_POINT_FULL_EMOJI_TEXT} BASE* em 25% '
        f'para aumentar o '
        f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* e a '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* em '
        f'(25% do valor base + 1% x Rank x Nível).'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.PALADIN.value,
        'skill_list': [ConfessionSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {}
        damage_types = None

        super().__init__(
            name=PenitenceSkill.NAME,
            description=PenitenceSkill.DESCRIPTION,
            rank=PenitenceSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SELF,
            skill_type=SkillTypeEnum.BUFF,
            skill_defense=SkillDefenseEnum.NA,
            char=char,
            use_equips_damage_types=False,
            requirements=PenitenceSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def function(self, char: 'BaseCharacter' = None) -> dict:
        char = self.char
        player_name = char.player_name
        level = self.level_rank
        condition = PenitenceCondition(character=char, level=level)
        report_list = char.status.set_conditions(condition)
        status_report_text = '\n'.join(
            [report['text'] for report in report_list]
        )
        report = {
            'text': (
                f'*{player_name}* Constringe o seu *Cilício*, '
                f'reduzindo o seu '
                f'*{HIT_POINT_FULL_EMOJI_TEXT}* '
                f'em {condition.bonus_hit_points} pontos '
                f'em favor de aumentar a seu '
                f'*{PHYSICAL_ATTACK_EMOJI_TEXT}* '
                f'em {condition.bonus_physical_attack} pontos e a '
                f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* '
                f'em {condition.bonus_magical_defense} pontos.\n\n'
                f'{ALERT_SECTION_HEAD_ADD_STATUS}'
                f'{status_report_text}'
            )
        }

        return report


class ConfiscationSkill(BaseSkill):
    NAME = PaladinSkillEnum.CONFISCATION.value
    DESCRIPTION = (
        f'Usa o poder da fé para desferir um raio de *Energia Sagrada*, '
        f'causando dano '
        f'*{get_damage_emoji_text(DamageEnum.BLESSING)}* com base na '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* (125% + 5% x Rank x Nível) e '
        f'*Confiscando* um *Buff* aleatótio do alvo.'
    )
    RANK = 1
    REQUIREMENTS = Requirement(**{
        'classe_name': ClasseEnum.PALADIN.value,
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_DEFENSE: 1.25,
        }
        damage_types = [DamageEnum.BLESSING]

        super().__init__(
            name=ConfiscationSkill.NAME,
            description=ConfiscationSkill.DESCRIPTION,
            rank=ConfiscationSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=ConfiscationSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def hit_function(
        self,
        target: 'BaseCharacter',
        damage: int,
        total_damage: int,
    ) -> dict:
        report = {'text': ''}
        player_name = self.char.player_name
        target_name = target.player_name
        buff_list = list(target.status.get_buffs())
        if target.is_alive and buff_list:
            buff_condition = choice(buff_list)
            buff_name = buff_condition.full_name
            buff_condition_copy = copy_condition(
                condition=buff_condition,
                character=self.char
            )
            status_report = target.status.remove_condition(buff_condition)
            set_report_list = self.char.status.set_conditions(
                buff_condition_copy
            )
            status_report_text = status_report['text']
            set_report_text = '\n'.join(
                [report['text'] for report in set_report_list]
            )
            report['text'] = (
                f'*{player_name}* confiscou *{buff_name}*\n'
                f'*{target_name}*: {status_report_text}\n'
                f'*{player_name}*: {set_report_text}'
            )

        return report


class ExcommunicateSkill(BaseSkill):
    NAME = PaladinSkillEnum.EXCOMMUNICATE.value
    DESCRIPTION = (
        f'Usa o poder do seu dogma para desferir uma rajada '
        f'de *Energia Sagrada*, '
        f'causando dano '
        f'*{get_damage_emoji_text(DamageEnum.BLESSING)}* com base na '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* (150% + 5% x Rank x Nível) e '
        f'*Eliminando* todos os *Buff* do alvo.'
    )
    RANK = 2
    REQUIREMENTS = Requirement(**{
        'level': 40,
        'classe_name': ClasseEnum.PALADIN.value,
        'skill_list': [ConfiscationSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_DEFENSE: 1.50,
        }
        damage_types = [DamageEnum.BLESSING]

        super().__init__(
            name=ExcommunicateSkill.NAME,
            description=ExcommunicateSkill.DESCRIPTION,
            rank=ExcommunicateSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=ExcommunicateSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def hit_function(
        self,
        target: 'BaseCharacter',
        damage: int,
        total_damage: int,
    ) -> dict:
        report = {'text': ''}
        buff_list = list(target.status.get_buffs())
        if target.is_alive and buff_list:
            report['text'] += '\n'.join([
                target.status.remove_condition(buff_condition)['text']
                for buff_condition in buff_list
            ])

        return report


class ExileSkill(BaseSkill):
    NAME = PaladinSkillEnum.EXILE.value
    DESCRIPTION = (
        f'Usa uma manifestação poderosa da fé e da justiça para invocar '
        f'um torrencial de *Energia Sagrada*, '
        f'causando dano '
        f'*{get_damage_emoji_text(DamageEnum.BLESSING)}* com base na '
        f'*{MAGICAL_DEFENSE_EMOJI_TEXT}* (175% + 5% x Rank x Nível), '
        f'*Eliminando* todos os *Buff* do alvo e '
        f'adicionando as condições '
        f'*{get_debuff_emoji_text(DebuffEnum.CURSE)}* e '
        f'*{get_debuff_emoji_text(DebuffEnum.EXHAUSTION)}* com nível igual ao '
        f'(Rank x Nível).'
    )
    RANK = 3
    REQUIREMENTS = Requirement(**{
        'level': 80,
        'classe_name': ClasseEnum.PALADIN.value,
        'skill_list': [ConfiscationSkill.NAME, ExcommunicateSkill.NAME]
    })

    def __init__(self, char: 'BaseCharacter', level: int = 1):
        base_stats_multiplier = {}
        combat_stats_multiplier = {
            CombatStatsEnum.MAGICAL_DEFENSE: 1.75,
        }
        damage_types = [DamageEnum.BLESSING]

        super().__init__(
            name=ExileSkill.NAME,
            description=ExileSkill.DESCRIPTION,
            rank=ExileSkill.RANK,
            level=level,
            base_stats_multiplier=base_stats_multiplier,
            combat_stats_multiplier=combat_stats_multiplier,
            target_type=TargetEnum.SINGLE,
            skill_type=SkillTypeEnum.ATTACK,
            skill_defense=SkillDefenseEnum.MAGICAL,
            char=char,
            use_equips_damage_types=False,
            requirements=ExileSkill.REQUIREMENTS,
            damage_types=damage_types
        )

    def hit_function(
        self,
        target: 'BaseCharacter',
        damage: int,
        total_damage: int,
    ) -> dict:
        report = {'text': ''}
        buff_list = list(target.status.get_buffs())
        if target.is_alive and buff_list:
            report['text'] += '\n'.join([
                target.status.remove_condition(buff_condition)['text']
                for buff_condition in buff_list
            ])

        if target.is_alive:
            level = self.level_rank

            curse_condition = CurseCondition(level=level)
            status_report = target.status.add_condition(curse_condition)
            report['status_text'] = status_report['text'] + '\n'

            exhaustion_condition = ExhaustionCondition(level=level)
            status_report = target.status.add_condition(exhaustion_condition)
            report['status_text'] += status_report['text']

        return report


SKILL_WAY_DESCRIPTION = {
    'name': 'Inquisidor',
    'description': (
        'O Inquisidor é um paladino cuja fé se manifesta em uma '
        'busca implacável pela justiça. '
        'Ele é um detetive sagrado, utilizando sua fé e '
        'conhecimento para desvendar mistérios, '
        'caçar hereges e erradicar o mal. '
        'Sua missão é punir os culpados, '
        'mesmo que isso signifique banhar-se nas forças sombrias.'
    ),
    'skill_list': [
        FloggingsSkill,
        CutThroatSkill,
        VladsPunishmentSkill,
        ConfessionSkill,
        PenitenceSkill,
    ]
}


if __name__ == '__main__':
    from rpgram.conditions.debuff import CurseCondition
    from rpgram.constants.test import PALADIN_CHARACTER

    skill = FloggingsSkill(PALADIN_CHARACTER)
    print(skill)
    print(PALADIN_CHARACTER.cs.physical_attack)
    print(PALADIN_CHARACTER.to_attack(
        defender_char=PALADIN_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    PALADIN_CHARACTER.skill_tree.learn_skill(FloggingsSkill)

    skill = CutThroatSkill(PALADIN_CHARACTER)
    print(skill)
    print(PALADIN_CHARACTER.cs.physical_attack)
    print(PALADIN_CHARACTER.to_attack(
        defender_char=PALADIN_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    PALADIN_CHARACTER.skill_tree.learn_skill(CutThroatSkill)

    skill = VladsPunishmentSkill(PALADIN_CHARACTER)
    print(skill)
    print(PALADIN_CHARACTER.cs.physical_attack)
    print(PALADIN_CHARACTER.to_attack(
        defender_char=PALADIN_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    PALADIN_CHARACTER.skill_tree.learn_skill(VladsPunishmentSkill)

    curse_condition = CurseCondition(level=5)
    PALADIN_CHARACTER.status.add_condition(curse_condition)
    skill = ConfessionSkill(PALADIN_CHARACTER)
    print(skill)
    print(PALADIN_CHARACTER.cs.magical_defense)
    print(PALADIN_CHARACTER.cs.show_hit_points)
    print(skill.function(PALADIN_CHARACTER))
    PALADIN_CHARACTER.skill_tree.learn_skill(ConfessionSkill)

    skill = PenitenceSkill(PALADIN_CHARACTER)
    print(skill)
    print(PALADIN_CHARACTER.cs.base_physical_attack,
          PALADIN_CHARACTER.cs.physical_attack)
    print(PALADIN_CHARACTER.cs.base_magical_defense,
          PALADIN_CHARACTER.cs.magical_defense)
    print(PALADIN_CHARACTER.cs.base_hit_points,
          PALADIN_CHARACTER.cs.show_hit_points)
    print(skill.function(PALADIN_CHARACTER))
    print(PALADIN_CHARACTER.cs.physical_attack)
    print(PALADIN_CHARACTER.cs.magical_defense)
    print(PALADIN_CHARACTER.cs.show_hit_points)
    PALADIN_CHARACTER.skill_tree.learn_skill(PenitenceSkill)

    skill = ConfiscationSkill(PALADIN_CHARACTER)
    print(skill)
    print(PALADIN_CHARACTER.cs.magical_defense)
    print(PALADIN_CHARACTER.to_attack(
        defender_char=PALADIN_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    PALADIN_CHARACTER.skill_tree.learn_skill(ConfiscationSkill)

    skill = ExcommunicateSkill(PALADIN_CHARACTER)
    print(skill)
    print(PALADIN_CHARACTER.cs.magical_defense)
    print(PALADIN_CHARACTER.to_attack(
        defender_char=PALADIN_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    PALADIN_CHARACTER.skill_tree.learn_skill(ExcommunicateSkill)

    skill = PenitenceSkill(PALADIN_CHARACTER)
    skill.function(PALADIN_CHARACTER)

    skill = ExileSkill(PALADIN_CHARACTER)
    print(skill)
    print(PALADIN_CHARACTER.cs.magical_defense)
    print(PALADIN_CHARACTER.to_attack(
        defender_char=PALADIN_CHARACTER,
        attacker_skill=skill,
        verbose=True,
    )['text'])
    PALADIN_CHARACTER.skill_tree.learn_skill(ExileSkill)

    print('\n'.join([
        report['text']
        for report in PALADIN_CHARACTER.activate_status()
    ]))
