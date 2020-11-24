#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Initial author: Bryan Hu .

@ThatXliner .

Version: v0.1.1

A pure-python command-line regular expression tool for
stream filtering, extracting, and parsing.

Better than ``grep`` 😃👍

"""
import argparse
import functools
import operator
import re
import sys
from typing import List, Match, Optional, Pattern, Union, Iterator, NoReturn
from collections.abc import Iterable
from . import __version__

ACTION_CHOICES: List[str] = ["match", "m", "search", "s", "findall", "f"]

parser = argparse.ArgumentParser(
    description="A regex tool for the command line",
    prog="ret",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

parser.add_argument("regex", help="The regex to use")
parser.add_argument(
    "action",
    choices=ACTION_CHOICES,
    help="What to do with the regex. Options are %s" % ", ".join(ACTION_CHOICES),
    metavar="ACTION",
    default="search",
)
parser.add_argument(
    "input",
    nargs="?",
    help="The input file to read from",
    default=sys.stdin,
    type=argparse.FileType(mode="r"),
)

parser.add_argument(
    "--group", "-g", help="The group to return", default="0", dest="group"
)
parser.add_argument(
    "--version",
    action="version",
    version=__version__,
    help="Print the version information and exit. "
    "It's very minimal: just the version number. "
    "No program name, nada.",
)


flags = parser.add_argument_group("flags", description="The regex flags to add")

flags.add_argument(
    "-i",
    "--ignore-case",
    action="append_const",
    const=re.IGNORECASE,
    help="Match case-insensitively",
    dest="re_flags",
)
flags.add_argument(
    "-x",
    "--extended-re",
    action="append_const",
    const=re.VERBOSE,
    help="Use extended regex where whitespace doesn't matter and you can use # Comments",
    dest="re_flags",
)
flags.add_argument(
    "-a",
    "--ascii",
    action="append_const",
    const=re.ASCII,
    help=R"Make \w, \W, \b, \B, \d, \D, \s and \S only match ASCII characters",
    dest="re_flags",
)
flags.add_argument(
    "-m",
    "--multiline",
    action="append_const",
    const=re.MULTILINE,
    help="Use multiline matching. `^` and `$` will now match the beginning "
    "and end of each line.",
    dest="re_flags",
)
flags.add_argument(
    "-d",
    "--dotall",
    action="append_const",
    const=re.DOTALL,
    help="Make `.` also match whitespace characters",
    dest="re_flags",
)
parser.add_argument(
    "--verbose",
    "--debug",
    action="store_true",
    help="Activate verbose output (a.k.a. debug mode)",
    default=False,
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

    # Determine what action to take
    if args.action in {"match", "m"}:  # type: ignore
        output: Union[Iterator[Match[str]], Optional[Match[str]]] = pattern.match(
            text_input
        )
    elif args.action in {"search", "s"}:  # type: ignore
        output = pattern.search(text_input)

    elif args.action in {"findall", "f"}:  # type: ignore
        output = pattern.finditer(text_input)

    # elif args.action in {"split", "sp"}:  # type: ignore
    #     output = pattern.split(INPUT)
    else:
        raise NotImplementedError

    if not output:  # It didn't match 😔
        sys.exit(1)

    # It matched 😄
    # Get the group to return (default is 0, the entire match)
    try:
        group: Union[str, int] = int(args.group)  # type: ignore
    except ValueError:
        group: Union[str, int] = str(args.group)  # type: ignore

    # Print the group
    try:
        assert output
        if isinstance(output, Iterable):  # If it was `findall`
            print("\n".join([match[group] for match in output]))
        else:
            print(output[group])
    except IndexError as index:
        raise ValueError(
            f"{group} is not a valid group identifier. You probably did a typo..."
        ) from index
    sys.exit(0)


if __name__ == "__main__":
    main()
