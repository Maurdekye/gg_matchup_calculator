from argparse import ArgumentParser
from pathlib import Path
from csv import DictReader
from itertools import *
from functools import *

parser = ArgumentParser("Calculate character rankings based on matchup data")
parser.add_argument("file", type=Path, help="CSV file containing character matchup data")
parser.add_argument("--max-settle", type=float, default=0.000001, help="Wait unil the final scores settle this much before giving a final answer")
parser.add_argument("--max-iters", type=int, default=1000, help="Max number of iterations before manually exiting")

def main(args):
    with args.file.open(newline='') as file:
        data = {r['VS'] : {c: float(m)/100 for c, m in r.items() if c not in ['VS', r['VS']]} for r in DictReader(file)}
    
    scores = {c: 0 for c in data.keys()}
    grand_mult = 1
    iters = 0
    hit_max_iters = False
    while True:
        mults = {c: 2**s for c, s in scores.items()}
        scores = {c: sum((2*s - 1) * mults[o] * grand_mult for o, s in data[c].items()) for c in data.keys()}
        total_abs_score = sum(abs(s) for s in scores.values())
        last_grand_mult = grand_mult
        grand_mult = 1 / total_abs_score
        mult_diff = abs(last_grand_mult - grand_mult)
        iters += 1
        if mult_diff < args.max_settle:
            break
        if iters >= args.max_iters:
            hit_max_iters = True
            break
    
    if hit_max_iters:
        print(f"Did not settle after {iters} iterations! data must be weird owO")
    
    print(f"""Took {iters} iterations to settle to a grand multiplier of {grand_mult}.
These are the individual ranking scores:""")
    for i, (c, s) in enumerate(sorted(scores.items(), key=lambda x:x[1], reverse=True)):
        print(f"{i+1}. {c}: {s}")

if __name__ == "__main__":
    main(parser.parse_args())