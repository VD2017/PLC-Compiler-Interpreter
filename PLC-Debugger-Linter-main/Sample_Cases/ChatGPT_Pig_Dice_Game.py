import random

class PigDiceGame:
    def __init__(self, target_score=100):
        self.target_score = target_score
        self.players = []
        self.scores = []
    
    def add_player(self, name):
        """Add a player to the game."""
        self.players.append(name)
        self.scores.append(0)  # Initialize each player's score to 0

    def roll_die(self):
        """Simulate rolling a 6-sided die."""
        return random.randint(1, 6)

    def turn(self, player_index):
        """Execute a turn for a player."""
        turn_total = 0
        player_name = self.players[player_index]
        print(f"\n{player_name}'s turn!")

        while True:
            roll = self.roll_die()
            print(f"{player_name} rolled a {roll}")

            if roll == 1:
                print(f"{player_name} loses all points for this turn!")
                return 0  # The player loses all points for this turn
            
            turn_total += roll
            print(f"Turn total so far: {turn_total}")

            # Ask if the player wants to hold or roll again
            decision = input("Do you want to roll again? (y/n): ").strip().lower()
            if decision != 'y':
                print(f"{player_name} holds with {turn_total} points for this turn.")
                return turn_total

    def play_game(self):
        """Main loop to play the game."""
        current_player = 0

        while max(self.scores) < self.target_score:
            print(f"\nCurrent Scores: {dict(zip(self.players, self.scores))}")
            # Play a turn for the current player
            turn_points = self.turn(current_player)
            self.scores[current_player] += turn_points

            # Check if the current player has won
            if self.scores[current_player] >= self.target_score:
                print(f"\n{self.players[current_player]} wins with {self.scores[current_player]} points!")
                break

            # Switch to the next player
            current_player = (current_player + 1) % len(self.players)

if __name__ == "__main__":
    game = PigDiceGame()

    # Add players to the game
    num_players = int(input("Enter the number of players: "))
    for i in range(num_players):
        player_name = input(f"Enter the name for player {i + 1}: ")
        game.add_player(player_name)

    # Start the game
    game.play_game()
