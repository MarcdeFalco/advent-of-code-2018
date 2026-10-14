"""Advent of Code 2018, jour 22 : grotte et outils.

L'indice géologique de chaque case dépend de ses voisines de gauche et du
dessus : `indice` et `erosion` s'appellent mutuellement, avec un cache
(mémoïsation). Le type d'une case est son érosion modulo 3.
Partie 1 : somme des types sur le rectangle entre l'entrée et la cible.
Partie 2 : algorithme de Dijkstra (variante paresseuse, avec un tas) sur les
états (x, y, outil) : changer d'outil coûte 7, avancer d'une case coûte 1 si
l'outil tenu convient aux deux cases (table COMPATIBLES).
"""
import re
from heapq import heappush, heappop

ROCHE, HUMIDE, ETROIT = 0, 1, 2
RIEN, TORCHE, ESCALADE = 0, 1, 2

# (type de la case, type de la case voisine, outil) permettant d'avancer
COMPATIBLES = [
    (ROCHE, ROCHE, TORCHE), (ROCHE, ROCHE, ESCALADE),
    (HUMIDE, HUMIDE, ESCALADE), (HUMIDE, HUMIDE, RIEN),
    (ETROIT, ETROIT, TORCHE), (ETROIT, ETROIT, RIEN),
    (ROCHE, HUMIDE, ESCALADE), (HUMIDE, ROCHE, ESCALADE),
    (ROCHE, ETROIT, TORCHE), (ETROIT, ROCHE, TORCHE),
    (HUMIDE, ETROIT, RIEN), (ETROIT, HUMIDE, RIEN),
]


def autre_outil(tp, outil):
    """Outil que l'on prend en changeant dans une case de type tp."""
    if tp == ROCHE:
        return ESCALADE if outil == TORCHE else TORCHE
    if tp == HUMIDE:
        return ESCALADE if outil == RIEN else RIEN
    return TORCHE if outil == RIEN else RIEN  # ETROIT


def grotte(profondeur, cx, cy):
    cache = {}

    def indice(x, y):
        if (x, y) not in cache:
            if (x, y) in [(0, 0), (cx, cy)]:
                v = 0
            elif y == 0:
                v = x * 16807
            elif x == 0:
                v = y * 48271
            else:
                v = erosion(x - 1, y) * erosion(x, y - 1)
            cache[x, y] = v
        return cache[x, y]

    def erosion(x, y):
        return (indice(x, y) + profondeur) % 20183

    return lambda x, y: erosion(x, y) % 3


def partie1(profondeur, cx, cy):
    type_case = grotte(profondeur, cx, cy)
    # parcours par indices croissants : le cache se remplit sans récursion
    # profonde
    return sum(type_case(x, y) for x in range(cx + 1) for y in range(cy + 1))


def partie2(profondeur, cx, cy):
    type_case = grotte(profondeur, cx, cy)
    tas = [(0, 0, 0, TORCHE)]
    vus = set()
    while tas:
        t, x, y, outil = heappop(tas)
        if (x, y, outil) in vus:
            continue
        vus.add((x, y, outil))
        if (x, y, outil) == (cx, cy, TORCHE):
            return t
        tp = type_case(x, y)
        heappush(tas, (t + 7, x, y, autre_outil(tp, outil)))
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if x + dx < 0 or y + dy < 0:
                continue
            if (tp, type_case(x + dx, y + dy), outil) in COMPATIBLES:
                heappush(tas, (t + 1, x + dx, y + dy, outil))


with open('input.txt') as f:
    profondeur, cx, cy = map(int, re.findall(r'\d+', f.read()))
print(partie1(profondeur, cx, cy))
print(partie2(profondeur, cx, cy))
