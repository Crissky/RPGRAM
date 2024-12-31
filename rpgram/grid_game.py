from random import choice, randint, sample
from typing import Iterable, NamedTuple, Union

from rpgram.enums.rarity import RarityEnum


RARITY_RANGE_DICT = {
    RarityEnum.COMMON: (3, 3, 2),
    RarityEnum.UNCOMMON: (3, 4, 2),
    RarityEnum.RARE: (3, 3, 3),
    RarityEnum.EPIC: (3, 4, 3),
    RarityEnum.LEGENDARY: (3, 5, 4),
    RarityEnum.MYTHIC: (3, 7, 5),
}


class Coordinates(NamedTuple):
    row: int
    col: int
    text: str

    def __str__(self):
        return f'{self.text}: {self.row}, {self.col}'

    def __repr__(self):
        return f'Coor({self})'


class GridGame:
    def __init__(
        self,
        n_rows: int = None,
        n_cols: int = None,
        n_options: int = None,
        rarity: Union[str, RarityEnum] = None
    ):
        self.__all_colors = ['🔴', '🔵', '🟡', '🟢', '🟣']
        self.__bad_target = self.__all_colors[0]
        self.__good_target = self.__all_colors[1]
        if isinstance(rarity, str):
            rarity = RarityEnum[rarity]

        if isinstance(rarity, RarityEnum):
            n_min, n_max, n_options = RARITY_RANGE_DICT[rarity]
            n_range = range(n_min, n_max + 1)
            n_rows = choice(n_range)
            if (n_rows % 2) == 0:
                n_range = range(n_min, n_max + 1, 2)
            n_cols = choice(n_range)
        elif rarity is not None:
            raise TypeError(
                f'Rarity deve ser do tipo RarityEnum ou None. '
                f'Tipo: {type(rarity)}.'
            )

        if n_rows < 3 or n_cols < 3:
            raise ValueError('O Gride deve ter ao menos 3 linhas e 3 colunas.')

        if n_options is not None:
            n_options = int(n_options)
        else:
            n_options = len(self.__all_colors)

        if n_options > len(self.__all_colors):
            raise ValueError(
                f'O valor máximo de n_options é {len(self.__all_colors)}'
            )
        elif n_options < 2:
            raise ValueError('O valor mínimo de n_options é 2.')

        self.__rarity = rarity
        self.__n_rows = int(n_rows)
        self.__n_cols = int(n_cols)
        self.__colors = self.__all_colors[:n_options]
        self.__grid = [self.__bad_target] * (n_cols * n_rows)
        self.shuffle()

    def switch(self, row: int, col: int) -> bool:
        if row < 0 or row >= self.n_rows:
            raise IndexError(f'row index out of range [0:{self.n_rows-1}]')
        if col < 0 or col >= self.n_cols:
            raise IndexError(f'col index out of range [0:{self.n_cols-1}]')

        before_total_good = self.total_good

        index = (row * self.n_cols) + col
        self.__grid[index] = self.get_next_color(self.__grid[index])

        # Switch left neighbor (if exists)
        if col > 0:
            index = (row * self.n_cols) + col - 1
            self.__grid[index] = self.get_next_color(self.__grid[index])

        # Switch right neighbor (if exists)
        if col < self.n_cols - 1:
            index = (row * self.n_cols) + col + 1
            self.__grid[index] = self.get_next_color(self.__grid[index])

        # Switch upper neighbor (if exists)
        if row > 0:
            index = ((row - 1) * self.n_cols) + col
            self.__grid[index] = self.get_next_color(self.__grid[index])

        # Switch lower neighbor (if exists)
        if row < self.n_rows - 1:
            index = ((row + 1) * self.n_cols) + col
            self.__grid[index] = self.get_next_color(self.__grid[index])

        is_good_move = before_total_good < self.total_good
        return is_good_move

    def get_next_color(self, value) -> str:
        """Retorna o próximo valor na lista após o valor especificado. 
        Se o valor for o último da lista, retorna o primeiro elemento.
        """

        index = self.__colors.index(value)
        next_index = (index + 1) % len(self.__colors)
        return self.__colors[next_index]

    def shuffle(self):
        grid_size = self.size
        max_targets = grid_size // 2
        total_shuffle = randint(1, max_targets)
        target_list = sample(range(grid_size), total_shuffle)
        colors = self.__colors.copy()
        colors.remove(self.__bad_target)
        for index in target_list:
            self.__grid[index] = choice(colors)

    def __str__(self):
        data = []
        for i in range(0, self.size, self.n_cols):
            text = str([self.__grid[i:i+self.n_cols]])
            data.append(text)

        return '\n'.join(data)

    def __iter__(self) -> Iterable[Coordinates]:
        for row in range(self.n_rows):
            for col in range(self.n_cols):
                index = (row * self.n_cols) + col
                text = self.__grid[index]
                yield Coordinates(row, col, text)

    @property
    def is_solved(self) -> bool:
        grid = self.grid
        colors = self.colors
        colors.remove(self.__bad_target)
        result = False
        for color in colors:
            if grid.count(color) == self.size:
                result = True
                break

        return result

    rarity: RarityEnum = property(lambda self: self.__rarity)
    n_rows: int = property(lambda self: self.__n_rows)
    n_cols: int = property(lambda self: self.__n_cols)
    grid: list = property(lambda self: self.__grid.copy())
    size: int = property(lambda self: len(self.__grid))
    total_good: int = property(
        lambda self: self.__grid.count(self.__good_target)
    )
    total_bad: int = property(
        lambda self: self.__grid.count(self.__bad_target)
    )
    colors: list = property(lambda self: self.__colors.copy())
    colors_text: str = property(lambda self: ', '.join(self.colors))
    full_colors_text: str = property(lambda self: f'Cores: {self.colors_text}')
    is_failed: bool = property(lambda self: self.total_bad == self.size)


if __name__ == '__main__':
    g = GridGame(3, 3)
    print(g.grid)
    print(g.n_rows)
    print(g.n_cols)
    print(g)
    print(g.is_solved, g.is_failed)
    g.switch(1, 1)
    print(g)

    def switch_all(grid: GridGame):
        n_rows = grid.n_rows
        n_cols = grid.n_cols
        for row in range(n_rows):
            for col in range(n_cols):
                grid.switch(row=row, col=col)

    # Test Iteration
    for n_options in range(2, 6):
        for col in range(3, 8):
            for row in range(3, 8):
                g = GridGame(row, col, n_options)
                print([coor for coor in g])
                switch_all(g)
                print('-'*50)

    # Test Rarity
    for rarity in RarityEnum:
        g = GridGame(rarity=rarity)
        print(f'rarity: {g.rarity}, n_rows: {g.n_rows}, n_cols: {g.n_cols}')
        print(g.n_rows)

    print(g.colors)
    print(g.is_solved)
    print(g.colors)
