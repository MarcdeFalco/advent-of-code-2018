"""Advent of Code 2018, jour 19 : traduction à la main du programme d'entrée.

Le programme fait parcourir à R3 et R1 toutes les valeurs de 1 à N (N est
dans R4 après l'initialisation, cf. `python3 s.py trace`) et ajoute R3 à R0
chaque fois que R3 * R1 == N : il calcule la somme des diviseurs de N.
Cette traduction littérale, en O(N^2), reste beaucoup trop lente pour la
partie 2 (N de l'ordre de 10^7) ; elle sert à faire apparaître la fonction
calculée. Usage : python3 programme_traduit.py N
"""
import sys

R4 = int(sys.argv[1])
R0 = 0
R3 = 1
while True:
    R1 = 1
    while True:
        if R3 * R1 == R4:
            R0 = R0 + R3
            print(R0)  # progression : somme des diviseurs trouvés
        R1 += 1
        if R1 > R4:
            break
    R3 += 1
    if R3 > R4:
        break

print(R0)
