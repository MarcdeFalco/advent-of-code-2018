"""Advent of Code 2018, jour 10 : points mobiles qui écrivent un message.

On fait avancer les points seconde par seconde et l'on n'affiche la grille
que lorsque la boîte englobante est petite (au plus 500 de côté). Le message
(partie 1) se lit à l'œil sur l'affichage, et la seconde affichée au-dessus
est la réponse de la partie 2 : le script est un outil de visualisation et
ne calcule pas lui-même les réponses.
"""
import re

FORMAT = re.compile(r'position=<(.*),(.*)> velocity=<(.*),(.*)>')

with open('input.txt') as f:
    points = [list(map(int, FORMAT.match(ligne).groups()))
              for ligne in f.read().strip().split('\n')]

for seconde in range(1, 100000):
    for p in points:  # p = [x, y, vx, vy]
        p[0] += p[2]
        p[1] += p[3]
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    if max(ys) - min(ys) > 500 or max(xs) - min(xs) > 500:
        continue
    positions = {(p[0], p[1]) for p in points}
    print(seconde)
    for y in range(min(ys), max(ys) + 1):
        print(''.join('#' if (x, y) in positions else ' '
                      for x in range(min(xs), max(xs) + 1)))
    print()
