import argparse

import output

from categories import Category

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c",
                        required=True,
                        help="Config map")
    parser.add_argument("--output", "-o",
                        required=True,
                        help="Output template")
    parser.add_argument("--num", "-n", type=int, default=1, help="Number of items to create")
    args = parser.parse_args()

    c = Category.create(args.config)
    for n in range(args.num):
        print(output.render(args.output, c.items))
