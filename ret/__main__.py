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
import logging
import operator
import re
import sys
from collections.abc import Iterable
from typing import Iterator, List, Match, NoReturn, Optional, Pattern, Union

from . import __version__

ACTION_CHOICES: List[str] = ["match", "m", "search", "s", "findall", "f"]

###
# Define re-flags options
###

with_flags: argparse.ArgumentParser = argparse.ArgumentParser(add_help=False)
flags = with_flags.add_argument_group("flags", description="The regex flags to add")
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

###
# Define capture group options
###

with_group: argparse.ArgumentParser = argparse.ArgumentParser(add_help=False)
with_group.add_argument(
    "--group", "-g", help="The group to return", default="0", dest="group"
)

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
    dest="verbose",
)

###
# Actions
###

actions = parser.add_subparsers(
    title="actions",
    dest="action",
    metavar="ACTION",
    help="What to do with the regex. Options are %s" % ", ".join(ACTION_CHOICES),
)
match_parser = actions.add_parser(
    "match", aliases=("m"), parents=[with_flags, with_group]
)

search_parser = actions.add_parser(
    "search", aliases=("s"), parents=[with_flags, with_group]
)

findall_parser = actions.add_parser(
    "findall", aliases=("f"), parents=[with_flags, with_group]
)
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
    logging.basicConfig(
        format="%(asctime)s -- %(levelname)s: %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        level=logging.DEBUG if args.verbose else logging.WARN,  # type: ignore
    )
    logging.info("Processing regex flags")
    re_flags: int = functools.reduce(
        operator.or_,  # type: ignore
        args.re_flags if args.re_flags is not None else [0],  # type: ignore
    )
    logging.info("Creating pattern object")
    pattern: Pattern[str] = re.compile(
        args.regex,  # type: ignore
        flags=re_flags or 0,  # XXX: Unnecessary?
    )

    logging.info("Reading file %r", args.input.name)  # type: ignore
    # NOTE: Memory-map?
    with args.input as input_file:  # type: ignore
        text_input: str = input_file.read()  # type: ignore

    # Default to "search"
    action: str = args.action or "search"  # type: ignore
    logging.info("Regex action: %s", action)
    logging.info("Matching...")
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

    logging.info("Did not match, returning...")
    if not output:  # It didn't match
        sys.exit(1)

    # It matched!
    # Get the group to return (default is 0, the entire match)
    try:
        group: Union[str, int] = int(args.group)  # type: ignore
    except ValueError:
        group: Union[str, int] = str(args.group)  # type: ignore
    logging.info("Matched. Capture group: %r", group)

    # Print the group
    try:
        assert output
        if isinstance(output, Iterable):  # If it was `findall`
            assert isinstance(args.sep, str)  # type: ignore
            logging.info(
                "Outputting %r, joined by sep: %r, with group: %r",
                output,
                args.sep,
                group,
            )
            print(args.sep.join([match[group] for match in output]))
        else:
            logging.info("Outputting %r, with group: %r", output, group)
            print(output[group])
    except IndexError as index:
        raise ValueError(
            f"{group} is not a valid group identifier. You probably did a typo..."
        ) from index

    logging.info("Done.")
    sys.exit(0)


if __name__ == "__main__":
    main()
