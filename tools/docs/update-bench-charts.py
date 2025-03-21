# ---------------------------------------------------------------------
# Gufo HTTP: Generate benchmark charts
# ---------------------------------------------------------------------
# Copyright (C) 2024, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------
"""Parse bechmark results and generate charts."""

# Python modules
import enum
import re
from dataclasses import dataclass
from typing import Iterable, List, Tuple

# Third-party modules
import matplotlib.pyplot as plt
from matplotlib import ticker

rx_name = re.compile(r"^Name \(time in (\S+)\)")


@dataclass
class Benchmark(object):
    """Benchmark descriptor.

    Attributes:
        path: Output chart path.
        title: Chart title.
    """

    path: str
    title: str


BENCHMARKS = [
    Benchmark(
        title="Single HTTP/1.1 Requests (Median)",
        path="docs/single_x100_1k.png",
    ),
    Benchmark(
        title="100 Linear HTTP/1.1 Requests (Median)",
        path="docs/linear_x100_1k.png",
    ),
    Benchmark(
        title="100 Parallel HTTP/1.1 Requests (Median)",
        path="docs/p4_x100_1k.png",
    ),
    Benchmark(
        title="Single HTTPS Requests (Median)",
        path="docs/https_single_x100_1k.png",
    ),
    Benchmark(
        title="100 Linear HTTPS Requests (Median)",
        path="docs/https_linear_x100_1k.png",
    ),
    Benchmark(
        title="100 Parallel HTTPS Requests (Median)",
        path="docs/https_p4_x100_1k.png",
    ),
]

NAME_MAP = {"gufo_http": "Gufo HTTP", "pycurl": "PycURL"}


def normalize_name(s: str) -> str:
    """Normalize test name.

    Args:
        s: Test name.

    Returns:
        Normalized name.
    """
    if s.startswith("test_"):
        s = s[5:]
    mode = ""
    if s.endswith("_sync"):
        s = s[:-5]
        mode = " (Sync)"
    elif s.endswith("_async"):
        s = s[:-6]
        mode = " (Async)"
    s = NAME_MAP.get(s, s)
    return f"{s}{mode}"


def build_barchart(
    bench: Benchmark, data: List[Tuple[str, float]], scale: str
) -> None:
    """Build bar chart into PNG file.

    Args:
        bench: Benchmark description.
        data: List of (name, value).
        scale: Time scale label.
    """

    def is_gufo_http(s: str) -> bool:
        return "Gufo HTTP" in s

    # Extracting test names and measured values from the data
    tests, values = zip(*data)

    # Creating the bar chart
    plt.figure(figsize=(10, 6))
    plt.barh(
        tests,
        values,
        color=[
            "#2c3e50" if is_gufo_http(test) else "#34495e" for test in tests
        ],
    )
    plt.xlabel(f"Time ({scale})")
    plt.title(bench.title)
    # Adding thousands separator to y-axis labels
    plt.gca().xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))
    # Adding text annotations for ratio between each bar and smallest one
    min_value = min(values)
    for test, value in zip(tests, values):
        ratio = value / min_value
        fontweight = "bold" if is_gufo_http(test) else "normal"
        plt.text(
            value, test, f" x{ratio:.2f}", va="center", fontweight=fontweight
        )
    # Make y-axis labels bold for test names containing "gufo_http"
    for tick_label in plt.gca().get_yticklabels():
        if is_gufo_http(tick_label.get_text()):
            tick_label.set_weight("bold")
    # Adjusting right padding to shift border to the right
    plt.subplots_adjust(right=1.3)
    # Saving the plot as an SVG file
    print(f"Writing {bench.path}")
    plt.savefig(bench.path, format="png", bbox_inches="tight")
    plt.close()


class Mode(enum.Enum):
    """Parser mode.

    Attributes:
        WAITING: Waiting for table of results.
        SKIP_LINE: Table detected, need to skip next line.
        PARSING: Parsing table.
    """

    WAITING = 0
    SKIP_LINE = 1
    PARSING = 2


def iter_results(path: str) -> Iterable[Tuple[str, List[Tuple[str, float]]]]:
    """Read benchmarks docs and extract values for charts.

    Args:
        path: README.md path

    Returns:
        Yields tuple of (scale, data block)
    """
    r = []
    mode = Mode.WAITING
    scale = None
    with open(path) as fp:
        for line in fp:
            ln = line.strip()
            if mode == Mode.WAITING:
                m = rx_name.search(ln)
                if m:
                    scale = m.group(1)
                    mode = Mode.SKIP_LINE
            elif mode == Mode.SKIP_LINE:
                mode = Mode.PARSING
            elif mode == Mode.PARSING:
                if ln.startswith("---"):
                    mode = Mode.WAITING
                    yield scale, r
                    r = []
                else:
                    parts = ln.split()
                    name = normalize_name(parts[0])
                    value = float(parts[9].replace(",", ""))
                    r.append((name, value))


def main() -> None:
    """Main function."""
    for bench, (scale, data) in zip(
        BENCHMARKS, iter_results("docs/benchmarks.md")
    ):
        build_barchart(bench, data, scale)


if __name__ == "__main__":
    main()
