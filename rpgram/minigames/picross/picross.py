import random


class Picross:
    def __init__(self, width=5, height=5):
        # Initialize empty board
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.solution = [[0] * width for _ in range(height)]
        self.row_hints = []
        self.col_hints = []

    def generate_random_puzzle(self):
        # Generate random solution
        for i in range(self.height):
            for j in range(self.width):
                self.solution[i][j] = random.choice([0, 1])

        # Generate hints based on solution
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

    def make_move(self, row, col):
        # Toggle cell between filled (1) and empty (0)
        if 0 <= row < self.height and 0 <= col < self.width:
            self.board[row][col] = 1 - self.board[row][col]
            return True
        return False

    def check_win(self):
        # Check if current board matches solution
        return self.board == self.solution

    def print_board(self):
        # Print column hints
        max_col_hints = max(len(hints) for hints in self.col_hints)
        max_row_hints = max(len(hints) for hints in self.row_hints)
        col_span = (max_row_hints * 2) + 2
        for i in range(max_col_hints-1, -1, -1):
            print(" " * col_span, end="")
            for j in range(self.width):
                if i < len(self.col_hints[j]):
                    print(f"{self.col_hints[j][-(i+1)]:2}", end=" ")
                else:
                    print("  ", end=" ")
            print()

        # Print horizontal line
        print("   " + "-" * (self.width * 3))

        # Print board with row hints
        for i in range(self.height):
            # Print row hints
            hints_str = " ".join(str(x) for x in self.row_hints[i])
            print(f"{hints_str:>{max_row_hints*2}}", end=" |")

            # Print board row
            for j in range(self.width):
                symbol = "■" if self.board[i][j] == 1 else "□"
                print(f" {symbol}", end=" ")
            print()


if __name__ == "__main__":
    game = Picross()
    game.generate_random_puzzle()
    game.print_board()
    for i in game.solution:
        print(i)
