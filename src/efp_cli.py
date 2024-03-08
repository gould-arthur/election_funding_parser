#!/usr/bin/env python3
"""
CLI setup for Election Funding Parser
Author: Arthur H. Gould
"""
from argparse import ArgumentParser
from efp_populator import Populator
from os import remove


def cli_main():

    parser = ArgumentParser()
    parser.add_argument('-y', '--year', type=int, required=True,
                        help="year between 1980 and 2014 to parse data")
    parser.add_argument('-o', '--output_db', type=str, required=False,
                        default="base_populated.db",
                        help="filename to store database as")
    parser.add_argument('-i', '--ignore_existing', action='store_true',
                        required=False, default=False,
                        help="set flag to ignore existing files and download regardless of \
                            whether or not files exist")
    parser.add_argument('-c', '--clean', default=False, action='store_true',
                        help="When set, program will remove all created files aside from the log file")
    parser.add_argument('-l', '--lower-memory', action='store_true', default=False,
                        help="flag to signify that device has lower memory. Will result in slower execution")

    args = parser.parse_args()

    p = Populator(args.output_db, args.ignore_existing, args.lower_memory)
    with p:
        try:
            p.populate(args.year)
        except KeyError:
            print(f"Invalid Date '{args.year}'\n"
                  "Date must be an election (even) year between 1980 and 2014")

    if args.clean:
        remove(p._database_name)
        remove(f"data_{args.year}.gz")


if __name__ == "__main__":
    cli_main()
