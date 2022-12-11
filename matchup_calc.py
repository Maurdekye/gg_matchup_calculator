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

    scores, grand_mult, _, iters, hit_max_iters = next(dropwhile(
        lambda params: params[2] >= args.max_settle and not params[4],
        accumulate(
            count(1),
            lambda params, it: (
                (lambda scores, grand_mult: (
                    (lambda new_scores: (
                        (lambda new_grand_mult: (
                            new_scores,
                            new_grand_mult,
                            abs(grand_mult - new_grand_mult),
                            it,
                            it >= args.max_iters,
                        ))(
                            1 / sum(abs(s) for s in new_scores.values()), 
                        )
                    ))(
                        {c: sum((2*s - 1) * 2**scores[o] * grand_mult for o, s in data[c].items()) for c in data.keys()},
                    )
                ))(
                    params[0],
                    params[1],
                )
            ),
            initial = ({c: 0 for c in data.keys()}, 1, args.max_settle+1, 0, False),
        ),
    ))

    if hit_max_iters:
        print(f"Did not settle after {iters} iterations! data must be weird owO")
    
    print(f"""Took {iters} iterations to settle to a grand multiplier of {grand_mult}.
These are the individual ranking scores:""")
    for i, (c, s) in enumerate(sorted(scores.items(), key=lambda x:x[1], reverse=True)):
        print(f"{i+1}. {c}: {s}")

if __name__ == "__main__":
    main(parser.parse_args())