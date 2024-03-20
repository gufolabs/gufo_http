# ---------------------------------------------------------------------
# Gufo HTTP: Generate reference pages.
# ---------------------------------------------------------------------
# Copyright (C) 2024, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------

# Python module
from itertools import chain
from pathlib import Path

# Third-party modules
import mkdocs_gen_files


def main() -> None:
    """Generate reference index."""
    nav = mkdocs_gen_files.Nav()

    src = Path("src")
    for path in sorted(chain(src.rglob("*.py"), src.rglob("*.pyi"))):
        module_path = path.relative_to("src").with_suffix("")
        doc_path = path.relative_to("src").with_suffix(".md")
        full_doc_path = Path("reference", doc_path)
        parts = tuple(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")
            full_doc_path = full_doc_path.with_name("index.md")
        elif parts[-1] == "__main__":
            continue
        nav[("gufo.http",) + parts[2:]] = str(doc_path)
        with mkdocs_gen_files.open(full_doc_path, "w") as fd:
            identifier = ".".join(parts)
            fd.write(f"# {identifier}\n\n::: {identifier}\n")
        mkdocs_gen_files.set_edit_path(full_doc_path, path)

    with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
        nav_file.writelines(nav.build_literate_nav())


main()
