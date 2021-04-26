from game_sources.cards import Card
from random import shuffle


class Deck:
    """A one-dimensional vector from linear algebra.

    All entries are stored as float's.
    """

    def __init__(self, *, card_count_total=52):
        self._cards = []
        self._card_count_total = card_count_total

        cards_needed = int((card_count_total / 4) + 2)

        for _ in range(2, cards_needed):
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
        shuffle(self._cards)

    def take_top_card_from_deck(self):
        return self._cards.pop()
