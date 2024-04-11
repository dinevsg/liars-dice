import time
from players.cpu_player import CpuPlayer
from players.main_player import MainPlayer


class Game:
    VALID_BETS = []

    def __init__(self):
        self.all_players = []
        self.current_player = None
        self.previous_player = None
        self.wild_ones = None

    def create_main_player(self):
        while True:
            main_player_name = (input("Choose your name:\n-- "))
            if main_player_name == "" or main_player_name.isspace():
                print(f"Your name could not be blank! Try again")
                continue
            break

        self.all_players.append(MainPlayer(main_player_name))
        print(f"Welcome {main_player_name}!")
        time.sleep(1)

    def create_cpu_player(self):
        print("How many players you want to play against? Choose up to 5 players!")
        while True:
            try:
                cpu_players_count = int(input("-- "))
                if cpu_players_count > len(CpuPlayer.CPU_NAMES):
                    print("Maximum opponents you can have is 5! Try again")
                    continue
                elif cpu_players_count <= 0:
                    print(f"You can't play by yourself! Choose number greater than 0")
                    continue
                break
            except ValueError:
                print("You MUST type a number! Try again")

        for cpu in range(1, cpu_players_count + 1):
            cpu_player_name = CpuPlayer.CPU_NAMES.pop(0)
            self.all_players.append(CpuPlayer(cpu_player_name))
            time.sleep(1)
            print(f"{cpu_player_name} joined the game.")

    # Function to activate wild ones
    def activate_wild_ones(self):
        time.sleep(1)
        print(f"Do you want to activate wild ones mode?")
        while True:
            wild_ones_choice = input("Choose [y]es or [n]\n-- ").lower().strip()
            if wild_ones_choice != "y" and wild_ones_choice != "n":
                print(f"You must type 'y' to choose 'yes' or 'n' for 'no'")
                continue
            break

        self.wild_ones = True if wild_ones_choice == "y" else False

    # Function to calculate all the bets in the game
    def calculate_valid_bets(self):
        # Total count of dice
        dice_count = [player for player in self.all_players for _ in player.hand]
        dice_value = [1, 2, 3, 4, 5, 6]
        # This comprehension will help me to define the valid bets properly
        # For example if there are two players in the game, respectively there will be 10 dice at all
        # When one of the player lost a die, the new round will start with 9 dice
        # So it will be easier to calculate the bets and force players to make a valid bet
        Game.VALID_BETS = [[d_count, d_value] for d_count in range(1, len(dice_count) + 1) for d_value in dice_value]

    # Function to place the player's bet properly
    def game_bet(self):
        if self.check_is_current_player_main():
            while True:
                try:
                    time.sleep(1)
                    main_player_bet = [int(n) for n in input("Place your bet (e.g.: 1 2)\n-- ").split(" ")]
                    self.current_player.place_bet(main_player_bet)
                    # If main player type more than two digits, the first two will be taken as dice count and dice value
                    if len(main_player_bet) > 2:
                        print("The first two numbers are picked as 'dice count' and 'dice value'")
                        break
                    # Prevent main player to type dice value greater than '6', so the game won't throw an error
                    if main_player_bet[1] > 6:
                        print(f"You can't set dice value greater than 6! Die has only six sides")
                    break
                # Prevent main player to type wrong input, so the game won't throw an error
                except ValueError:
                    print("You must type only digits! (e.g.: 1 2)")
                except IndexError:
                    print("You must type exactly two digits! (e.g.: 1 2)")

        else:
            self.current_player.place_bet(Game.VALID_BETS)

    # Function to roll new dice after each round
    def re_roll(self):
        time.sleep(1)
        print("---------- Rolling new dice ----------")
        for player in self.all_players:
            time.sleep(1)
            player.re_roll_dice()
            if player.__class__.__name__ == "MainPlayer":
                print(f"{'Your new dice are' if len(player.hand) > 1 else 'Your new die is'}"
                      f" - {', '.join([str(die) for die in player.hand])}"
                      f"\n--------------------------------------")

    # Check if current player is main player
    def check_is_current_player_main(self):
        if self.current_player.__class__.__name__ == "MainPlayer":
            return True
        # Otherwise None will be returned. So it help me to define the main player's position properly
        return False if self.previous_player.__class__.__name__ == "MainPlayer" else None

    # Function to check if player bet is possible
    def check_is_bet_valid(self):
        # First check if current player is main player
        if self.check_is_current_player_main():
            while True:
                # Force main player to bet "dice count" and "dice value" properly
                if self.current_player.bet not in Game.VALID_BETS:
                    # Force main player to make a higher bet than the last one
                    if self.current_player.bet[0] < Game.VALID_BETS[0][0] or Game.VALID_BETS[0][1] == 6:  # NOT SURE
                        print(f"You must bet dice count greater or equal to {Game.VALID_BETS[0][0]}!")
                    # Force main player to make a higher bet than the last one
                    elif self.current_player.bet[0] == Game.VALID_BETS[0][0] \
                            and self.current_player.bet[1] <= Game.VALID_BETS[0][1]:
                        print(f"You must bet dice value greater than {Game.VALID_BETS[0][1]}!")
                    # Print a message to main player if bet is higher than the last possible bet
                    elif self.current_player.bet[0] > Game.VALID_BETS[-1][0]:
                        print(f"The maximum dice count you can bet is {Game.VALID_BETS[-1][0]}!")

                    self.game_bet()
                    continue

                print(f"\U0001F3B2 Your bet is - {self.current_player.bet[0]}: {self.current_player.bet[1]}")
                break
        # If current player is cpu player
        # For a proper bet by the CPU player I calculate that the player will never place a bet
        # which will be impossible to win.
        # What does it mean? For example if there are 2 players in the game
        # the total dice count will be 10(at some point).
        # So if the player bets ten fours but at least one die in their hand is not four (e.g. "4, 4, 4, 2")
        # and in the best scenario the other player has "4, 4, 4, 4, 4,"
        # the maximum dice count of all the fours in the game will be 9.
        # This is impossible-to-win bet so the CPU player will never bet anything like this
        else:
            while True:
                all_other_dice = len([die for player in self.all_players for die in player.hand]) - len(
                    self.current_player.hand)
                cpu_player_current_bet_count = self.current_player.bet[0]
                cpu_player_current_bet_value = self.current_player.bet[1]
                if self.wild_ones and cpu_player_current_bet_value != 1:
                    max_count_of_bet_value = (self.current_player.hand.count(cpu_player_current_bet_value) +
                                              all_other_dice + self.current_player.hand.count(1))

                else:
                    max_count_of_bet_value = (self.current_player.hand.count(cpu_player_current_bet_value) +
                                              all_other_dice)

                if cpu_player_current_bet_count > max_count_of_bet_value:
                    self.game_bet()
                    continue
                time.sleep(1)
                print(f"\U0001F3B2 {self.current_player.name} bets - "
                      f"{self.current_player.bet[0]}: {self.current_player.bet[1]}")
                break

        # bet_index is needed to define the exact index of player's bet in the list of valid bets
        bet_index = Game.VALID_BETS.index(self.current_player.bet)
        # Slice the valid bets' list to prevent players from betting an invalid bet
        Game.VALID_BETS = Game.VALID_BETS[bet_index + 1:]

    def current_player_decision(self):
        self.current_player.bet_or_liar_decision()
        # And here is the tricky part
        # Cpu player is memorizing who loses a die
        # So he could properly calculate how many dice are in the game at this point, after that -
        # Cpu player will subtract his total dice count and receive the total dice count for the other players
        # It makes sense when cpu player calculates that dice count bet from the previous player is impossible
        # Because cpu player does not have the needed quantity + the other dice count in total could not
        # be equal or less than the previous player dice count bet
        # So the overall bet will not pass and the previous player is definitely a liar
        # For example if there are 2 players in game, respectively there will be 10 dice (at some point) in the game
        # If previous player bet is '6: 2' in the best scenario the previous player has five dice with value '2'
        # and cpu player does not have '2' in his hand (nor wild ones)
        # cpu player immediately knows that this bet is impossible to pass so his decision will be "liar"
        if not self.check_is_current_player_main():
            all_other_dice = len([die for player in self.all_players for die in player.hand]) - len(self.current_player.hand)
            if self.wild_ones and self.previous_player.bet[1] != 1:
                max_count_of_bet_value = (self.current_player.hand.count(self.previous_player.bet[1]) +
                                          all_other_dice + self.current_player.hand.count(1))

            else:
                max_count_of_bet_value = (self.current_player.hand.count(self.previous_player.bet[1]) +
                                          all_other_dice)

            if self.previous_player.bet[0] > max_count_of_bet_value:
                self.current_player.decision = "liar"

    def new_round(self):
        self.calculate_valid_bets()

        while True:
            self.current_player = self.all_players.pop(0)
            self.all_players.append(self.current_player)

            if not self.previous_player:
                self.game_bet()
                self.check_is_bet_valid()

            else:
                if not Game.VALID_BETS:
                    time.sleep(1)
                    print(f"There are no more valid bets!\nThe only decision is 'liar'")
                    break

                self.current_player_decision()
                if self.current_player.decision == "liar":
                    break

                else:
                    self.game_bet()
                    self.check_is_bet_valid()

            self.previous_player = self.all_players[-1]

    def round_summary(self):
        all_dice = [die for player in self.all_players for die in player.hand]
        main_player = [player for player in self.all_players if player.__class__.__name__ == "MainPlayer"]
        bet_dice_count = self.previous_player.bet[0]
        bet_dice_value = self.previous_player.bet[1]
        actual_dice_count = all_dice.count(bet_dice_value)

        if self.wild_ones and bet_dice_value != 1:
            actual_dice_count += all_dice.count(1)
        time.sleep(1)
        print(f"The total count of dice with value '{bet_dice_value}' is {actual_dice_count}")
        if actual_dice_count < bet_dice_count:
            round_loser = self.previous_player
            time.sleep(1)
            print(f"\U0001F534 You lost a die"
                  if self.check_is_current_player_main() is False
                  else f"\U0001F534 {self.previous_player.name} lost a die")

        else:
            round_loser = self.current_player
            time.sleep(1)
            print(f"\U0001F534 You lost a die"
                  if self.check_is_current_player_main() is True
                  else f"\U0001F534 {self.current_player.name} lost a die")

        round_loser.remove_die()
        loser_index = self.all_players.index(round_loser)
        self.all_players.pop(loser_index)
        self.all_players.insert(0, round_loser)
        self.previous_player = None

        for player in self.all_players:
            if len(main_player[0].hand) == 0:
                time.sleep(1)
                print(f"Goodbye! You lost all of your dice!\n Thanks for playing"
                      f"---------- I would love to join Strypes AWESOME team ----------")
                raise SystemExit

            elif len(player.hand) == 0:
                self.all_players.remove(player)
                time.sleep(1)
                print(f"{player.name} doesn't have any dice left\n"
                      f"He was kicked out of the game!")

    def show_all_players_hands(self):
        output_show_hands = ""
        if self.check_is_current_player_main():
            output_show_hands += f"\U0000274C You said {self.previous_player.name} is liar"

        else:
            if self.previous_player.__class__.__name__ == "MainPlayer":
                time.sleep(1)
                output_show_hands += f"\U0000274C {self.current_player.name} said you are liar"
            else:
                time.sleep(1)
                output_show_hands += f"\U0000274C {self.current_player.name} said {self.previous_player.name} is liar"
        output_show_hands += "\n---------- Revealing all dice ----------"

        for player in self.all_players:
            apo = "'s"
            output_show_hands += (f"\n{'Your' if player.__class__.__name__ == 'MainPlayer' else player.name + apo}"
                                  f" {'dice are' if len(player.hand) > 1 else 'die is'}"
                                  f" - {', '.join([str(die) for die in player.hand])}")

        output_show_hands += "\n----------------------------------------"
        time.sleep(1)
        print(output_show_hands)

    def play_game(self):
        print(f"---------- Liar's Dice ----------")
        self.create_main_player()
        self.create_cpu_player()
        self.activate_wild_ones()
        print(f"Your dice are - {', '.join([str(die) for die in self.all_players[0].hand])}")

        while True:
            self.new_round()
            self.show_all_players_hands()
            self.round_summary()

            if len(self.all_players) == 1:
                break

            self.re_roll()

        end_str = ("---------- Congratulations! You win! ----------"
                   f"\nDice left - {', '.join(str(die) for die in self.all_players[0].hand)}"
                   f"\n---------- I would love to join Strypes AWESOME team ----------")
        print(end_str)


a = Game()
a.play_game()
