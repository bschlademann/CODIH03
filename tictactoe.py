class TicTacToe():
    def __init__(self):
        # initiate board with 9 empty Strings
        self.board = [" " for _ in range(9)]
        self.current_player = "X"

    def print_board(self):
        print("\n")
        print(self.board[6], "|", self.board[7], "|", self.board[8], " (7-9)")
        print("---------")
        print(self.board[3], "|", self.board[4], "|", self.board[5], " (4-6)")
        print("---------")
        print(self.board[0], "|", self.board[1], "|", self.board[2], " (1-3)")
        print("\n")

    def has_winner(self):
        win_conditions = [
            # horizontally
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            # vertically
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            # diagonally
            (0, 4, 8), (2, 4, 6)
        ]

        for a, b, c in win_conditions:
            # iterate over win_conditions, check if current board has 3 matching symbols in a row in any direction
            # {and self.board[a] != " "} is necessary to prevent the function to recognize 3 empty cells as a wincondition
            if self.board[a] == self.board[b] == self.board[c] and self.board[a] != " ":
                return self.current_player

        # check if board is filled / has no " " Strings
        if " " not in self.board:
            return "tie"
        # unless a an entry in win_conditions is found or a tie is reached return false
        return False

    def play(self):
        # main loop
        print("tic-tac-toe")
        game_over = False

        while not game_over:
            self.print_board()

            # input by user
            try:
                # input() returns String, parse to int
                move = int(
                    input(
                        f"Player {self.current_player}, choose a cell (1-9): ")
                )
                # parse player input to correct List index
                boardIndex = self.getBoardIndex(move)

                # if cell is empty
                if self.board[boardIndex] == " ":
                    # fill cell with current_player-symbol
                    self.board[boardIndex] = self.current_player
                    # then check, if current_player has won
                    result = self.has_winner()
                    # result is true if tie is reached or board contains a wincondition
                    if result:
                        self.print_board()
                        if result == "tie":
                            print("the game ended in a tie")
                        else:
                            print(
                                f"Player {result} won.")
                        # end the game if someone won or a tie was reached
                        game_over = True
                    else:
                        # change player
                        if self.current_player == "X":
                            self.current_player = "O"
                        else:
                            self.current_player = "X"
                else:
                    # handle entry of occupied cell number
                    print("cell already occupied, choose another cell")

            except ValueError as e:
                # catch invalid entries
                print(f"invalid input: {e}")

    def getBoardIndex(self, i: int):
        if 1 <= i <= 9:
            return i-1
        else:
            raise ValueError("only 1-9 are valid entries")


game = TicTacToe()
game.play()
