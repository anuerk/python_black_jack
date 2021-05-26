"""This module does define a game card player"""

from game_sources.hands import Hand


class Player:
    """A blueprint for a game card player"""

    def __init__(self, name, *, dealer=False):
        self._dealer = dealer

        if dealer:
            self._name = "Dealer"
            self._bet_available = 1000
            self._bet_current_round = 999999
        else:
            self._bet_available = 1000
            self._bet_current_round = 0
            self._name = name

        self._hand = []
        self._hand.append(Hand(self))

    def __repr__(self):
        """Text representation."""
        name = self.__class__.__name__
        return f"{name} ({self._name}, {self._hand})"

    def __repr__(self):
        """Text representation"""
        name = self.__class__.__name__
        args = repr(self._name) + repr(self._name) + repr(self._dealer)
        return f"{name}({args})"

    @property
    def bet_available(self):
        """returns the current players available bet amount"""
        return self._bet_available

    @property
    def bet_current_round(self):
        """returns the current players available bet amount"""
        return self._bet_current_round

    @property
    def cards(self):
        """return the current round card of the player"""
        return self._hand

    @property
    def is_dealer(self):
        """checks if a given player is a dealer"""
        return self._dealer

    @property
    def get_name(self):
        """returns the current players name"""
        return self._name

    @property
    def get_hand(self):
        """returns the card hand of a player"""
        return self._hand

    def reset_round(self):
        """reset the players properties for the current round"""
        self._hand = []
        self._hand.append(Hand(self))

    def update_player_bet_rest(self, number):
        """updates the players game bet amount with the round result"""
        self._bet_available -= number

    def set_bet_current_round(self, bet_amount):
        """updates the current bet"""
        self._bet_current_round = bet_amount

    def spilt_hand(self):
        """splits the players hand to two hands"""
        # add a new hand with one card from the other hand
        self.update_player_bet_rest(self.bet_current_round * 2)

        self._hand.append(Hand(self))
        self._hand[1].cards.append(self._hand[0].cards[0])

        # also split the score
        score_from_old_hand = self._hand[0].get_score / 2
        self._hand[0].update_hand_score(-1 * score_from_old_hand)
        self._hand[1].update_hand_score(score_from_old_hand)

        # and remove the card from the other hand
        del self._hand[0].cards[0]
