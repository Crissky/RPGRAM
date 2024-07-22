from bson import ObjectId
from datetime import datetime
from random import choices, random, uniform
from typing import List, TypeVar, Union

from constant.text import ALERT_SECTION_HEAD, ALERT_SECTION_HEAD_ADD_STATUS, TEXT_DELIMITER
from function.text import escape_basic_markdown_v2, remove_bold, remove_code

from rpgram.conditions.factory import condition_factory
from rpgram.dice import Dice
from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.race import MALEGNE_RACES
from rpgram.enums.skill import (
    MAGICAL_DEFENSE_ENUM_LIST,
    PHYSICAL_DEFENSE_ENUM_LIST
)
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.equips import Equips
from rpgram.skills.basic_attack import (
    MagicalAttackSkill,
    PhysicalAttackSkill,
    PrecisionAttackSkill
)
from rpgram.skills.skill_base import BaseSkill
from rpgram.skills.skill_tree import SkillTree
from rpgram.status import Status
from rpgram.boosters.classe import Classe
from rpgram.boosters.race import Race
from rpgram.constants.text import (
    CHARACTER_EMOJI_TEXT,
    CLASS_EMOJI_TEXT,
    RACE_EMOJI_TEXT
)
from rpgram.stats import BaseStats, CombatStats


TBaseCharacter = TypeVar('TBaseCharacter', bound='BaseCharacter')


