#!/usr/bin/env python
import sys
import argparse

from eusurvey import engine

parser = argparse.ArgumentParser()
parser.add_argument('--ingest', help='Imports the given URL.')

if __name__ == "__main__":
    args = parser.parse_args()
    if args.ingest:
        engine.import_survey(args.ingest)
    sys.exit(0)
