"""This module does define a the hand of a card player"""


class Hand:
    """A blueprint for a player card hand"""

    def __init__(self, player):
        self._active = True  #
        self._cards = []
        self._score = 0
        self._player = player
        self._insurance = False

    def __repr__(self):
        """Text representation."""
        name = self.__class__.__name__
        return f"{name} ({self._player}, {self._cards})"

    def take_card(self, card):
        """player takes a new card from a given deck"""
        self.update_hand_score(card.get_card_value)
        self._cards.append(card)

    @property
    def cards(self):
        """return the current round card of the player"""
        return self._cards

    @property
    def is_active(self):
        """defines if the player is finished"""
        return self._active

    def set_hand_mode(self, active):
        """updates the player if he does want more cards"""
        self._active = active

    def set_insurance(self, param):
        """marker for insurance move from player"""
        self._insurance = param

    @property
    def get_score(self):
        """returns the current player round score"""
        return self._score

    def update_hand_score(self, update_value):
        """updates the current player score of his cards"""
        self._score += update_value

    def display_hand_cards(self):
        """returns the players cards current on his hand"""
        card_list = []
        for card in self._cards:
            card_list.append(card.display_card)
        return card_list

    def split_is_possible(self):
        """check if the cards of the players are equal. needed for split"""
        if (
            self._cards[0].get_card_value == self._cards[1].get_card_value
            and len(self._cards) == 2
        ):
            return True
        return False
