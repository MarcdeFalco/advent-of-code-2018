"""Advent of Code 2018, jour 25 : constellations.

Deux points sont reliés si leur distance de Manhattan en 4D est au plus 3 ;
le nombre de constellations est le nombre de composantes connexes de ce
graphe, compté par des parcours en profondeur avec une pile explicite. Chaque
dépilement teste tous les points : O(n^2). (Le 25 décembre n'a qu'une partie.)
"""


def distance(p, q):
    return sum(abs(a - b) for a, b in zip(p, q))


def partie1(points):
    nb_composantes = 0
    visite = [False] * len(points)
    for depart in range(len(points)):
        if not visite[depart]:
            pile = [depart]
            while pile:
                i = pile.pop()
                if not visite[i]:
                    visite[i] = True
                    for j in range(len(points)):
                        if (not visite[j]
                                and distance(points[i], points[j]) <= 3):
                            pile.append(j)
            nb_composantes += 1
    return nb_composantes


with open('input.txt') as f:
    points = [tuple(map(int, ligne.split(',')))
              for ligne in f.read().strip().split('\n')]
print(partie1(points))
