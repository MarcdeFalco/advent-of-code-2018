"""Advent of Code 2018, jour 17 : écoulement d'eau dans un sol argileux.

Les cases (sable, argile, mouillé, eau stagnante) sont dans un dictionnaire.
À chaque itération, un parcours avec pile explicite mouille tout ce que
l'eau atteint depuis la source : elle descend si possible, sinon s'étale.
Les cases mouillées comprises entre deux murs d'argile deviennent de l'eau
stagnante ; on efface alors les cases mouillées et on recommence, jusqu'à ce
que plus rien ne se remplisse. Chaque itération refait un parcours complet :
le calcul est lent (une minute environ) mais simple.
Partie 1 : cases atteintes par l'eau (mouillées ou stagnantes) entre la plus
petite et la plus grande ordonnée d'argile. Partie 2 : eau stagnante.
"""
from collections import defaultdict

SABLE, ARGILE, MOUILLE, EAU = 0, 1, 2, 3


def lire(texte):
    cases = defaultdict(int)
    for ligne in texte.split('\n'):
        a, b = ligne.split(', ')
        axe, v = a.split('=')
        v = int(v)
        debut, fin = map(int, b.split('=')[1].split('..'))
        for w in range(debut, fin + 1):
            if axe == 'x':
                cases[v, w] = ARGILE
            else:
                cases[w, v] = ARGILE
    return cases


def remplir(cases):
    """Fait couler l'eau ; à la fin, les cases mouillées de la dernière
    itération sont conservées."""
    xs = [x for x, y in cases]
    ys = [y for x, y in cases]
    minx, maxx, maxy = min(xs), max(xs), max(ys)

    def entre_deux_murs(x, y):
        xg = x - 1
        while xg >= minx and cases[xg, y] in [EAU, MOUILLE]:
            xg -= 1
        xd = x + 1
        while xd <= maxx and cases[xd, y] in [EAU, MOUILLE]:
            xd += 1
        return cases[xg, y] == ARGILE and cases[xd, y] == ARGILE

    def mouiller(x, y):
        """Parcours depuis la source ; renvoie la liste des cases mouillées."""
        mouillees = []
        a_traiter = [(x, y)]
        while a_traiter:
            x, y = a_traiter.pop()
            if y > maxy or cases[x, y] == MOUILLE:
                continue
            cases[x, y] = MOUILLE
            mouillees.append((x, y))
            if cases[x, y + 1] in [SABLE, MOUILLE]:
                a_traiter.append((x, y + 1))  # l'eau tombe
            else:
                for dx in [-1, 1]:  # elle s'étale sur l'argile ou l'eau
                    if cases[x + dx, y] == SABLE:
                        a_traiter.append((x + dx, y))
        return mouillees

    while True:
        rempli = False
        for x, y in mouiller(500, 0):
            if entre_deux_murs(x, y):
                rempli = True
                cases[x, y] = EAU
        if not rempli:
            break
        for c in cases:
            if cases[c] == MOUILLE:
                cases[c] = SABLE


def compter(cases, miny, maxy, types):
    return sum(1 for (x, y), t in cases.items()
               if miny <= y <= maxy and t in types)


def partie1(cases, miny, maxy):
    return compter(cases, miny, maxy, [EAU, MOUILLE])


def partie2(cases, miny, maxy):
    return compter(cases, miny, maxy, [EAU])


with open('input.txt') as f:
    cases = lire(f.read().strip())
ys = [y for x, y in cases]
miny, maxy = min(ys), max(ys)
remplir(cases)
print(partie1(cases, miny, maxy))
print(partie2(cases, miny, maxy))
