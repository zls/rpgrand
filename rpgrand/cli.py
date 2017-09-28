import argparse

from .output import render

from .categories import Category

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c",
                        required=True,
                        help="Config map")
    parser.add_argument("--output", "-o",
                        help="Output template")
    parser.add_argument("--num", "-n", type=int, default=1, help="Number of items to create")
    args = parser.parse_args()

    c = Category.create(args.config)
    for n in range(args.num):
        print(render(args.output, c.items))
