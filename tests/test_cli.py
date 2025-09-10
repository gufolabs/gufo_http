# ---------------------------------------------------------------------
# Gufo HTTP: CLI tests
# ---------------------------------------------------------------------
# Copyright (C) 2024-25, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------

# Python modules
import tempfile
from typing import List, Optional

# Third-party modules
import pytest

# Gufo HTTP modules
from gufo.http.cli import Cli, ExitCode
from gufo.http.httpd import Httpd


class GuardedCli(Cli):
    def die(self, msg: Optional[str] = None) -> None:
        """Die with message."""
        raise RuntimeError(msg or "")


@pytest.mark.parametrize(
    "args",
    [[], ["-o-"], ["-o", "/dev/stdout", "--output=-"]],
)
def test_cli_get_stdout(
    httpd: Httpd, capsys: pytest.CaptureFixture[str], args: List[str]
) -> None:
    cli_args = [*args, httpd.prefix]
    r = GuardedCli().run(cli_args)
    captured = capsys.readouterr()
    assert r == ExitCode.OK
    assert "</html>" in captured.out


def test_cli_get_localhost(httpd: Httpd, capsys: pytest.CaptureFixture[str]) -> None:
    r = GuardedCli().run(["http://localhost/"])
    captured = capsys.readouterr()
    assert r == ExitCode.OK
    assert "</html>" in captured.out


def test_cli_get_file(
    httpd: Httpd,
) -> None:
    with tempfile.NamedTemporaryFile() as tmp:
        cli_args = ["-o", tmp.name, httpd.prefix]
        r = GuardedCli().run(cli_args)
        assert r == ExitCode.OK
        with open(tmp.name) as fp:
            data = fp.read()
            assert "</html>" in data


def test_cli_get_wrong_file(
    httpd: Httpd,
) -> None:
    path = "/tmpxxxxxx/yyyyy/zzzzzz"  # noqa: S108
    cli_args = ["-o", path, httpd.prefix]
    with pytest.raises(RuntimeError):
        GuardedCli().run(cli_args)


def test_cli_get_invalid_url(
    httpd: Httpd,
) -> None:
    with pytest.raises(RuntimeError):
        GuardedCli().run(["https://test.example.com/"])
