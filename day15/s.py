"""Advent of Code 2018, jour 15 : combat d'elfes et de gobelins.

Les unités sont des couples (camp, points de vie) posés dans la grille. À
son tour, une unité qui n'est pas au contact d'un ennemi lance un parcours
en largeur vers chaque case libre adjacente à un ennemi et fait un pas sur
le plus court chemin (départagé par le premier pas dans l'ordre de lecture),
puis attaque l'ennemi adjacent le plus faible.
Partie 1 : issue du combat (tours complets fois points de vie restants).
Partie 2 : on augmente la force des elfes de 1 en 1, en interrompant le
combat à la première mort d'elfe, jusqu'à ce que les elfes gagnent sans perte.
Remarques : le départage ne trie pas d'abord par case cible, et une unité
tombée exactement à 0 point de vie n'est pas retirée (test `< 0`).
"""
from collections import deque
from itertools import product

DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def lire_grille(texte):
    grille = [list(ligne) for ligne in texte.split('\n')]
    for ligne in grille:
        for x, c in enumerate(ligne):
            if c in 'EG':
                ligne[x] = (c, 200)
    return grille


def est_unite(case):
    return type(case) == tuple


def ennemis(u1, u2):
    return est_unite(u1) and est_unite(u2) and u1[0] != u2[0]


def chemin(grille, xs, ys, xc, yc):
    """Plus court chemin de (xs, ys) à (xc, yc), en partant de la fin :
    chemin[-1] est le départ, chemin[-2] le premier pas. [] si impossible."""
    a_visiter = deque([(xs, ys)])
    pred = {}
    while a_visiter:
        x, y = a_visiter.popleft()
        if (x, y) == (xc, yc):
            p = [(xc, yc)]
            while p[-1] in pred:
                p.append(pred[p[-1]])
            return p
        for dx, dy in [(0, -1), (-1, 0), (1, 0), (0, 1)]:
            if grille[y + dy][x + dx] == '.' and (x + dx, y + dy) not in pred:
                pred[x + dx, y + dy] = (x, y)
                a_visiter.append((x + dx, y + dy))
    return []


def combat(grille_initiale, force_elfes, arret_mort_elfe):
    """Renvoie (camp vainqueur, issue). Si arret_mort_elfe, le combat
    s'arrête dès qu'un elfe meurt et le vainqueur renvoyé est 'G'."""
    grille = [ligne[:] for ligne in grille_initiale]
    w, h = len(grille[0]), len(grille)
    force = {'E': force_elfes, 'G': 3}
    tour = 1
    while True:
        fin = None
        a_jouer = [(x, y) for y, x in product(range(h), range(w))
                   if est_unite(grille[y][x])]
        for x, y in a_jouer:
            if not est_unite(grille[y][x]):
                continue  # unité tuée pendant ce tour
            camp = grille[y][x][0]
            au_contact = any(ennemis(grille[y][x], grille[y + dy][x + dx])
                             for dx, dy in DIRECTIONS)
            if not au_contact:
                # déplacement
                cibles = []
                il_reste_des_ennemis = False
                for y2, x2 in product(range(h), range(w)):
                    if ennemis(grille[y][x], grille[y2][x2]):
                        il_reste_des_ennemis = True
                        for dx, dy in DIRECTIONS:
                            if grille[y2 + dy][x2 + dx] == '.':
                                cibles.append((x2 + dx, y2 + dy))
                if not il_reste_des_ennemis:
                    fin = camp
                    break
                chemins = []
                for xc, yc in cibles:
                    p = chemin(grille, x, y, xc, yc)
                    if p:
                        chemins.append(p)
                if chemins:
                    # plus court, puis premier pas dans l'ordre de lecture
                    p = min(chemins,
                            key=lambda p: (len(p), p[-2][1], p[-2][0]))
                    x2, y2 = p[-2]
                    grille[y2][x2] = grille[y][x]
                    grille[y][x] = '.'
                    x, y = x2, y2
            # attaque de l'ennemi adjacent le plus faible
            adjacents = [(x + dx, y + dy) for dx, dy in DIRECTIONS
                         if ennemis(grille[y][x], grille[y + dy][x + dx])]
            if adjacents:
                xc, yc = min(adjacents,
                             key=lambda c: (grille[c[1]][c[0]][1], c[1], c[0]))
                pv = grille[yc][xc][1] - force[camp]
                if pv < 0:
                    if camp == 'G' and arret_mort_elfe:
                        fin = 'G'
                        break
                    grille[yc][xc] = '.'
                else:
                    grille[yc][xc] = (grille[yc][xc][0], pv)
        if fin is not None:
            break
        tour += 1

    tours_complets = tour - 1
    points_de_vie = sum(c[1] for ligne in grille for c in ligne
                        if est_unite(c))
    return fin, tours_complets * points_de_vie


def partie1(grille):
    return combat(grille, 3, False)[1]


def partie2(grille):
    force = 3
    while True:
        vainqueur, issue = combat(grille, force, True)
        if vainqueur == 'E':
            return issue
        force += 1


with open('input.txt') as f:
    grille = lire_grille(f.read().strip())
print(partie1(grille))
print(partie2(grille))
