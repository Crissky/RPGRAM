from typing import List

from constant.text import ALERT_SECTION_HEAD, SECTION_HEAD, TEXT_DELIMITER
from function.text import escape_basic_markdown_v2, remove_bold, remove_code
from rpgram.constants.stats.stats_combat import FULL_HEAL_VALUE
from rpgram.constants.text import (
    BARRIER_POINT_FULL_EMOJI_TEXT,
    EVASION_EMOJI_TEXT,
    EVASION_EMOJI_TEXT_ABB,
    HIT_EMOJI_TEXT,
    HIT_EMOJI_TEXT_ABB,
    HIT_POINT_DEAD_EMOJI_TEXT,
    HIT_POINT_FULL_EMOJI_TEXT,
    HIT_POINT_INJURED_EMOJI_TEXT,
    INITIATIVE_EMOJI_TEXT,
    INITIATIVE_EMOJI_TEXT_ABB,
    MAGICAL_ATTACK_EMOJI_TEXT,
    MAGICAL_ATTACK_EMOJI_TEXT_ABB,
    MAGICAL_DEFENSE_EMOJI_TEXT,
    MAGICAL_DEFENSE_EMOJI_TEXT_ABB,
    PHYSICAL_ATTACK_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT_ABB,
    PHYSICAL_DEFENSE_EMOJI_TEXT,
    PHYSICAL_DEFENSE_EMOJI_TEXT_ABB,
    PRECISION_ATTACK_EMOJI_TEXT,
    PRECISION_ATTACK_EMOJI_TEXT_ABB
)
from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.stats import BaseStats
from rpgram.boosters import StatsBooster
from rpgram.status import Status


GENERAL_LEVEL = 5
HIT_POINTS_CONSTITUTION = 23
HIT_POINTS_STRENGTH = 12
HIT_POINTS_LEVEL = 100
INITIATIVE_DEXTERITY = 3
INITIATIVE_INTELLIGENCE = 3
INITIATIVE_WISDOM = 3
INITIATIVE_CHARISMA = 6
PHYSICAL_ATTACK_STRENGTH = 6
PHYSICAL_ATTACK_DEXTERITY = 2
PRECISION_ATTACK_STRENGTH = 2
PRECISION_ATTACK_DEXTERITY = 5
MAGICAL_ATTACK_INTELLIGENCE = 8
MAGICAL_ATTACK_WISDOM = 4
PHYSICAL_DEFENSE_CONSTITUTION = 5
PHYSICAL_DEFENSE_DEXTERITY = 2
MAGICAL_DEFENSE_WISDOM = 8
MAGICAL_DEFENSE_INTELLIGENCE = 4
MAGICAL_DEFENSE_CONSTITUTION = 2
HIT_DEXTERITY = 4
HIT_INTELLIGENCE = 3
HIT_WISDOM = 3
HIT_CHARISMA = 7
EVASION_DEXTERITY = 4
EVASION_INTELLIGENCE = 2
EVASION_WISDOM = 2
EVASION_CHARISMA = 7


