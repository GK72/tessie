#!/usr/bin/env python3

"""Entrypoint to running tests"""

import argparse

from typing import List, Tuple

DESCRIPTION: str = """
Tessie Framework
"""

EPILOG: str = """
The test definitions must be given in a Python script and must have a
`run_test` function receiving a `dict` with the command line arguments.
"""

def main(args: argparse.Namespace, fwd_args: List[str]) -> None:
    """ Read test definitions from file and execute them """

    with open(args.tests, "r", encoding="utf-8") as inf:
        exec(inf.read(), globals())                                                                 # pylint: disable=W0122
        run_test(fwd_args)                                                                          # type: ignore # pylint: disable=E0602 # Customization point


def parse_args() -> Tuple[argparse.Namespace, List[str]]:
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(description=DESCRIPTION, epilog=EPILOG)
    parser.add_argument("tests", help="Test definitions")

    return parser.parse_known_args()


if __name__ == "__main__":
    argv = parse_args()
    main(argv[0], argv[1])
