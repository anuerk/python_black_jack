"""This module does define a game card"""


class Card:
    """A blueprint for a game card """

    def __init__(self, card_type, card_number_string, card_number_int):
        """create a new card deck object.

        Args:
            card_type: the type of the card (diamonds ace of spades cross)
            card_number_string: the number of the card (7, 8, ...... king, ace)
            card_number_int: the integer value of the card
        """
        self._type = card_type
        self._card_number_int = card_number_int
        self._card_number_string = card_number_string

    def __repr__(self):
        """Text representation"""
        name = self.__class__.__name__
        args = (
            f"('{self._type}', '{self._card_number_string}', {self._card_number_int} ) "
        )
        return_string = f"{name}", args
        return str(return_string)

    @property
    def get_card_value(self):
        """returns the integer value of a given card"""
        return self._card_number_int

    @property
    def get_card_string(self):
        """returns a value string of a given card"""
        return self._card_number_string

    @property
    def display_card(self):
        """displays a card for humans"""
        return self._type + " " + self._card_number_string

    def update_value(self, value):
        """updates the integer value of a card. probably used for ace"""
        self._card_number_int = value
        return self
