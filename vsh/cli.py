#!/usr/bin/env python3
import argparse
import importlib
from . import scripts


def lazy_import(name):
    module = importlib.import_module(name)
    return module


def parse_app_args(args=None):
    parser = argparse.ArgumentParser(description='vsh command line utility')
    subparsers = parser.add_subparsers(dest='command', required=True)
    scripts.setup(subparsers)
    return parser.parse_args()


def main():
    args = parse_app_args()
    command = lazy_import('vsh.scripts.'+args.command)
    command.run(args)

if __name__ == "__main__":
    main()
