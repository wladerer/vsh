#!/usr/bin/env python3
import argparse
import scripts.bands as bands
import scripts.analysis as analysis
import scripts.db as db
import scripts.slabgen as slabgen
import scripts.freeze as freeze
import scripts.inputs as inputs


def parse_app_args(args=None):
    parser = argparse.ArgumentParser(description='vsh command line utility')
    subparsers = parser.add_subparsers(dest='command')

    #bands
    bands.setup_args(subparsers)

    #analysis
    analysis.setup_args(subparsers)

    #db
    db.setup_args(subparsers)

    #slabgen
    slabgen.setup_args(subparsers)

    #freeze
    freeze.setup_args(subparsers)

    #inputs
    inputs.setup_args(subparsers)

    return parser.parse_args(args)

def main():
    parsed_args = parse_app_args()

    command_map = {
        "bands": bands.run,
        "analysis": analysis.run,
        "db": db.run,
        "slabgen": slabgen.run,
        "freeze": freeze.run,
        "inputs": inputs.run
    }

    command_map[parsed_args.command](parsed_args)

if __name__ == "__main__":
    main()