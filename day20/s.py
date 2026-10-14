"""Advent of Code 2018, jour 20 : plan décrit par une expression régulière.

L'expression est transformée par descente récursive en arbre : une séquence
est une liste dont les éléments sont des directions ou des groupes
d'alternatives (listes de séquences). Plutôt que de construire le plan, on
explore en largeur les chaînes de directions, en ne gardant que celles qui
sont un préfixe d'un mot du langage (fonction `prefixe`), et l'on retient
pour chaque salle la plus petite longueur qui l'atteint. On ne prolonge
qu'une chaîne par salle, ce qui suppose que deux chemins vers la même salle
ont les mêmes suites possibles. Le calcul prend environ une minute.
Partie 1 : plus grande distance. Partie 2 : salles à distance >= 1000.
"""
import sys
from collections import deque

sys.setrecursionlimit(1000000)  # parse s'appelle une fois par caractère


def parse(texte):
    """Lit une séquence ; renvoie (reste du texte, séquence lue)."""
    if texte == '' or texte[0] in '|)':
        return texte, []
    if texte[0] in 'NESW':
        direction = texte[0]
        texte, suite = parse(texte[1:])
        return texte, [direction] + suite
    assert texte[0] == '('
    alternatives = []
    while texte[0] != ')':
        texte, alternative = parse(texte[1:])  # saute '(' ou '|'
        alternatives.append(alternative)
    texte, suite = parse(texte[1:])  # saute ')'
    return texte, [alternatives] + suite


def prefixe(seq, s):
    """La chaîne s est-elle un préfixe d'un mot décrit par seq ?"""
    if s == '':
        return True
    if seq == []:
        return False
    if seq[0] == s[0]:
        return prefixe(seq[1:], s[1:])
    if type(seq[0]) == list:
        return any(prefixe(alternative + seq[1:], s) for alternative in seq[0])
    return False


def distances(seq):
    """Parcours en largeur sur les chaînes ; renvoie salle -> distance."""
    dist = {}
    a_tester = deque([''])
    while a_tester:
        s = a_tester.popleft()
        if prefixe(seq, s):
            x = s.count('E') - s.count('W')
            y = s.count('S') - s.count('N')
            if (x, y) not in dist or dist[x, y] > len(s):
                dist[x, y] = len(s)
                for c in 'ESNW':
                    a_tester.append(s + c)
    return dist


def partie1(dist):
    return max(dist.values())


def partie2(dist):
    return sum(1 for d in dist.values() if d >= 1000)


with open('input.txt') as f:
    seq = parse(f.read().strip()[1:-1])[1]  # sans ^ ni $
dist = distances(seq)
print(partie1(dist))
print(partie2(dist))
