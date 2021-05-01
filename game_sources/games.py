"""This module does define the game logic. it uses players, decks, cards and the game class"""
from game_sources import Player, Round


class Game:
    """defines the main game logic"""

    def __init__(self):
        """Create a new game.  """
        self._cards = None  # the cards in the game
        self._players = []  # a list of players
        self._game_result = None  # result of the round
        self._current_player_card_set = []  #
        self._current_player_new_card = None
        self._current_player = None

        initial_game = True
        game = True

        while game:
            if initial_game:
                self.start_game_round()
            else:
                self.reset_round_result()

            # general game loop
            Round(self._players, self._cards)

            y_or_n = input("Game over - new round? (yes or no)")
            if y_or_n in ("no", "n"):
                game = False

            initial_game = False

    @staticmethod
    def print_rules():
        """just prints the black jack rules"""
        print(
            "\n"
            + "Black jack Rules:\n\n"
            + "Starting value: $ 1000 \n\n"
            + "Card values:\n\n"
            + "Numbers: numerical value, 2-9 points\n"
            + "Jack, queen, king: 10 points\n"
            + "Ace: 1 or 11 points\n\n"
            + "Aim:\n\n"
            + "The object of the game is to reach 21 points or to be closer to 21 than the dealer. "
            + "If the 21 is exceeded, you have overbought and lose your stake. "
            + "If you are closer to 21 than the dealer you get double your stake, "
            + "with a blackjack you get back 2.5 times. In the event of a tie, "
            + "everyone receives their stake again.\nHave fun!\n"
        )

    def start_game_round(self):
        """initialize the black jack game"""
        print("Welcome to 21, Black Jack!")
        user_input = input(
            "Would you like to read the game and program instructions? (yes or no) "
        )

        if user_input in ("yes", "y"):
            self.print_rules()

        while user_input == "":
            user_input = input("You did not enter Anything. How is your answer? ")
            if user_input == "yes":
                self.print_rules()

        self.define_player()

    def reset_round_result(self):
        """resets all round properties of the game"""
        self._cards = None
        self._game_result = None
        self._current_player_card_set = None
        self._current_player_new_card = None
        self._current_player = None
        self._nearest_score = 0

        # reset player properties
        for a_player in self._players:
            a_player.reset_round()

    @property
    def players(self):
        """returns the current game players"""
        return self._players

    def get_player_by_name(self, name):
        """gets a players name an returns the player object"""

        for player in self._players:
            if player.get_name == name:
                return player

        return None

    def define_player(self):
        """sets the game players - dealer inclusive"""
        incorrect_human_input = True
        player_count = 0
        while incorrect_human_input:
            try:
                player_count = int(input("How many people want to play? "))
                if player_count < 1 or player_count > 7:
                    print("Please insert a number (1 - 7)")
                else:
                    incorrect_human_input = False
            except ValueError:
                print("Please insert a number (1 - 7)")

        # add dealer first
        self._players = [Player("Dealer", dealer=True)]

        for _ in range(0, player_count):
            incorrect_human_input = True
            while incorrect_human_input:
                player_name = input("Please insert player name: ")
                if player_name in ("", "Dealer"):
                    print("Name is not allowed")
                else:
                    self._players.append(Player(player_name))
                    incorrect_human_input = False
