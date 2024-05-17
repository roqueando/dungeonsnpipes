import base
import sys
import json


def main():
    print("extracting spells...")

    spells = base.get_spells_from_api()
    sys.stdout.write(json.dumps(spells))


if __name__ == '__main__':
    main()
