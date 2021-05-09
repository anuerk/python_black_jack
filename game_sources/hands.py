"""This module does define a the hand of a card player"""


class Hand:
    """A blueprint for a player card hand"""

    def __init__(self, player):
        self._cards = []
        self._player = player

    def __repr__(self):
        """Text representation."""
        name = self.__class__.__name__
        return f"{name} ({self._player}, {self._cards})"

    def take_card(self, card):
        """player takes a new card from a given deck"""
        self._player.update_player_score(card.get_card_value)
        self._cards.append(card)

    @property
    def cards(self):
        """return the current round card of the player"""
        return self._cards

    def update_player_score(self, update_value):
        """updates the current player score of his cards"""
        self._player.get_score += update_value

    def display_hand_cards(self):
        """returns the players cards current on his hand"""
        card_list = []
        for card in self._cards:
            card_list.append(card.display_card)
        return card_list
