"""Advent of Code 2018, jour 3 : rectangles de tissu superposés.

Un dictionnaire compte, pour chaque case du tissu, le nombre de rectangles
qui la couvrent. Partie 1 : nombre de cases couvertes au moins deux fois.
Partie 2 : le seul rectangle dont toutes les cases ont un compteur égal à 1.
Le temps est proportionnel à la surface totale des rectangles.
"""
from collections import defaultdict


def lire_rectangles(texte):
    """Une ligne « #123 @ 3,2: 5x4 » donne (123, 3, 2, 5, 4)."""
    rectangles = []
    for ligne in texte.split('\n'):
        ident, _, coin, taille = ligne.split()
        x, y = map(int, coin[:-1].split(','))
        largeur, hauteur = map(int, taille.split('x'))
        rectangles.append((int(ident[1:]), x, y, largeur, hauteur))
    return rectangles


def cases(rectangle):
    _, x, y, largeur, hauteur = rectangle
    for dx in range(largeur):
        for dy in range(hauteur):
            yield x + dx, y + dy


def couverture(rectangles):
    compteur = defaultdict(int)
    for rectangle in rectangles:
        for case in cases(rectangle):
            compteur[case] += 1
    return compteur


def partie1(rectangles):
    compteur = couverture(rectangles)
    return sum(1 for case in compteur if compteur[case] > 1)


def partie2(rectangles):
    compteur = couverture(rectangles)
    for rectangle in rectangles:
        if all(compteur[case] == 1 for case in cases(rectangle)):
            return rectangle[0]


with open('input.txt') as f:
    rectangles = lire_rectangles(f.read().strip())
print(partie1(rectangles))
print(partie2(rectangles))
