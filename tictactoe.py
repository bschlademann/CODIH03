import random
import json
import os
from typing import Callable, Literal, Dict, List, Tuple


class TicTacToe:
    def __init__(self):
        # initiate board
        self.board: List[str] = [" " for _ in range(9)]
        self.current_player: str = "X"
        self.win_conditions: List[Tuple[int, int, int]] = [
            # horizontally
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            # vertically
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            # diagonally
            (0, 4, 8), (2, 4, 6)
        ]

        # q-learning parameters
        self.q_table: Dict[str, List[float]] = {}
        self.learning_rate: float = 0.3
        self.discount_factor: float = 0.9
        self.epsilon: float = 0.1
        # load existing q-learned knowledge
        self.load_q_table()

    # ui and core logic

    def print_board(self):
        """classic text-based board output"""
        print("\n")
        print(self.board[6], "|", self.board[7], "|", self.board[8], " (7-9)")
        print("---------")
        print(self.board[3], "|", self.board[4], "|", self.board[5], " (4-6)")
        print("---------")
        print(self.board[0], "|", self.board[1], "|", self.board[2], " (1-3)")
        print("\n")

    def has_winner(self) -> str | Literal[False]:
        for a, b, c in self.win_conditions:
            if self.board[a] == self.board[b] == self.board[c] and self.board[a] != " ":
                return self.current_player
        if " " not in self.board:
            return "tie"
        return False

    def play(self):
        print("tic-tac-toe: you are playing against the q-learning ai")
        print("commands: 'q' to quit, 'r' to restart")
        game_over = False

        while not game_over:
            self.print_board()
            if self.current_player == "X":
                user_input = input(
                    f"player {self.current_player}, choose a cell (1-9): ").lower().strip()
                if user_input == 'q':
                    return
                if user_input == 'r':
                    self.clear_board()
                    continue
                try:
                    board_index = self.get_board_index(int(user_input))
                except ValueError as e:
                    print(f"invalid input: {e}")
                    continue
            else:
                board_index = self.get_ai_q_move()

            if self.board[board_index] == " ":
                self.board[board_index] = self.current_player
                result = self.has_winner()
                if result:
                    self.print_board()
                    if result == "tie":
                        print("the game ended in a tie.")
                    else:
                        print(f"player {result} won.")

                    if input("play again? (y/n): ").lower().strip() == 'y':
                        self.clear_board()
                    else:
                        game_over = True
                else:
                    self.current_player = "O" if self.current_player == "X" else "X"
            else:
                print("cell already occupied!")

    def get_board_index(self, i: int) -> int:
        if 1 <= i <= 9:
            return i-1
        raise ValueError("only 1-9 are valid entries")

    def get_available_moves(self) -> List[int]:
        return [i for i, cell in enumerate(self.board) if cell == " "]

    # ai profiles

    def get_ai_random_move(self) -> int:
        return random.choice(self.get_available_moves())

    def get_completing_move(self, symbol: str) -> int | None:
        # finds a move that completes a line for the given symbol
        for a, b, c in self.win_conditions:
            line = [self.board[a], self.board[b], self.board[c]]
            if line.count(symbol) == 2 and line.count(" ") == 1:
                return [a, b, c][line.index(" ")]
        return None

    def get_ai_win_or_block_move(self) -> int:
        # dynamic move to win or block based on current player; defaults to random
        opponent = "O" if self.current_player == "X" else "X"

        # 1. try to win
        move = self.get_completing_move(self.current_player)
        if move is not None:
            return move

        # 2. try to block
        move = self.get_completing_move(opponent)
        if move is not None:
            return move

        # 3. default to random
        return self.get_ai_random_move()

    def get_ai_newell_simon_move(self) -> int:
        available = self.get_available_moves()
        opponent = "O" if self.current_player == "X" else "X"

        # win/block logic
        win_move = self.get_completing_move(self.current_player)
        if win_move is not None:
            return win_move

        block_move = self.get_completing_move(opponent)
        if block_move is not None:
            return block_move

        # center, corners, sides
        if 4 in available:
            return 4
        for corner in [0, 2, 6, 8]:
            if corner in available:
                return corner
        return self.get_ai_random_move()

    def get_ai_q_move(self) -> int:
        # uses q-table to choose the best learned move
        state = self.get_state()
        available = self.get_available_moves()

        if state not in self.q_table:
            self.q_table[state] = [0.0] * 9

        q_values = [self.q_table[state][i] for i in available]
        max_q = max(q_values)
        best_moves = [i for i in available if self.q_table[state][i] == max_q]
        return random.choice(best_moves)

    # option c: implementation of q-learning

    def get_state(self) -> str:
        return "".join(self.board)

    def update_q_table(self, old_state: str, action: int, reward: float, new_state: str):
        # standard q-learning update formula
        if old_state not in self.q_table:
            self.q_table[old_state] = [0.0] * 9
        if new_state not in self.q_table:
            self.q_table[new_state] = [0.0] * 9

        old_value = self.q_table[old_state][action]
        next_max = max(self.q_table[new_state])

        new_value = old_value + self.learning_rate * \
            (reward + self.discount_factor * next_max - old_value)
        self.q_table[old_state][action] = new_value

    def save_q_table(self, filename: str = "q_table.json"):
        # saves the learned brain to a json file
        with open(filename, "w") as f:
            json.dump(self.q_table, f)

    def load_q_table(self, filename: str = "q_table.json"):
        # loads the brain from a json file
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    self.q_table = json.load(f)
            except Exception:
                self.q_table = {}

    def train_ai(self, numberGames: int = 10000):
        # training loop to fill the q-table by playing against a variety of opponents
        print(f"training in progress ({numberGames} games)")

        for _ in range(numberGames):
            self.clear_board()
            game_over = False

            # select a teacher for this game to ensure a versatile brain
            # rotating teachers prevents the ai from becoming too passive or too specialized
            teacher_logic = random.choice([
                self.get_ai_random_move,
                self.get_ai_win_or_block_move,
                self.get_ai_newell_simon_move
            ])

            # track the move history for both players to distribute rewards at the end
            history: Dict[str, Tuple[str, int] | None] = {"X": None, "O": None}

            while not game_over:
                state = self.get_state()
                player = self.current_player

                if player == "X":
                    # the learner: uses epsilon-greedy to explore or use known q-values
                    move = self.get_ai_random_move() if random.random(
                    ) < self.epsilon else self.get_ai_q_move()
                else:
                    # the teacher: provides a consistent challenge for the learner
                    move = teacher_logic()

                history[player] = (state, move)
                self.board[move] = player
                result = self.has_winner()

                if result:
                    if result == "tie":
                        # reward both for a tie; 0.5 is a 'neutral-positive' outcome
                        for p in ["X", "O"]:
                            record = history[p]
                            if record:
                                self.update_q_table(
                                    record[0], record[1], 0.5, self.get_state())
                    else:
                        # winner gets 1.0, loser gets -1.0 punishment
                        winner = result
                        loser = "O" if winner == "X" else "X"
                        win_rec = history[winner]
                        loss_rec = history[loser]

                        if win_rec:
                            self.update_q_table(
                                win_rec[0], win_rec[1], 1.0, self.get_state())
                        if loss_rec:
                            self.update_q_table(
                                loss_rec[0], loss_rec[1], -1.0, self.get_state())
                    game_over = True
                else:
                    # intermediate move update with 0 immediate reward
                    self.update_q_table(state, move, 0.0, self.get_state())
                    self.current_player = "O" if self.current_player == "X" else "X"

        # save the accumulated knowledge back to the json file
        self.save_q_table()
        print("training complete, model saved")

    # simulations

    def simulate_matchup(self, p1_name: str, p1_logic: Callable[[], int], p2_name: str, p2_logic: Callable[[], int], games: int = 1000):
        wins_p1, wins_p2, ties = 0, 0, 0
        for _ in range(games):
            self.clear_board()
            while True:
                move = p1_logic() if self.current_player == "X" else p2_logic()
                self.board[move] = self.current_player
                result = self.has_winner()
                if result:
                    if result == "X":
                        wins_p1 += 1
                    elif result == "O":
                        wins_p2 += 1
                    else:
                        ties += 1
                    break
                self.current_player = "O" if self.current_player == "X" else "X"
        print(f"{p1_name:20} vs {p2_name:20} | p1 wins: {wins_p1:4} | p2 wins: {wins_p2:4} | ties: {ties:4}")

    def run_all_comparisons(self, games: int = 1000):
        if not self.q_table:
            self.train_ai()
        print(f"simulation: {games} games per matchup)")
        profiles: List[Tuple[str, Callable[[], int]]] = [
            ("random", self.get_ai_random_move),
            ("simple", self.get_ai_win_or_block_move),
            ("newell simon", self.get_ai_newell_simon_move),
            ("q-learning ai", self.get_ai_q_move)
        ]
        for p1_name, p1_logic in profiles:
            for p2_name, p2_logic in profiles:
                self.simulate_matchup(
                    f"🗡️ {p1_name}", p1_logic, f"🛡️ {p2_name}", p2_logic, games)
        self.clear_board()

    def clear_board(self):
        self.board = [" " for _ in range(9)]
        self.current_player = "X"

game = TicTacToe()
# game.train_ai()
game.run_all_comparisons()
