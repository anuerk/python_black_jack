"""This module does define a card deck for a black jack game"""

from random import shuffle
from game_sources.cards import Card


class Deck:
    """A blueprint for a game card deck"""

    def __init__(self, *, deck_count=1):
        self._cards = []

        for _ in range(0, deck_count):
            for _ in range(2, 15):
                if _ == 11:
                    card_string = "JACK"
                    card_int = 10
                elif _ == 12:
                    card_string = "QUEEN"
                    card_int = 10
                elif _ == 13:
                    card_string = "KING"
                    card_int = 10
                elif _ == 14:
                    card_string = "ACE"
                    card_int = 11
                else:
                    card_int = _
                    card_string = str(_)

                self._cards.append(Card("HEART", card_string, card_int))
                self._cards.append(Card("TILE", card_string, card_int))
                self._cards.append(Card("PIKE", card_string, card_int))
                self._cards.append(Card("CLOVER", card_string, card_int))

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, index):
        try:
            return self._cards[index]
        except IndexError:
            n_cards = len(self)
            raise IndexError(f"the deck has only {n_cards} cards") from None

    def mix_deck(self):
        """mixes a given card deck"""
        shuffle(self._cards)

    def take_top_card_from_deck(self):
        """returns the first card from a deck of cards"""
        return self._cards.pop()
