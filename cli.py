import argparse
import __main__

if __name__ == "__main__":
    print("Can't run cli.py on its own...")
    exit(1)

__parser__ = argparse.ArgumentParser(
                    prog=f'Advent of Code 2024 - Day {__main__.__file__.split("_")[1].split(".")[0]}',
                    description='Solves the Advent of Code problems of the given day')
__parser__.add_argument('-v', '--verbose', action='store_true', help="Print out verbose info.")
__parser__.add_argument('-i', '--visualize', action='store_true', help="Show problem visualization, if available.")
__parser__.add_argument('-s', '--sample', action='store_true', help="Use sample data if available.")

__args__ = __parser__.parse_args()

verbose = __args__.verbose
visualize = __args__.visualize
sample = __args__.sample
