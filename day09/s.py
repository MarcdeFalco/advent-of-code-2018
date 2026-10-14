"""Advent of Code 2018, jour 9 : billes en cercle.

Le cercle est une deque dont la tête est la bille courante : tourner d'un
cran dans un sens ou dans l'autre coûte O(1), comme poser ou retirer une
bille en tête. La partie 2 multiplie le nombre de billes par 100 : environ
7 millions d'étapes en temps linéaire (une liste Python, avec insertion au
milieu en O(n), serait quadratique).
"""
import re
from collections import defaultdict, deque


def jouer(nb_joueurs, derniere):
    cercle = deque([0])

    def tourner_horaire():
        cercle.append(cercle.popleft())

    def tourner_antihoraire():
        cercle.appendleft(cercle.pop())

    scores = defaultdict(int)
    for bille in range(1, derniere + 1):
        joueur = (bille - 1) % nb_joueurs
        if bille % 23 == 0:
            for _ in range(7):
                tourner_antihoraire()
            scores[joueur] += bille + cercle.popleft()
        else:
            tourner_horaire()
            tourner_horaire()
            cercle.appendleft(bille)
    return max(scores.values())


def partie1(nb_joueurs, derniere):
    return jouer(nb_joueurs, derniere)


def partie2(nb_joueurs, derniere):
    return jouer(nb_joueurs, 100 * derniere)


with open('input.txt') as f:
    nb_joueurs, derniere = map(int, re.findall(r'\d+', f.read()))
print(partie1(nb_joueurs, derniere))
print(partie2(nb_joueurs, derniere))
