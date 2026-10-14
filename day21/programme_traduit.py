"""Advent of Code 2018, jour 21 : traduction à la main du programme d'entrée.

Le programme ne s'arrête que si le registre 0 est égal à la valeur R2
calculée par la boucle extérieure. On engendre la suite des valeurs R2
comparées jusqu'à la première répétition (la suite est alors cyclique).
Partie 1 : la première valeur donne l'arrêt le plus rapide.
Partie 2 : la dernière valeur nouvelle avant le cycle donne l'arrêt le plus
tardif. Les valeurs vues sont dans une liste (test `in` linéaire).
"""


def valeurs_comparees(k):
    valeurs = []
    r2 = 0
    while True:
        r5 = r2 | 65536
        r2 = k
        while True:
            r2 = r2 + (r5 & 255)
            r2 = ((r2 & 16777215) * 65899) & 16777215
            if r5 < 256:
                break
            r5 = r5 // 256
        if r2 in valeurs:
            return valeurs
        valeurs.append(r2)


def partie1(valeurs):
    return valeurs[0]


def partie2(valeurs):
    return valeurs[-1]


with open('input.txt') as f:
    # constante du programme d'entrée : la plus grande valeur d'un seti
    k = max(int(l.split()[1]) for l in f if l.startswith('seti'))
valeurs = valeurs_comparees(k)
print(partie1(valeurs))
print(partie2(valeurs))
