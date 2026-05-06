import random
from typing import Callable, Literal
class TicTacToe():
    def __init__(self):
        # initiate board with 9 empty Strings
        self.board = [" " for _ in range(9)]
        self.current_player = "X"
        self.win_conditions = [
            # horizontally
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            # vertically
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            # diagonally
            (0, 4, 8), (2, 4, 6)
        ]

    def print_board(self):
        print("\n")
        print(self.board[6], "|", self.board[7], "|", self.board[8], " (7-9)")
        print("---------")
        print(self.board[3], "|", self.board[4], "|", self.board[5], " (4-6)")
        print("---------")
        print(self.board[0], "|", self.board[1], "|", self.board[2], " (1-3)")
        print("\n")

    def has_winner(self):

        for a, b, c in self.win_conditions:
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
        print("tic-tac-toe: you are playing against smart")
        # notify player about quit and restart options
        print("commands: enter 'q' to quit or 'r' to restart the game")
        game_over = False

        while not game_over:
            self.print_board()
            # player's turn
            if self.current_player == "X":
                # input by player
                user_input = input(f"Player {self.current_player}, choose a cell (1-9) or command (r)estart/(q)uit: ").lower().strip()
                
                # check for quit condition
                if user_input == 'q':
                    print("game exited")
                    return
                
                # check for restart condition
                if user_input == 'r':
                    print("restarting game...")
                    self.clear_board()
                    continue

                try:
                    # input() returns String, parse to int
                    playerMove = int(user_input)
                    # parse player input to correct List index
                    boardIndex = self.getBoardIndex(playerMove)
                except ValueError as e:
                    print(f"invalid input: {e}")
                    # go back to start of the loop
                    continue
            # ai's turn
            else:
                boardIndex = self.get_ai_smart_move()

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
                    
                    # keep asking until valid y/n input is provided
                    while True:
                        choice = input("play again? (y/n): ").lower().strip()
                        if choice == 'y':
                            self.clear_board()
                            break
                        elif choice == 'n':
                            game_over = True
                            break
                        else:
                            print("invalid input, please enter 'y' or 'n'")
                else:
                    # change player
                    if self.current_player == "X":
                        self.current_player = "O"
                    else:
                        self.current_player = "X"
            else:
                # handle entry of occupied cell number
                print("cell already occupied, choose another cell")
    
    def getBoardIndex(self, i: int):
        if 1 <= i <= 9:
            return i-1
        else:
            raise ValueError("only 1-9 are valid entries")

    def get_available_moves(self):
        return [i for i, cell in enumerate(self.board) if cell == " "]

    def get_ai_random_move(self):
        # get all available moves
        available_moves = self.get_available_moves()
        # randomly select the index of a free cell
        return random.choice(available_moves)

    def get_completing_move(self, symbol: Literal["X", "O"]):
        # look for a move that completes a row for the given symbol
        for a, b, c in self.win_conditions:
            line = [self.board[a], self.board[b], self.board[c]]
            # check if two cells are occupied by symbol and one is free
            if line.count(symbol) == 2 and line.count(" ") == 1:
                indices = [a, b, c]
                return indices[line.index(" ")]
        return None

    def get_ai_win_or_block_move(self):
        # can (a)i win?
        move = self.get_completing_move("O")
        if move is not None:
            return move

        # must (a)i block?
        move = self.get_completing_move("X")
        if move is not None:
            return move
        return None

    def get_ai_win_or_block_or_random_move(self):
        # save result of tactical check
        move = self.get_ai_win_or_block_move()

        # if tactical move (win/block) is found, return it
        if move is not None:
            return move

        # fallback: random move
        return self.get_ai_random_move()

    def get_ai_smart_move(self):
        available_moves = self.get_available_moves()

        # priority 1 & 2: win or block
        move = self.get_ai_win_or_block_move()
        if move is not None:
            return move

        # priority 3: create fork
        # check every free cell if it creates two winning lines
        for move in available_moves:
            self.board[move] = "O"
            winning_paths = 0
            for a, b, c in self.win_conditions:
                line = [self.board[a], self.board[b], self.board[c]]
                if line.count("O") == 2 and line.count(" ") == 1:
                    winning_paths += 1
            self.board[move] = " "  # undo move
            if winning_paths >= 2:
                return move

        # priority 4: block opponent fork
        # if opponent could create a fork, we must block it
        opp_forks: list[int] = []
        for move in available_moves:
            self.board[move] = "X"
            winning_paths = 0
            for a, b, c in self.win_conditions:
                line = [self.board[a], self.board[b], self.board[c]]
                if line.count("X") == 2 and line.count(" ") == 1:
                    winning_paths += 1
            self.board[move] = " "
            if winning_paths >= 2:
                opp_forks.append(move)

        if len(opp_forks) == 1:
            return opp_forks[0]
        elif len(opp_forks) > 1:
            # special case: if opponent has multiple forks, force defense
            # but not on a cell that allows them a fork
            for move in available_moves:
                self.board[move] = "O"
                # create a two-in-a-row
                for a, b, c in self.win_conditions:
                    line = [self.board[a], self.board[b], self.board[c]]
                    if line.count("O") == 2 and line.count(" ") == 1:
                        block_move = [a, b, c][line.index(" ")]
                        if block_move not in opp_forks:
                            self.board[move] = " "
                            return move
                self.board[move] = " "

        # priority 5: occupy center
        if self.board[4] == " ":
            return 4

        # priority 6: occupy opposite corner
        corner_pairs = [(0, 8), (2, 6), (8, 0), (6, 2)]
        for start, target in corner_pairs:
            if self.board[start] == "X" and self.board[target] == " ":
                return target

        # priority 7: occupy corner
        for move in [0, 2, 6, 8]:
            if move in available_moves:
                return move

        # priority 8: occupy side
        for move in [1, 3, 5, 7]:
            if move in available_moves:
                return move

        # fallback: random move
        return self.get_ai_random_move()

    def simulate_matchup(self, p1_name: str, p1_logic: Callable[[], int], p2_name: str, p2_logic: Callable[[], int], games: int = 1000):
        wins_p1, wins_p2, ties = 0, 0, 0
        
        for _ in range(games):
            self.board = [" " for _ in range(9)]
            self.current_player = "X" # P1 startet immer als X
            
            while True:
                # check who's turn it is
                if self.current_player == "X":
                    move = p1_logic()
                else:
                    move = p2_logic()
                
                # current_player makes their move
                self.board[move] = self.current_player
                
                # check if game is over: winner/tie
                result = self.has_winner()
                if result:
                    if result == "X": wins_p1 += 1
                    elif result == "O": wins_p2 += 1
                    else: ties += 1
                    break
                
                # change player
                self.current_player = "O" if self.current_player == "X" else "X"
                
        print(f"{p1_name:10} vs {p2_name:10} | {p1_name} wins: {wins_p1:4} | {p2_name} wins: {wins_p2:4} | Ties: {ties:4}")

    def run_all_comparisons(self, games: int = 1000):
        print(f"--- simulation ({games} games) ---")

        self.simulate_matchup("random", self.get_ai_random_move,
                              "simple", self.get_ai_win_or_block_or_random_move, games)

        self.simulate_matchup("simple", self.get_ai_win_or_block_or_random_move,
                              "smart", self.get_ai_smart_move, games)

        self.simulate_matchup("random", self.get_ai_random_move,
                              "Smart", self.get_ai_smart_move, games)

        self.simulate_matchup("smart", self.get_ai_smart_move,
                              "smart", self.get_ai_smart_move, games)
        
        self.clear_board()

    def clear_board(self):
        self.board = [" " for _ in range(9)]

game = TicTacToe()
game.run_all_comparisons()
game.play()
