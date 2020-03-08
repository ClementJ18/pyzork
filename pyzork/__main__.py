import argparse

parser = argparse.ArgumentParser(description='Create the boilerplate code for your adventure')
parser.add_argument('setup', help='Setup this directory for your adventure with some boilerplate')
parser.add_argument('start', help='Start the adventure in this directory')
args = parser.parse_args()

if args.start:
    #do boilerplate
    pass
elif args.setup:
    #start the adventure
    import game
    
    from pyzork.utils import game_loop
    
    game_loop(game.WORLD)
    

