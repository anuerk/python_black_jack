from game_sources.cards import Card
from game_sources.players import Player
from random import shuffle
import random


class Deck:
    """A one-dimensional vector from linear algebra.

    All entries are stored as float's.
    """

    def __init__(self, *, card_count_total=52):
        # todo : doc string + check für card count durch 4 teilbar
        self._cards = []
        self._card_count_total = card_count_total

        cards_needed = int((card_count_total / 4) + 2)

        for _ in range(2, cards_needed):
            if _ == 11:
                card_value_string = "Jack"
                card_value_int = 10
            elif _ == 12:
                card_value_string = "Dame"
                card_value_int = 10
            elif _ == 13:
                card_value_string = "King"
                card_value_int = 10
            elif _ == 14:
                card_value_string = "Ace"
                card_value_int = 11
            else:
                card_value_int = _
                card_value_string = str(_)

            # problem: bube dame könig -> 10 - ass 1 || 11

            self._cards.append(
                Card("heart ", card_value_string, card_value_int)
            )  # erstellt neue Karte in deck
            self._cards.append(Card("diamonds ", card_value_string, card_value_int))
            self._cards.append(Card("spades", card_value_string, card_value_int))
            self._cards.append(Card("cross", card_value_string, card_value_int))

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, index):  # => implementiert indexing
        try:
            return self._cards[index]
        except IndexError:
            n_entries = len(self)  # dispatcht zur __len__ funktion
            raise IndexError(
                f"the vector has only {n_entries} entries"
            ) from None  # unterdrückt den e

    def mix_deck(self):
        """"""
        # self._cards = shuffle(self._cards)
        shuffle(self._cards)

    def take_top_card_from_deck(self):  # todo nicht random sonder oberste
        """"""
        card_pick = self._cards[0]
        self._cards.remove(card_pick)
        return card_pick
