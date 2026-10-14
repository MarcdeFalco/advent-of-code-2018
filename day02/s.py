"""Advent of Code 2018, jour 2 : identifiants de boîtes.

Partie 1 : pour chaque identifiant, on regarde si une lettre y apparaît
exactement deux fois, ou exactement trois fois (avec str.count).
Partie 2 : on compare toutes les paires d'identifiants position par
position et on garde celle qui diffère d'un seul caractère : O(n^2 L).
"""


def partie1(identifiants):
    nb_deux, nb_trois = 0, 0
    for ident in identifiants:
        if any(ident.count(c) == 2 for c in ident):
            nb_deux += 1
        if any(ident.count(c) == 3 for c in ident):
            nb_trois += 1
    return nb_deux * nb_trois


def partie2(identifiants):
    for id1 in identifiants:
        for id2 in identifiants:
            differences = sum(1 for a, b in zip(id1, id2) if a != b)
            if differences == 1:
                # la réponse est formée des lettres communes
                return ''.join(a for a, b in zip(id1, id2) if a == b)


with open('input.txt') as f:
    identifiants = f.read().strip().split('\n')
print(partie1(identifiants))
print(partie2(identifiants))
