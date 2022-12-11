from argparse import ArgumentParser
from pathlib import Path

parser = ArgumentParser("Calculate character rankings based on matchup data")
parser.add_argument("file", type=Path, required=True, help="CSV file containing character matchup data")

def main(args):
    pass

if __name__ == "__main__":
    main(parser.parse_args())