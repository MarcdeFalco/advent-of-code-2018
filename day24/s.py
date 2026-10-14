"""Advent of Code 2018, jour 24 : combat entre deux armées.

Chaque groupe est un objet `Groupe` ; la méthode __lt__ donne l'ordre de
choix des cibles (puissance effective, puis initiative). La simulation
alterne phase de choix des cibles et phase d'attaque par initiative
décroissante. Une situation où plus personne ne peut tuer renvoie -42,
compté comme une défaite. `combat` renvoie le nombre d'unités restantes,
positif si le système immunitaire gagne, négatif si l'infection gagne.
Partie 1 : unités restantes de l'armée gagnante, sans bonus.
Partie 2 : bonus minimal cherché par dichotomie, ce qui suppose l'issue
monotone en le bonus (ce n'est pas garanti, à cause des arrondis et des
impasses).
"""
import re
from copy import deepcopy

FORMAT = re.compile(r'(?P<nombre>\d+) units each with (?P<pv>\d+) hit points'
                    r'( \((?P<spec>.*)\))? with an attack that does '
                    r'(?P<attaque>\d+) (?P<type>\w+) damage at initiative '
                    r'(?P<initiative>\d+)')


class Groupe:
    def __init__(self, m):
        self.pv = int(m.group('pv'))
        self.nombre = int(m.group('nombre'))
        self.attaque = int(m.group('attaque'))
        self.type_attaque = m.group('type')
        self.initiative = int(m.group('initiative'))
        self.immunites = []
        self.faiblesses = []
        if m.group('spec') is not None:
            # « immune to a, b; weak to c » (dans un ordre quelconque)
            for partie in m.group('spec').split('; '):
                if partie.startswith('immune'):
                    self.immunites = partie[len('immune to '):].split(', ')
                else:
                    self.faiblesses = partie[len('weak to '):].split(', ')

    def puissance(self):
        return self.nombre * self.attaque

    def degats(self, cible):
        if self.type_attaque in cible.immunites:
            return 0
        p = self.puissance()
        if self.type_attaque in cible.faiblesses:
            p *= 2
        return p

    def __lt__(self, autre):
        return ((self.puissance(), self.initiative)
                < (autre.puissance(), autre.initiative))


def lire(texte):
    lignes = texte.split('\n')
    i = 1
    immunitaire = []
    while lignes[i] != '':
        immunitaire.append(Groupe(FORMAT.match(lignes[i])))
        i += 1
    infection = [Groupe(FORMAT.match(l)) for l in lignes[i + 2:]]
    return [immunitaire, infection]


def combat(armees, bonus=0):
    for g in armees[0]:
        g.attaque += bonus
    while [] not in armees:
        # choix des cibles
        cibles = {}
        for armee in armees:
            armee.sort(reverse=True)
        for i in range(2):
            defenseurs = armees[1 - i][:]
            for attaquant in armees[i]:
                if defenseurs == []:
                    continue
                meilleure = defenseurs[0]
                for d in defenseurs:
                    degats = attaquant.degats(d)
                    if degats == 0:
                        continue
                    degats_meilleure = attaquant.degats(meilleure)
                    if (degats, d.puissance(), d.initiative) > \
                            (degats_meilleure, meilleure.puissance(),
                             meilleure.initiative):
                        meilleure = d
                if attaquant.degats(meilleure) > 0:
                    defenseurs.remove(meilleure)
                    cibles[attaquant] = meilleure

        # attaques
        des_morts = False
        groupes = sorted(armees[0] + armees[1], key=lambda g: g.initiative,
                         reverse=True)
        for g in groupes:
            if g.nombre > 0 and g in cibles:
                cible = cibles[g]
                tues = min(g.degats(cible) // cible.pv, cible.nombre)
                if tues > 0:
                    des_morts = True
                cible.nombre -= tues
        for i in range(2):
            armees[i] = [g for g in armees[i] if g.nombre > 0]
        if not des_morts:
            return -42  # impasse

    return sum(g.nombre for g in armees[0]) - sum(g.nombre for g in armees[1])


def partie1(armees):
    return abs(combat(deepcopy(armees)))


def partie2(armees):
    debut, fin = 0, 10000
    while debut < fin:
        milieu = (debut + fin) // 2
        if combat(deepcopy(armees), milieu) > 0:
            fin = milieu
        else:
            debut = milieu + 1
    return combat(deepcopy(armees), debut)


with open('input.txt') as f:
    armees = lire(f.read().strip())
print(partie1(armees))
print(partie2(armees))
