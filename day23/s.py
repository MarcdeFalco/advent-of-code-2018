"""Advent of Code 2018, jour 23 : nanobots.

Chaque nanobot couvre un octaèdre : la boule de rayon r pour la distance de
Manhattan en 3D.
Partie 1 : nombre de nanobots dans la zone de celui qui a le plus grand rayon.
Partie 2 : pas de solution.
"""
import re

FORMAT = re.compile(r'pos=<(.*),(.*),(.*)>, r=(.*)')


def distance(x1, y1, z1, x2, y2, z2):
    return abs(x2 - x1) + abs(y2 - y1) + abs(z2 - z1)


def partie1(nanobots):
    x, y, z, r = max(nanobots, key=lambda n: n[3])
    return sum(1 for x2, y2, z2, _ in nanobots
               if distance(x, y, z, x2, y2, z2) <= r)


def partie2_essai(nanobots):
    """Heuristique sur les sommets ; renvoie (sommet, nombre de nanobots)."""
    sommets = []
    for x, y, z, r in nanobots:
        sommets += [(x, y, z - r), (x, y, z + r), (x, y - r, z),
                    (x, y + r, z), (x - r, y, z), (x + r, y, z)]
    compte = {}
    for s in sommets:
        compte[s] = sum(1 for x2, y2, z2, r in nanobots
                        if distance(*s, x2, y2, z2) <= r)
    meilleur = max(compte.values())
    for s in compte:
        if compte[s] == meilleur:
            return s, meilleur


with open('input.txt') as f:
    nanobots = [tuple(map(int, FORMAT.match(ligne).groups()))
                for ligne in f.read().strip().split('\n')]
print(partie1(nanobots))
print('partie 2 (essai, pas une réponse) :', partie2_essai(nanobots))
