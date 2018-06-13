import argparse
import sys

from . import __version__

from .output import render

from .config_map import ConfigMap
from .categories import Category

SEP = '---'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c",
                        help="Config map")
    parser.add_argument("--output", "-o",
                        help="Output template")
    parser.add_argument("--num", "-n", type=int, default=1, help="Number of items to create")
    parser.add_argument('--version', '-v', action='store_true')
    args = parser.parse_args()

    if args.version:
        print(__version__)
        sys.exit(0)

    cm = ConfigMap(args.config)
    c = Category.create(cm)
    count = 0
    for n in range(args.num):
        if count > 0:
            print(SEP)
        print(render(args.output, c.items))
        count += 1
