import argparse
from pathlib import Path

from buffer import Buffer


def main():
    parser = argparse.ArgumentParser(prog="trax", description="Edit text files")
    parser.add_argument("file", type=Path)
    args = parser.parse_args()
    file: Path = args.file
    Buffer(file)


main()
