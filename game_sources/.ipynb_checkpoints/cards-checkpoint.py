class Card:
    """a game card
    All entries are stored as float's
    """

    def __init__(self, card_type, card_number_string, card_number_int):
        """create a new matrix object.

        Args:
            type: the type of the card (diamonds ace of spades cross)
            number: the number of the card (7, 8, ...... king, ace)
            todo
        """
        self._type = card_type
        # self._number = (card_number_int, card_number_string)
        self._card_number_int = card_number_int
        self._card_number_string = card_number_string  # todo

    def __repr__(self):  # Addressat kann auch ein Log-File sein
        """Text representation"""
        name = self.__class__.__name__
        # args = repr(self._type + " " + self._number)
        return f"{name} ({self._type}, {self._card_number_string}, {self._card_number_int} )  todo"

    @property
    def get_card_value(self):
        """"""
        return self._card_number_int

    @property
    def get_card_string(self):
        """"""
        return self._card_number_string
    
    @property
    def display_card(self):
        """"""
        return self._type + " " + self._card_number_string

    def update_value(self, value):  # currently not used
        """"""
        self.card_value_int = value

    def ace_one_value(self):  # currently not used
        """updates the value of ace - 11 to ace - 1
        """
        self._card_value_int = 1
        self._card_number_string = "ACE_1"
