class TicTacToe:
    def __init__(self):
        # Creates an empty 3x3 board (represented as a list of 9 empty strings)
        self.board = [""] * 9
        self.current_player = "X"
        self.winner = None
        self.game_over = False

    def make_move(self, position: int):
        if self.game_over:
            return f"Game over. Winner: {self.winner}"
        if position < 0 or position > 8:
            return "Invalid move. Position must be 0-8."
        if self.board[position] != "":
            return "Position already taken!"

        # Mark the board
        self.board[position] = self.current_player
        
        # Check if this move won the game
        self._check_win_or_draw()

        # Swap turns if game is still going
        if not self.game_over:
            self.current_player = "O" if self.current_player == "X" else "X"
            return f"Move accepted. {self.current_player}'s turn."
        
        return f"Game over! Winner: {self.winner}"

    def _check_win_or_draw(self):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        
        # Check for a winner
        for condition in win_conditions:
            a, b, c = condition
            if self.board[a] != "" and self.board[a] == self.board[b] == self.board[c]:
                self.winner = self.board[a]
                self.game_over = True
                return
                
        # Check for a draw
        if "" not in self.board:
            self.winner = "Draw"
            self.game_over = True