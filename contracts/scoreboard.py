class Scoreboard:
    def __init__(self):
        self.players = {}
        self.game_history = [] # Stores every move for hardcore players

    def record_move(self, position: int, player_symbol: str):
        # This records a single move on-chain
        move_entry = {"pos": position, "symbol": player_symbol}
        self.game_history.append(move_entry)
        return f"Move {player_symbol} at {position} recorded."

    def record_match(self, player_address: str, result: str):
        if player_address not in self.players:
            self.players[player_address] = {"wins": 0, "losses": 0, "ties": 0}
        
        if result == "win":
            self.players[player_address]["wins"] += 1
        elif result == "loss":
            self.players[player_address]["losses"] += 1
        elif result == "tie":
            self.players[player_address]["ties"] += 1
            
        return f"Final result {result} recorded."