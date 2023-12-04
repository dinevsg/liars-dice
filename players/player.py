import random
from abc import ABC, abstractmethod


class Player(ABC):

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.decision = ""
        self.bet = []
        self.roll_dice()
        
    def roll_dice(self):
        for die in range(1, 5 + 1):
            die = random.randint(1, 6)
            self.hand.append(die)

    def remove_die(self):
        self.hand.pop()

    def re_roll_dice(self):
        number_of_dice = len(self.hand)
        self.hand.clear()
        for die in range(1, number_of_dice + 1):
            die = random.randint(1, 6)
            self.hand.append(die)

    @abstractmethod
    def bet_or_liar_decision(self):
        pass

    @abstractmethod
    def place_bet(self, player_bet):
        pass

