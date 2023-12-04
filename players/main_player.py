from players.player import Player


class MainPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    # Function to define main player's decision
    def bet_or_liar_decision(self):
        while True:
            main_player_decision = input("Choose [b]et or [l]iar\n-- ").lower().strip()
            predefined = ["b", "l"]
            # Force main player to not make a wrong input, so the game won't throw an error
            if main_player_decision not in predefined:
                print(f"You must type 'b' to choose bet or 'l' for liar")
                continue

            self.decision = "bet" if main_player_decision == predefined[0] else "liar"
            break

    # Function to place the main player's bet
    def place_bet(self, player_bet):
        if not self.decision:
            self.decision = "bet"

        self.bet = [player_bet[0], player_bet[1]]
