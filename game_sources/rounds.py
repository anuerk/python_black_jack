"""This module does define the logic for a black jack round.
it inherits its settings from a black jack instance"""
from game_sources import Deck


class Round:
    """defines the logic for the black jack round"""

    def __init__(self, players, cards):
        """start a round for the black jack game"""

        print("")
        self._players = players
        self._cards = cards
        self._nearest_score = 0

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
                    a_player.get_hand[0].display_hand_cards(),
                )

        print("")

        for a_player in self._players:
            self._current_player = a_player
            for deck_counter, hand in enumerate(a_player.get_hand):
                if hand.is_active and a_player.is_dealer is False:  # human-player
                    while hand.is_active:
                        print(
                            a_player.get_name,
                            " it is your turn. Current cards: ",
                            hand.display_hand_cards(),
                            sep="",
                        )
                        player_decision = input(
                            "What now? stand, hit, split, double, ..."
                        ).lower()

                        if player_decision == "stand":
                            hand.set_hand_mode(False)
                        elif player_decision == "hit":
                            self._current_player_new_card = (
                                self._cards.take_top_card_from_deck()
                            )

                            # find optimal ace value for player
                            self.check_ace_options(hand)

                            a_player.get_hand[deck_counter].take_card(
                                self._current_player_new_card
                            )

                            print(
                                "\nyou have picked",
                                self._current_player_new_card.display_card,
                            )

                            self.check_busted_hand(hand)
                        elif player_decision == "split":
                            if hand.cards_are_equal():
                                a_player.spilt_hand()
                            else:
                                print("you need to have two cards with the same value. 3 cards are too much")
                        elif player_decision == "double":
                            a_player.set_bet_current_round(
                                a_player.bet_current_round * 2
                            )
                            double_decision = input(
                                "doubled your bet :) also a new card?"
                            ).lower()
                            if double_decision == "yes" or double_decision == "y":
                                self._current_player_new_card = (
                                    self._cards.take_top_card_from_deck()
                                )

                                # find optimal ace value for player
                                self.check_ace_options(hand)

                                a_player.get_hand[deck_counter].take_card(
                                    self._current_player_new_card
                                )

                                print(
                                    "\nyou have picked",
                                    self._current_player_new_card.display_card,
                                )
                            hand.set_hand_mode(False)

                        elif player_decision == "insurance":
                            hand.set_insurance(True)
                            hand.set_bet_current_round(hand.bet_current_round / 2)

                            if hole_card.get_card_string == "ACE":
                                ...
                            else:
                                ...

                            """todo Versicherung (Insurance): Sollte die erste Karte des Dealers ein Ass sein, kann 
                            Der Dealer wird seine Hole-Karte  überprüfen, bevor die
                              Spieler an der Reihe sind. Ist die zweite Karte des Dealers nun eine Zehn oder Bildkarte, 
                              hat er tatsächlich einen Blackjack und die Versicherung wird im Verhältnis 2:1 an den 
                              Spieler ausgezahlt. Hat der Dealer keinen Blackjack, geht der Versicherungsbetrag an die
                               Bank und das Spiel geht normal weiter, ohne dass der Dealer seine zweite Karte vorzeitig 
                               aufdeckt."""

                        print("")

                    if hand.get_score <= 21:
                        if hand.get_score > self._nearest_score:
                            self._nearest_score = hand.get_score

        print("Round over - hole card is", hole_card)

        # dealer must have at least a score of 17
        self.check_dealer_min_val()
        if self._players[0].get_hand[0].get_score <= 21:
            if self._players[0].get_hand[0].get_score > self._nearest_score:
                self._nearest_score = self._players[0].get_hand[0].get_score
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
        a_player.get_hand[0].take_card(new_card)
        return new_card

    def check_ace_options(self, hand):
        """checks player cards for possibility to reduce score"""

        ace_count = 0
        current_player_aces = []

        # find optimal ace value for player
        for current_player_card in hand.cards:
            if "ACE" in current_player_card.get_card_string:
                ace_count += 1
                current_player_aces.append(current_player_card)

        if self._current_player_new_card.get_card_value == 11:
            ace_count += 1

        if (
            ace_count > 0
            and hand.get_score + self._current_player_new_card.get_card_value > 21
        ):
            # problem is the new ace?
            if self._current_player_new_card.get_card_value == 11:
                self._current_player_new_card.update_value(1)

            if hand.get_score + self._current_player_new_card.get_card_value > 21:
                for card in hand.cards:
                    if (
                        card.get_card_value == 11
                        and hand.get_score
                        + self._current_player_new_card.get_card_value
                        > 21
                    ):  # there was already an ace on the players hand
                        card.update_value(1)
                        hand.update_hand_score(-10)

    @classmethod
    def check_busted_hand(cls, a_hand):
        """checks if a players score is above 21
        returns True OR False
        """
        if a_hand.get_score > 21:  # already lost?
            a_hand.set_hand_mode(False)
            print("BUST - over 21")
        else:
            a_hand.set_hand_mode(True)

    def check_dealer_min_val(self):
        """dealer must have at least a score of 17.
        it (we are gender neutral ;)) has to take new card until he reaches a score of 17
        """
        self._current_player = self._players[0]
        while self._players[0].get_hand[0].get_score < 17:
            self._current_player_new_card = self._cards.take_top_card_from_deck()
            self._players[0].get_hand[0].take_card(self._current_player_new_card)
            print("Dealer picked new card:", self._current_player_new_card.display_card)

            if self._players[0].get_hand[0].get_score > 21:
                self.check_ace_options(self._players[0].get_hand[0])

    def calculate_round_winner(self):
        """
        calculates who wins the round
        """
        player_results = []
        push_count = 0
        dealer_busted = False

        for player in self._players:
            for hand in player.get_hand:
                # filter busted players first
                if hand.get_score > 21:
                    if player.get_name == "Dealer":
                        dealer_busted = True
                    player_results.append((player, "LOSE", hand.get_score))
                    player.update_player_bet_rest(player.bet_current_round)
                else:
                    if dealer_busted:
                        player_results.append((player, "WINS", hand.get_score))
                        if self.is_blackjack(player.get_hand[0].cards):
                            player.update_player_bet_rest(player.bet_current_round * -1)
                        else:
                            player.update_player_bet_rest(
                                player.bet_current_round * -1.5
                            )
                    else:
                        if (
                            hand.get_score == self._nearest_score
                            and self._players[0].get_hand[0].get_score
                            != self._nearest_score
                        ):  # player wins and dealer not
                            player_results.append((player, "WINS", hand.get_score))
                            if self.is_blackjack(player.get_hand[0].cards):
                                player.update_player_bet_rest(
                                    player.bet_current_round * -1
                                )
                            else:
                                player.update_player_bet_rest(
                                    player.bet_current_round * -1.5
                                )
                        elif (
                            hand.get_score == self._nearest_score
                            and self._players[0].get_hand[0].get_score
                            == self._nearest_score
                        ):  # player and dealer win
                            player_results.append((player, "PUSH", hand.get_score))
                            player.update_player_bet_rest(0)
                            push_count += 1
                        else:
                            player_results.append((player, "LOSE", hand.get_score))
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