class BaseCharacter:
    def __init__(
        self,
        char_name: str,
        classe: Classe,
        race: Race,
        player_id: int = None,
        equips: Equips = None,
        status: Status = {},
        level: int = 1,
        xp: int = 0,
        base_strength: int = 0,
        base_dexterity: int = 0,
        base_constitution: int = 0,
        base_intelligence: int = 0,
        base_wisdom: int = 0,
        base_charisma: int = 0,
        points_multiplier: int = 3,
        combat_damage: int = 0,
        combat_death_counter: int = 0,
        skill_tree: dict = {},
        _id: ObjectId = None,
        created_at: datetime = None,
        updated_at: datetime = None
    ) -> None:
        if isinstance(_id, str):
            _id = ObjectId(_id)
        if equips is None:
            equips = Equips(player_id=player_id, _id=ObjectId())

        condition_list = []
        if isinstance(status, dict):
            condition_args = status.pop('condition_args', [])
            for condition_arg in condition_args:
                if condition_arg.pop('need_character', False):
                    condition_arg['character'] = self
                condition = condition_factory(**condition_arg)
                condition_list.append(condition)

        self.__name = char_name
        self.__id = _id
        self.__classe = classe
        self.__race = race
        self.__player_id = player_id
        self.__equips = equips
        self.__status = Status(conditions=[])
        self.__base_stats = BaseStats(
            level=level,
            xp=xp,
            base_strength=base_strength,
            base_dexterity=base_dexterity,
            base_constitution=base_constitution,
            base_intelligence=base_intelligence,
            base_wisdom=base_wisdom,
            base_charisma=base_charisma,
            points_multiplier=points_multiplier,
            stats_boosters=[
                self.__race,
                self.__classe,
                self.__equips,
                self.__status
            ]
        )
        self.__combat_stats = CombatStats(
            base_stats=self.__base_stats,
            damage=combat_damage,
            death_counter=combat_death_counter,
        )
        self.__equips.attach_observer(self.__base_stats)
        self.__equips.attach_observer(self.__combat_stats)
        self.__status.attach_observer(self.__base_stats)
        self.__status.attach_observer(self.__combat_stats)
        self.__status.set_conditions(*condition_list)
        self.__skill_tree = SkillTree(
            character=self,
            current_action_points=skill_tree.get('current_action_points'),
            max_action_points=skill_tree.get('max_action_points'),
        )
        self.__skill_tree.set_skill(*skill_tree.get('skill_list', []))
        self.__created_at = created_at
        self.__updated_at = updated_at

    # BATTLE FUNCTIONS
    def get_attack_value(self, attack_name) -> int:
        if attack_name == 'physical_attack':
            return self.cs.physical_attack
        elif attack_name == 'precision_attack':
            return self.cs.precision_attack
        elif attack_name == 'magical_attack':
            return self.cs.magical_attack

    def get_defense_value(self, defense_name) -> int:
        if defense_name == 'physical_defense':
            return self.cs.physical_defense
        elif defense_name == 'magical_defense':
            return self.cs.magical_defense

    def get_defense_name(self, attacker_skill: BaseSkill) -> str:
        skill_defense = attacker_skill.skill_defense
        if skill_defense in MAGICAL_DEFENSE_ENUM_LIST:
            defense_name = 'magical_defense'
        elif skill_defense in PHYSICAL_DEFENSE_ENUM_LIST:
            defense_name = 'physical_defense'
        else:
            raise KeyError(
                f'Não existe uma defesa válida para "{skill_defense}".'
            )

        return defense_name

    def get_basic_attack_by_name(
        self,
        attack_name: Union[str, CombatStatsEnum]
    ) -> BaseSkill:
        if isinstance(attack_name, CombatStatsEnum):
            attack_name = attack_name.value

        if attack_name == CombatStatsEnum.PHYSICAL_ATTACK.value:
            return PhysicalAttackSkill(self)
        elif attack_name == CombatStatsEnum.PRECISION_ATTACK.value:
            return PrecisionAttackSkill(self)
        elif attack_name == CombatStatsEnum.MAGICAL_ATTACK.value:
            return MagicalAttackSkill(self)
        else:
            raise KeyError(f'"{attack_name}" não é um ataque básico válido.')

    def weighted_choice_basic_attack(self) -> BaseSkill:
        basic_attack_dict = {
            basic_attack: basic_attack.power
            for basic_attack in self.basic_attacks
        }
        population = list(basic_attack_dict.keys())
        weights = basic_attack_dict.values()

        return choices(population, weights=weights)[0]

    def get_best_basic_attack(self) -> BaseSkill:
        basic_attack_dict = {
            basic_attack: basic_attack.power
            for basic_attack in self.basic_attacks
        }
        basic_attack = max(basic_attack_dict, key=basic_attack_dict.get)

        return basic_attack

    def activate_status(self) -> List[dict]:
        reports = self.__status.activate(self)
        return reports

    def break_conditions(self) -> List[dict]:
        reports = self.__status.break_conditions()
        return reports

    def activate_status_string(self) -> str:
        activate_status_report_list = self.activate_status()
        text = ''
        if activate_status_report_list:
            text += '\n\n'
            text += ALERT_SECTION_HEAD.format('*STATUS REPORT*')
            text += '\n'
            for status_report in activate_status_report_list:
                text += status_report['text'] + '\n'
            text = text.rstrip()

        return text

    def activate_status_to_attack(self, defender_char: TBaseCharacter) -> str:
        text = ''
        defender_player_name = defender_char.player_name
        break_status_report_list = defender_char.break_conditions()
        activate_status_report_list = defender_char.activate_status()
        if break_status_report_list or activate_status_report_list:
            text += '\n\n'
            text += ALERT_SECTION_HEAD.format('*STATUS REPORT*')
            text += '\n'
            text += f'*{defender_player_name}*:\n'
            for status_report in break_status_report_list:
                condition_name = status_report['condition_name']
                text += f'Ataque quebrou a condição "{condition_name}". '
                text += status_report['text'] + '\n'
            for status_report in activate_status_report_list:
                text += status_report['text'] + '\n'
            text = text.rstrip()

        return text

    def add_action_points(self, value: int = 1) -> dict:
        return self.skill_tree.add_action_points(value)

    def sub_action_points(self, value: int = 1) -> dict:
        return self.skill_tree.sub_action_points(value)

    def get_accuracy(
        self,
        attacker_skill: BaseSkill,
        defender_dice: Dice,
    ) -> float:
        '''Retorna a acurácia do ataque, baseada no ACERTO do do ATACANTE
        e na EVASÃO do DEFENSOR
        '''
        attacker_dice = attacker_skill.dice
        hit = attacker_dice.boosted_hit
        evasion = defender_dice.boosted_evasion

        accuracy = hit / evasion
        accuracy = min(accuracy, 1.0)
        dice_bonus = (attacker_dice.value - defender_dice.value) / 100
        accuracy = accuracy + dice_bonus
        accuracy = min(accuracy, self.max_accuracy)
        accuracy = max(accuracy, self.min_accuracy)

        return accuracy

    def test_dodge(
        self,
        attacker_skill: BaseSkill,
        defender_dice: Dice,
    ) -> dict:
        '''Testa se o inimigo esquivou do ataque, retornando True
        caso tenha esquivado e False, caso contrário.
        '''

        attacker_dice = attacker_skill.dice
        defender_char = defender_dice.char
        attacker_is_critical = attacker_dice.is_critical
        defender_is_critical = defender_dice.is_critical
        attacker_is_critical_fail = attacker_dice.is_critical_fail
        defender_is_critical_fail = defender_dice.is_critical_fail
        accuracy = self.get_accuracy(
            attacker_skill=attacker_skill,
            defender_dice=defender_dice,
        )
        dodge_score = random()
        is_dodged = False

        # Adiciona bônus de ACCURACY com base no HP perdido
        if attacker_dice.is_player is True:
            accuracy_low_hp_bonus = attacker_dice.irate_hp / 2.5
            accuracy += accuracy_low_hp_bonus
        # Adiciona bônus de DODGE_SCORE com base no HP perdido
        if defender_dice.is_player is True:
            dodge_low_hp_bonus = defender_dice.irate_hp / 2.5
            dodge_score += dodge_low_hp_bonus

        is_dodged = (dodge_score >= accuracy)
        if defender_char.is_immobilized:
            is_dodged = False
        elif defender_is_critical_fail and not attacker_is_critical_fail:
            is_dodged = False
        elif not defender_is_critical and attacker_is_critical:
            is_dodged = False
        elif not defender_is_critical_fail and attacker_is_critical_fail:
            is_dodged = True
        elif defender_is_critical and not attacker_is_critical:
            is_dodged = True

        return {
            'attacker_accuracy': accuracy,
            'defender_dodge_score': dodge_score,
            'is_dodged': is_dodged,
            'is_immobilized': defender_char.is_immobilized,
        }

    def calculate_damage(
        self,
        defense_name: str,
        attacker_dice: Dice,
        defender_dice: Dice,
    ) -> int:
        '''Calcula o dano causado pelo ataque.
        '''

        BLOCK_MULTIPLIER = 0.50
        MIN_DAMAGE_MULTIPLIER = (
            0.50
            if defender_dice.is_critical_fail
            else 0.25
        )

        boosted_power_value = attacker_dice.boosted_power
        base_defense_value = defender_dice.get_base_stats(defense_name)
        boosted_defense_value = defender_dice.get_boosted_stats(defense_name)

        damage = boosted_power_value - boosted_defense_value
        min_damage = boosted_power_value * MIN_DAMAGE_MULTIPLIER
        min_damage = int(min_damage * uniform(0.90, 1.10))
        block_value = int(base_defense_value * BLOCK_MULTIPLIER)
        if attacker_dice.skill.is_true_damage:
            damage = max(damage, boosted_power_value)
        elif all((
            boosted_power_value > block_value,
            not defender_dice.is_critical,
            not attacker_dice.is_critical_fail,
        )):
            damage = max(damage, min_damage)

        return damage

    def to_attack(
        self,
        defender_char: TBaseCharacter,
        defender_dice: Union[Dice, int] = None,
        attacker_skill: Union[str, CombatStatsEnum, BaseSkill] = None,
        to_dodge: bool = False,
        to_defend: bool = True,
        rest_command: str = None,
        verbose: bool = False,
        markdown: bool = False,
    ) -> dict:
        '''Personagem ataca um alvo usando um dos ataques básicos. Caso não
        seja passado um attacker_action_name, será escolhido o atributo de
        ataque mais poderoso.
        '''

        report = {'text': ''}
        damage = 0
        defender_player_name = defender_char.player_name

        if isinstance(attacker_skill, (str, CombatStatsEnum)):
            attacker_skill = self.get_basic_attack_by_name(attacker_skill)
        elif not isinstance(attacker_skill, BaseSkill):
            attacker_skill = self.get_best_basic_attack()

        # if not isinstance(attacker_dice, Dice):
        #     atk_faces = attacker_dice if isinstance(attacker_dice, int) else 20
        #     attacker_dice = Dice(character=self, faces=atk_faces)
        attacker_dice = attacker_skill.dice
        if not isinstance(defender_dice, Dice):
            def_faces = defender_dice if isinstance(defender_dice, int) else 20
            defender_dice = Dice(character=defender_char, faces=def_faces)

        dodge_report = self.test_dodge(
            attacker_skill=attacker_skill,
            defender_dice=defender_dice,
        )

        base_power_value = attacker_dice.base_power
        boosted_power_value = attacker_dice.boosted_power

        defense_name = self.get_defense_name(attacker_skill)
        base_defense_value = defender_dice.get_base_stats(defense_name)
        boosted_defense_value = defender_dice.get_boosted_stats(defense_name)

        # Formating
        attack_name = attacker_skill.name
        defense_name = defense_name.replace('_', ' ')
        defense_name = defense_name.title()

        # ---------- DODGE ---------- #
        if (is_miss := to_dodge and dodge_report['is_dodged']):
            attacker_dice_text = attacker_dice.text
            defender_dice_text = defender_dice.text
            report['text'] = (
                f'*{defender_player_name}* *ESQUIVOU DO ATAQUE*\n'
                f'{EmojiEnum.DEFEND.value}{defender_dice_text} 𝗫 '
                f'{EmojiEnum.ATTACK.value}{attacker_dice_text}.'
            )
            report['text'] += self.activate_status_to_attack(defender_char)

        # ----------- HIT ----------- #
        else:
            # Get Damage
            pre_hit_report = attacker_skill.pre_hit_function(
                target=defender_char
            )
            pre_hit_text = pre_hit_report['text']
            hit_text = ''
            hit_status_text = ''
            damage = boosted_power_value
            is_immobilized = defender_char.is_immobilized
            if is_immobilized:
                immobilized_names = defender_char.status.immobilized_names()
            if to_defend and not is_immobilized:
                damage = self.calculate_damage(
                    defense_name=defense_name,
                    attacker_dice=attacker_dice,
                    defender_dice=defender_dice,
                )
            damage = max(damage, 0)
            total_damage = damage
            damage_text_list = [f'*{attack_name}*({damage})']
            condition_ratio_list = []

            # Get Special Damages
            if total_damage > 0:
                for special_damage in attacker_skill.special_damage_iter:
                    total_damage += special_damage.damage
                    damage_text = special_damage.damage_emoji_text
                    damage_text_list.append(damage_text)
                    condition_ratio_list.extend(
                        special_damage.condition_ratio_list
                    )

            # Apply Damage in Defender
            damage_report = defender_char.cs.damage_hit_points(
                value=total_damage,
                markdown=markdown
            )
            report.update(damage_report)

            activate_status_to_attack = ''
            if defender_char.is_alive:
                activate_status_to_attack = (
                    self.activate_status_to_attack(defender_char)
                )

            # Put the General Paragraph of the report['text']
            damage_or_defend_text = (
                f' que defendeu recebendo *{total_damage}* pontos de dano'
            )
            if total_damage > 0:
                hit_report = attacker_skill.hit_function(
                    target=defender_char,
                    damage=damage,
                    total_damage=total_damage,
                )
                hit_text = hit_report['text']
                hit_status_text = hit_report.get('status_text', '')
                damage_or_defend_text = (
                    f' e causou *{total_damage}* pontos de dano'
                )
                if len(damage_text_list) > 1:
                    damage_or_defend_text += '.\n'
                    damage_or_defend_text += ', '.join(damage_text_list)
            report['text'] = (
                f'*{self.full_name_with_level}* *ATACOU* '
                f'*{defender_player_name}*{damage_or_defend_text}.\n\n'
            )

            # Put the Pre Hit Paragraph of the report['text']
            if pre_hit_text:
                report['text'] += ALERT_SECTION_HEAD.format(f'*{attack_name}*')
                report['text'] += f'\n{pre_hit_text}\n\n'

            # Put the Dice Paragraph of the report['text']
            if verbose:
                report['text'] += (
                    f'*{attack_name}*: '
                    f'{boosted_power_value}({base_power_value}), '
                    f'{attacker_dice.text}\n'
                )
                if is_immobilized:
                    report['text'] += (
                        f'*Vulnerável*: Personagem não pôde se defender, pois '
                        f'está com {immobilized_names}.'
                        f'\n'
                    )
                elif attacker_skill.is_true_damage:
                    report['text'] += (
                        f'*Subjugado*: Personagem não pôde se defender, pois '
                        f'o ataque é indefensável.'
                        f'\n'
                    )
                else:
                    report['text'] += (
                        f'*{defense_name}*: '
                        f'{boosted_defense_value}({base_defense_value}), '
                        f'{defender_dice.text}\n'
                    )

            # Put the Damage Paragraph of the report['text']
            report['text'] += damage_report['text']

            # Put the Hit Paragraph of the report['text']
            if hit_text:
                report['text'] += f'\n\n'
                report['text'] += ALERT_SECTION_HEAD.format(f'*{attack_name}*')
                report['text'] += f'\n{hit_text}'

            # Put the Activate Status of the report['text']
            if activate_status_to_attack:
                report['text'] += activate_status_to_attack

            # Put the New Status Paragraph of the report['text']
            if defender_char.is_alive:
                status_report = defender_char.status.add_conditions_by_ratio(
                    *condition_ratio_list
                )
                if status_report['effective'] is True or hit_status_text:
                    report['text'] += '\n\n'
                    report['text'] += ALERT_SECTION_HEAD_ADD_STATUS
                    report['text'] += f'*{defender_player_name}*:'
                    if hit_status_text:
                        report['text'] += '\n' + hit_status_text
                    if status_report['effective'] is True:
                        report['text'] += '\n' + status_report['text']

            # Put the Dead Paragraph of the report['text']
            if defender_char.is_dead:
                report['text'] += f'\n\n*{defender_player_name}* morreu!'
                if rest_command:
                    report['text'] += (
                        f' Use o comando /{rest_command} para descansar.'
                    )
        # End Else

        report['text'] += '\n\n'
        if not markdown:
            report['text'] = remove_bold(report['text'])
            report['text'] = remove_code(report['text'])
        else:
            report['text'] = escape_basic_markdown_v2(report['text'])

        # Update the report
        report.update(defender_char.cs.basic_report)
        report.update({
            'attacker': self,
            'attacker_char': self,
            'attack': {
                'action': attack_name,
                'accuracy': (dodge_report['attacker_accuracy'] * 100),
                'dice_value': attacker_dice.value,
                'dice_text': attacker_dice.text,
                'is_critical': attacker_dice.is_critical,
                'atk': base_power_value,
                'boosted_atk': boosted_power_value,
                'skill': attacker_skill,
            },
            'defender': defender_char,
            'defender_char': defender_char,
            'defense': {
                'action': defense_name,
                'dodge_score': (dodge_report['defender_dodge_score'] * 100),
                'dice_value': defender_dice.value,
                'dice_text': defender_dice.text,
                'is_critical': defender_dice.is_critical,
                'def': base_defense_value,
                'boosted_def': boosted_defense_value,
                'damage': (damage * -1),
                'is_miss': is_miss
            },
        })

        return report

    # Getters
    @property
    def is_damaged(self) -> bool:
        return self.combat_stats.damaged

    @property
    def is_healed(self) -> bool:
        return self.combat_stats.healed

    @property
    def is_alive(self) -> bool:
        return self.combat_stats.alive

    @property
    def is_dead(self) -> bool:
        return self.combat_stats.dead

    @property
    def is_immobilized(self) -> bool:
        return self.status.immobilized

    @property
    def is_cursed(self) -> bool:
        return self.status.cursed

    @property
    def is_malegne(self) -> bool:
        race_name = self.race_name
        return any((
            race_name in MALEGNE_RACES,
            self.is_cursed
        ))

    @property
    def is_debuffed(self) -> bool:
        return self.status.debuffed

    @property
    def is_full_action_points(self) -> bool:
        return self.skill_tree.is_full_action_points

    @property
    def can_player_act(self) -> bool:
        return self.skill_tree.have_action_points

    @property
    def max_accuracy(self) -> float:
        accuracy = 0.95
        if self.is_enemy is True:
            accuracy = 0.80

        return accuracy

    @property
    def min_accuracy(self) -> float:
        accuracy = 0.30
        if self.is_enemy is True:
            accuracy = 0.10

        return accuracy

    @property
    def basic_attacks(self) -> List[BaseSkill]:
        return [
            PhysicalAttackSkill(self),
            PrecisionAttackSkill(self),
            MagicalAttackSkill(self),
        ]

    name: str = property(lambda self: self.__name)
    player_name: str = property(lambda self: self.__name)
    level: int = property(lambda self: self.__base_stats.level)
    xp: int = property(lambda self: self.__base_stats.xp)
    _id: ObjectId = property(lambda self: self.__id)
    player_id: int = property(lambda self: self.__player_id)
    is_enemy: bool = property(lambda self: False)
    is_player: bool = property(lambda self: not self.is_enemy)
    created_at: datetime = property(lambda self: self.__created_at)
    updated_at: datetime = property(lambda self: self.__updated_at)
    base_stats: BaseStats = property(fget=lambda self: self.__base_stats)
    combat_stats: CombatStats = property(fget=lambda self: self.__combat_stats)
    classe: Classe = property(fget=lambda self: self.__classe)
    race: Race = property(fget=lambda self: self.__race)
    equips: Equips = property(fget=lambda self: self.__equips)
    status: Status = property(fget=lambda self: self.__status)
    skill_tree: SkillTree = property(fget=lambda self: self.__skill_tree)
    current_action_points: int = property(
        fget=lambda self: self.__skill_tree.current_action_points
    )
    current_action_points_text: str = property(
        fget=lambda self: self.__skill_tree.current_action_points_text
    )
    skill_points_text: str = property(
        fget=lambda self: self.__skill_tree.skill_points_text
    )
    bs = base_stats
    cs = combat_stats
    race_name: str = property(lambda self: self.race.name)
    classe_name: str = property(lambda self: self.classe.name)
    full_name: str = property(
        lambda self: (
            f'{self.player_name}, O {self.race_name} {self.classe_name}'
        )
    )
    full_name_with_level: str = property(
        lambda self: f'{self.full_name} (LV: {self.bs.level})'
    )
    points_multiplier: int = property(
        lambda self: self.__base_stats.points_multiplier
    )
    actions = property(
        lambda self: ['physical_attack', 'precision_attack', 'magical_attack']
    )

    def get_sheet(self, verbose: bool = False, markdown: bool = False) -> str:
        text = f'*{CHARACTER_EMOJI_TEXT}*: {self.name}\n'
        if verbose:
            text += f'*ID Personagem*: {self.__id}\n'

        if not markdown:
            text = remove_bold(text)
            text = remove_code(text)
        else:
            text = escape_basic_markdown_v2(text)

        return text

    def get_all_sheets(
        self, verbose: bool = False, markdown: bool = False
    ) -> str:
        if verbose:
            text = (
                f'{self.get_sheet(verbose, markdown)}'
                f'{self.status.get_all_sheets(verbose, markdown)}\n'
                f'{self.skill_tree.get_sheet(verbose, markdown)}\n'
                f'{self.combat_stats.death_counter_text}\n'
                f'{self.base_stats.get_sheet(verbose, markdown)}\n'
                f'{self.combat_stats.get_sheet(verbose, markdown)}\n'
                f'{self.race.get_sheet(verbose, markdown)}\n'
                f'{self.classe.get_sheet(verbose, markdown)}\n'
                f'{self.equips.get_sheet(verbose, markdown)}\n'
            )
        else:
            # Trecho feito dessa forma para o escape_basic_markdown_v2 não ser
            # usado duas vezes nos textos que vem dos outros get_sheet, pois
            # o esperado seria somente uma \ e não duas.
            race_classe_text = (
                f'*{RACE_EMOJI_TEXT}*: {self.race.name}\n'
                f'*{CLASS_EMOJI_TEXT}*: {self.classe.name}\n'
            )
            if not markdown:
                race_classe_text = remove_bold(race_classe_text)
                race_classe_text = remove_code(race_classe_text)
            else:
                race_classe_text = escape_basic_markdown_v2(race_classe_text)
            text = (
                f'{self.get_sheet(verbose, markdown)}'
                f'{self.status.get_all_sheets(verbose, markdown)}\n'
                f'{race_classe_text}'
                f'{self.skill_tree.get_sheet(verbose, markdown)}\n'
                f'{self.combat_stats.death_counter_text}\n'
                f'{self.base_stats.get_sheet(verbose, markdown)}\n'
                f'{self.combat_stats.get_sheet(verbose, markdown)}\n'
                f'{self.equips.get_sheet(verbose, markdown)}'
            )

        return text

    def __str__(self) -> str:
        return (
            f'{TEXT_DELIMITER}\n'
            f'{self.get_all_sheets(True)}'
            f'{TEXT_DELIMITER}\n'
        )

    def __repr__(self) -> str:
        return (
            f'<Personagem: "{self.name} '
            f'({self.classe.name}/{self.race.name})", '
            f'LV: {self.bs.level}, '
            f'HP: {self.cs.show_hp}>'
        )

    def to_dict(self):
        return dict(
            char_name=self.name,
            _id=self.__id,
            level=self.base_stats.level,
            xp=self.base_stats.xp,
            base_strength=self.base_stats.base_strength,
            base_dexterity=self.base_stats.base_dexterity,
            base_constitution=self.base_stats.base_constitution,
            base_intelligence=self.base_stats.base_intelligence,
            base_wisdom=self.base_stats.base_wisdom,
            base_charisma=self.base_stats.base_charisma,
            points_multiplier=self.base_stats.points_multiplier,
            combat_damage=(self.cs.hit_points - self.cs.current_hit_points),
            combat_death_counter=self.cs.death_counter,
            race_name=self.race.name,
            classe_name=self.classe.name,
            equips_id=self.equips._id,
            status=self.status.to_dict(),
            skill_tree=self.skill_tree.to_dict(),
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BaseCharacter):
            if self._id is not None and other._id is not None:
                return all((
                    self.__id == other.__id,
                    self.name == other.name,
                ))
        return False


