#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Initial author: Bryan Hu .

@ThatXliner .

Version: v0.1.0

A regex tool for the command line

Better than ``grep`` 😃👍

"""
import argparse
import functools
import re
import sys
import operator
from typing import List, Match, Optional, Pattern, Union
import collections.abc
from . import __version__


ACTION_CHOICES: List[str] = ["match", "m", "search", "s", "findall", "f"]

parser = argparse.ArgumentParser(
    description="A regex tool for the command line",
    prog="ret",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument("regex", help="The regex to use", nargs="+")
parser.add_argument(
    "action",
    choices=ACTION_CHOICES,
    nargs="?",
    help="What to do with the regex",
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
    help="Print the version information and exit",
)


flags = parser.add_argument_group("flags", description="The regex flags to add")

flags.add_argument(
    "-i",
    "--ignore-case",
    action="append_const",
    const=re.IGNORECASE,
    help="Regex match case insensitively",
    dest="re_flags",
)
flags.add_argument(
    "-x",
    "--extended-re",
    action="append_const",
    const=re.VERBOSE,
    help="Use extended regex",
    dest="re_flags",
)
flags.add_argument(
    "-a",
    "--ascii",
    action="append_const",
    help="Use ascii-only matching",
    const=re.ASCII,
    dest="re_flags",
)
flags.add_argument(
    "-m",
    "--multiline",
    action="append_const",
    const=re.MULTILINE,
    help="Use multiline matching",
    dest="re_flags",
)
flags.add_argument(
    "-d",
    "--dotall",
    action="append_const",
    const=re.DOTALL,
    help="Use dot-all matching",
    dest="re_flags",
)
parser.add_argument(
    "--verbose",
    "--debug",
    action="store_true",
    help="Activate verbose output (a.k.a. debug mode)",
    default=False,
)

args = parser.parse_args()

RE_FLAGS: int = functools.reduce(
    operator.or_, args.re_flags if args.re_flags is not None else [], 0  # type: ignore
)
pattern: Pattern[str] = re.compile(args.regex[0], flags=RE_FLAGS)  # type: ignore
action: str = args.action  # "match", "search" or "findall"

# NOTE: Memory-map?
with args.input as f:  # type: ignore
    INPUT: str = f.read()  # type: ignore

# Determine what action to take
if args.action in {"match", "m"}:  # type: ignore
    OUTPUT: Union[List[str], Optional[Match[str]]] = pattern.match(INPUT)
elif args.action in {"search", "s"}:  # type: ignore
    OUTPUT = pattern.search(INPUT)

elif args.action in {"findall", "f"}:  # type: ignore
    OUTPUT = pattern.findall(INPUT)
# elif args.action in {"split", "sp"}:  # type: ignore
#     OUTPUT = pattern.split(INPUT)

else:
    raise NotImplementedError

if not OUTPUT:  # It didn't match 😔
    sys.exit(1)

# If the output is a sequence
elif isinstance(OUTPUT, collections.abc.Sequence):
    print("\n".join(OUTPUT))

else:  # It matched 😄
    # Get the group to return (default is 0, the entire match)
    try:
        GROUP: Union[str, int] = int(args.group)  # type: ignore
    except ValueError:
        GROUP: Union[str, int] = str(args.group)  # type: ignore

    # Print the group
    try:
        assert OUTPUT
        print(OUTPUT[GROUP])
    except IndexError as index:
        raise ValueError(
            f"{GROUP} is not a valid group identifier. You probably did a typo..."
        ) from index

sys.exit(0)
