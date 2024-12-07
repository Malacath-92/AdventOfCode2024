import argparse
import inspect
import pathlib

if __name__ == "__main__":
    print("Can't run cli.py on its own...")
    exit(1)

for frame in inspect.stack()[1:]:
    if frame.filename[0] != "<":
        prog_name = f'Advent of Code 2024 - Day {pathlib.Path(frame.filename).stem.split("_")[1]}'
        break

__parser__ = argparse.ArgumentParser(
    prog=prog_name,
    description="Solves the Advent of Code problems of the given day",
)
__parser__.add_argument(
    "-v", "--verbose", action="store_true", help="Print out verbose info."
)
__parser__.add_argument(
    "-i",
    "--visualize",
    action="store_true",
    help="Show problem visualization, if available.",
)
__parser__.add_argument(
    "-s", "--sample", action="store_true", help="Use sample data if available."
)

__args__ = __parser__.parse_args()

verbose = __args__.verbose
visualize = __args__.visualize
sample = __args__.sample