if __name__ == '__main__':
    from rpgram.boosters import Equipment
    from rpgram.enums import DamageEnum, EquipmentEnum
    helmet = Equipment(
        name='Capacete de Aço',
        equip_type=EquipmentEnum.HELMET,
        damage_types=None,
        weight=10,
        bonus_physical_defense=30,
        bonus_evasion=-5,
    )
    sword = Equipment(
        name='Espada Gigante de Aço',
        equip_type=EquipmentEnum.TWO_HANDS,
        damage_types=DamageEnum.SLASHING,
        weight=40,
        bonus_physical_attack=30,
        bonus_hit=15,
        bonus_evasion=-10,
    )
    armor = Equipment(
        name='Armadura de Aço',
        equip_type=EquipmentEnum.ARMOR,
        damage_types=None,
        weight=60,
        bonus_physical_defense=80,
        bonus_evasion=-25,
    )
    boots = Equipment(
        name='Botas de Couro',
        equip_type=EquipmentEnum.BOOTS,
        damage_types=None,
        weight=10,
        bonus_physical_defense=10,
        bonus_magical_defense=10,
        bonus_evasion=30,
    )
    ring = Equipment(
        name='Algum Anel',
        equip_type=EquipmentEnum.RING,
        damage_types=None,
        weight=0.1,
        bonus_evasion=100,
    )
    amulet = Equipment(
        name='Colar Brilhante',
        equip_type=EquipmentEnum.AMULET,
        damage_types=None,
        weight=0.2,
        bonus_charisma=150,
    )
    equips = Equips(
        player_id=123,
        helmet=helmet,
        left_hand=sword,
        armor=armor,
        boots=boots,
        ring=ring,
        amulet=amulet,
    )
    classe = Classe(
        name='Arqueiro',
        description='Arqueiro Teste',
        bonus_strength=5,
        bonus_dexterity=15,
        bonus_constitution=10,
        bonus_intelligence=10,
        bonus_wisdom=10,
        bonus_charisma=10,
        multiplier_strength=1,
        multiplier_dexterity=1.5,
        multiplier_constitution=1,
        multiplier_intelligence=1,
        multiplier_wisdom=1,
        multiplier_charisma=1,
    )
    race = Race(
        name='Elfo',
        description='Elfo Teste',
        bonus_strength=8,
        bonus_dexterity=12,
        bonus_constitution=8,
        bonus_intelligence=10,
        bonus_wisdom=12,
        bonus_charisma=10,
        multiplier_strength=1.0,
        multiplier_dexterity=1.0,
        multiplier_constitution=1.0,
        multiplier_intelligence=1.2,
        multiplier_wisdom=1.2,
        multiplier_charisma=1.0,
    )
    base_character = BaseCharacter(
        char_name='Personagem Teste',
        classe=classe,
        race=race,
        equips=equips,
        _id='ffffffffffffffffffffffff',
        level=21,
        xp=0,
        base_strength=10,
        base_dexterity=10,
        base_constitution=10,
        base_intelligence=10,
        base_wisdom=10,
        base_charisma=10,
        combat_damage=0,
    )
    print(base_character)
    base_character.base_stats.xp = 100
    base_character.base_stats.dexterity = 1
    base_character.combat_stats.hp = -100
    base_character.combat_stats.hit_points = 50
    print(base_character)
    print(base_character.to_dict())
    print(base_character.weighted_choice_basic_attack())
    print(base_character.get_best_basic_attack())
