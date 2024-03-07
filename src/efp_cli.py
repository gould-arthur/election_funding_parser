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
    parser.add_argument('-d', '--dry_run', default=False, action='store_true',
                        help="When set, program will remove all created files aside from the log file")

    args = parser.parse_args()

    with Populator(args.output_db, args.ignore_existing) as p:
        try:
            p.populate(args.year)

            if args.dry_run:
                remove(p._database_name)
                remove(f"data_{args.year}.gz")
        except KeyError:
            print(f"Invalid Date '{args.year}'\n"
                  "Date must be an election (even) year between 1980 and 2014")


if __name__ == "__main__":
    cli_main()
