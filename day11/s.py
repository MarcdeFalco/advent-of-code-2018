"""Advent of Code 2018, jour 11 : carré de puissance maximale.

La grille 300 x 300 des niveaux de puissance est calculée par formule. Les
sommes des carrés de côté k s'obtiennent à partir de celles de côté k - 1 en
ajoutant une ligne et une colonne (tabulation selon k). Chaque ajout coûte
O(k), d'où O(S^4) au total pour S = 300 : le calcul prend une minute.
Partie 1 : meilleur carré 3 x 3.
Partie 2 : meilleur carré de taille quelconque.
Remarque : les indices 0 à 299 servent directement de coordonnées, alors que
la grille de l'énoncé va de 1 à 300 ; c'est sans effet tant que le meilleur
carré ne touche pas ces bords.
"""
from itertools import product

S = 300


def niveau(x, y, serie):
    rack = x + 10
    puissance = (rack * y + serie) * rack
    return (puissance // 100) % 10 - 5


def sommes_des_carres(serie):
    """sommes[k - 1][y][x] : somme du carré de côté k et de coin (x, y)."""
    grille = [[niveau(x, y, serie) for x in range(S)] for y in range(S)]
    sommes = [grille]
    for k in range(2, S + 1):
        precedente = sommes[-1]
        g = [[0] * S for _ in range(S)]
        for x, y in product(range(S - k + 1), repeat=2):
            # carré de côté k - 1, plus la colonne de droite et la ligne du bas
            g[y][x] = (precedente[y][x]
                       + sum(grille[y + dy][x + k - 1] for dy in range(k))
                       + sum(grille[y + k - 1][x + dx] for dx in range(k - 1)))
        sommes.append(g)
    return sommes


def meilleur_carre(sommes, tailles):
    meilleur, meilleure_somme = None, None
    for k in tailles:
        for x, y in product(range(S - k + 1), repeat=2):
            s = sommes[k - 1][y][x]
            if meilleure_somme is None or s > meilleure_somme:
                meilleur, meilleure_somme = (x, y, k), s
    return meilleur


def partie1(sommes):
    x, y, _ = meilleur_carre(sommes, [3])
    return f'{x},{y}'


def partie2(sommes):
    return '%d,%d,%d' % meilleur_carre(sommes, range(1, S + 1))


with open('input.txt') as f:
    sommes = sommes_des_carres(int(f.read().strip()))
print(partie1(sommes))
print(partie2(sommes))
