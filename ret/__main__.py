#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Initial author: Bryan Hu .

@ThatXliner .

Version: v0.1.2

A pure-python command-line regular expression tool for
stream filtering, extracting, and parsing.

Better than ``grep`` 😃👍

"""
import argparse
import functools
import operator
import re
import sys
from collections.abc import Iterable
from typing import Iterator, List, Match, NoReturn, Optional, Pattern, Union

from . import __version__, cmd_opts

ACTION_CHOICES: List[str] = ["match", "m", "search", "s", "findall", "f"]


###
# Main parser
###

parser = argparse.ArgumentParser(
    description="A regex tool for the command line",
    prog="ret",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument("regex", help="The regex to use")
parser.add_argument(
    "input",
    nargs="?",
    help="The input file to read from",
    default=sys.stdin,
    type=argparse.FileType(mode="r"),
)

parser.add_argument(
    "--version",
    action="version",
    version=__version__,
    help="Print the version information and exit. "
    "It's very minimal: just the version number. "
    "No program name, nada.",
)
parser.add_argument(
    "--verbose",
    "--debug",
    action="store_true",
    help="Activate verbose output (a.k.a. debug mode)",
    default=False,
)

###
# Actions
###
flag_with_group = [cmd_opts.with_flags, cmd_opts.with_group]
actions = parser.add_subparsers(
    title="actions",
    dest="action",
    metavar="ACTION",
    help="What to do with the regex. Options are %s" % ", ".join(ACTION_CHOICES),
)
match_parser = actions.add_parser("match", aliases=("m"), parents=flag_with_group)

search_parser = actions.add_parser("search", aliases=("s"), parents=flag_with_group)

findall_parser = actions.add_parser("findall", aliases=("f"), parents=flag_with_group)
findall_parser.add_argument(
    "--output-sep", "-s", help="Output separator", default="\n", dest="sep"
)


def main() -> NoReturn:
    """The main CLI entry point.

    Returns
    -------
    NoReturn
        It exits via sys.exit

    """

    args = parser.parse_args()
    re_flags: int = functools.reduce(
        operator.or_,  # type: ignore
        args.re_flags if args.re_flags is not None else [0],  # type: ignore
    )
    pattern: Pattern[str] = re.compile(
        args.regex,  # type: ignore
        flags=re_flags or 0,
    )

    # NOTE: Memory-map?
    with args.input as input_file:  # type: ignore
        text_input: str = input_file.read()  # type: ignore

    # Default to "search"
    action: str = args.action or "search"  # type: ignore

    # Determine what action to take
    if action in {"match", "m"}:
        output: Union[Iterator[Match[str]], Optional[Match[str]]] = pattern.match(
            text_input
        )
    elif action in {"search", "s"}:
        output = pattern.search(text_input)

    elif action in {"findall", "f"}:
        output = pattern.finditer(text_input)

    # elif args.action in {"split", "sp"}:  # type: ignore
    #     output = pattern.split(INPUT)
    else:
        raise NotImplementedError

    if not output:  # It didn't match
        sys.exit(1)

    # It matched!
    # Get the group to return (default is 0, the entire match)
    try:
        group: Union[str, int] = int(args.group)  # type: ignore
    except ValueError:
        group: Union[str, int] = str(args.group)  # type: ignore

    # Print the group
    try:
        assert output
        if isinstance(output, Iterable):  # If it was `findall`
            assert isinstance(args.sep, str)  # type: ignore
            print(args.sep.join([match[group] for match in output]))
        else:
            print(output[group])
    except IndexError as index:
        raise ValueError(
            f"{group} is not a valid group identifier. You probably did a typo..."
        ) from index
    sys.exit(0)


if __name__ == "__main__":
    main()
