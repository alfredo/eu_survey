#!/usr/bin/env python
import sys
import argparse

from eusurvey import engine

parser = argparse.ArgumentParser()
parser.add_argument('--ingest', help='Imports the given URL.')
parser.add_argument('--update', action='store_true')
parser.add_argument('--forward', help='Submits the given URL.')
parser.add_argument('--map', help='Maps given survey URL.')


if __name__ == "__main__":
    args = parser.parse_args()
    if args.ingest:
        engine.import_survey(args.ingest, args.update)
    elif args.forward:
        engine.submit_surveys(args.forward)
    elif args.map:
        engine.map_survey(args.map)
    sys.exit(0)
