"""This module does define the game logic. it uses players, decks, cards and the game class"""

from game_sources import Player, Deck, Card


class Game:
    """defines the main game logic"""

    def __init__(self):
        """Create a new game.  """
        self._cards = None  # the cards in the game
        self._players = []  # a list of players
        self._game_result = None  # result of the round
        self._current_player_card_set = None  #
        self._current_player_new_card = None
        self._current_player = None
        self._nearest_score = 0

        initial_game = True
        game = True

        while game:
            if initial_game:
                self.start_game_round()
            else:
                self.reset_round_result()

            # general game loop
            self.play_round()

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

    def play_round(self):
        """start a round for the black jack game"""

        print("")

        # create card deck and mix
        self._cards = Deck(card_count_total=52)
        self._cards.mix_deck()

        # first card for all players - public
        for a_player in self._players:
            if a_player.is_dealer is not True:
                self.give_bet(a_player)
                self.user_wants_card(a_player)
            else:
                hole_card = self.user_wants_card(a_player)

        # second card for all players - public
        for a_player in self._players:
            if a_player.is_dealer is True:
                new_card = self.user_wants_card(a_player)
                print_string = "has picked the HOLE CARD and" + new_card.display_card
            else:
                new_card = self.user_wants_card(a_player)
                print_string = "has picked"

            print(
                a_player.get_name,
                print_string,
                a_player.display_hand_cards(),
            )

        print("")

        game_active = True
        while game_active:
            for a_player in self._players:
                self._current_player = a_player
                if a_player.is_active and a_player.is_dealer is False:  # human-player
                    print(
                        a_player.get_name,
                        " it is your turn. Current cards: ",
                        a_player.display_hand_cards(),
                        sep="",
                    )
                    player_decision = input(
                        "Do you want a new card? (yes or no) "
                    ).lower()
                    # currently only Stand or hit
                    if player_decision in ("no", "n"):
                        a_player.set_player_mode(False)
                    elif player_decision in ("yes", "y"):
                        self._current_player_new_card = (
                            self._cards.take_top_card_from_deck()
                        )

                        # find optimal ace value for player
                        self.check_ace_options()

                        a_player.take_card(self._current_player_new_card)

                        print("")
                        print(
                            "you have picked",
                            self._current_player_new_card.display_card,
                        )

                        self.check_busted_player(a_player)
                    print("")

            if self.all_human_players_finished():
                game_active = False

        print("")
        print("Dealer Hole card:", hole_card.display_card)

        # dealer must have at least a score of 17
        self.check_dealer_min_val()

        self._game_result = self.calculate_round_winner(
            [
                {"score": player.get_score, "name": player.get_name}
                for player in self._players
            ]
        )
        self.print_result()

    @property
    def players(self):
        """returns the current game players"""
        return self._players

    def get_player_by_name(self, name):
        """gets a players name an returns the player object"""

        for player in self._players:
            if player.get_name == name:
                return player

        return None  # todo

    def calculate_round_winner(self, players_and_score):
        """
        todo too many lists! too many everything! but it works :)
        """
        dealer_is_busted = False

        dealer_score = players_and_score[0]["score"]
        dealer_has_blackjack = players_and_score[0]["score"] == 21

        list_ordered_by_score = sorted(
            players_and_score, key=lambda k: k["score"], reverse=True
        )
        score_list_filtered = []
        for _ in list_ordered_by_score:
            score_list_filtered.append(_["score"])

        score_list_filtered = [
            score for score in score_list_filtered if score <= 21
        ]  # remove scores to high

        all_players_busted = all(i > 21 for i in score_list_filtered)

        if all_players_busted is False:
            # https://stackoverflow.com/questions/12141150/from-list-of-integers-get-number-closest-to-a-given-value
            self._nearest_score = min(score_list_filtered, key=lambda x: abs(x - 21))

        nearest_hit_count = 0  # multiple players & same score?

        winner_count = 0
        loser_count = 0

        result_list = []
        score_list = []
        name_list = []

        if all_players_busted:
            for item in list_ordered_by_score:
                current_player = self.get_player_by_name(item["name"])
                current_player.update_player_bet_rest(
                    (current_player.bet_current_round * -1)
                )
                list_item = {
                    "score": item["score"],
                    "name": item["name"],
                    "result": "BUST",
                    "bet_result": current_player.bet_available,
                }
                result_list.append(list_item)
        elif dealer_is_busted:
            for item in list_ordered_by_score:
                current_player = self.get_player_by_name(item["name"])

                if item["score"] <= 21 and item["name"] != "Dealer":
                    current_player.update_player_bet_rest(
                        current_player.bet_current_round
                    )
                    result_list.append(
                        {
                            "score": item["score"],
                            "name": item["name"],
                            "result": "WINS",
                            "bet_result": current_player.bet_available,
                        }
                    )
                else:
                    current_player.update_player_bet_rest(
                        current_player.bet_current_round * -1
                    )
                    result_list.append(
                        {
                            "score": item["score"],
                            "name": item["name"],
                            "result": "LOSE",
                            "bet_result": current_player.bet_available,
                        }
                    )
                    loser_count += 1

        elif dealer_has_blackjack:
            for item in list_ordered_by_score:
                score_list.append(item["score"])
                name_list.append(item["name"])

            # do we have a push?
            for score, name in zip(score_list, name_list):
                current_player = self.get_player_by_name(name)
                if score == 21 and name != "Dealer" and score == dealer_score:
                    current_player.update_player_bet_rest(0)
                    result = "PUSH"
                    winner_count += 1
                elif score == 21 and name == "Dealer":
                    current_player.update_player_bet_rest(
                        current_player.bet_current_round
                    )
                    result = "WINS"
                    winner_count += 1
                else:
                    current_player.update_player_bet_rest(
                        (current_player.bet_current_round * -1)
                    )
                    result = "LOSE"
                    loser_count += 1

                result_list.append(
                    {
                        "score": score,
                        "name": name,
                        "result": result,
                        "bet_result": current_player.bet_available,
                    }
                )

        else:  # most probably case
            for item in list_ordered_by_score:
                score_list.append(item["score"])
                name_list.append(item["name"])

            for score, name in zip(score_list, name_list):
                current_player = self.get_player_by_name(name)

                if score > 21:
                    current_player.update_player_bet_rest(
                        (current_player.bet_current_round * -1)
                    )
                    list_item = {
                        "score": score,
                        "name": name,
                        "result": "LOSE",
                        "bet_result": current_player.bet_available,
                    }
                    loser_count += 1
                else:
                    if score == self._nearest_score:
                        current_player.update_player_bet_rest(
                            current_player.bet_current_round
                        )
                        list_item = {
                            "score": score,
                            "name": name,
                            "result": "WINS",
                            "bet_result": current_player.bet_available,
                        }
                        winner_count += 1
                        nearest_hit_count += 1
                    else:
                        current_player.update_player_bet_rest(
                            (current_player.bet_current_round * -1)
                        )
                        list_item = {
                            "score": score,
                            "name": name,
                            "result": "LOSE",
                            "bet_result": current_player.bet_available,
                        }
                        loser_count += 1

                result_list.append(list_item)

        if winner_count > 1:  # happens when players have the same score
            i = 0
            print("multiple winners here")
            if self._nearest_score == 21:
                # blackjack is better than normal 21 todo here was something wrong!
                black_jack_winners = []
                for item in result_list:
                    if item["result"] == "WINS":
                        current_player_cards = self.get_player_cards(
                            a_player_name=item["name"]
                        )
                        self._current_player_card_set = current_player_cards
                        player_has_blackjack = self.is_blackjack()
                        if player_has_blackjack and item["score"] < 22:
                            black_jack_winners.append(item)
                            result_list[i]["result"] = "WINS"
                        else:
                            result_list[i]["result"] = "TODO"
                    else:
                        result_list[i]["result"] = "TODO"

                    i += 1
            elif dealer_score == self._nearest_score:
                for item in result_list:
                    if item["score"] == dealer_score and item["result"] == "WINS":
                        result_list[i]["result"] = "PUSH"
                        current_player = self.get_player_by_name(item["name"])
                        print("players bet amount total:", current_player.bet_available)
                        print(
                            "players bet this round:", current_player.bet_current_round
                        )
                        current_player.update_player_bet_rest(0)

                    i += 1

        return result_list

    def all_human_players_finished(self):
        """checks if all humans are finished"""
        for _ in self._players:
            if _.is_active and _.is_dealer is False:
                return False

        return True

    def is_blackjack(self):
        """check if the cards are a blackjack
        TODO
        """
        total_value = 0
        if (
            len(self._current_player_card_set) == 2
            or len(self._current_player_card_set) == 3
        ):

            for card in self._current_player_card_set:
                if isinstance(card, str):  # could be better todo
                    tmp_card = card.split()
                    card = Card(tmp_card[0], tmp_card[1], tmp_card[1])
                total_value += card.get_card_value

            if (
                self._current_player_card_set[0].get_card_value == 7
                and self._current_player_card_set[1].get_card_value == 7
                and self._current_player_card_set[2].get_card_value == 7
            ) or (total_value == 21 and len(self._current_player_card_set) == 2):
                # print("debug: is_blackjack TRUE")
                return True

        # print("debug: is_blackjack FALSE")
        return False

    def print_result(self):
        """gets a list with players: score, name, result
        and prints it
        """

        print("")
        print(
            "|------------------------------------------------------------------------|"
        )
        print(
            "|                ROUND OVER                                              |"
        )
        print(
            "|________________________________________________________________________|"
        )
        print(
            "|    Name                       |   Result   |   Score   |  Bet account  |"
        )
        print(
            "|------------------------------------------------------------------------|"
        )

        for player in self._game_result:

            if player["name"] != "Dealer":
                print(
                    "|  ",
                    "{0: <27}".format(player["name"]),
                    "|   ",
                    "{0: <8}".format(player["score"]),
                    "|   ",
                    "{0: <5}".format(player["result"]),
                    "|   ",
                    "{0: <5}".format(player["bet_result"]),
                    "     |",
                )
            else:
                print(
                    "|  ",
                    "{0: <27}".format(player["name"]),
                    "|   ",
                    "{0: <8}".format(player["score"]),
                    "|   ",
                    "{0: <5}".format(player["result"]),
                    "|",
                    "              |",
                )
        print(
            "|------------------------------------------------------------------------|"
        )

        print("")

    def check_ace_options(self):
        """checks player cards for possibility to reduce score"""

        ace_count = 0
        current_player_aces = []

        # find optimal ace value for player
        for current_player_card in self._current_player.cards:
            if "ACE" in current_player_card.get_card_string:
                ace_count += 1
                current_player_aces.append(current_player_card)

        if self._current_player_new_card.get_card_value == 11:
            ace_count += 1

        if (
            ace_count > 0
            and self._current_player.get_score
            + self._current_player_new_card.get_card_value
            > 21
        ):
            # problem is the new ace?
            if self._current_player_new_card.get_card_value == 11:
                self._current_player_new_card.update_value(1)

            if (
                self._current_player.get_score
                + self._current_player_new_card.get_card_value
                > 21
            ):
                for card in self._current_player.cards:
                    if (
                        card.get_card_value == 11
                        and self._current_player.get_score
                        + self._current_player_new_card.get_card_value
                        > 21
                    ):  # there was already an ace on the players hand
                        card.update_value(1)
                        self._current_player.update_player_score(-10)

    def get_player_cards(self, *, a_player_name):
        """returns the current card deck from a player"""
        player = self.get_player_by_name(a_player_name)
        return player.cards

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

    @classmethod
    def give_bet(cls, a_player):
        """displays player score inputs players bet amount"""
        players_bet = int(
            input(
                a_player.get_name
                + " it is your turn. still available: "
                + str(a_player.bet_available)
                + ". How much is your bet?"
            )
        )

        a_player.set_bet_current_round(players_bet)

    def user_wants_card(self, a_player):
        """takes a card from the deck and gives it to a given player"""
        new_card = self._cards.take_top_card_from_deck()
        a_player.take_card(new_card)
        return new_card

    @classmethod
    def check_busted_player(cls, a_player):
        """checks if a players score is above 21
        returns True OR False
        """
        if a_player.get_score > 21:  # already lost?
            a_player.set_player_mode(False)
            print("BUST - over 21")
        else:
            a_player.set_player_mode(True)

    def check_dealer_min_val(self):
        """dealer must have at least a score of 17.
        it (we are gender neutral ;)) has to take new card until he reaches a score of 17
        """
        self._current_player = self._players[0]
        while self._players[0].get_score < 17:
            self._current_player_new_card = self._cards.take_top_card_from_deck()
            self._players[0].take_card(self._current_player_new_card)
            print("Dealer picked new card:", self._current_player_new_card.display_card)

            if self._players[0].get_score > 21:
                self.check_ace_options()
