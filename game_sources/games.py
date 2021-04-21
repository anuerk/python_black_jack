from game_sources import Player, Deck, Card


class Game:
    def __init__(self, *, game="BlackJack"):
        """Create a new game.  """
        if game == "BlackJack":  # maybe more will come
            self.black_jack()

    @classmethod
    def black_jack(cls, ):
        """logic for a black jack game
        todo!
        """
        print("")
        
        incorrect_human_input = True
        while incorrect_human_input:
            try:
                player_count = int(input("How many people want to play? "))
                if player_count < 1 or  player_count > 7:
                    print("Please insert a number (1 - 7)")
                else:
                    incorrect_human_input = False    
            except ValueError:
                print("Please insert a number (1 - 7)")
                
                
        
        # initialise players
        players = []
        players.append(Player("Dealer", dealer=True))

        for _ in range(0, player_count):
            incorrect_human_input = True
            while incorrect_human_input:
                player_name = input("Please insert player name: ")
                if player_name == "" or player_name == "Dealer":
                    print("Name is not allowd")
                else:
                    players.append(Player(player_name))
                    incorrect_human_input = False    

        # create card deck and mix
        print("")
        game_cards = Deck(card_count_total=52)
        game_cards.mix_deck()

        cls._players = players
        cls._cards = game_cards

        # first card for all players - public
        for current_player in players:
            new_card = game_cards.take_top_card_from_deck()
            current_player.take_card(new_card)
            print(current_player.get_name, "has picked the HOLE CARD and", new_card.display_card)

        # second card for all players - public
        for current_player in players:
            new_card = game_cards.take_top_card_from_deck()
            current_player.take_card(new_card)
            print(current_player.get_name, "has picked the HOLE CARD and", new_card.display_card)

        print("")
        
        game_active = True
        while game_active:
            for current_player in players:
                if (
                    current_player.is_active and current_player.is_dealer == False
                ):  # human player logic
                    print(
                        current_player.get_name,
                        " it is your turn. Current cards: ",
                        current_player.display_hand_cards(),
                        sep="",
                    )  # todo: hide current cards for unauthorized user and display "nice" values
                    player_decision = input(
                        "Do you want a new card? (yes or no) "
                    ).lower()  # todo: maybe cursiv text in brackets
                    # currently only Stand or hit - todo spilt double Insurance
                    if player_decision == "no" or player_decision == "n":
                        current_player.set_player_mode(False)
                    elif player_decision == "yes" or player_decision == "y":
                        new_card = game_cards.take_top_card_from_deck()
                        current_player.take_card(new_card)
                        print("")
                        print("you have picked", new_card.display_card)  # todo visualisation of card
                        print("")
                    if current_player.get_score > 21:  # already lost?
                        current_player.set_player_mode(False)
                        
                        for current_player_card in current_player.cards:  # todo list comprehensino
                            if current_player_card.get_card_string == "ACE":  # todo problem. zieht es halt immer mehrmals ab :()                           
                                current_player.update_player_score(-10)
                                print("debug: ace reduction for player :) new score:", current_player.get_score)
                        
                        if current_player.get_score > 21:
                            print("over 21 - BUST ")
                        else:
                            current_player.set_player_mode(True)
                            
            # do we need a new round?
            if cls.all_human_players_finished():
                game_active = False

        print("")
        #dealer must have at least a score of 17        
        while players[0].get_score < 17:
            new_card = game_cards.take_top_card_from_deck()
            players[0].take_card(new_card)
            print("dealer picked new card", new_card.display_card)
        
            if players[0].get_score > 21: 
                for dealer_card in  players[0].cards:  # todo list comprehensino
                    if dealer_card.get_card_string == "ACE":  # todo - 2 mal mehr oder weniger gleiche abfrage
                        players[0].update_player_score(-10)
        
        ##########################
        # calculate final result # 
        ##########################
        final_result = []
        for player in players:
            if player.get_score > 21:
                special_result = "BUST"
            elif cls.is_blackjack(player._cards):                
                special_result = "BLACKJACK"
            else:
                special_result = ""
            
            player_result = {
                "score" : player.get_score,
                "name"  : player.get_name,
                "add_txt": special_result
            }
            final_result.append(player_result)

            
        #for key in sorted(final_result):
        #    print (key, final_result[key])
            
        #print(final_result)
        #if players[0].get_score > 21 :
        #    print("dealer BUST")
        #else:
        #    print("dealer finale score:", players[0].get_score)
        cls.print_result_table(final_result)    
        #winner = cls.get_winning_player()
        #print("todo win lose push And the winner is", winner[0], " ", winner[1])

    @property
    def get_player(self):
        """"""
        return self._players
    
    @classmethod
    def print_result_table(cls, players_and_score):
        """"""
        list_ordered_by_score = sorted(players_and_score, key=lambda k: k['score'], reverse=True)
        print("|--------------------------------------------------------|")
        print("|        ROUND FINISHED                                  |")
        print("|                                                        |")
        print("| Result  | Score | Name                 | Info          |")

        dealer_is_busted = False
        dealer_score = players_and_score[0]["score"]
        push_result = False
        if players_and_score[0]["add_txt"] == "BUST":
            dealer_is_busted = True
        
        for item in list_ordered_by_score:
            formatted_name = "{:<19}".format(item["name"])
            formatted_txt = "{:<12}".format(item["add_txt"])
            if item["score"] > 21:
                print("|  LOSE y |  ", item["score"], " | ", formatted_name , "| ", formatted_txt, "|")
            elif item["score"] <= 21 and dealer_is_busted:
                print("|  WIN 1  |  ", item["score"], " | ", formatted_name , "| ", formatted_txt, "|")
            elif item["score"] == dealer_score and item["name"] != "Dealer":
                push_result = True
                print("|  PUSH   |  ", item["score"], " | ", formatted_name , "| ", formatted_txt, "|") 
            else:
                #Sonst gewinnen nur jene Spieler, deren Kartenwerte näher an 21 Punkte heranreichen als der des Dealers. aber blackjack ist z.b. 21 aus 10, 10, ass todo
                if (21 - dealer_score) > (21 - item["score"]): 
                    print("|  WIN 2  |  ", item["score"], " | ", formatted_name , "| ", formatted_txt, "|")
                else:
                    print("|  LOSE x |  ", item["score"], " | ", formatted_name , "| ", formatted_txt, "|")
        
        print("|--------------------------------------------------------|")

        
    @classmethod
    def get_winning_player(cls):
        """i think this one is not needed"""
        game_result = []
        current_winner = "Dealer"
        current_winner_score = 0

        for _ in cls._players:
            player_score = _.get_score
            if player_score < 22:  # nicht mehr gewinn relevant
                if player_score >= current_winner_score:
                    current_winner = (_.get_name, player_score)

                current_winner_score = player_score

        return current_winner
    
    @classmethod
    def all_human_players_finished(cls):
        """"""
        for _ in cls._players:
            if _.is_active and _.is_dealer == False:
                return False

        return True
    
    @classmethod
    def is_blackjack(cls, card_set):
        """check if the cards are a blackjack"""
        total_value = 0
        if len(card_set) == 2 or len(card_set) == 3:
            for _ in card_set:
                total_value += _.get_card_value
            
            if(card_set[0].get_card_value == 7 and card_set[1].get_card_value == 7 and card_set[2].get_card_value == 7) or (total_value == 21 and len(card_set) == 2):
                return True
                        
        return False