class CombatStats:
    def __init__(
        self,
        base_stats: BaseStats = None,
        level: int = 1,
        base_strength: int = 0,
        base_dexterity: int = 0,
        base_constitution: int = 0,
        base_intelligence: int = 0,
        base_wisdom: int = 0,
        base_charisma: int = 0,
        damage: int = 0,
        death_counter: int = 0,
        stats_boosters: List[StatsBooster] = None,
    ) -> None:
        if not isinstance(base_stats, BaseStats):
            base_stats = BaseStats(
                level=level,
                base_strength=base_strength,
                base_dexterity=base_dexterity,
                base_constitution=base_constitution,
                base_intelligence=base_intelligence,
                base_wisdom=base_wisdom,
                base_charisma=base_charisma,
                stats_boosters=stats_boosters
            )
        self.__base_stats = base_stats
        self.__damage = int(damage)
        self.__death_counter = int(death_counter)

        self.__stats_boosters = base_stats.stats_boosters

    def set_damage(self, value: int) -> None:
        is_dead_start = self.dead
        value = int(value * -1)
        if value > 0:
            print(f'Recebeu {value} de Dano!!!', end=' ')
        elif value < 0:
            if self.dead:
                print(f'Não pode curar um personagem morto.')
                return None
            print(f'Recebeu {-value} de Cura.', end=' ')
        self.__damage += value
        if self.__damage > self.hit_points:
            self.__damage = self.hit_points
        elif self.__damage < 0:
            self.__damage = 0
        print(f'HP: {self.show_hp}')
        is_dead_end = self.dead
        if not is_dead_start and is_dead_end:
            print(f'Morreu!!!')
            self.__add_death_counter()
            self.clean_status_by_death()

    def damage_hit_points(
        self,
        value: int,
        markdown: bool = False,
        ignore_barrier: bool = False,
    ) -> dict:
        '''Adiciona dano ao personagem.
        '''

        value = -int(abs(value))
        old_hp = self.current_hit_points
        old_show_hp = self.show_hit_points
        status = self.get_status()
        remaining_damage = value
        barrier_damage_text = ''
        if ignore_barrier is False:
            barrier_damage_report = status.add_barrier_damage(value)
            remaining_damage = -barrier_damage_report['remaining_damage']
            barrier_damage_text = barrier_damage_report['text']

        self.set_damage(remaining_damage)
        new_hp = self.current_hit_points
        new_show_hp = self.show_hit_points
        absolute_damage = (old_hp - new_hp)
        text = (
            f'{barrier_damage_text}'
            f'*HP*: {old_show_hp} ››› {new_show_hp} (*{remaining_damage}*).'
        )

        if not markdown:
            text = remove_bold(text)
            text = remove_code(text)
        else:
            text = escape_basic_markdown_v2(text)

        return {
            'old_hp': old_hp,
            'old_show_hp': old_show_hp,
            'new_hp': new_hp,
            'new_show_hp': new_show_hp,
            'damage': value,
            'absolute_damage': absolute_damage,
            'action': 'DANO',
            'text': text,
            **self.basic_report
        }

    def physical_damage_hit_points(
        self,
        value: int,
        markdown: bool = False
    ) -> dict:
        attack = int(abs(value))
        defense = self.physical_defense
        value = attack - defense
        if value < 0:
            value = 0

        guard_text = f'Defendeu com {defense} pontos de DEFESA FÍSICA.'
        if not markdown:
            guard_text = remove_bold(guard_text)
            guard_text = remove_code(guard_text)
        else:
            guard_text = escape_basic_markdown_v2(guard_text)

        report = self.damage_hit_points(value, markdown)
        report['action'] = 'ATAQUE FÍSICO'
        report['attack'] = attack
        report['defense'] = defense
        report['defense_name'] = 'DEFESA FÍSICA'
        report['guard_text'] = guard_text

        return report

    def magical_damage_hit_points(
        self,
        value: int,
        markdown: bool = False
    ) -> dict:
        attack = int(abs(value))
        defense = self.magical_defense
        value = attack - defense
        if value < 0:
            value = 0

        guard_text = f'Defendeu com {defense} pontos de DEFESA MÁGICA.'
        if not markdown:
            guard_text = remove_bold(guard_text)
            guard_text = remove_code(guard_text)
        else:
            guard_text = escape_basic_markdown_v2(guard_text)

        report = self.damage_hit_points(value, markdown)
        report['action'] = 'ATAQUE MÁGICO'
        report['attack'] = attack
        report['defense'] = defense
        report['defense_name'] = 'DEFESA MÁGICA'
        report['guard_text'] = guard_text

        return report

    def clean_status_by_death(self) -> dict:
        status = self.get_status()

        if isinstance(status, Status):
            status_report = status.clean_status()
            self.__death()
            return status_report
        else:
            raise AttributeError(f'"{Status.__name__}" não encontrado.')

    def get_status(self) -> Status:
        status_class_name = Status.__name__
        status = self.__base_stats.get_stats_boosters(status_class_name)
        if not isinstance(status, Status):
            raise AttributeError(f'"{status_class_name}" não encontrado.')

        return status

    def cure_hit_points(
        self,
        value: int,
        markdown: bool = False
    ) -> dict:
        if value == FULL_HEAL_VALUE:
            value = self.hit_points

        value = int(abs(value))
        old_hp = self.current_hit_points
        old_show_hp = self.show_hit_points
        self.set_damage(value)
        new_hp = self.current_hit_points
        new_show_hp = self.show_hit_points
        true_cure = (new_hp - old_hp)
        text = (
            f'*{HIT_POINT_FULL_EMOJI_TEXT}*: '
            f'{old_show_hp} ››› {new_show_hp} (*{true_cure}*).'
        )

        if not markdown:
            text = remove_bold(text)
            text = remove_code(text)
        else:
            text = escape_basic_markdown_v2(text)

        return {
            'old_hp': old_hp,
            'old_show_hp': old_show_hp,
            'new_hp': new_hp,
            'new_show_hp': new_show_hp,
            'cure': value,
            'true_cure': true_cure,
            'action': 'CURA',
            'text': text,
            **self.basic_report
        }

    def revive(
        self,
        value: int = 1,
        markdown: bool = False
    ) -> dict:
        if value == FULL_HEAL_VALUE:
            value = self.hit_points

        value = -abs(int(value))
        old_hp = self.current_hit_points
        old_show_hp = self.show_hit_points
        report = {
            'old_hp': old_hp,
            'old_show_hp': old_show_hp,
            'cure': value,
            'text': None,
            **self.basic_report
        }
        if self.alive:
            print('Não pode reviver um personagem vivo.')
            text = 'Não pode reviver um personagem vivo.'

            if not markdown:
                text = remove_bold(text)
                text = remove_code(text)
            else:
                text = escape_basic_markdown_v2(text)

            report['text'] = text
            return report
        elif value < 0:
            print(f'Reviveu restaurando {-value} de HP.', end=' ')
        self.__damage = self.hit_points  # define dano para um valor máximo
        self.__damage += value
        if self.__damage > self.hit_points:
            self.__damage = self.hit_points
        elif self.__damage < 0:
            self.__damage = 0
        print(f'HP: {self.show_hp}')
        new_hp = self.current_hit_points
        new_show_hp = self.show_hit_points
        true_cure = (new_hp - old_hp)
        text = f'*HP*: {old_show_hp} ››› {new_show_hp} (*{true_cure}*).'

        if not markdown:
            text = remove_bold(text)
            text = remove_code(text)
        else:
            text = escape_basic_markdown_v2(text)

        report.update({
            'old_hp': old_hp,
            'old_show_hp': old_show_hp,
            'new_hp': new_hp,
            'new_show_hp': new_show_hp,
            'cure': value,
            'true_cure': true_cure,
            'action': 'Reviver',
            'text': text,
            **self.basic_report
        })

        return report

    def get_attr_sum_from_stats_boosters(self, attribute: str) -> int:
        value = sum([
            getattr(stats_booster, attribute)
            for stats_booster in self.__stats_boosters
        ])

        return int(value)

    def update(self) -> None:
        self.check_if_dead()

    def check_if_dead(self) -> None:
        if self.dead and not self.is_status_empty:
            self.clean_status_by_death()
        elif self.dead:
            self.__death()

    def __add_death_counter(self):
        self.__death_counter += 1

    def __death(self):
        self.__damage = self.hit_points

    # Getters
    # Combat Attributes
    @property
    def hit_points(self) -> int:
        return int(
            10 + self.base_hit_points + self.bonus_hit_points
        )

    @property
    def current_hit_points(self) -> int:
        return int(
            self.hit_points - self.__damage
        )

    @property
    def rate_hit_points(self) -> float:
        return round(self.current_hit_points / self.hit_points, 2)
    rate_hp = rate_hit_points

    @property
    def irate_hit_points(self) -> float:
        '''Inverse rate_hit_points'''

        return (1 - self.rate_hit_points)
    irate_hp = irate_hit_points

    @property
    def show_hit_points(self) -> str:
        current_hit_points = max(self.current_hit_points, 0)
        alert_text = ''
        if self.current_hit_points < 0:
            alert_text = EmojiEnum.UNDER_ZERO.value
        return f'{current_hit_points}/{self.hit_points}{alert_text}'
    show_hp = show_hit_points

    @property
    def show_barrier_points(self) -> str:
        status = self.get_status()

        return status.show_barrier_points

    @property
    def damaged(self) -> bool:
        return self.__damage > 0

    @property
    def healed(self) -> bool:
        return not self.damaged

    @property
    def alive(self) -> bool:
        return self.current_hit_points > 0

    @property
    def dead(self) -> bool:
        return not self.alive

    @property
    def is_status_empty(self) -> bool:
        status = self.get_status()

        if isinstance(status, Status):
            return status.is_empty
        else:
            return True

    @property
    def base_hit_points(self) -> int:
        return int(
            10 +
            (self.constitution * HIT_POINTS_CONSTITUTION) +
            (self.strength * HIT_POINTS_STRENGTH) +
            (self.level * HIT_POINTS_LEVEL)
        )

    @property
    def base_initiative(self) -> int:
        return int(
            (self.dexterity * INITIATIVE_DEXTERITY) +
            (self.intelligence * INITIATIVE_INTELLIGENCE) +
            (self.wisdom * INITIATIVE_WISDOM) +
            (self.charisma * INITIATIVE_CHARISMA) +
            (self.level * GENERAL_LEVEL)
        )

    @property
    def base_physical_attack(self) -> int:
        return int(
            (self.strength * PHYSICAL_ATTACK_STRENGTH) +
            (self.dexterity * PHYSICAL_ATTACK_DEXTERITY) +
            (self.level * GENERAL_LEVEL)
        )

    @property
    def base_precision_attack(self) -> int:
        return int(
            (self.strength * PRECISION_ATTACK_STRENGTH) +
            (self.dexterity * PRECISION_ATTACK_DEXTERITY) +
            (self.level * GENERAL_LEVEL)
        )

    @property
    def base_magical_attack(self) -> int:
        return int(
            (self.intelligence * MAGICAL_ATTACK_INTELLIGENCE) +
            (self.wisdom * MAGICAL_ATTACK_WISDOM) +
            (self.level * GENERAL_LEVEL)
        )

    @property
    def base_physical_defense(self) -> int:
        return int(
            (self.constitution * PHYSICAL_DEFENSE_CONSTITUTION) +
            (self.dexterity * PHYSICAL_DEFENSE_DEXTERITY) +
            (self.level * GENERAL_LEVEL)
        )

    @property
    def base_magical_defense(self) -> int:
        return int(
            (self.wisdom * MAGICAL_DEFENSE_WISDOM) +
            (self.intelligence * MAGICAL_DEFENSE_INTELLIGENCE) +
            (self.constitution * MAGICAL_DEFENSE_CONSTITUTION) +
            (self.level * GENERAL_LEVEL)
        )

    @property
    def base_hit(self) -> int:
        return int(
            (self.dexterity * HIT_DEXTERITY) +
            (self.intelligence * HIT_INTELLIGENCE) +
            (self.wisdom * HIT_WISDOM) +
            (self.charisma * HIT_CHARISMA) +
            (self.level * GENERAL_LEVEL)
        )

    @property
    def base_evasion(self) -> int:
        return int(
            (self.dexterity * EVASION_DEXTERITY) +
            (self.intelligence * EVASION_INTELLIGENCE) +
            (self.wisdom * EVASION_WISDOM) +
            (self.charisma * EVASION_CHARISMA) +
            (self.level * GENERAL_LEVEL)
        )

    @property
    def initiative(self) -> int:
        return int(
            self.base_initiative +
            self.bonus_initiative
        )

    @property
    def physical_attack(self) -> int:
        return int(
            self.base_physical_attack +
            self.bonus_physical_attack
        )

    @property
    def precision_attack(self) -> int:
        return int(
            self.base_precision_attack +
            self.bonus_precision_attack
        )

    @property
    def magical_attack(self) -> int:
        return int(
            self.base_magical_attack +
            self.bonus_magical_attack
        )

    @property
    def physical_defense(self) -> int:
        return int(
            self.base_physical_defense +
            self.bonus_physical_defense
        )

    @property
    def magical_defense(self) -> int:
        return int(
            self.base_magical_defense +
            self.bonus_magical_defense
        )

    @property
    def hit(self) -> int:
        return int(
            self.base_hit +
            self.bonus_hit
        )

    @property
    def evasion(self) -> int:
        return int(
            self.base_evasion +
            self.bonus_evasion
        )

    # Setters
    # Combat Attributes
    @hit_points.setter
    def hit_points(self, value) -> None:
        self.set_damage(value)

    hp = hit_points

    @current_hit_points.setter
    def current_hit_points(self, value) -> None:
        self.set_damage(value)

    current_hp = current_hit_points

    @property
    def basic_report(self) -> dict:
        return {
            'damaged': self.damaged,
            'healed': self.healed,
            'alive': self.alive,
            'dead': self.dead,
        }

    # Getters
    # Base Attributes
    level = property(fget=lambda self: self.__base_stats.level)
    strength = property(fget=lambda self: self.__base_stats.strength)
    dexterity = property(fget=lambda self: self.__base_stats.dexterity)
    constitution = property(fget=lambda self: self.__base_stats.constitution)
    intelligence = property(fget=lambda self: self.__base_stats.intelligence)
    wisdom = property(fget=lambda self: self.__base_stats.wisdom)
    charisma = property(fget=lambda self: self.__base_stats.charisma)

    # Getters
    # Bonus Combat Attributes
    @property
    def bonus_hit_points(self) -> int:
        return self.get_attr_sum_from_stats_boosters('bonus_hit_points')

    @property
    def bonus_initiative(self) -> int:
        return self.get_attr_sum_from_stats_boosters('bonus_initiative')

    @property
    def bonus_physical_attack(self) -> int:
        return self.get_attr_sum_from_stats_boosters('bonus_physical_attack')

    @property
    def bonus_precision_attack(self) -> int:
        return self.get_attr_sum_from_stats_boosters('bonus_precision_attack')

    @property
    def bonus_magical_attack(self) -> int:
        return self.get_attr_sum_from_stats_boosters('bonus_magical_attack')

    @property
    def bonus_physical_defense(self) -> int:
        return self.get_attr_sum_from_stats_boosters('bonus_physical_defense')

    @property
    def bonus_magical_defense(self) -> int:
        return self.get_attr_sum_from_stats_boosters('bonus_magical_defense')

    @property
    def bonus_hit(self) -> int:
        return self.get_attr_sum_from_stats_boosters('bonus_hit')

    @property
    def bonus_evasion(self) -> int:
        return self.get_attr_sum_from_stats_boosters('bonus_evasion')

    @property
    def death_counter(self) -> int:
        return self.__death_counter

    @property
    def death_counter_text(self) -> str:
        return f'{EmojiEnum.DEAD.value}Mortes: {self.__death_counter}'

    # Getters
    # Stats Boosters
    @property
    def stats_boosters(self) -> set:
        return self.__stats_boosters

    def get_sheet(self, verbose: bool = False, markdown: bool = False) -> str:
        base_init = self.initiative - self.bonus_initiative
        base_hp = self.hit_points - self.bonus_hit_points
        base_phy_atk = self.physical_attack - self.bonus_physical_attack
        base_pre_atk = self.precision_attack - self.bonus_precision_attack
        base_mag_atk = self.magical_attack - self.bonus_magical_attack
        base_phy_def = self.physical_defense - self.bonus_physical_defense
        base_mag_def = self.magical_defense - self.bonus_magical_defense
        base_hit = self.hit - self.bonus_hit
        base_evasion = self.evasion - self.bonus_evasion

        text = f'*{SECTION_HEAD.format("ATRIBUTOS DE COMBATE")}*\n'

        if self.dead:
            text += f'`{HIT_POINT_DEAD_EMOJI_TEXT}: {self.show_hit_points} '
        elif self.damaged:
            text += f'`{HIT_POINT_INJURED_EMOJI_TEXT}: {self.show_hit_points} '
        else:
            text += f'`{HIT_POINT_FULL_EMOJI_TEXT}: {self.show_hit_points} '

        if verbose:
            text += f'[{base_hp}{self.bonus_hit_points:+}]'
        text += '`\n'

        text += f'`{BARRIER_POINT_FULL_EMOJI_TEXT}: {self.show_barrier_points}'
        text += '`\n'

        text += f'`{INITIATIVE_EMOJI_TEXT}: {self.initiative:02} '
        if verbose:
            text += f'[{base_init}{self.bonus_initiative:+}]'
        text += '`\n'

        text += f'`{PHYSICAL_ATTACK_EMOJI_TEXT}: {self.physical_attack:02} '
        if verbose:
            text += f'[{base_phy_atk}{self.bonus_physical_attack:+}]'
        text += '`\n'

        text += f'`{PRECISION_ATTACK_EMOJI_TEXT}: {self.precision_attack:02} '
        if verbose:
            text += f'[{base_pre_atk}{self.bonus_precision_attack:+}]'
        text += '`\n'

        text += f'`{MAGICAL_ATTACK_EMOJI_TEXT}: {self.magical_attack:02} '
        if verbose:
            text += f'[{base_mag_atk}{self.bonus_magical_attack:+}]'
        text += '`\n'

        text += f'`{PHYSICAL_DEFENSE_EMOJI_TEXT}: {self.physical_defense:02} '
        if verbose:
            text += f'[{base_phy_def}{self.bonus_physical_defense:+}]'
        text += '`\n'

        text += f'`{MAGICAL_DEFENSE_EMOJI_TEXT}: {self.magical_defense:02} '
        if verbose:
            text += f'[{base_mag_def}{self.bonus_magical_defense:+}]'
        text += '`\n'

        text += f'`{HIT_EMOJI_TEXT}: {self.hit:02} '
        if verbose:
            text += f'[{base_hit}{self.bonus_hit:+}]'
        text += '`\n'

        text += f'`{EVASION_EMOJI_TEXT}: {self.evasion:02} '
        if verbose:
            text += f'[{base_evasion}{self.bonus_evasion:+}]'
        text += '`\n'

        if not markdown:
            text = remove_bold(text)
            text = remove_code(text)
        else:
            text = escape_basic_markdown_v2(text)

        return text

    def get_all_sheets(
        self, verbose: bool = False, markdown: bool = False
    ) -> str:
        base_stats_sheet = self.__base_stats.get_sheet(verbose, markdown)
        combat_stats_sheet = self.get_sheet(verbose, markdown)
        return (
            f'{base_stats_sheet}\n'
            f'{combat_stats_sheet}'
        )

    def alert_sheet(self):
        text = f'{ALERT_SECTION_HEAD.format("A. CBT")}\n\n'

        if self.dead:
            text += f'{HIT_POINT_DEAD_EMOJI_TEXT}: {self.show_hit_points}\n'
        elif self.damaged:
            text += f'{HIT_POINT_INJURED_EMOJI_TEXT}: {self.show_hit_points}\n'
        else:
            text += f'{HIT_POINT_FULL_EMOJI_TEXT}: {self.show_hit_points}\n'

        text += f'{INITIATIVE_EMOJI_TEXT_ABB}: {self.initiative}\n'
        text += f'{PHYSICAL_ATTACK_EMOJI_TEXT_ABB}: {self.physical_attack}\n'
        text += f'{PRECISION_ATTACK_EMOJI_TEXT_ABB}: {self.precision_attack}\n'
        text += f'{MAGICAL_ATTACK_EMOJI_TEXT_ABB}: {self.magical_attack}\n'
        text += f'{PHYSICAL_DEFENSE_EMOJI_TEXT_ABB}: {self.physical_defense}\n'
        text += f'{MAGICAL_DEFENSE_EMOJI_TEXT_ABB}: {self.magical_defense}\n'
        text += f'{HIT_EMOJI_TEXT_ABB}: {self.hit}\n'
        text += f'{EVASION_EMOJI_TEXT_ABB}: {self.evasion}\n'

        return text

    def __repr__(self) -> str:
        return (
            f'{TEXT_DELIMITER}\n'
            f'{self.__base_stats.get_sheet(True)}\n'
            f'{self.get_sheet(True)}'
            f'{TEXT_DELIMITER}\n'
        )

    def __getitem__(self, item: str) -> int:
        item = item.lower()

        hp_enum = CombatStatsEnum.HP.value
        current_hp_enum = CombatStatsEnum.CURRENT_HP.value
        iniative_enum = CombatStatsEnum.INITIATIVE.value
        physical_attack_enum = CombatStatsEnum.PHYSICAL_ATTACK.value
        precision_attack_enum = CombatStatsEnum.PRECISION_ATTACK.value
        magical_attack_enum = CombatStatsEnum.MAGICAL_ATTACK.value
        physical_defense_enum = CombatStatsEnum.PHYSICAL_DEFENSE.value
        magical_defense_enum = CombatStatsEnum.MAGICAL_DEFENSE.value
        hit_enum = CombatStatsEnum.HIT.value
        evasion_enum = CombatStatsEnum.EVASION.value

        if item in [hp_enum, 'hit_points', 'hit_point']:
            return self.hit_points
        elif item in [current_hp_enum, 'current_hp']:
            return self.current_hit_points
        elif item in [iniative_enum]:
            return self.initiative
        elif item in [physical_attack_enum, 'physical attack']:
            return self.physical_attack
        elif item in [precision_attack_enum, 'precision attack']:
            return self.precision_attack
        elif item in [magical_attack_enum, 'magical attack']:
            return self.magical_attack
        elif item in [physical_defense_enum, 'physical defense']:
            return self.physical_defense
        elif item in [magical_defense_enum, 'magical defense']:
            return self.magical_defense
        elif item in [hit_enum]:
            return self.hit
        elif item in [evasion_enum]:
            return self.evasion
        else:
            raise KeyError(
                f'Atributo "{item}" não encontrado.\n'
                'Atributos disponíveis: initiative, physical_attack, '
                'precision_attack, magical_attack, physical_defense, '
                'magical_defense, hit, evasion.'
            )


