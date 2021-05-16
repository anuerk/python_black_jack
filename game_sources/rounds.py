"""This module does define the logic for a black jack round.
it inherits its settings from a black jack instance"""
from game_sources import Deck


class Round:
    """defines the logic for the black jack round"""

    def __init__(self, players, cards):
        """start a round for the black jack game"""

        self._players = players
        self._cards = cards
        self._nearest_score = 0

        print("")

        # create card deck and mix
        self._cards = Deck(deck_count=6)
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
                print(
                    a_player.get_name,
                    "has picked the HOLE CARD and",
                    new_card.display_card,
                )
            else:
                self.user_wants_card(a_player)

                print(
                    a_player.get_name,
                    "has picked",
                    a_player.get_hand.display_hand_cards(),
                )

        print("")

        for a_player in self._players:
            self._current_player = a_player
            if a_player.is_active and a_player.is_dealer is False:  # human-player
                while a_player.is_active:
                    print(
                        a_player.get_name,
                        " it is your turn. Current cards: ",
                        a_player.get_hand.display_hand_cards(),
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

                        a_player.get_hand.take_card(self._current_player_new_card)

                        print("")
                        print(
                            "you have picked",
                            self._current_player_new_card.display_card,
                        )

                        self.check_busted_player(a_player)
                    print("")

                if a_player.get_score <= 21:
                    if a_player.get_score > self._nearest_score:
                        self._nearest_score = a_player.get_score

        print("")
        print("Dealer Hole card:", hole_card.display_card)

        # dealer must have at least a score of 17
        self.check_dealer_min_val()
        if self._players[0].get_score <= 21:
            if self._players[0].get_score > self._nearest_score:
                print("debug dealer has nearest score alone")
                self._nearest_score = self._players[0].get_score
        self._game_result = self.calculate_round_winner()

        self.print_result()

    @classmethod
    def give_bet(cls, a_player):
        """displays player score inputs players bet amount"""
        incorrect_human_input = True
        players_bet = 0
        while incorrect_human_input:
            try:
                players_bet = int(
                    input(
                        a_player.get_name
                        + " it is your turn. still available: "
                        + str(a_player.bet_available)
                        + ". How much is your bet?"
                    )
                )
                incorrect_human_input = False
            except ValueError:
                print("Please insert a number")

        a_player.set_bet_current_round(players_bet)

    def user_wants_card(self, a_player):
        """takes a card from the deck and gives it to a given player"""
        new_card = self._cards.take_top_card_from_deck()
        a_player.get_hand.take_card(new_card)
        return new_card

    def check_ace_options(self):
        """checks player cards for possibility to reduce score"""

        ace_count = 0
        current_player_aces = []

        # find optimal ace value for player
        for current_player_card in self._current_player.get_hand.cards:
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
                for card in self._current_player.get_hand.cards:
                    if (
                        card.get_card_value == 11
                        and self._current_player.get_score
                        + self._current_player_new_card.get_card_value
                        > 21
                    ):  # there was already an ace on the players hand
                        card.update_value(1)
                        self._current_player.update_player_score(-10)

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
            self._players[0].get_hand.take_card(self._current_player_new_card)
            print("Dealer picked new card:", self._current_player_new_card.display_card)

            if self._players[0].get_score > 21:
                self.check_ace_options()

    def calculate_round_winner(self):
        """
        calculates who wins the round
        """
        player_results = []
        push_count = 0
        dealer_busted = False

        for player in self._players:
            # filter busted players first
            if player.get_score > 21:
                if player.get_name == "Dealer":
                    dealer_busted = True
                player_results.append((player, "LOSE", player.get_score))
                player.update_player_bet_rest(player.bet_current_round)
            else:
                if dealer_busted:
                    player_results.append((player, "WINS", player.get_score))
                    if self.is_blackjack(player.get_hand.cards):
                        player.update_player_bet_rest(player.bet_current_round * -1)
                    else:
                        player.update_player_bet_rest(player.bet_current_round * -1.5)
                else:
                    if (
                        player.get_score == self._nearest_score
                        and self._players[0].get_score != self._nearest_score
                    ):  # player wins and dealer not
                        player_results.append((player, "WINS", player.get_score))
                        if self.is_blackjack(player.get_hand.cards):
                            player.update_player_bet_rest(player.bet_current_round * -1)
                        else:
                            player.update_player_bet_rest(
                                player.bet_current_round * -1.5
                            )
                    elif (
                        player.get_score == self._nearest_score
                        and self._players[0].get_score == self._nearest_score
                    ):  # player and dealer win
                        player_results.append((player, "PUSH", player.get_score))
                        player.update_player_bet_rest(0)
                        push_count += 1
                    else:
                        print("debug", player.get_score, player.get_name)
                        player_results.append((player, "LOSE", player.get_score))
                        player.update_player_bet_rest(player.bet_current_round)

        if push_count == 1:
            # if dealer has the nearest score alone, he is the winner
            player_results.append((player_results[0][0], "WINS", player_results[0][2]))
            player_results.pop(0)

        return player_results

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
            if player[0].get_name != "Dealer":
                print(
                    "|  ",
                    "{0: <27}".format(player[0].get_name),
                    "|   ",
                    "{0: <8}".format(player[2]),
                    "|   ",
                    "{0: <5}".format(player[1]),
                    "|   ",
                    "{0: <5}".format(int(player[0].bet_available)),
                    "     |",
                )
            else:
                print(
                    "|  ",
                    "{0: <27}".format(player[0].get_name),
                    "|   ",
                    "{0: <8}".format(player[2]),
                    "|   ",
                    "{0: <5}".format(player[1]),
                    "|",
                    "              |",
                )
        print(
            "|------------------------------------------------------------------------|"
        )

        print("")

    @classmethod
    def is_blackjack(cls, a_card_set):
        """check if the cards are a blackjack"""
        total_value = 0
        for card in a_card_set:
            total_value += card.get_card_value

        if len(a_card_set) == 2 or len(a_card_set) == 3:
            if (
                a_card_set[0].get_card_value == 7
                and a_card_set[1].get_card_value == 7
                and a_card_set[2].get_card_value == 7
            ) or (total_value == 21 and len(a_card_set) == 2):
                return True
        return False
