"""Advent of Code 2018, jour 12 : automate cellulaire sur une ligne infinie.

L'état est un dictionnaire position -> plante, ce qui permet à la ligne de
s'étendre dans les deux sens ; à chaque génération on ne parcourt que
l'intervalle des plantes élargi de 2.
Partie 1 : somme des positions des plantes après 20 générations.
Partie 2 (50 milliards de générations) : en simulant 1000 générations, on
observe qu'après un régime transitoire le motif se translate et que la somme
croît d'une constante à chaque génération ; on extrapole cette croissance
linéaire.
"""
from collections import defaultdict


def lire(texte):
    lignes = texte.split('\n')
    etat = defaultdict(bool)
    for i, c in enumerate(lignes[0][len('initial state: '):]):
        etat[i] = c == '#'
    regles = {}
    for ligne in lignes[2:]:
        motif, resultat = ligne.split(' => ')
        regles[motif] = resultat == '#'
    return etat, regles


def evoluer(etat, regles):
    suivant = defaultdict(bool)
    plantes = [i for i in etat if etat[i]]
    for i in range(min(plantes) - 2, max(plantes) + 3):
        voisinage = ''.join('#' if etat[i + k] else '.' for k in range(-2, 3))
        suivant[i] = regles.get(voisinage, False)
    return suivant


def somme(etat):
    return sum(i for i in etat if etat[i])


def partie1(etat, regles):
    for _ in range(20):
        etat = evoluer(etat, regles)
    return somme(etat)


def partie2(etat, regles, generations=50_000_000_000):
    sommes = []
    for _ in range(1000):
        etat = evoluer(etat, regles)
        sommes.append(somme(etat))
    pas = sommes[-1] - sommes[-2]
    assert sommes[-1] - sommes[-100] == 99 * pas, 'régime pas encore linéaire'
    return sommes[-1] + (generations - 1000) * pas


with open('input.txt') as f:
    etat, regles = lire(f.read().strip())
print(partie1(etat, regles))
print(partie2(etat, regles))