if __name__ == '__main__':
    base_stats = BaseStats(10, stats_boosters=[Status(conditions=[])])
    combat_stats = CombatStats(
        base_stats=base_stats,
        level=10,
        base_strength=6,
        base_dexterity=6,
        base_constitution=6,
        base_intelligence=3,
        base_wisdom=3,
        base_charisma=4,
        damage=0,
    )

    print(combat_stats)
    # Danos e Cura
    combat_stats.hit_points = -10
    combat_stats.current_hit_points = -20
    combat_stats.hp = -30
    combat_stats.hp = 10  # Cura
    print(combat_stats)

    print('cure_hit_points')
    print(combat_stats.cure_hit_points(100))
    print('physical_damage_hit_points')
    print(combat_stats.physical_damage_hit_points(20))
    print('magical_damage_hit_points')
    print(combat_stats.magical_damage_hit_points(20))
    print('damage_hit_points')
    print(combat_stats.damage_hit_points(100))
    print('cure_hit_points')
    print(combat_stats.cure_hit_points(100))

    # Testa se a função reviver revive com HP negativo.
    combat_stats = CombatStats(
        base_stats=base_stats,
        level=10,
        base_strength=0,
        base_dexterity=0,
        base_constitution=30,
        base_intelligence=0,
        base_wisdom=0,
        base_charisma=0,
        damage=1000,
    )
    print(combat_stats)
    combat_stats.revive()
    print(combat_stats)
