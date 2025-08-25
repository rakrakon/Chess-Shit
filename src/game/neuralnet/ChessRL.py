from src.game.Board import Board
from src.game.neuralnet.BoardEncoder import encode_board
from src.game.neuralnet.LegalMovesEncoder import board_legal_action_indices
from src.game.neuralnet.ActionEncoder import decode_action

class ChessRL:
    def __init__(self):
        self.board = Board()
        self.done = False

    def reset(self):
        """Resets the board to the initial state and returns the encoded state"""
        self.board = Board()
        self.done = False
        return encode_board(self.board)

    def step(self, action_idx):
        """
        Executes the action on the board and returns (next_state, reward, done)
        """
        if self.done:
            raise ValueError("Game is over. Call reset() to start a new game.")

        reward = 0

        from_pos, to_pos, promotion = decode_action(action_idx)

        if promotion is None:
            self.board.move_piece(from_pos, to_pos)
        else:
            self.board.promote_pawn(from_pos, promotion)


        if self.is_game_over():
            self.done = True
            winner = self.get_winner()
            if winner is None:
                reward = 0  # Draw
            elif winner == self.board.get_current_turn():
                reward = -1  # Opponent just won
            else:
                reward = 1   # Current player just won

        next_state = encode_board(self.board)
        return next_state, reward, self.done

    def get_valid_actions(self):
        """Returns a list of legal action indices for the current state"""
        return board_legal_action_indices(self.board)

    def is_game_over(self):
        return self.board.has_ended

    def get_winner(self):
        """Returns the winner color, or None for draw"""
        return self.board.winner

    def render(self):
        """Prints the board to console"""
        self.board.print_board()
