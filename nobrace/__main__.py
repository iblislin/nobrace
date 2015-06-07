import sys

from .converter import Converter


if __name__ == '__main__':
    try:
        filename = sys.argv[1]
    except:
        sys.exit(1)

    c = Converter(filename)
    c.convert()
