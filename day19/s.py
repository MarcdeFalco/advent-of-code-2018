"""Advent of Code 2018, jour 19 : processeur à six registres.

Interprète des seize opérations du jour 16, avec un registre lié au compteur
ordinal (donné par la directive #ip).
Partie 1 : registre 0 à la fin, en partant de registres nuls.
Partie 2 : avec le registre 0 initialisé à 1, le programme ne termine pas en
temps raisonnable. `python3 s.py trace` l'exécute en affichant chaque
instruction : on y lit le grand entier N calculé par l'initialisation.
programme_traduit.py, traduction à la main du programme, montre qu'il somme
les diviseurs de N (par une double boucle en O(N^2), elle aussi trop lente) :
la réponse est la somme des diviseurs de N.
"""
import sys

# Les seize opérations : nature des opérandes A et B ('r' registre,
# 'i' valeur immédiate, '-' ignoré) et calcul effectué.
OPERATIONS = {
    'addr': ('rr', lambda a, b: a + b),
    'addi': ('ri', lambda a, b: a + b),
    'mulr': ('rr', lambda a, b: a * b),
    'muli': ('ri', lambda a, b: a * b),
    'banr': ('rr', lambda a, b: a & b),
    'bani': ('ri', lambda a, b: a & b),
    'borr': ('rr', lambda a, b: a | b),
    'bori': ('ri', lambda a, b: a | b),
    'setr': ('r-', lambda a, b: a),
    'seti': ('i-', lambda a, b: a),
    'gtir': ('ir', lambda a, b: 1 if a > b else 0),
    'gtri': ('ri', lambda a, b: 1 if a > b else 0),
    'gtrr': ('rr', lambda a, b: 1 if a > b else 0),
    'eqir': ('ir', lambda a, b: 1 if a == b else 0),
    'eqri': ('ri', lambda a, b: 1 if a == b else 0),
    'eqrr': ('rr', lambda a, b: 1 if a == b else 0),
}


def executer(op, args, regs):
    """Renvoie les registres après l'instruction (nouvelle liste). Lève
    ValueError si un opérande registre (ou C) n'est pas un registre valide."""
    a, b, c = args
    modes, calcul = OPERATIONS[op]
    valides = range(len(regs))
    if c not in valides:
        raise ValueError
    valeurs = []
    for mode, v in zip(modes, (a, b)):
        if mode == 'r':
            if v not in valides:
                raise ValueError
            v = regs[v]
        valeurs.append(v)
    regs2 = regs[:]
    regs2[c] = calcul(*valeurs)
    return regs2


def lire(texte):
    lignes = texte.split('\n')
    registre_pc = int(lignes[0].split()[1])
    instructions = [(l.split()[0], list(map(int, l.split()[1:])))
                    for l in lignes[1:]]
    return registre_pc, instructions


def executer_programme(registre_pc, instructions, r0, trace=False):
    regs = [0] * 6
    regs[0] = r0
    while regs[registre_pc] < len(instructions):
        op, args = instructions[regs[registre_pc]]
        avant = regs
        regs = executer(op, args, regs)
        if trace:
            print(op, *args, avant, '->', regs)
        regs[registre_pc] += 1
    return regs


def partie1(registre_pc, instructions):
    return executer_programme(registre_pc, instructions, 0)[0]


with open('input.txt') as f:
    registre_pc, instructions = lire(f.read().strip())
if 'trace' in sys.argv:
    executer_programme(registre_pc, instructions, 1, trace=True)
else:
    print(partie1(registre_pc, instructions))
    print('partie 2 : voir programme_traduit.py')
