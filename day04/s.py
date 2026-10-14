"""Advent of Code 2018, jour 4 : gardes endormis.

Les horodatages sont au format année-mois-jour heure:minute : le tri
lexicographique des lignes est donc le tri chronologique. Pour chaque garde,
on note les minutes d'endormissement et de réveil (elles vont par paires),
puis on construit l'histogramme des minutes passées à dormir.
Partie 1 : le garde qui dort le plus, fois sa minute favorite.
Partie 2 : le couple (garde, minute) le plus fréquent.
"""
import re
from collections import defaultdict

FORMAT = re.compile(r'\[\d+-\d+-\d+ \d+:(?P<minute>\d+)\] (?P<action>.*)')


def lire_statistiques(texte):
    """Renvoie la liste des (sommeil total, fréquence de la minute favorite,
    minute favorite, garde)."""
    evenements = defaultdict(list)  # garde -> minutes d'endormissement/réveil
    garde = None
    for ligne in sorted(texte.split('\n')):
        m = FORMAT.match(ligne)
        minute = int(m.group('minute'))
        action = m.group('action')
        if action.startswith('Guard'):
            garde = int(action.split()[1][1:])
        else:  # 'falls asleep' ou 'wakes up', en alternance
            evenements[garde].append(minute)

    statistiques = []
    for garde, minutes in evenements.items():
        sommeil = 0
        histogramme = defaultdict(int)
        for i in range(len(minutes) // 2):
            debut, fin = minutes[2 * i], minutes[2 * i + 1]
            sommeil += fin - debut
            for m in range(debut, fin):
                histogramme[m] += 1
        favorite = minutes[0]
        for m in histogramme:
            if histogramme[m] > histogramme[favorite]:
                favorite = m
        statistiques.append((sommeil, histogramme[favorite], favorite, garde))
    return statistiques


def partie1(statistiques):
    _, _, minute, garde = max(statistiques)
    return minute * garde


def partie2(statistiques):
    _, minute, garde = max(s[1:] for s in statistiques)
    return minute * garde


with open('input.txt') as f:
    statistiques = lire_statistiques(f.read().strip())
print(partie1(statistiques))
print(partie2(statistiques))
