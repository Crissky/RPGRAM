from random import randint, sample


class GridGame:
    def __init__(self, n_rows: int, n_cols: int):
        if n_rows < 3 or n_cols < 3:
            raise ValueError('O Gride deve ter ao menos 3 linhas e 3 colunas.')
        self.__n_rows = int(n_rows)
        self.__n_cols = int(n_cols)
        self.__grid = [False] * (n_cols * n_rows)
        self.shuffle()

    def switch(self, row: int, col: int):
        if row < 0 or row >= self.n_rows:
            raise IndexError(f'row index out of range [0:{self.n_rows-1}]')
        if col < 0 or col >= self.n_cols:
            raise IndexError(f'col index out of range [0:{self.n_cols-1}]')

        index = (row * self.n_rows) + col
        self.__grid[index] = not self.__grid[index]

        # Switch left neighbor (if exists)
        if col > 0:
            index = (row * self.n_rows) + col - 1
            self.__grid[index] = not self.__grid[index]

        # Switch right neighbor (if exists)
        if col < self.n_cols - 1:
            index = (row * self.n_rows) + col + 1
            self.__grid[index] = not self.__grid[index]

        # Switch upper neighbor (if exists)
        if row > 0:
            index = ((row - 1) * self.n_rows) + col
            self.__grid[index] = not self.__grid[index]

        # Switch lower neighbor (if exists)
        if row < self.n_rows - 1:
            index = ((row + 1) * self.n_rows) + col
            self.__grid[index] = not self.__grid[index]

    def shuffle(self):
        grid_len = len(self.__grid)
        max_targets = (grid_len // 2)
        total_shuffle = randint(1, max_targets)
        target_list = sample(range(grid_len), total_shuffle)
        for index in target_list:
            self.__grid[index] = True

    def __str__(self):
        data = []
        for i in range(0, self.size, self.n_cols):
            text = str([self.__grid[i:i+self.n_cols]])
            data.append(text)

        return '\n'.join(data)

    n_rows = property(lambda self: self.__n_rows)
    n_cols = property(lambda self: self.__n_cols)
    grid = property(lambda self: self.__grid.copy())
    size = property(lambda self: len(self.__grid))
    is_solved = property(lambda self: all(self.__grid))
    is_failed = property(
        lambda self: self.__grid.count(False) == len(self.__grid)
    )


if __name__ == '__main__':
    g = GridGame(3, 3)
    print(g.grid)
    print(g.n_rows)
    print(g.n_cols)
    print(g)
    print(g.is_solved, g.is_failed)
    g.switch(1, 1)
    print(g)
