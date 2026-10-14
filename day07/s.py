"""Advent of Code 2018, jour 7 : tâches dépendantes.

Algorithme de Kahn : `restants[t]` compte les prédécesseurs non terminés de
la tâche t, et l'on prend toujours la plus petite tâche disponible.
La simulation avance seconde par seconde avec plusieurs ouvriers, chacun
ayant un temps restant ; une tâche terminée décrémente les compteurs de ses
successeurs. Partie 1 : ordre de fin avec un seul ouvrier (le temps ne joue
alors aucun rôle). Partie 2 : durée totale avec cinq ouvriers, une tâche
durant 60 secondes plus son rang dans l'alphabet.
"""
from collections import defaultdict


def simuler(lignes, nb_ouvriers):
    """Renvoie (ordre de fin des tâches, durée totale)."""
    successeurs = defaultdict(list)
    restants = defaultdict(int)
    for ligne in lignes:
        mots = ligne.split()
        avant, apres = mots[1], mots[-3]
        successeurs[avant].append(apres)
        restants[apres] += 1

    a_faire = sorted(set(successeurs) | set(restants))
    duree = lambda t: ord(t) - ord('A') + 61
    temps_restant = [0] * nb_ouvriers
    tache_en_cours = [None] * nb_ouvriers
    ordre = []
    secondes = 0
    while a_faire:
        # attribution d'une tâche disponible à chaque ouvrier libre
        for o in range(nb_ouvriers):
            if temps_restant[o] == 0:
                disponibles = [t for t in a_faire if restants[t] == 0]
                if disponibles:
                    tache = disponibles[0]
                    a_faire.remove(tache)
                    tache_en_cours[o] = tache
                    temps_restant[o] = duree(tache)
        # une seconde de travail
        for o in range(nb_ouvriers):
            if temps_restant[o] > 0:
                temps_restant[o] -= 1
                if temps_restant[o] == 0:
                    ordre.append(tache_en_cours[o])
                    for suivante in successeurs[tache_en_cours[o]]:
                        restants[suivante] -= 1
                    tache_en_cours[o] = None
        secondes += 1
    # plus rien à attribuer : il reste à finir les tâches en cours
    return ''.join(ordre), secondes + max(temps_restant)


def partie1(lignes):
    return simuler(lignes, 1)[0]


def partie2(lignes):
    return simuler(lignes, 5)[1]


with open('input.txt') as f:
    lignes = f.read().strip().split('\n')
print(partie1(lignes))
print(partie2(lignes))
