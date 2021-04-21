# -*- coding: utf-8 -*-
#Benutzung von Umlauten

from game_sources import Game

game = True
while game:
    rules = "\nBlack jack Rules:\nHave fun!"
    user_input = input("\nWelcome to 21, Black Jack! \n\nWould you like to read the game and program instructions? (yes or no) ")

    if user_input == "yes" or user_input == "y":
        print(rules)

    while user_input == "":
        user_input = input("You did not enter enything. How is your answer? ")
        if user_input == "yes":
            print(rules)

    black_jack = Game(game="BlackJack")

    y_or_n = input("Game over - new round? (yes or no)")
    if y_or_n == "no" or y_or_n == "n":
        game = False

# Todo: 

#Ansage, wenn der Spieler drüber ist: "Du bist raus!"
#Ass problem
#Geld Eisatz


# untentschieden - dealer gewinnt
# dealer zählt anders
# cheat_modus - kartenzählen (Anzeige: Anzahl der Karten im Deck)
# docstring
# input validation
# todo repr umbau, dass instanzierung möglich ist
# card aufbau (tuple) string int, etc
# user names not euql
# prüfen von karten deck (semantisch ;)
# intitial - regel anzeigen? ja oder nein 
#zu 52 Blatt, also 312 Karten gespielt 
# mehr als 21 bust
# black jack ist entweder Ass + 10

