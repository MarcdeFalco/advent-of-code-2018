"""Advent of Code 2018, jour 14 : tableau de recettes.

La suite des scores est stockée dans un array('b'), tableau d'octets bien
plus compact qu'une liste d'entiers pour les quelque 2 * 10^7 chiffres
nécessaires. Chaque étape ajoute un ou deux chiffres en O(1) amorti.
Partie 1 : les dix chiffres qui suivent les N premiers.
Partie 2 : nombre de chiffres avant la première apparition du motif ; comme
une étape peut ajouter deux chiffres, on compare la fin du tableau avec un
décalage d de 0 ou 1 (une première version, qui ne regardait que la toute
fin, pouvait manquer le motif).
"""
from array import array


def etape(recettes, lutins):
    a, b = recettes[lutins[0]], recettes[lutins[1]]
    if a + b >= 10:
        recettes.append(1)
        recettes.append((a + b) % 10)
    else:
        recettes.append(a + b)
    lutins[0] = (lutins[0] + 1 + a) % len(recettes)
    lutins[1] = (lutins[1] + 1 + b) % len(recettes)


def partie1(texte):
    n = int(texte)
    recettes = array('b', [3, 7])
    lutins = [0, 1]
    while len(recettes) < n + 10:
        etape(recettes, lutins)
    return ''.join(map(str, recettes[n:n + 10]))


def partie2(texte):
    motif = array('b', [int(c) for c in texte])
    v = len(motif)
    recettes = array('b', [3, 7])
    lutins = [0, 1]
    while True:
        etape(recettes, lutins)
        if len(recettes) > v:
            for d in range(2):
                fin = len(recettes) - d
                if recettes[fin - v:fin] == motif:
                    return fin - v


with open('input.txt') as f:
    texte = f.read().strip()
print(partie1(texte))
print(partie2(texte))
