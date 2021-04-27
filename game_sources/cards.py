class Card:
    """a game card
    All entries are stored as float's
    """

    def __init__(self, card_type, card_number_string, card_number_int):
        """create a new card deck object.

        Args:
            card_type: the type of the card (diamonds ace of spades cross)
            card_number_string: the number of the card (7, 8, ...... king, ace)
            card_number_int: the integer value of the card
        """
        self._type = card_type
        # self._number = (card_number_int, card_number_string)
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
        return self._card_number_int

    @property
    def get_card_string(self):
        return self._card_number_string

    @property
    def display_card(self):
        return self._type + " " + self._card_number_string

    def update_value(self, value):
        self._card_number_int = value
        return self
