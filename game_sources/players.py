"""This module does define a game card player"""

from game_sources.hands import Hand


class Player:
    """A blueprint for a game card player"""

    def __init__(self, name, *, dealer=False):
        self._active = True  #
        self._score = 0
        self._dealer = dealer

        if dealer:
            self._name = "Dealer"
            self._bet_available = 1000
            self._bet_current_round = 999999
        else:
            self._bet_available = 1000
            self._bet_current_round = 0
            self._name = name

        self._hand = Hand(self)

    def __repr__(self):
        """Text representation."""
        name = self.__class__.__name__
        return f"{name} ({self._name}, {self._hand})"

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
    def is_active(self):
        """defines if the player is finished"""
        return self._active

    @property
    def is_dealer(self):
        """checks if a given player is a dealer"""
        return self._dealer

    @property
    def get_name(self):
        """returns the current players name"""
        return self._name

    @property
    def get_score(self):
        """returns the current player round score"""
        return self._score

    @property
    def get_hand(self):
        """returns the card hand of a player"""
        return self._hand

    def set_player_mode(self, active):
        """updates the player if he does want more cards"""
        self._active = active

    def update_player_score(self, update_value):
        """updates the current player score of his cards"""
        self._score += update_value

    def reset_round(self):
        """reset the players properties for the current round"""
        self._hand = Hand(self)
        self._active = True
        self._score = 0

    def update_player_bet_rest(self, number):
        """updates the players game bet amount with the round result"""
        self._bet_available -= number

    def set_bet_current_round(self, bet_amount):
        """updates the current bet"""
        self._bet_current_round = bet_amount
