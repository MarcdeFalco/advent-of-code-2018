"""Advent of Code 2018, jour 16 : identifier les codes d'opération.

`executer` implémente les seize opérations ; elle lève ValueError sur un
registre invalide, ce qui élimine aussi des candidats. Pour chaque exemple
(avant, instruction, après), on calcule l'ensemble des opérations
compatibles. Partie 1 : nombre d'exemples compatibles avec au moins trois
opérations. Partie 2 : on intersecte ces ensembles par code, puis, comme au
sudoku, on fixe un code qui n'a plus qu'un candidat et on retire cette
opération des autres ; on exécute enfin le programme et on lit le registre 0.
La propagation continue jusqu'à ce que tous les codes soient fixés, y
compris les derniers singletons.
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


def lire(texte):
    """Renvoie la liste des exemples et le programme de test."""
    lignes = texte.split('\n')
    exemples = []
    i = 0
    while i + 2 < len(lignes) and lignes[i] != '':
        avant = eval(lignes[i][len('Before: '):])
        instruction = list(map(int, lignes[i + 1].split()))
        apres = eval(lignes[i + 2][len('After:  '):])
        exemples.append((avant, instruction, apres))
        i += 4
    programme = [list(map(int, l.split())) for l in lignes[i + 2:]]
    return exemples, programme


def compatibles(avant, instruction, apres):
    _, a, b, c = instruction
    ops = []
    for op in OPERATIONS:
        try:
            if executer(op, [a, b, c], avant) == apres:
                ops.append(op)
        except ValueError:
            pass
    return ops


def partie1(exemples, programme):
    return sum(1 for e in exemples if len(compatibles(*e)) >= 3)


def partie2(exemples, programme):
    candidats = {code: set(OPERATIONS) for code in range(16)}
    for avant, instruction, apres in exemples:
        code = instruction[0]
        candidats[code] &= set(compatibles(avant, instruction, apres))

    correspondance = {}
    while candidats:
        code = next(c for c, ops in candidats.items() if len(ops) == 1)
        op = candidats.pop(code).pop()
        correspondance[code] = op
        for ops in candidats.values():
            ops.discard(op)

    regs = [0, 0, 0, 0]
    for code, a, b, c in programme:
        regs = executer(correspondance[code], [a, b, c], regs)
    return regs[0]


with open('input.txt') as f:
    exemples, programme = lire(f.read().strip())
print(partie1(exemples, programme))
print(partie2(exemples, programme))
