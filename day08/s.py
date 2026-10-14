"""Advent of Code 2018, jour 8 : arbre sérialisé.

Un nœud est codé par : nombre de fils, nombre de métadonnées, les fils, puis
les métadonnées. `lire(i)` lit le nœud qui commence à l'indice i (descente
récursive) et renvoie l'indice qui suit avec l'arbre, un couple
(liste des fils, liste des métadonnées).
Partie 1 : somme de toutes les métadonnées.
Partie 2 : valeur d'un nœud, les métadonnées désignant des fils (numérotés
à partir de 1).
"""


def lire_arbre(entiers):
    def lire(i):
        nb_fils, nb_meta = entiers[i], entiers[i + 1]
        fils = []
        j = i + 2
        for _ in range(nb_fils):
            j, f = lire(j)
            fils.append(f)
        return j + nb_meta, (fils, entiers[j:j + nb_meta])

    return lire(0)[1]


def somme_metadonnees(arbre):
    fils, meta = arbre
    return sum(somme_metadonnees(f) for f in fils) + sum(meta)


def valeur(arbre):
    fils, meta = arbre
    if fils == []:
        return sum(meta)
    # les indices hors bornes sont ignorés
    return sum(valeur(fils[k - 1]) for k in meta if k <= len(fils))


def partie1(arbre):
    return somme_metadonnees(arbre)


def partie2(arbre):
    return valeur(arbre)


with open('input.txt') as f:
    arbre = lire_arbre(list(map(int, f.read().split())))
print(partie1(arbre))
print(partie2(arbre))
