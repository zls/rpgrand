import argparse

from .output import render

from .config_map import ConfigMap
from .categories import Category

SEP = '---'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c",
                        required=True,
                        help="Config map")
    parser.add_argument("--output", "-o",
                        help="Output template")
    parser.add_argument("--num", "-n", type=int, default=1, help="Number of items to create")
    args = parser.parse_args()

    cm = ConfigMap(args.config)
    c = Category.create(cm)
    count = 0
    for n in range(args.num):
        if count > 0:
            print(SEP)
        print(render(args.output, c.items))
        count += 1
