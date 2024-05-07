class GridGame:
    def __init__(self, n_rows: int, n_cols: int):
        if n_rows < 2 or n_cols < 2:
            raise ValueError('O Gride deve ter ao menos 2 linhas e 2 colunas.')
        self.__n_rows = int(n_rows)
        self.__n_cols = int(n_cols)
        self.__grid = [False] * (n_cols * n_rows)

    def switch(self, row: int, col: int):
        if row < 0 or row >= self.n_rows:
            raise IndexError(f'row index out of range [{self.n_rows}]')
        if col < 0 or col >= self.n_cols:
            raise IndexError(f'col index out of range [{self.n_cols}]')

        index = (row * self.n_rows) + col
        self.__grid[index] = not self.__grid[index]

        # Compare with left neighbor (if exists)
        if col > 0:
            index = (row * self.n_rows) + col - 1
            self.__grid[index] = not self.__grid[index]

        # Compare with right neighbor (if exists)
        if col < self.n_cols - 1:
            index = (row * self.n_rows) + col + 1
            self.__grid[index] = not self.__grid[index]

        # Compare with upper neighbor (if exists)
        if row > 0:
            index = ((row - 1) * self.n_rows) + col
            self.__grid[index] = not self.__grid[index]

        # Compare with lower neighbor (if exists)
        if row < self.n_rows - 1:
            index = ((row + 1) * self.n_rows) + col
            self.__grid[index] = not self.__grid[index]

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


if __name__ == '__main__':
    g = GridGame(3, 3)
    print(g.grid)
    print(g.n_rows)
    print(g.n_cols)
    print(g)
    g.switch(1, 1)
    print(g)
