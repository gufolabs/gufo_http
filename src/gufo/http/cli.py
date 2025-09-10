# ---------------------------------------------------------------------
# Gufo HTTP: Httpd context manager
# ---------------------------------------------------------------------
# Copyright (C) 2024-25, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------
"""
`gufo-http` command-line utility.

Attributes:
    NAME: Utility name
"""

# Python modules
import argparse
import sys
from enum import IntEnum
from http import HTTPStatus
from typing import List, NoReturn, Optional

from gufo.http import HttpError

# Gufo HTTP modules
from gufo.http.sync_client import HttpClient

NAME = "gufo-http"


class ExitCode(IntEnum):
    """
    Cli exit codes.

    Attributes:
        OK: Successful exit
    """

    OK = 0
    ERR = 1


class Cli(object):
    """`gufo-thor` CLI utility class."""

    def die(self, msg: Optional[str] = None) -> NoReturn:
        """Die with message."""
        if msg:
            print(msg)
        sys.exit(1)

    def run(self: "Cli", args: List[str]) -> ExitCode:
        """
        Parse command-line arguments and run appropriate command.

        Args:
            args: List of command-line arguments
        Returns:
            ExitCode
        """
        # Prepare command-line parser
        parser = argparse.ArgumentParser(prog=NAME, description="HTTP Client")
        parser.add_argument("url", nargs=1, help="URL")
        parser.add_argument(
            "-o", "--output", required=False, help="Write output to file"
        )
        # Parse arguments
        ns = parser.parse_args(args)
        # Prepare parameters
        url = ns.url[0]
        output_path: Optional[str] = ns.output
        if output_path and output_path == "-":
            output_path = None
        # Fetch
        with HttpClient() as client:
            try:
                r = client.get(url)
            except (HttpError, ConnectionError, TimeoutError) as e:
                self.die(f"ERROR: {e}")
            if r.status != HTTPStatus.OK.value:
                self.die(f"Invalid response code: {r.status}")
            if output_path:
                try:
                    with open(output_path, "w") as fp:
                        fp.write(r.content.decode())
                except OSError as e:
                    self.die(f"ERROR: {e.args[1]}")
            else:
                print(r.content.decode())
        return ExitCode.OK


def main() -> int:
    """Run `noc-thor` with command-line arguments."""
    return Cli().run(sys.argv[1:]).value
