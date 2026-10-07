"""Render the labelled 1.0.1 formulation Markdown into the manuscript Appendix A include.

Usage (from the repository root):
    python3 manuscript/revisions/softx-r2/render_formulation.py [--pandoc PATH]

Runs pandoc (markdown -> latex, as FHOPS' export_docs_assets.py does), then replaces pandoc's
equal-width longtable for the implementation mapping with a narrow-label longtable and turns
inline code into breakable \\breakpath identifiers.
"""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "fhops_operational_formulation_labelled.md"
DST = HERE.parents[1] / "sections" / "includes" / "fhops_operational_formulation.tex"
HEADER = (
    "% GENERATED from manuscript/revisions/softx-r2/fhops_operational_formulation_labelled.md\n"
    "% by render_formulation.py (pandoc markdown -> latex); edit the Markdown, then re-render.\n"
)

TABLE_HEAD = r"""{\small
\begin{longtable}{@{}>{\raggedright\arraybackslash}p{0.11\linewidth}>{\raggedright\arraybackslash}p{0.85\linewidth}@{}}
\toprule
Block & Pyomo objects and rules \\
\midrule
\endhead
"""
TABLE_TAIL = "\\bottomrule\n\\end{longtable}}\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pandoc", default="pandoc")
    args = parser.parse_args()
    tex = subprocess.run(
        [args.pandoc, "-f", "markdown", "-t", "latex", str(SRC)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout

    # Rebuild the mapping table from pandoc's body rows (after \endlastfoot).
    m = re.search(r"\\begin\{longtable\}.*?\\endlastfoot\n(.*?)\\end\{longtable\}\n", tex, re.S)
    if not m:
        raise SystemExit("mapping table not found in pandoc output")
    rows = m.group(1).replace("\\bottomrule\\noalign{}\n", "")
    tex = tex[: m.start()] + TABLE_HEAD + rows + TABLE_TAIL + tex[m.end() :]

    # Code identifiers: pandoc emits unbreakable \texttt; \breakpath (url's \path) breaks at
    # dots, underscores, and slashes, so long Pyomo names stay inside the text block.
    def _code(match: re.Match[str]) -> str:
        return "\\breakpath{" + match.group(1).replace("\\_", "_") + "}"

    tex = re.sub(r"\\texttt\{([A-Za-z0-9_.\\/(),=]+?)\}", _code, tex)
    if re.search(r"\\texttt\{[^}]*\\_", tex):
        raise SystemExit("unconverted identifier with underscores in pandoc output")

    DST.write_text(HEADER + tex)
    print(f"wrote {DST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
