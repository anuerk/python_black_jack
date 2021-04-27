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
    black_jack = Game()

    y_or_n = input(
        "Game over - new round? (yes or no)"
    )  # todo - same settings as before? so no need to enter
    if y_or_n == "no" or y_or_n == "n":
        game = False
    else:
        initial_game = False


# Todo:
# Geld Eisatz
# ergebnisse:
# blackjack -> einsatz * 2.5
# push -> einsatz
# cheat_modus - kartenzählen (Anzeige: Anzahl der Karten im Deck)
# intitial - regel anzeigen? ja oder nein
# 6 decks - 52 Blatt, also 312 Karten gespielt
# weitere optionen split, double, insurance https://www.bettingexpert.com/de/casino/blackjack/regeln
