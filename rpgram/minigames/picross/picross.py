import random

from io import StringIO
from typing import Iterable, Union

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
        self.mark = 1
        self.generated = False

    def generate_random_picross(self):
        for i in range(self.height):
            for j in range(self.width):
                self.solution[i][j] = random.choice([0, 1])
                if self.total_solution_marks >= (self.total_squares * 0.60):
                    self.generated = True
                    break

        if self.generated is True:
            self.generate_hints()
        else:
            self.generate_random_picross()

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
        for n_col in range(self.width):
            count = 0
            hints = []
            for n_row in range(self.height):
                if self.solution[n_row][n_col] == 1:
                    count += 1
                elif count > 0:
                    hints.append(count)
                    count = 0
            if count > 0:
                hints.append(count)
            if not hints:
                hints = [0]
            self.col_hints.append(hints)

    def toggle_mark(self):
        self.mark = -self.mark

    def make_move(self, n_row: int, n_col: int) -> bool:
        # Toggle cell between filled/xmark (1 or -1) and empty (0)
        if self.mark not in [0, 1, -1]:
            raise ValueError('Value precisa ser 0, 1, ou -1')

        if 0 <= n_row < self.height and 0 <= n_col < self.width:
            if self.board[n_row][n_col] == self.mark:
                self.board[n_row][n_col] = 0
            else:
                self.board[n_row][n_col] = self.mark
                if self.mark == 1 and self.solution[n_row][n_col] == 0:
                    return False
            return True
        return None

    def check_win(self) -> bool:
        for row in range(self.height):
            for col in range(self.width):
                if self.solution[row][col] == 1 and self.board[row][col] != 1:
                    return False
                if self.solution[row][col] == 0 and self.board[row][col] == 1:
                    return False
        return True

    def number_to_symbol(self, number: int) -> str:
        if number == 1:
            symbol = '⬛'
        elif number == 0:
            symbol = '⬜'
        elif number == -1:
            symbol = '❌'

        return symbol

    def coor_to_symbol(self, n_row: int, n_col: int) -> str:
        return self.number_to_symbol(self.board[n_row][n_col])

    @property
    def text(self) -> str:
        text_io = StringIO()
        max_col_hints = max(len(hints) for hints in self.col_hints)
        max_row_hints = max(len(hints) for hints in self.row_hints)
        col_span = (max_row_hints * 2) + 1

        # Print column hints
        for i in range(max_col_hints-1, -1, -1):
            print(' ' * col_span, end='', file=text_io)
            for n_col in range(self.width):
                if i < len(self.col_hints[n_col]):
                    print(
                        f'{self.col_hints[n_col][-(i+1)]:2}',
                        end='',
                        file=text_io
                    )
                else:
                    print(' ', end=' ', file=text_io)
            print(file=text_io)

        # Print horizontal line
        print((' ' * col_span) + '-' * (self.width * 2), file=text_io)

        # Print board with row hints
        for n_row in range(self.height):
            # Print row hints
            hints_str = ' '.join(str(x) for x in self.row_hints[n_row])
            print(f'{hints_str:>{max_row_hints*2}}', end='|', file=text_io)

            # Print board row
            for n_col in range(self.width):
                symbol = self.coor_to_symbol(n_row, n_col)
                print(f'{symbol}', end='', file=text_io)
            print(file=text_io)

        text_io.seek(0)
        text = text_io.read()
        text_io.close()

        return text

    @property
    def current_mark_text(self) -> str:
        return self.number_to_symbol(self.mark)

    def __str__(self) -> str:
        return '\n'.join(
            ''.join(self.number_to_symbol(n) for n in row)
            for row in self.board
        )

    @property
    def total_squares(self) -> int:
        return self.width * self.height

    @property
    def total_solution_marks(self) -> int:
        return sum(sum(row) for row in self.solution)

    def __iter__(self) -> Iterable[dict]:
        for n_row in range(self.height):
            for n_col in range(self.width):
                text = self.coor_to_symbol(n_row, n_col)
                yield {
                    'text': text,
                    'row': n_row,
                    'col': n_col,
                }


if __name__ == '__main__':
    game = PicrossGame()
    game.generate_random_picross()
    game.make_move(0, 0)
    game.toggle_mark()
    game.make_move(4, 4)
    print('=' * 79)
    print(game.text)
    print(f'Marcas: {game.total_solution_marks}/{game.total_squares}')
    print('=' * 79)
    for i in game.solution:
        print(i)

    print('\nGame 2')
    game = PicrossGame(rarity=RarityEnum.UNCOMMON)
    game.generate_random_picross()
    game.make_move(0, 0)
    game.toggle_mark()
    game.make_move(1, 1)
    print('=' * 79)
    print(game.text)
    print(f'Marcas: {game.total_solution_marks}/{game.total_squares}')
    print('=' * 79)
    for i in game.solution:
        print(i)
    print(f'\n{game}')

    for i in game:
        print(i)
