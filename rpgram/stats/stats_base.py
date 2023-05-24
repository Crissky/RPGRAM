from typing import List

from constants.text import SECTION_HEAD, TEXT_DELIMITER
from functions.text import escape_basic_markdown_v2, remove_bold, remove_code
from rpgram.boosters import StatsBooster


class BaseStats:
    '''Classe que representa as estatísticas básicas de um personagem.

    Fonte: https://i.pinimg.com/originals/ee/9b/0c/ee9b0cd5fc0c94dcfb215ad94c6a6871.jpg'''

    def __init__(
        self,
        level: int = 1,
        xp: int = 0,
        base_strength: int = 0,
        base_dexterity: int = 0,
        base_constitution: int = 0,
        base_intelligence: int = 0,
        base_wisdom: int = 0,
        base_charisma: int = 0,
        stats_boosters: List[StatsBooster] = []
    ) -> None:
        if level < 1 and isinstance(level, int):
            raise ValueError('Nível deve ser um inteiro maior que zero.')
        self.__level = int(level)
        self.__current_xp = int(xp)

        self.__base_strength = int(base_strength)
        self.__base_dexterity = int(base_dexterity)
        self.__base_constitution = int(base_constitution)
        self.__base_intelligence = int(base_intelligence)
        self.__base_wisdom = int(base_wisdom)
        self.__base_charisma = int(base_charisma)

        self.__stats_boosters = set(stats_boosters)

        self.update()
        self.check_attributes()

    def __get_points(self) -> int:
        max_level_points = self.__level * 3
        points = max_level_points - self.total_base_stats
        if points < 0:
            raise ValueError(
                f'Foi gasto mais Pontos nos atributos que o Nível permite.\n'
                f'Total de Pontos do Nível {self.__level}: '
                f'{max_level_points}.\n'
                f'Total de Pontos gastos: {self.total_base_stats}.'
            )
        return points

    def __get_modifier_stats(self, attribute_points: int) -> int:
        return (attribute_points - 10) // 2

    def __add_stats(self, points: int, attribute: str) -> None:
        points = int(points)
        clean_attribute = attribute.split('_')[-1].title()
        print(f'Adicionando {points} Ponto(s) de {clean_attribute}.')
        if points > self.points:
            raise ValueError(
                f'Não há Pontos({points}) suficientes para adicionar.\n'
                f'Atualmente você tem {self.points} Ponto(s).'
            )
        if points <= 0:
            raise ValueError(
                f'Não é possível adicionar menos que '
                f'1 Ponto de {clean_attribute}.'
            )
        new_value = getattr(self, attribute) + points
        setattr(self, attribute, new_value)

    def update(self) -> None:
        self.__boost_stats()

    def check_attributes(self) -> None:
        self.__get_points()

    def __boost_stats(self) -> None:
        self.__bonus_strength = 0
        self.__bonus_dexterity = 0
        self.__bonus_constitution = 0
        self.__bonus_intelligence = 0
        self.__bonus_wisdom = 0
        self.__bonus_charisma = 0

        self.__multiplier_strength = 1
        self.__multiplier_dexterity = 1
        self.__multiplier_constitution = 1
        self.__multiplier_intelligence = 1
        self.__multiplier_wisdom = 1
        self.__multiplier_charisma = 1

        for sb in self.__stats_boosters:
            self.__bonus_strength += int(sb.bonus_strength)
            self.__bonus_dexterity += int(sb.bonus_dexterity)
            self.__bonus_constitution += int(sb.bonus_constitution)
            self.__bonus_intelligence += int(sb.bonus_intelligence)
            self.__bonus_wisdom += int(sb.bonus_wisdom)
            self.__bonus_charisma += int(sb.bonus_charisma)

            self.__multiplier_strength += sb.multiplier_strength - 1.0
            self.__multiplier_dexterity += sb.multiplier_dexterity - 1.0
            self.__multiplier_constitution += sb.multiplier_constitution - 1.0
            self.__multiplier_intelligence += sb.multiplier_intelligence - 1.0
            self.__multiplier_wisdom += sb.multiplier_wisdom - 1.0
            self.__multiplier_charisma += sb.multiplier_charisma - 1.0

    # Getters
    @property
    def total_base_stats(self) -> int:
        return int(sum([
            self.base_strength,
            self.base_dexterity,
            self.base_constitution,
            self.base_intelligence,
            self.base_wisdom,
            self.base_charisma
        ]))

    @property
    def level(self) -> int:
        return self.__level

    @property
    def classe_level(self) -> int:
        return (self.__level // 10) + 1

    @property
    def next_level_xp(self) -> int:
        return self.__level * 100

    @property
    def points(self) -> int:
        return self.__get_points()

    @property
    def xp(self) -> int:
        return self.__current_xp

    # Base Attributes
    @property
    def base_strength(self) -> int:
        return self.__base_strength

    @property
    def base_dexterity(self) -> int:
        return self.__base_dexterity

    @property
    def base_constitution(self) -> int:
        return self.__base_constitution

    @property
    def base_intelligence(self) -> int:
        return self.__base_intelligence

    @property
    def base_wisdom(self) -> int:
        return self.__base_wisdom

    @property
    def base_charisma(self) -> int:
        return self.__base_charisma

    # Attributes
    @property
    def strength(self) -> int:
        return int(
            (self.base_strength + self.bonus_strength) *
            self.multiplier_strength
        )

    @property
    def dexterity(self) -> int:
        return int(
            (self.base_dexterity + self.bonus_dexterity) *
            self.multiplier_dexterity
        )

    @property
    def constitution(self) -> int:
        return int(
            (self.base_constitution + self.bonus_constitution) *
            self.multiplier_constitution
        )

    @property
    def intelligence(self) -> int:
        return int(
            (self.base_intelligence + self.bonus_intelligence) *
            self.multiplier_intelligence
        )

    @property
    def wisdom(self) -> int:
        return int(
            (self.base_wisdom + self.bonus_wisdom) *
            self.multiplier_wisdom
        )

    @property
    def charisma(self) -> int:
        return int(
            (self.base_charisma + self.bonus_charisma) *
            self.multiplier_charisma
        )

    # Setters
    @xp.setter
    def xp(self, value: int) -> None:
        value = int(value)
        if value <= 0:
            raise ValueError(
                f'Não é possível adicionar Pontos de Experiência menor que 1.'
            )
        print(f'Ganhou {value} Pontos de Experiência.')
        while value > 0:
            self.__current_xp += value
            if self.__current_xp >= self.next_level_xp:
                value = self.__current_xp - self.next_level_xp
                self.__current_xp = 0
                self.__level += 1
                print(
                    f'Subiu para o Nível {self.__level}. '
                    f'Agora possui {self.points} Pontos.'
                )
            else:
                break

    @base_strength.setter
    def base_strength(self, value: int) -> None:
        self.__add_stats(value, '_BaseStats__base_strength')

    @base_dexterity.setter
    def base_dexterity(self, value: int) -> None:
        return self.__add_stats(value, '_BaseStats__base_dexterity')

    @base_constitution.setter
    def base_constitution(self, value: int) -> None:
        return self.__add_stats(value, '_BaseStats__base_constitution')

    @base_intelligence.setter
    def base_intelligence(self, value: int) -> None:
        return self.__add_stats(value, '_BaseStats__base_intelligence')

    @base_wisdom.setter
    def base_wisdom(self, value: int) -> None:
        return self.__add_stats(value, '_BaseStats__base_wisdom')

    @base_charisma.setter
    def base_charisma(self, value: int) -> None:
        return self.__add_stats(value, '_BaseStats__base_charisma')

    @strength.setter
    def strength(self, value: int) -> None:
        self.base_strength = value

    @dexterity.setter
    def dexterity(self, value: int) -> None:
        self.base_dexterity = value

    @constitution.setter
    def constitution(self, value: int) -> None:
        self.base_constitution = value

    @intelligence.setter
    def intelligence(self, value: int) -> None:
        self.base_intelligence = value

    @wisdom.setter
    def wisdom(self, value: int) -> None:
        self.base_wisdom = value

    @charisma.setter
    def charisma(self, value: int) -> None:
        self.base_charisma = value

    xp_points = xp

    # Getters and Setters
    # Attribute Bonus
    @property
    def bonus_strength(self) -> int:
        return self.__bonus_strength

    @property
    def bonus_dexterity(self) -> int:
        return self.__bonus_dexterity

    @property
    def bonus_constitution(self) -> int:
        return self.__bonus_constitution

    @property
    def bonus_intelligence(self) -> int:
        return self.__bonus_intelligence

    @property
    def bonus_wisdom(self) -> int:
        return self.__bonus_wisdom

    @property
    def bonus_charisma(self) -> int:
        return self.__bonus_charisma

    # Getters and Setters
    # Attribute Bonus
    @property
    def multiplier_strength(self) -> float:
        return (
            self.__multiplier_strength
            if self.__multiplier_strength >= 0.1
            else 0.1
        )

    @property
    def multiplier_dexterity(self) -> float:
        return (
            self.__multiplier_dexterity
            if self.__multiplier_dexterity >= 0.1
            else 0.1
        )

    @property
    def multiplier_constitution(self) -> float:
        return (
            self.__multiplier_constitution
            if self.__multiplier_constitution >= 0.1
            else 0.1
        )

    @property
    def multiplier_intelligence(self) -> float:
        return (
            self.__multiplier_intelligence
            if self.__multiplier_intelligence >= 0.1
            else 0.1
        )

    @property
    def multiplier_wisdom(self) -> float:
        return (
            self.__multiplier_wisdom
            if self.__multiplier_wisdom >= 0.1
            else 0.1
        )

    @property
    def multiplier_charisma(self) -> float:
        return (
            self.__multiplier_charisma
            if self.__multiplier_charisma >= 0.1
            else 0.1
        )

    # Getters
    # Attribute Modifiers
    @property
    def mod_strength(self) -> int:
        return self.__get_modifier_stats(self.strength)

    @property
    def mod_dexterity(self) -> int:
        return self.__get_modifier_stats(self.dexterity)

    @property
    def mod_constitution(self) -> int:
        return self.__get_modifier_stats(self.constitution)

    @property
    def mod_intelligence(self) -> int:
        return self.__get_modifier_stats(self.intelligence)

    @property
    def mod_wisdom(self) -> int:
        return self.__get_modifier_stats(self.wisdom)

    @property
    def mod_charisma(self) -> int:
        return self.__get_modifier_stats(self.charisma)

    # Getters
    # Stats Boosters
    @property
    def stats_boosters(self) -> set:
        return set(self.__stats_boosters)

    def __getitem__(self, key: str) -> int:
        key = key.upper()
        if key in ['STR', 'FOR', 'STRENGTH', 'FORCA', 'FORÇA']:
            return self.strength
        elif key in ['DEX', 'DES', 'DEXTERITY', 'DESTREZA']:
            return self.dexterity
        elif key in ['CON', 'CONSTITUTION', 'CONSTITUICAO', 'CONSTITUIÇÃO']:
            return self.constitution
        elif key in ['INT', 'INTELLIGENCE', 'INTELIGENCIA', 'INTELIGÊNCIA']:
            return self.intelligence
        elif key in ['WIS', 'SAB', 'WISDOM', 'SABEDORIA']:
            return self.wisdom
        elif key in ['CHA', 'CAR', 'CHARISMA', 'CARISMA']:
            return self.charisma
        elif key in ['XP', 'EXPERIENCE', 'EXPERIENCIA', 'EXPERIÊNCIA']:
            return self.xp
        else:
            raise KeyError(
                f'Atributo "{key}" não encontrado.\n'
                f'Atributos disponíveis: FOR, DES, CON, INT, SAB, CAR.'
            )

    def __setitem__(self, key: str, value: int) -> None:
        key = key.upper()
        if key in ['STR', 'FOR', 'STRENGTH', 'FORCA', 'FORÇA']:
            self.strength = value
        elif key in ['DEX', 'DES', 'DEXTERITY', 'DESTREZA']:
            self.dexterity = value
        elif key in ['CON', 'CONSTITUTION', 'CONSTITUICAO', 'CONSTITUIÇÃO']:
            self.constitution = value
        elif key in ['INT', 'INTELLIGENCE', 'INTELIGENCIA', 'INTELIGÊNCIA']:
            self.intelligence = value
        elif key in ['WIS', 'SAB', 'WISDOM', 'SABEDORIA']:
            self.wisdom = value
        elif key in ['CHA', 'CAR', 'CHARISMA', 'CARISMA']:
            self.charisma = value
        elif key in ['XP', 'EXPERIENCE', 'EXPERIENCIA', 'EXPERIÊNCIA']:
            self.xp = value
        else:
            raise KeyError(
                f'Atributo "{key}" não encontrado. '
                f'Atributos disponíveis: FOR, DES, CON, INT, SAB, CAR.'
            )

    def get_sheet(self, verbose: bool = False, markdown: bool = False) -> str:
        text = (
            f'Nível: {self.level} (Nível da Classe: {self.classe_level})\n'
            f'Experiência: {self.xp}/{self.next_level_xp}\n'
            f'Pontos: {self.points}\n\n'
        )

        text += f"*{SECTION_HEAD.format('ATRIBUTOS BASE')}*\n"

        text += f'`FOR: {self.strength:02} '
        if verbose:
            text += (
                f'[{self.base_strength}{self.bonus_strength:+}]'
                f'x{self.multiplier_strength:.2f} '
            )
        text += f'({self.mod_strength:+})`\n'

        text += f'`DES: {self.dexterity:02} '
        if verbose:
            text += (
                f'[{self.base_dexterity}{self.bonus_dexterity:+}]'
                f'x{self.multiplier_dexterity:.2f} '
            )
        text += f'({self.mod_dexterity:+})`\n'

        text += f'`CON: {self.constitution:02} '
        if verbose:
            text += (
                f'[{self.base_constitution}{self.bonus_constitution:+}]'
                f'x{self.multiplier_constitution:.2f} '
            )
        text += f'({self.mod_constitution:+})`\n'

        text += f'`INT: {self.intelligence:02} '
        if verbose:
            text += (
                f'[{self.base_intelligence}{self.bonus_intelligence:+}]'
                f'x{self.multiplier_intelligence:.2f} '
            )
        text += f'({self.mod_intelligence:+})`\n'

        text += f'`SAB: {self.wisdom:02} '
        if verbose:
            text += (
                f'[{self.base_wisdom}{self.bonus_wisdom:+}]'
                f'x{self.multiplier_wisdom:.2f} '
            )
        text += f'({self.mod_wisdom:+})`\n'

        text += f'`CAR: {self.charisma:02} '
        if verbose:
            text += (
                f'[{self.base_charisma}{self.bonus_charisma:+}]'
                f'x{self.multiplier_charisma:.2f} '
            )
        text += f'({self.mod_charisma:+})`\n'

        if not markdown:
            text = remove_bold(text)
            text = remove_code(text)
        else:
            text = escape_basic_markdown_v2(text)

        return text

    def get_all_sheets(
        self, verbose: bool = False, markdown: bool = False
    ) -> str:
        return self.get_sheet(verbose=verbose, markdown=markdown)

    def __repr__(self) -> str:
        return (
            f'{TEXT_DELIMITER}\n'
            f'{self.get_sheet(True)}'
            f'{TEXT_DELIMITER}\n'
        )


if __name__ == '__main__':
    stats = BaseStats(
        level=1.50,
        xp=0,
        base_strength=3,
        base_dexterity=0,
        base_constitution=0,
        base_intelligence=0,
        base_wisdom=0,
        base_charisma=0
    )
    print(stats)
    stats.xp = 310
    print(stats)
    stats.strength = 1
    print(stats)
    stats.dexterity = 1
    print(stats)
    stats.constitution = 1
    print(stats)
    stats.intelligence = 1
    print(stats)
    stats.wisdom = 1
    print(stats)
    stats.charisma = 1
    print(stats)
