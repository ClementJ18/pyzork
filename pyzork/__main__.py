import argparse

parser = argparse.ArgumentParser(description='Create the boilerplate code for your adventure')
parser.add_argument('start', help='Setup this directory for your adventure with some boilerplate')
args = parser.parse_args()

if args.start:
    #do boilerplate
    pass

