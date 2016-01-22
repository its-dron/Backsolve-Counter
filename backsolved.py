import csv
from time import strptime

timePattern ="%m/%d/%y %H:%M"

METAS = set()

# Puzzle -> Meta it is in
PUZZLES = { }

# Team name -> ( Puzzle -> Time solved )
SOLVED = {}

# Puzzle -> set of teams that solved
SOLVED_INV = {}

# Puzzle name -> set of teams that backsolved
BACKSOLVED = {}

pname = "puzzles.csv"
fname = "data.csv"

us = "frumious bandersnatch"

# Load puzzles
with open(pname, 'rU') as f:
    linereader = csv.reader(f)
    linereader.next()
    for row in linereader:
        puzzle = row[1].lower()
        meta = row[2].lower()
        PUZZLES[puzzle] = meta
        METAS.add(meta)

with open(fname, 'rU') as f:
    linereader = csv.reader(f)
    linereader.next() # burn header
    for row in linereader:
        time = strptime(row[0], timePattern)
        team = row[1].lower()
        puzzle = row[2].lower()
        isCorrect = row[4] == "CORRECT"
        isMeta = puzzle in METAS

        if isCorrect:
            if team not in SOLVED:
                SOLVED[team] = {}

            if puzzle not in SOLVED_INV:
                SOLVED_INV[puzzle] = set()

            SOLVED[team][puzzle] = time
            SOLVED_INV[puzzle].add(team)

            if not isMeta:
                meta = PUZZLES[puzzle]
                if meta in SOLVED[team]:
                    if puzzle not in BACKSOLVED:
                        BACKSOLVED[puzzle] = set()
                    BACKSOLVED[puzzle].add(team)

# Hardcoding this in because we know we backsolved it but we submitted before the meta
BACKSOLVED["the dogged pursuit of justice, aka: caught red-handed"].add(us)

ratios = {}

for puzzle, teams in BACKSOLVED.items():
    n = len(teams)
    s = len(SOLVED_INV[puzzle])
    r = float(n) / s

    if n > 2:
        ratios[puzzle] = r

import operator

sorted_ratios = sorted(ratios.items(), key=operator.itemgetter(1))

for v in sorted_ratios[::-1]:
	print v[1], len(SOLVED_INV[v[0]]), v[0]
