#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Initial author: Bryan Hu.

@ThatXliner.

A file containing the configuration argument parser objects

"""
import argparse
import re

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
