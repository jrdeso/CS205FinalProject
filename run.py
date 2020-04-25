import argparse
import os

from towerd.Game import Game


def init_parser():
    parser = argparse.ArgumentParser(description='Tower Defence')
    parser.add_argument('--width', type=int, default=800,
                        help='Width of the window')
    parser.add_argument('--height', type=int, default=600,
                        help='Height of the window')
    parser.add_argument('-d', '--datapath', type=str, default='data',
                        help='The game data files.')
    return parser


args = init_parser().parse_args()
game = Game(width=args.width, height=args.height, datadir=args.datapath)
game.run('data/maps/default.json')
