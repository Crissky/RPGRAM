from bson import ObjectId
from datetime import datetime
from random import choices, random
from typing import List, Tuple, TypeVar

from constant.text import ALERT_SECTION_HEAD, TEXT_DELIMITER
from function.text import escape_basic_markdown_v2, remove_bold, remove_code

from rpgram.dice import Dice
from rpgram.equips import Equips
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
        status: Status = None,
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
        _id: ObjectId = None,
        created_at: datetime = None,
        updated_at: datetime = None
    ) -> None:
        if isinstance(_id, str):
            _id = ObjectId(_id)
        if equips is None:
            equips = Equips(player_id=player_id, _id=ObjectId())
        if status is None:
            status = Status(player_id=player_id, _id=ObjectId())

        self.__name = char_name
        self.__id = _id
        self.__classe = classe
        self.__race = race
        self.__player_id = player_id
        self.__equips = equips
        self.__status = status
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
        self.__created_at = created_at
        self.__updated_at = updated_at

    # BATTLE FUNCTIONS
    def get_action_attack_value(self, action_name) -> int:
        if action_name == 'physical_attack':
            return self.cs.physical_attack
        elif action_name == 'precision_attack':
            return self.cs.precision_attack
        elif action_name == 'magical_attack':
            return self.cs.magical_attack

    def get_action_defense(self, action_name) -> Tuple[int, str]:
        if action_name == 'magical_attack':
            defense_value = self.cs.magical_defense
            defense_action = 'magical_defense'
        else:
            defense_value = self.cs.physical_defense
            defense_action = 'physical_defense'
        return defense_value, defense_action

    def weighted_choice_action_attack(self) -> str:
        actions = {
            action: self.get_action_attack_value(action)
            for action in self.actions
        }
        population = list(actions.keys())
        weights = actions.values()

        return choices(population, weights=weights)[0]

    def get_best_action_attack(self):
        actions = {
            action: self.get_action_attack_value(action)
            for action in self.actions
        }
        action = max(actions, key=actions.get)

        return action

    def activate_status(self) -> List[dict]:
        reports = self.__status.activate(self)
        return reports

    def battle_activate_status(self) -> List[dict]:
        reports = self.__status.battle_activate(self)
        return reports

    def get_accuracy(
        self,
        defender_char: TBaseCharacter,
        attacker_dice: Dice,
        defender_dice: Dice,
    ) -> float:
        hit = self.cs.hit
        evasion = defender_char.cs.evasion
        attacker_dice.throw(rethrow=False)
        defender_dice.throw(rethrow=False)

        accuracy = hit / evasion
        accuracy = min(accuracy, 1.0)
        dice_bonus = (attacker_dice.value - defender_dice.value) / 100
        accuracy = accuracy + dice_bonus
        accuracy = min(accuracy, 0.95)
        accuracy = max(accuracy, 0.1)

        return accuracy

    def test_dodge(
        self,
        defender_char: TBaseCharacter,
        attacker_dice: Dice,
        defender_dice: Dice,
    ) -> dict:
        '''Testa se o inimigo esquivou do ataque, retornando True 
        caso tenha esquivado e False, caso contrário. '''
        accuracy = self.get_accuracy(
            defender_char=defender_char,
            attacker_dice=attacker_dice,
            defender_dice=defender_dice,
        )
        dodge_score = random()
        is_dodged = False
        if not defender_char.is_immobilized:
            is_dodged = (dodge_score >= accuracy)

        return {
            'attacker_accuracy': accuracy,
            'defender_dodge_score': dodge_score,
            'is_dodged': is_dodged,
            'is_immobilized': defender_char.is_immobilized,
        }

    def calculate_damage(
        self,
        defense_value: int,
        defender_dice: Dice,
        attacker_dice: Dice,
    ) -> int:
        BLOCK_MULTIPLIER = 0.50
        MIN_DAMAGE_MULTIPLIER = 0.25

        defense_value_boosted = defender_dice.boosted_value
        attack_value_boosted = attacker_dice.boosted_value

        damage = attack_value_boosted - defense_value_boosted
        min_damage = int(attack_value_boosted * MIN_DAMAGE_MULTIPLIER)
        block_value = int(defense_value * BLOCK_MULTIPLIER)
        if all((
            attack_value_boosted > block_value,
            not defender_dice.is_critical,
            not attacker_dice.is_critical_fail,
        )):
            damage = max(damage, min_damage)

        return max(damage, 0)

    def to_attack(
        self,
        defender_char: TBaseCharacter,
        attacker_dice: Dice = Dice(20),
        defender_dice: Dice = Dice(20),
        attacker_action_name: str = None,
        to_dodge: bool = False,
        to_defend: bool = True,
        rest_command: str = None,
        verbose: bool = False,
        markdown: bool = False,
    ) -> dict:
        '''Personagem ataca um alvo usando um dos ataques básicos. Caso não 
        seja passado um attacker_action_name, será escolhido o atributo de 
        ataque mais poderoso.'''

        report = {'text': ''}
        damage = 0
        defender_player_name = defender_char.player_name
        attacker_dice.throw(rethrow=False)
        defender_dice.throw(rethrow=False)

        dodge_report = self.test_dodge(
            defender_char=defender_char,
            attacker_dice=attacker_dice,
            defender_dice=defender_dice,
        )

        if not isinstance(attacker_action_name, str):
            attacker_action_name = self.get_best_action_attack()
        attack_value = self.get_action_attack_value(attacker_action_name)
        attack_value_boosted = attacker_dice.boost_value(attack_value)

        (
            defense_value,
            defense_action_name
        ) = defender_char.get_action_defense(attacker_action_name)
        defense_value_boosted = defender_dice.boost_value(defense_value)

        if (is_miss := to_dodge and dodge_report['is_dodged']):
            report['text'] = (
                f'{defender_player_name} *ESQUIVOU DO ATAQUE* de '
                f'*{self.full_name_with_level}*.\n\n'
            )
            report.update(defender_char.cs.basic_report)
        else:
            # Formating
            attacker_action_name = attacker_action_name.replace('_', ' ')
            attacker_action_name = attacker_action_name.title()
            defense_action_name = defense_action_name.replace('_', ' ')
            defense_action_name = defense_action_name.title()

            # Get Damage
            damage = attack_value_boosted
            if to_defend and not defender_char.is_immobilized:
                damage = self.calculate_damage(
                    defense_value=defense_value,
                    defender_dice=defender_dice,
                    attacker_dice=attacker_dice,
                )
            damage = max(damage, 0)
            total_damage = damage
            damage_text_list = [f'*{attacker_action_name}*({damage})']
            status_report_list = []

            # Get Special Damages
            if total_damage > 0:
                for special_damage in self.equips.special_damage_iter:
                    damage_name = special_damage.damage_name
                    spec_damage = special_damage.damage
                    total_damage += spec_damage
                    damage_text = f'*{damage_name}*({spec_damage})'
                    damage_text_list.append(damage_text)

                    condition_ratio_list = special_damage.condition_ratio_list
                    status_report = defender_char.status.add_by_ratio(
                        *condition_ratio_list
                    )
                    status_report_list.append(status_report)

            # Apply Damage in Defender
            damage_report = defender_char.cs.damage_hit_points(
                value=total_damage,
                markdown=markdown
            )
            report.update(damage_report)

            # Put the General Paragraph of the report['text']
            damage_or_defend_text = (
                f' que defendeu recebendo *{total_damage}* pontos de dano'
            )
            if total_damage > 0:
                damage_or_defend_text = (
                    f' e causou *{total_damage}* pontos de dano'
                )
                if len(damage_text_list) > 1:
                    damage_or_defend_text += '.\n'
                    damage_or_defend_text += ', '.join(damage_text_list)
            report['text'] = (
                f'*{self.full_name_with_level}* *ATACOU* '
                f'{defender_player_name}{damage_or_defend_text}.\n\n'
            )

            # Put the Dice Paragraph of the report['text']
            if verbose:
                report['text'] += (
                    f'*{attacker_action_name}*: '
                    f'{attack_value_boosted}({attack_value}), '
                    f'{attacker_dice.text}\n'
                )
                if defender_char.is_immobilized:
                    report['text'] += (
                        f'*Vulnerável*: Personagem não pôde se defender pois '
                        f'está com {defender_char.status.immobilized_names()}.'
                        f'\n'
                    )
                else:
                    report['text'] += (
                        f'*{defense_action_name}*: '
                        f'{defense_value_boosted}({defense_value}), '
                        f'{defender_dice.text}\n'
                    )

            # Put the Damege Paragraph of the report['text']
            report['text'] += damage_report['text']

            # Put the Status Paragraph of the report['text']
            if status_report_list:
                report['text'] += '\n\n'
                report['text'] += ALERT_SECTION_HEAD.format(
                    'STATUS ADICIONADOS'
                )
                report['text'] += '\n\n'
                report['text'] += f'{defender_player_name}:\n'
                for status_report in status_report_list:
                    report['text'] += status_report['text'] + '\n'
                report['text'] = report['text'].rstrip()

            # Put the Activate Status of the report['text']
            activate_status_report_list = defender_char.activate_status()
            if activate_status_report_list:
                report['text'] += '\n\n'
                report['text'] += ALERT_SECTION_HEAD.format(
                    'STATUS REPORT'
                )
                report['text'] += '\n\n'
                report['text'] += f'{defender_player_name}:\n'
                for status_report in activate_status_report_list:
                    report['text'] += status_report['text'] + '\n'
                report['text'] = report['text'].rstrip()

            # Put the Dead Paragraph of the report['text']
            damage_report['dead'] = defender_char.is_dead
            if damage_report['dead']:
                report['text'] += f'\n\n{defender_player_name} morreu!'
                if rest_command:
                    report['text'] += (
                        f' Use o comando /{rest_command} para descansar.'
                    )
            report['text'] += '\n\n'

        if not markdown:
            report['text'] = remove_bold(report['text'])
            report['text'] = remove_code(report['text'])
        else:
            report['text'] = escape_basic_markdown_v2(report['text'])

        # Update the report
        report.update({
            'attacker': self,
            'attacker_char': self,
            'attack': {
                'action': attacker_action_name,
                'accuracy': (dodge_report['attacker_accuracy'] * 100),
                'dice_value': attacker_dice.value,
                'dice_text': attacker_dice.text,
                'is_critical': attacker_dice.is_critical,
                'atk': attack_value,
                'boosted_atk': attack_value_boosted,
            },
            'defender': defender_char,
            'defender_char': defender_char,
            'defense': {
                'action': defense_action_name,
                'dodge_score': (dodge_report['defender_dodge_score'] * 100),
                'dice_value': defender_dice.value,
                'dice_text': defender_dice.text,
                'is_critical': defender_dice.is_critical,
                'def': defense_value,
                'boosted_def': defense_value_boosted,
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

    name: str = property(lambda self: self.__name)
    player_name: str = property(lambda self: self.__name)
    level: int = property(lambda self: self.__base_stats.level)
    xp: int = property(lambda self: self.__base_stats.xp)
    _id: ObjectId = property(lambda self: self.__id)
    base_stats: BaseStats = property(fget=lambda self: self.__base_stats)
    combat_stats: CombatStats = property(fget=lambda self: self.__combat_stats)
    classe: Classe = property(fget=lambda self: self.__classe)
    race: Race = property(fget=lambda self: self.__race)
    player_id = property(lambda self: self.__player_id)
    equips: Equips = property(fget=lambda self: self.__equips)
    status: Status = property(fget=lambda self: self.__status)
    created_at: datetime = property(lambda self: self.__created_at)
    updated_at: datetime = property(lambda self: self.__updated_at)
    bs = base_stats
    cs = combat_stats
    race_name: str = property(lambda self: self.race.name)
    classe_name: str = property(lambda self: self.classe.name)
    full_name: str = property(
        lambda self: (
            f'{self.player_name}, O {self.race_name} {self.classe_name}'
        )
    )
    full_name_with_level = property(
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
            status_id=self.status._id,
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
    print(base_character.weighted_choice_action_attack())
