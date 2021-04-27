class Player:
    """A game card player"""

    def __init__(self, name, *, dealer=False, stake=0):
        self._cards = []
        self._order = None
        self._active = True  #
        self._score = 0
        self._dealer = dealer
        self._stakes = stake

        if dealer:
            self._name = "Dealer"
            self._bet_available = 1000
            self._bet_current_round = 999999
        else:
            self._bet_available = 1000
            self._bet_current_round = 0
            self._name = name

    def __repr__(self):
        """Text representation."""
        name = self.__class__.__name__
        return f"{name} ({self._name}, {self._cards})"

    def take_card(self, card):
        self.update_player_score(card.get_card_value)
        self._cards.append(card)

    @property
    def bet_available(self):
        return self._bet_available

    @property
    def bet_current_round(self):
        return self._bet_current_round

    @property
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
        """returns the players cards current on his hand"""
        card_list = []
        for card in self._cards:
            card_list.append(card.display_card)
        return card_list

    def reset_round(self):
        self._cards = []
        self._active = True
        self._score = 0

    def update_player_bet_rest(self, number):
        print("debug update_player_bet_rest")
        print(self.get_name)
        print("bevore", self._bet_available)
        self._bet_available += number
        print("geändert um", number)
        print("after", self._bet_available)