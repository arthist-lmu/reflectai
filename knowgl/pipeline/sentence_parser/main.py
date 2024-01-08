import os
import sys
import re
import argparse
from pipeline.plugin import Plugin
from pipeline.manager import Manager


def parse_args():
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("-v", "--verbose", action="store_true", help="verbose output")
    parser.add_argument("-p", "--plugin", help="verbose output")
    parser.add_argument(
        "-t", "--text", required=True, help="text for language detection"
    )
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    manager = Manager(os.path.abspath(os.path.dirname(__file__)))
    plugin = manager.build_plugin(args.plugin)
    # # coreference_resolution = FCoref()

    print(plugin(args.text))

    return 0


if __name__ == "__main__":
    sys.exit(main())
