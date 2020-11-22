# pylint: disable=all
import platform
import subprocess
import shlex


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


class TestClass:
    def test_findall(self):
        if not platform.system() == "Windows":  # *nix tests
            assert _pipe_command("ls -1", R'python -m ret ".+" findall') == "\n".join(
                subprocess.check_output(shlex.split("ls -1")).decode().split()
            )
            assert _pipe_command(
                "ls -1 ", R' python -m ret "(\w+)\..{4}" f -g 1'
            ) == "\n".join(
                ("poetry", "pyproject")
            )  # All files with an extension of length 4
        else:  # Windows tests
            assert True

    def test_search(self):
        if not platform.system() == "Windows":  # *nix tests
            ...
        else:  # Windows tests
            assert True

    def test_match(self):
        if not platform.system() == "Windows":  # *nix tests
            ...
        else:  # Windows tests
            assert True
