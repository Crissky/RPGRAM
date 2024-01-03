from typing import List

from constant.text import SECTION_HEAD, TEXT_DELIMITER
from function.text import escape_basic_markdown_v2, remove_bold, remove_code
from rpgram.constants.text import (
    EVASION_EMOJI_TEXT,
    HIT_EMOJI_TEXT,
    HIT_POINT_DEAD_EMOJI_TEXT,
    HIT_POINT_FULL_EMOJI_TEXT,
    HIT_POINT_INJURED_EMOJI_TEXT,
    INITIATIVE_EMOJI_TEXT,
    MAGICAL_ATTACK_EMOJI_TEXT,
    MAGICAL_DEFENSE_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT,
    PHYSICAL_DEFENSE_EMOJI_TEXT,
    PRECISION_ATTACK_EMOJI_TEXT
)
from rpgram.enums.emojis import EmojiEnum
from rpgram.stats import BaseStats
from rpgram.boosters import StatsBooster


FULL_HEAL_VALUE = 'FULL_HEAL'


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
        stats_boosters: List[StatsBooster] = []
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

        self.__stats_boosters = set(base_stats.stats_boosters)
        self.update()

    def set_damage(self, value: int) -> None:
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

    def damage_hit_points(self, value: int, action_name: str = None) -> dict:
        if action_name == 'physical_attack':
            return self.physical_damage_hit_points(value)
        elif action_name == 'precision_attack':
            return self.physical_damage_hit_points(value)
        elif action_name == 'magical_attack':
            return self.magical_damage_hit_points(value)

        value = -int(abs(value))
        old_hp = self.current_hit_points
        old_show_hp = self.show_hit_points
        self.set_damage(value)
        new_hp = self.current_hit_points
        new_show_hp = self.show_hit_points
        absolute_damage = (old_hp - new_hp)
        return {
            'old_hp': old_hp,
            'old_show_hp': old_show_hp,
            'new_hp': new_hp,
            'new_show_hp': new_show_hp,
            'damage': value,
            'absolute_damage': absolute_damage,
            'damaged': self.damaged,
            'healed': self.healed,
            'alive': self.alive,
            'dead': self.dead,
            'action': 'DANO',
            'text': f'HP: {old_show_hp} ››› {new_show_hp} ({value}).'
        }

    def physical_damage_hit_points(self, value: int) -> dict:
        attack = int(abs(value))
        defense = self.physical_defense
        value = attack - defense
        if value < 0:
            value = 0
        report = self.damage_hit_points(value)
        report['action'] = 'ATAQUE FÍSICO'
        report['attack'] = attack
        report['defense'] = defense
        report['defense_name'] = 'DEFESA FÍSICA'
        report['guard_text'] = (
            f'Defendeu com {defense} pontos de DEFESA FÍSICA.'
        )

        return report

    def magical_damage_hit_points(self, value: int) -> dict:
        attack = int(abs(value))
        defense = self.magical_defense
        value = attack - defense
        if value < 0:
            value = 0
        report = self.damage_hit_points(value)
        report['action'] = 'ATAQUE MÁGICO'
        report['attack'] = attack
        report['defense'] = defense
        report['defense_name'] = 'DEFESA MÁGICA'
        report['guard_text'] = (
            f'Defendeu com {defense} pontos de DEFESA MÁGICA.'
        )

        return report

    def cure_hit_points(self, value: int) -> dict:
        if value == FULL_HEAL_VALUE:
            value = self.hit_points
        value = int(abs(value))
        old_hp = self.current_hit_points
        old_show_hp = self.show_hit_points
        self.set_damage(value)
        new_hp = self.current_hit_points
        new_show_hp = self.show_hit_points
        true_cure = (new_hp - old_hp)
        return {
            'old_hp': old_hp,
            'old_show_hp': old_show_hp,
            'new_hp': new_hp,
            'new_show_hp': new_show_hp,
            'cure': value,
            'true_cure': true_cure,
            'damaged': self.damaged,
            'healed': self.healed,
            'alive': self.alive,
            'dead': self.dead,
            'action': 'CURA',
            'text': f'HP: {old_show_hp} ››› {new_show_hp} ({true_cure}).'
        }

    def revive(self, value: int = 1) -> dict:
        value = -abs(int(value))
        old_hp = self.current_hit_points
        old_show_hp = self.show_hit_points
        if self.alive:
            print(f'Não pode reviver um personagem vivo.')
            return None
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
        return {
            'old_hp': old_hp,
            'old_show_hp': old_show_hp,
            'new_hp': new_hp,
            'new_show_hp': new_show_hp,
            'cure': value,
            'true_cure': true_cure,
            'damaged': self.damaged,
            'healed': self.healed,
            'alive': self.alive,
            'dead': self.dead,
            'action': 'Reviver',
            'text': f'HP: {old_show_hp} ››› {new_show_hp} ({true_cure}).'
        }

    def update(self) -> None:
        self.__boost_stats()

    def __boost_stats(self) -> None:
        self.__bonus_hit_points = 0
        self.__bonus_initiative = 0
        self.__bonus_physical_attack = 0
        self.__bonus_precision_attack = 0
        self.__bonus_magical_attack = 0
        self.__bonus_physical_defense = 0
        self.__bonus_magical_defense = 0
        self.__bonus_hit = 0
        self.__bonus_evasion = 0

        for sb in self.__stats_boosters:
            self.__bonus_hit_points += int(sb.bonus_hit_points)
            self.__bonus_initiative += int(sb.bonus_initiative)
            self.__bonus_physical_attack += int(sb.bonus_physical_attack)
            self.__bonus_precision_attack += int(sb.bonus_precision_attack)
            self.__bonus_magical_attack += int(sb.bonus_magical_attack)
            self.__bonus_physical_defense += int(sb.bonus_physical_defense)
            self.__bonus_magical_defense += int(sb.bonus_magical_defense)
            self.__bonus_hit += int(sb.bonus_hit)
            self.__bonus_evasion += int(sb.bonus_evasion)

    # Getters
    # Combat Attributes
    @property
    def hit_points(self) -> int:
        return int(
            10 +
            (self.constitution * 15) +
            (self.strength * 8) +
            self.bonus_hit_points
        )

    @property
    def current_hit_points(self) -> int:
        return int(
            self.hit_points - self.__damage
        )

    @property
    def show_hit_points(self) -> str:
        current_hit_points = max(self.current_hit_points, 0)
        alert_text = ''
        if self.current_hit_points < 0:
            alert_text = EmojiEnum.UNDER_ZERO.value
        return f'{current_hit_points}/{self.hit_points}{alert_text}'

    show_hp = show_hit_points

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
    def initiative(self) -> int:
        return int(
            (self.dexterity * 2) +
            (self.wisdom * 3) +
            (self.charisma * 3) +
            self.bonus_initiative
        )

    @property
    def physical_attack(self) -> int:
        return int(
            (self.strength * 3) +
            (self.dexterity * 2) +
            self.bonus_physical_attack
        )

    @property
    def precision_attack(self) -> int:
        return int(
            (self.dexterity * 4) +
            self.bonus_precision_attack
        )

    @property
    def magical_attack(self) -> int:
        return int(
            (self.intelligence * 4) +
            (self.wisdom * 2) +
            self.bonus_magical_attack
        )

    @property
    def physical_defense(self) -> int:
        return int(
            (self.constitution * 3) +
            (self.dexterity * 2) +
            self.bonus_physical_defense
        )

    @property
    def magical_defense(self) -> int:
        return int(
            (self.wisdom * 4) +
            (self.intelligence * 2) +
            (self.constitution * 2) +
            self.bonus_magical_defense
        )

    @property
    def hit(self) -> int:
        return int(
            (self.dexterity * 3) +
            (self.wisdom * 2) +
            (self.charisma * 2) +
            self.bonus_hit
        )

    @property
    def evasion(self) -> int:
        return int(
            (self.dexterity * 3) +
            (self.wisdom * 2) +
            (self.charisma * 2) +
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

    # Getters
    # Base Attributes
    strength = property(fget=lambda self: self.__base_stats.strength)
    dexterity = property(fget=lambda self: self.__base_stats.dexterity)
    constitution = property(fget=lambda self: self.__base_stats.constitution)
    intelligence = property(fget=lambda self: self.__base_stats.intelligence)
    wisdom = property(fget=lambda self: self.__base_stats.wisdom)
    charisma = property(fget=lambda self: self.__base_stats.charisma)

    # Getters
    # Bonus Combat Attributes
    @property
    def bonus_initiative(self) -> int:
        return self.__bonus_initiative

    @property
    def bonus_physical_attack(self) -> int:
        return self.__bonus_physical_attack

    @property
    def bonus_precision_attack(self) -> int:
        return self.__bonus_precision_attack

    @property
    def bonus_magical_attack(self) -> int:
        return self.__bonus_magical_attack

    @property
    def bonus_physical_defense(self) -> int:
        return self.__bonus_physical_defense

    @property
    def bonus_magical_defense(self) -> int:
        return self.__bonus_magical_defense

    @property
    def bonus_hit_points(self) -> int:
        return self.__bonus_hit_points

    @property
    def bonus_hit(self) -> int:
        return self.__bonus_hit

    @property
    def bonus_evasion(self) -> int:
        return self.__bonus_evasion

    # Getters
    # Stats Boosters
    @property
    def stats_boosters(self) -> set:
        return set(self.__stats_boosters)

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
        text += f'`\n'

        text += f'`{INITIATIVE_EMOJI_TEXT}: {self.initiative:02} '
        if verbose:
            text += f'[{base_init}{self.bonus_initiative:+}]'
        text += f'`\n'

        text += f'`{PHYSICAL_ATTACK_EMOJI_TEXT}: {self.physical_attack:02} '
        if verbose:
            text += f'[{base_phy_atk}{self.bonus_physical_attack:+}]'
        text += f'`\n'

        text += f'`{PRECISION_ATTACK_EMOJI_TEXT}: {self.precision_attack:02} '
        if verbose:
            text += f'[{base_pre_atk}{self.bonus_precision_attack:+}]'
        text += f'`\n'

        text += f'`{MAGICAL_ATTACK_EMOJI_TEXT}: {self.magical_attack:02} '
        if verbose:
            text += f'[{base_mag_atk}{self.bonus_magical_attack:+}]'
        text += f'`\n'

        text += f'`{PHYSICAL_DEFENSE_EMOJI_TEXT}: {self.physical_defense:02} '
        if verbose:
            text += f'[{base_phy_def}{self.bonus_physical_defense:+}]'
        text += f'`\n'

        text += f'`{MAGICAL_DEFENSE_EMOJI_TEXT}: {self.magical_defense:02} '
        if verbose:
            text += f'[{base_mag_def}{self.bonus_magical_defense:+}]'
        text += f'`\n'

        text += f'`{HIT_EMOJI_TEXT}: {self.hit:02} '
        if verbose:
            text += f'[{base_hit}{self.bonus_hit:+}]'
        text += f'`\n'

        text += f'`{EVASION_EMOJI_TEXT}: {self.evasion:02} '
        if verbose:
            text += f'[{base_evasion}{self.bonus_evasion:+}]'
        text += f'`\n'

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

    def __repr__(self) -> str:
        return (
            f'{TEXT_DELIMITER}\n'
            f'{self.__base_stats.get_sheet(True)}\n'
            f'{self.get_sheet(True)}'
            f'{TEXT_DELIMITER}\n'
        )


if __name__ == '__main__':
    base_stats = BaseStats(10)
    combat_stats = CombatStats(
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
