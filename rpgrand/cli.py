import argparse

from pprint import pprint

from categories import Category

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c", help="Config map")
    parser.add_argument("--output", "-o", help="Output template")
    parser.add_argument("--num", "-n", type=int, default=1, help="Number of items to create")
    args = parser.parse_args()

    c = Category.create(args.config)
    for n in range(args.num):
        pprint(c)
