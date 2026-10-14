"""Advent of Code 2018, jour 21 : interprète utilisé pour l'exploration.

Exécute le programme d'entrée (mêmes opérations qu'aux jours 16 et 19) en
affichant l'état des registres aux instructions 6 et 12, pour comprendre ce
que calcule la boucle. Avec le registre 0 nul, le programme ne s'arrête
jamais : interrompre avec Ctrl+C. La solution est dans programme_traduit.py.
"""

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


with open('input.txt') as f:
    lignes = f.read().strip().split('\n')
registre_pc = int(lignes[0].split()[1])
instructions = [(l.split()[0], list(map(int, l.split()[1:])))
                for l in lignes[1:]]

regs = [0] * 6
while regs[registre_pc] < len(instructions):
    op, args = instructions[regs[registre_pc]]
    avant = regs
    regs = executer(op, args, regs)
    if regs[registre_pc] in [12, 6]:
        print(op, *args, avant, '->', regs)
    regs[registre_pc] += 1
print(regs[0])
