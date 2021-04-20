class Player:
    """A game card player"""

    def __init__(self, name, *, dealer=False):
        self._cards = []
        self._order = None
        self._active = True  #
        self._score = 0
        self._dealer = dealer
        if dealer:
            self._name = "Dealer"
        else:
            self._name = name

    def __repr__(self):
        """Text representation."""
        name = self.__class__.__name__
        return f"{name} ({self._name}, {self._cards})"

    def take_card(self, card):
        self.update_player_score(card.get_card_value)
        self._cards.append(card)

    @property  # erstellt ein read-only Attribu
    def cards(self):
        return self._cards

    @property
    def is_active(self):
        """defines if the player is finished"""
        return self._active

    @property
    def is_dealer(self):
        return self._dealer

    @property
    def get_name(self):
        return self._name

    @property
    def get_score(self):
        return self._score

    def set_player_mode(self, active):
        self._active = active

    def update_player_score(self, update_value):
        """"""
        self._score += update_value
        
    def display_hand_cards(self):
        """todo"""
        card_list = []
        for card in self._cards:
            card_list.append(card.display_card)
        return list(card_list)
       
