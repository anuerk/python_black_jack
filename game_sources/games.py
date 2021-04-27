from game_sources import Player, Deck, Card


class Game:
    def __init__(self):
        """Create a new game.  """
        self._cards = None
        self._players = None

        print("")

        incorrect_human_input = True
        player_count = 0
        while incorrect_human_input:
            try:
                player_count = int(input("How many people want to play? "))
                if player_count < 1 or player_count > 7:
                    print("Please insert a number (1 - 7)")
                else:
                    incorrect_human_input = False
            except ValueError:
                print("Please insert a number (1 - 7)")

        # initialise players
        players = [Player("Dealer", dealer=True)]

        for _ in range(0, player_count):
            incorrect_human_input = True
            while incorrect_human_input:
                player_name = input("Please insert player name: ")
                if player_name == "" or player_name == "Dealer":
                    print("Name is not allowed")
                else:
                    players.append(Player(player_name))
                    incorrect_human_input = False

        # create card deck and mix
        print("")
        self._players = players
        game_cards = Deck(card_count_total=52)
        game_cards.mix_deck()

        self._players = players
        self._cards = game_cards

        # first card for all players - public
        for a_player in players:
            if a_player.is_dealer is True:
                hole_card = game_cards.take_top_card_from_deck()
                a_player.take_card(hole_card)
            else:
                new_card = game_cards.take_top_card_from_deck()
                a_player.take_card(new_card)

        # second card for all players - public
        for a_player in players:
            if a_player.is_dealer is True:
                new_card = game_cards.take_top_card_from_deck()
                a_player.take_card(new_card)
                print(
                    a_player.get_name,
                    "has picked the HOLE CARD and",
                    new_card.display_card,
                )
            else:
                new_card = game_cards.take_top_card_from_deck()
                a_player.take_card(new_card)
                print(
                    a_player.get_name,
                    "has picked",
                    a_player.display_hand_cards(),
                )

        print("")

        game_active = True
        while game_active:
            for a_player in players:

                if a_player.is_active and a_player.is_dealer is False:  # human-player
                    print(
                        a_player.get_name,
                        " it is your turn. Current cards: ",
                        a_player.display_hand_cards(),
                        sep="",
                    )
                    player_decision = input(
                        "Do you want a new card? (yes or no) "
                    ).lower()
                    # currently only Stand or hit
                    if player_decision == "no" or player_decision == "n":
                        a_player.set_player_mode(False)
                    elif player_decision == "yes" or player_decision == "y":
                        new_card = game_cards.take_top_card_from_deck()

                        # find optimal ace value for player
                        self.check_ace_options(a_player, new_card)

                        a_player.take_card(new_card)

                        print("")
                        print("you have picked", new_card.display_card)

                    if a_player.get_score > 21:  # already lost?
                        a_player.set_player_mode(False)

                        if a_player.get_score > 21:
                            print("BUST - over 21")
                        else:
                            a_player.set_player_mode(True)

                    print("")

            if self.all_human_players_finished(players):
                game_active = False

        print("")
        print("Dealer Hole card:", hole_card.display_card)

        # dealer must have at least a score of 17
        while players[0].get_score < 17:
            new_card = game_cards.take_top_card_from_deck()
            players[0].take_card(new_card)
            print("Dealer picked new card:", new_card.display_card)

            if players[0].get_score > 21:
                self.check_ace_options(players[0], new_card)

        game_result = self.calculate_round_winner(
            [{"score": player.get_score, "name": player.get_name} for player in players]
        )
        self.print_result(game_result)

    @property
    def players(self):
        return self._players

    def get_player_by_name(self, name):
        for _ in self._players:
            if _.get_name == name:
                return _

    def calculate_round_winner(self, players_and_score):
        """
        todo too many lists!
        """
        dealer_is_busted = False
        dealer_has_blackjack = False
        dealer_score = players_and_score[0]["score"]
        if dealer_score > 21:
            dealer_is_busted = True
        elif dealer_score == 21:

            dealer_has_blackjack = True
        # dealer gets special treatment

        list_ordered_by_score = sorted(
            players_and_score, key=lambda k: k["score"], reverse=True
        )
        score_list_filtered = []
        for _ in list_ordered_by_score:
            score_list_filtered.append(_["score"])

        score_list_filtered = [
            score for score in score_list_filtered if score <= 21
        ]  # remove scores to high

        all_players_busted = all(i > 21 for i in score_list_filtered)

        if all_players_busted is False:
            # https://stackoverflow.com/questions/12141150/from-list-of-integers-get-number-closest-to-a-given-value
            nearest_score = min(score_list_filtered, key=lambda x: abs(x - 21))

        nearest_hit_count = 0  # multiple players & same score?

        winner_count = 0
        loser_count = 0

        result_list = []
        score_list = []
        name_list = []
        player_result = []

        if all_players_busted:
            for item in list_ordered_by_score:
                list_item = {
                    "score": item["score"],
                    "name": item["name"],
                    "result": "BUST",
                }
                result_list.append(list_item)
        elif dealer_is_busted:
            for item in list_ordered_by_score:
                if item["score"] <= 21 and item["name"] != "Dealer":
                    score_list.append(item["score"])
                    name_list.append(item["name"])
                    player_result.append("WINS")
                    winner_count += 1
                else:
                    score_list.append(item["score"])
                    name_list.append(item["name"])
                    player_result.append("LOSE")
                    loser_count += 1

            for score, name, z in zip(score_list, name_list, player_result):
                result_list.append({"score": score, "name": name, "result": z})

        elif dealer_has_blackjack:
            for item in list_ordered_by_score:
                score_list.append(item["score"])
                name_list.append(item["name"])

            # do we have a push?
            for score, name in zip(score_list, name_list):
                if score == 21 and name != "Dealer" and score == dealer_score:
                    result_list.append({"score": score, "name": name, "result": "PUSH"})
                    winner_count += 1
                elif score == 21 and name == "Dealer":
                    result_list.append({"score": score, "name": name, "result": "WINS"})
                    winner_count += 1
                else:
                    result_list.append({"score": score, "name": name, "result": "LOSE"})
                    loser_count += 1

        else:  # most probably case
            for item in list_ordered_by_score:
                score_list.append(item["score"])
                name_list.append(item["name"])

            for score, name in zip(score_list, name_list):
                if score > 21:
                    list_item = {"score": score, "name": name, "result": "LOSE"}
                    loser_count += 1
                else:
                    if score == nearest_score:
                        list_item = {"score": score, "name": name, "result": "WINS"}
                        winner_count += 1
                        nearest_hit_count += 1
                    else:
                        list_item = {"score": score, "name": name, "result": "LOSE"}
                        loser_count += 1

                result_list.append(list_item)

        if winner_count > 1:  # happens when players have the same score
            i = 0

            if nearest_score == 21:
                # blackjack is better than normal 21
                black_jack_winners = []
                for item in result_list:
                    if item["result"] == "WINS":
                        current_player_cards = self.get_player_cards(
                            a_player_name=item["name"]
                        )
                        player_has_blackjack = self.is_blackjack(current_player_cards)
                        if player_has_blackjack and item["score"] < 22:
                            black_jack_winners.append(item)
                            result_list[i]["result"] = "WINS"
                        else:
                            result_list[i]["result"] = "LOSE"
                    else:
                        result_list[i]["result"] = "LOSE"

                    i += 1
            elif dealer_score == nearest_score:
                for item in result_list:
                    if item["score"] == dealer_score and item["result"] == "WINS":
                        result_list[i]["result"] = "PUSH"
                    i += 1

        return result_list

    def all_human_players_finished(self, human_player_list):
        for _ in human_player_list:
            if _.is_active and _.is_dealer is False:
                return False

        return True

    def is_blackjack(self, card_set):
        """check if the cards are a blackjack"""
        total_value = 0
        if len(card_set) == 2 or len(card_set) == 3:

            for card in card_set:
                if isinstance(card, str):  # could be better todo
                    tmp_card = card.split()
                    card = Card(tmp_card[0], tmp_card[1], tmp_card[1])
                total_value += card.get_card_value

            if (
                card_set[0].get_card_value == 7
                and card_set[1].get_card_value == 7
                and card_set[2].get_card_value == 7
            ) or (total_value == 21 and len(card_set) == 2):
                return True

        return False

    def print_result(self, game_result):  # ide hint should be static? todo
        """gets a list with players: score, name, result
        and prints it
        """
        print("")
        print("|¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯|")
        print("|                ROUND OVER                                  |")
        print("|____________________________________________________________|")
        print("|    Name                       |       Result   |   Score   |")
        print("|¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯|")
        for player in game_result:
            print(
                "|  ",
                "{0: <27}".format(player["name"]),
                "|   ",
                "{0: <11}".format(player["score"]),
                "|    ",
                "{0: <5}".format(player["result"]),
                "|",
            )
        print("|____________________________________________________________|")
        print("")

    def check_ace_options(self, xy_player, new_card):
        """checks player cards for possibility to reduce score"""

        new_card = new_card
        current_player = xy_player
        ace_count = 0
        current_player_aces = []

        # find optimal ace value for player
        for current_player_card in current_player.cards:
            if "ACE" in current_player_card.get_card_string:
                ace_count += 1
                current_player_aces.append(current_player_card)

        if new_card.get_card_value == 11:
            ace_count += 1

        if ace_count > 0 and current_player.get_score + new_card.get_card_value > 21:
            # problem is the new ace?
            if new_card.get_card_value == 11:
                new_card.update_value(1)

            if current_player.get_score + new_card.get_card_value > 21:
                for card in current_player.cards:
                    if (
                        card.get_card_value == 11
                        and current_player.get_score + new_card.get_card_value > 21
                    ):  # there was already an ace on the players hand
                        card.update_value(1)
                        current_player.update_player_score(-10)

    def get_player_cards(self, *, a_player_name):
        player = self.get_player_by_name(a_player_name)
        return player.cards
