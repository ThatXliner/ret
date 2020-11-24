#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=all
import platform
import subprocess
import shlex
from ret import __version__
from ret.__main__ import ACTION_CHOICES
import pytest


def _pipe_command(command1: str, command2: str) -> str:
    return (
        subprocess.check_output(
            shlex.split(command2),
            stdin=subprocess.Popen(
                shlex.split(command1), stdout=subprocess.PIPE
            ).stdout,
        )
        .decode()
        .strip()
    )


def _grep_on_all(thing_to_grep: str) -> str:
    return (
        f'findstr "{thing_to_grep}"'
        if platform.system() == "Windows"
        else f'grep "{thing_to_grep}"'
    )


def _run_cmd(cmd: str) -> subprocess.CompletedProcess:
    return subprocess.run(shlex.split(cmd))


def _output_of(cmd: str) -> str:
    return subprocess.check_output(shlex.split(cmd)).decode().strip()


class TestClass:
    ls = 'echo "%s"' % "\n".join(
        (
            "LICENSE",
            "README.rst",
            "poetry.lock",
            "pyproject.toml",
            "ret",
            "setup.cfg",
            "tests",
        )
    )

    def test_findall(self):
        assert _pipe_command(self.ls, 'python -m ret ".+" findall') == "\n".join(
            subprocess.check_output(shlex.split(self.ls)).decode().split()
        )

        # Make sure "f" works too
        assert _pipe_command(
            self.ls, R' python -m ret "(\w+)\..{4}" f -g 1'
        ) == "\n".join(("poetry", "pyproject"))
        assert _pipe_command(
            self.ls, R' python -m ret "(?P<some_long_group_name>\w+)\..{4}" f -g some_long_group_name'
        ) == "\n".join(("poetry", "pyproject"))


    def test_search(self):
        assert _pipe_command(
            self.ls, R'python -m ret "LICENSE" search'
        ) == _pipe_command(self.ls, _grep_on_all("LICENSE"))
        assert _pipe_command(
            self.ls, R'python -m ret "LICENSE" search --ignore-case --extended-re'
        ) == _pipe_command(self.ls, _grep_on_all("LICENSE"))

    def test_match(self):
        ...

    def test_meta(self):
        assert _output_of("python -m ret --version") == __version__
        assert _run_cmd("python -m ret --help").returncode == 0

    def test_raises(self):
        _run_cmd("python -m ret").returncode == 2
        _run_cmd('python -m ret "Some regex"').returncode == 2
        with pytest.raises(subprocess.CalledProcessError):
            assert _output_of(
                'python -m ret "some regex" invalid_action'
            ) == "ret: error: argument ACTION: invalid choice: '%s' (choose from %s)" % (
                "invalid_action",
                ", ".join((f"'{x}'" for x in ACTION_CHOICES)),
            )

    def test_flags(self):
        assert (
            _pipe_command(self.ls, ' python -m ret "LICeNSE" --ignore-case -i f')
            == "LICENSE"
        )
        assert (
            _pipe_command(
                self.ls,
                ' python -m ret " \n\n# Comments yay\nLICENSE     " -x --extended-re f',
            )
            == "LICENSE"
        )
        assert (
            _pipe_command(self.ls, ' python -m ret "ret" -i --ignore-case f') == "ret"
        )
        als = 'echo "%s"' % "\n".join(
            (
                "LCÎCENSE",
                "LREADME.rst",
                "poetry.lock",
                "pyproject.toml",
                "ret.no",
                "setup.cfg",
                "tests.yes",
            )
        )
        assert (
            _pipe_command(als, R' python -m ret "L\w+" -a --ascii f')
            == "LC\nLREADME"
        )
        assert (
            _pipe_command(self.ls, 'python -m ret "LICENSE" -m --multiline f')
            == "LICENSE"
        )
