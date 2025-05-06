import random
from typing import Union

from rpgram.enums.function import get_enum_index
from rpgram.enums.rarity import RarityEnum


class PicrossGame:
    def __init__(
        self,
        width: int = 5,
        height: int = 5,
        rarity: Union[str, RarityEnum] = None
    ):
        if isinstance(rarity, str):
            rarity = RarityEnum[rarity]
        if isinstance(rarity, RarityEnum):
            width = 3
            height = 3
            self.rarity = rarity
            rarity_level = get_enum_index(self.rarity)
            for i in range(rarity_level):
                if i % 2 == 0:
                    height += 1
                else:
                    width += 1
        elif rarity is not None:
            raise TypeError(
                f'Rarity deve ser do tipo RarityEnum ou None. '
                f'Tipo: {type(rarity)}.'
            )

        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.solution = [[0] * width for _ in range(height)]
        self.row_hints = []
        self.col_hints = []

    def generate_random_puzzle(self):
        for i in range(self.height):
            for j in range(self.width):
                self.solution[i][j] = random.choice([0, 1])

        self.generate_hints()

    def generate_hints(self):
        # Generate row hints
        self.row_hints = []
        for row in self.solution:
            count = 0
            hints = []
            for cell in row:
                if cell == 1:
                    count += 1
                elif count > 0:
                    hints.append(count)
                    count = 0
            if count > 0:
                hints.append(count)
            if not hints:
                hints = [0]
            self.row_hints.append(hints)

        # Generate column hints
        self.col_hints = []
        for j in range(self.width):
            count = 0
            hints = []
            for i in range(self.height):
                if self.solution[i][j] == 1:
                    count += 1
                elif count > 0:
                    hints.append(count)
                    count = 0
            if count > 0:
                hints.append(count)
            if not hints:
                hints = [0]
            self.col_hints.append(hints)

    def make_move(self, row: int, col: int, value: int) -> bool:
        # Toggle cell between filled/xmark (1 or -1) and empty (0)
        if value not in [0, 1, -1]:
            raise ValueError('Value precisa ser 0, 1, ou -1')

        if 0 <= row < self.height and 0 <= col < self.width:
            if self.board[row][col] == value:
                self.board[row][col] = 0
            else:
                self.board[row][col] = value
            return True
        return False

    def check_win(self) -> bool:
        return self.board == self.solution

    def print_board(self):
        max_col_hints = max(len(hints) for hints in self.col_hints)
        max_row_hints = max(len(hints) for hints in self.row_hints)
        col_span = (max_row_hints * 2) + 3
        # Print column hints
        for i in range(max_col_hints-1, -1, -1):
            print(' ' * col_span, end='')
            for j in range(self.width):
                if i < len(self.col_hints[j]):
                    print(f'{self.col_hints[j][-(i+1)]:2}', end=' ')
                else:
                    print('  ', end=' ')
            print()

        # Print horizontal line
        print((' ' * col_span) + '-' * (self.width * 3))

        # Print board with row hints
        for i in range(self.height):
            # Print row hints
            hints_str = ' '.join(str(x) for x in self.row_hints[i])
            print(f'{hints_str:>{max_row_hints*2}}', end=' |')

            # Print board row
            for j in range(self.width):
                if self.board[i][j] == 1:
                    symbol = '⬛'
                elif self.board[i][j] == 0:
                    symbol = '⬜'
                elif self.board[i][j] == -1:
                    symbol = '❌'

                print(f' {symbol}', end='')
            print()


if __name__ == '__main__':
    game = PicrossGame()
    game.generate_random_puzzle()
    game.make_move(0, 0, 1)
    game.make_move(4, 4, -1)
    game.print_board()
    for i in game.solution:
        print(i)

    print('\nGame 2')
    game = PicrossGame(rarity=RarityEnum.UNCOMMON)
    game.generate_random_puzzle()
    game.make_move(0, 0, 1)
    game.make_move(1, 1, -1)
    game.print_board()
    for i in game.solution:
        print(i)
