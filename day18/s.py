"""Advent of Code 2018, jour 18 : automate cellulaire sur un milliard d'étapes.

L'évolution est déterministe et le nombre de grilles est fini : la suite des
états est ultimement périodique. On garde la liste des états (sous forme de
chaînes) jusqu'à la première répétition : si l'état i est égal à l'état
j < i, l'état n (n >= j) est l'état j + (n - j) mod (i - j).
Partie 1 : état après 10 minutes. Partie 2 : état après 10^9 minutes.
La réponse est le nombre d'arbres fois le nombre de chantiers.
"""
from itertools import product


def suivant(grille):
    w, h = len(grille[0]), len(grille)
    nouvelle = [['.'] * w for _ in range(h)]
    for x, y in product(range(w), range(h)):
        arbres, chantiers = 0, 0
        for dx, dy in product(range(-1, 2), repeat=2):
            if (dx, dy) != (0, 0) and 0 <= x + dx < w and 0 <= y + dy < h:
                voisin = grille[y + dy][x + dx]
                if voisin == '|':
                    arbres += 1
                if voisin == '#':
                    chantiers += 1
        case = grille[y][x]
        if case == '.' and arbres >= 3:
            nouvelle[y][x] = '|'
        elif case == '|':
            nouvelle[y][x] = '#' if chantiers >= 3 else '|'
        elif case == '#' and chantiers > 0 and arbres > 0:
            nouvelle[y][x] = '#'
    return nouvelle


def etats_jusqu_au_cycle(grille):
    """Renvoie la liste des états vus (chaînes), le début et la période du
    cycle."""
    vus = []
    while True:
        etat = ''.join(''.join(ligne) for ligne in grille)
        if etat in vus:
            debut = vus.index(etat)
            return vus, debut, len(vus) - debut
        vus.append(etat)
        grille = suivant(grille)


def valeur_apres(grille, n):
    vus, debut, periode = etats_jusqu_au_cycle(grille)
    if n >= debut:
        n = debut + (n - debut) % periode
    etat = vus[n]
    return etat.count('|') * etat.count('#')


def partie1(grille):
    return valeur_apres(grille, 10)


def partie2(grille):
    return valeur_apres(grille, 1_000_000_000)


with open('input.txt') as f:
    grille = [list(ligne) for ligne in f.read().strip().split('\n')]
print(partie1(grille))
print(partie2(grille))
