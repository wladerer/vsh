#!/usr/bin/env python3
import argparse
import scripts
import importlib.util
import sys


def lazy_import(name):
    spec = importlib.util.find_spec(name)
    loader = importlib.util.LazyLoader(spec.loader)
    spec.loader = loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    loader.exec_module(module)
    return module


def parse_app_args(args=None):
    parser = argparse.ArgumentParser(description='vsh command line utility')
    subparsers = parser.add_subparsers(dest='command', required=True)
    scripts.setup(subparsers)
    return parser.parse_args()


def main():
    args = parse_app_args()
    command = lazy_import('scripts.'+args.command)
    command.run(args)

if __name__ == "__main__":
    main()
