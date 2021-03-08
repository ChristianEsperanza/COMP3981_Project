from space import Space
from space import Piece


class Board:

    def __init__(self):
        self._board = Board.generate_empty_board()

    @property
    def board(self):
        return self._board

    @staticmethod
    def generate_board():
        board_2 = [
            ['(I, 5)', '(I, 6)', '(I, 7)', '(I, 8)', '(I, 9)'],
            ['(H, 4)', '(H, 5)', '(H, 6)', '(H, 7)', '(H, 8)', '(H, 9)'],
            ['(G, 3)', '(G, 4)', '(G, 5)', '(G, 6)', '(G, 7)', '(G, 8)', '(G, 9)'],
            ['(F, 2)', '(F, 3)', '(F, 4)', '(F, 5)', '(F, 6)', '(F, 7)', '(F, 8)', '(F, 9)'],
            ['(E, 1)', '(E, 2)', '(E, 3)', '(E, 4)', '(E, 5)', '(E, 6)', '(E, 7)', '(E, 8)', '(E, 9)'],
            ['(D, 1)', '(D, 2)', '(D, 3)', '(D, 4)', '(D, 5)', '(D, 6)', '(D, 7)', '(D, 8)'],
            ['(C, 1)', '(C, 2)', '(C, 3)', '(C, 4)', '(C, 5)', '(C, 6)', '(C, 7)'],
            ['(B, 1)', '(B, 2)', '(B, 3)', '(B, 4)', '(B, 5)', '(B, 6)'],
            ['(A, 1)', '(A, 2)', '(A, 3)', '(A, 4)', '(A, 5)']
        ]
        return board_2

    @staticmethod
    def generate_board_with_spaces(board):
        board_space = []
        for line in board:
            board_space_line = []
            for space_name in line:
                board_space_line.append(Space(space_name))
            board_space.append(board_space_line)
        return board_space

    @staticmethod
    def print_board(board):
        index_factor = -4
        odd_line_count = False
        for line in board:
            for i in range(0, abs(index_factor)):
                print("    ", end="")
            index_factor += 1
            odd_line_count = not odd_line_count
            for space in line:
                print(f"{space}", end="  ")
            print("\n\n")

    def modify_pieces(self, positions, piece_type: Piece):

        print(self.board)
        for position in positions:
            row, index = position
            self.board[row][index].piece = piece_type
            print(f"{position[0]}|{position[1]}")

    def default_board_start(self):
        white_pieces = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
                        (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                        (2, 2), (2, 3), (2, 4)]
        black_pieces = [(8, 0), (8, 1), (8, 2), (8, 3), (8, 4),
                        (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5),
                        (6, 2), (6, 3), (6, 4)]
        self.modify_pieces(white_pieces, Piece.WHITE)
        self.modify_pieces(black_pieces, Piece.BLACK)

    def print_board_with_space(self):
        index_factor = -4
        odd_line_count = False
        for line in self.board:
            # Prints indents.
            for i in range(0, abs(index_factor)):
                print("    ", end="")
            odd_line_count = not odd_line_count
            for space in line:
                print(f"{space.space_id}", end="  ")

            print()
            # Prints indents.
            for i in range(0, abs(index_factor)):
                print("    ", end="")
            index_factor += 1

            for space in line:
                print(f"{space.piece}", end="   ")

            print("\n")

    @staticmethod
    def generate_empty_board():
        pre_board = Board.generate_board()
        return Board.generate_board_with_spaces(pre_board)

    def __str__(self):
        return self.board


def main():
    board = Board()
    board.default_board_start()
    board.print_board_with_space()


if __name__ == '__main__':
    main()
