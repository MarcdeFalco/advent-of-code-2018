"""Advent of Code 2018, jour 13 : wagonnets sur des rails.

Plutôt que de simuler sur la grille de caractères, on décompose le réseau en
rectangles (repérés par leur coin '/' en haut à gauche), on rattache chaque
wagonnet à un rectangle et on note, pour chaque croisement '+', les
rectangles qui s'y coupent. Un virage est géré par `virage`, un croisement
par un changement de rectangle selon le compteur cyclique du wagonnet
(gauche, tout droit, droite). À chaque tick, les wagonnets bougent dans
l'ordre de lecture ; ceux qui se percutent sont retirés en fin de tick.
Partie 1 : lieu du premier accident. Partie 2 : position du dernier wagonnet.
Remarque : le test de collision ne saute pas les wagonnets déjà accidentés
pendant le même tick, ce qui pourrait compter une collision de trop.
"""

DEPLACEMENT = {'v': (0, 1), '^': (0, -1), '<': (-1, 0), '>': (1, 0)}
A_GAUCHE = {'v': '>', '>': '^', '^': '<', '<': 'v'}
A_DROITE = {'v': '<', '<': '^', '^': '>', '>': 'v'}


def lire_reseau(lignes):
    largeur, hauteur = len(lignes[0]), len(lignes)
    rectangles = []  # (x, y, largeur, hauteur)
    coins_bas_droite = []
    for y in range(hauteur):
        for x in range(largeur):
            if lignes[y][x] == '/' and (x, y) not in coins_bas_droite:
                k = 1
                while lignes[y][x + k] != '\\':
                    k += 1
                l_rect = k + 1
                k = 1
                while lignes[y + k][x] != '\\':
                    k += 1
                h_rect = k + 1
                rectangles.append((x, y, l_rect, h_rect))
                coins_bas_droite.append((x + l_rect - 1, y + h_rect - 1))

    def sur_rectangle(r, x, y):
        rx, ry, rl, rh = rectangles[r]
        return ((x in (rx, rx + rl - 1) and ry <= y < ry + rh)
                or (y in (ry, ry + rh - 1) and rx <= x < rx + rl))

    wagonnets = []  # (rectangle, x, y, direction, compteur)
    croisements = {}
    for y in range(hauteur):
        for x in range(largeur):
            if lignes[y][x] in '<>v^':
                for r in range(len(rectangles)):
                    if sur_rectangle(r, x, y):
                        wagonnets.append((r, x, y, lignes[y][x], -1))
                        break
            if lignes[y][x] == '+':
                croisements[x, y] = [r for r in range(len(rectangles))
                                     if sur_rectangle(r, x, y)]
    return rectangles, croisements, wagonnets


def simuler(lignes):
    """Renvoie (lieu du premier accident, position du dernier wagonnet)."""
    rectangles, croisements, wagonnets = lire_reseau(lignes)

    def virage(r, x, y, d):
        """Nouvelle direction en (x, y) sur le rectangle r (coins compris)."""
        rx, ry, rl, rh = rectangles[r]
        if rx < x < rx + rl - 1 or ry < y < ry + rh - 1:
            return d
        if d in '<>' and y == ry:
            return 'v'
        if d in '<>' and y == ry + rh - 1:
            return '^'
        if d in '^v' and x == rx:
            return '>'
        if d in '^v' and x == rx + rl - 1:
            return '<'

    premier_accident = None
    while True:
        accidentes = []
        wagonnets.sort(key=lambda w: (w[2], w[1]))
        for i in range(len(wagonnets)):
            if i in accidentes:
                continue
            r, x, y, d, n = wagonnets[i]
            dx, dy = DEPLACEMENT[d]
            x, y = x + dx, y + dy
            autre = None
            if (x, y) in croisements:
                n = (n + 1) % 3
                for r2 in croisements[x, y]:
                    if r2 != r:
                        autre = r2
            if autre is None or n == 1:  # tout droit (ou pas de croisement)
                wagonnets[i] = (r, x, y, virage(r, x, y, d), n)
            elif n == 2:  # à droite
                d = A_DROITE[d]
                wagonnets[i] = (autre, x, y, virage(autre, x, y, d), n)
            else:  # n == 0 : à gauche
                d = A_GAUCHE[d]
                wagonnets[i] = (autre, x, y, virage(autre, x, y, d), n)

            for j in range(len(wagonnets)):
                if i != j and wagonnets[j][1:3] == (x, y):
                    accidentes += [i, j]
                    if premier_accident is None:
                        premier_accident = (x, y)

        wagonnets = [wagonnets[i] for i in range(len(wagonnets))
                     if i not in accidentes]
        if len(wagonnets) == 1:
            return premier_accident, wagonnets[0][1:3]


def partie1(lignes):
    return '%d,%d' % simuler(lignes)[0]


def partie2(lignes):
    return '%d,%d' % simuler(lignes)[1]


with open('input.txt') as f:
    # pas de strip : les espaces en début de ligne comptent
    lignes = f.read()[:-1].split('\n')
print(partie1(lignes))
print(partie2(lignes))
