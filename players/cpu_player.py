import random
from players.player import Player


class CpuPlayer(Player):
    CPU_NAMES = ["Benjamin Franklin", "Albert Einstein", "Bill Gates", "Elon Musk", "Donald Trump"]

    def __init__(self, name):
        super().__init__(name)

    # Function to define cpu player's decision
    def bet_or_liar_decision(self):
        # Thanks to 'random' module the 'bet' decision will be 8 times more than the 'liar' decision
        cpu_player_decision = random.choices(["bet", "liar"], weights=(8, 1))
        self.decision = "bet" if cpu_player_decision[0] == "bet" else "liar"

    # Function to place the cpu player's bet
    def place_bet(self, player_bet):
        if not self.decision:
            self.decision = "bet"

        cpu_player_bet = random.choice(player_bet)
        self.bet = [cpu_player_bet[0], cpu_player_bet[1]]

