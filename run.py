import argparse
import os
os.environ['DATA_DIR'] = os.environ.get('DATA_DIR', 'data')
os.environ['ASSET_DIR'] = os.environ.get('ASSET_DIR', 'asset')

from towerd.Game import Game


def init_parser():
    parser = argparse.ArgumentParser(description='Tower Defence')
    parser.add_argument('--width', type=int, default=800,
                        help='Width of the window')
    parser.add_argument('--height', type=int, default=600,
                        help='Height of the window')
    return parser


args = init_parser().parse_args()
game = Game(width=args.width, height=args.height)
game.start()
