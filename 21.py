# -*- coding: utf-8 -*-
# Benutzung von Umlauten

from game_sources import Game

game = True
initial_game = True

while game:
    if initial_game:
        rules = "\nBlack jack Rules:\nHave fun!"
        user_input = input(
            "\nWelcome to 21, Black Jack! \n\nWould you like to read the game and program instructions? (yes or no) "
        )

        if user_input == "yes" or user_input == "y":
            print(rules)  # todo

        while user_input == "":
            user_input = input("You did not enter enything. How is your answer? ")
            if user_input == "yes":
                print(rules)

    # general game loop
    black_jack = Game(game="BlackJack")

    y_or_n = input(
        "Game over - new round? (yes or no)"
    )  # todo - same settings as before? so no need to enter
    if y_or_n == "no" or y_or_n == "n":
        game = False
    else:
        initial_game = False


# Todo:

# Geld Eisatz
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
# black jack ist entweder Ass + 10

# todo:
# einsatz einbauen + gewinn verteilung
# bis zu sieben Spieler + input validation für user anzahl (nur int)
# 6 decks - 52 Blatt, also 312 Karten gespielt

# final score ermitteln:

# print_final_score()
## black jack ist entweder Ass + 10 oder 7 + 7 + 7
## black jack ist besser als normale 21
## mehr als 21 bust
## untentschieden - dealer gewinnt

# nice to have
## cheat_modus - kartenzählen
## docstring
## weitere optionen split, double, insurance https://www.bettingexpert.com/de/casino/blackjack/regeln
