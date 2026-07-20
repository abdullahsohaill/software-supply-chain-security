#!/usr/bin/env python3
"""Compute Jaccard positive-unit overlap for held-out extraction decisions.

Each input CSV must contain columns named ``Abdullah`` and ``NotebookLM``.
Every non-empty value in those columns must be either 0 or 1.

Example:
    python3 scripts/compute_audit_jaccard.py cyclonedx_audit.csv
    python3 scripts/compute_audit_jaccard.py cyclonedx.csv spdx.csv cisa.csv
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


REQUIRED_COLUMNS = ("Abdullah", "NotebookLM")


def read_labels(csv_path: Path) -> tuple[list[int], list[int]]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("the CSV has no header row")

        missing = [name for name in REQUIRED_COLUMNS if name not in reader.fieldnames]
        if missing:
            raise ValueError(
                f"missing required column(s): {', '.join(missing)}; "
                f"found: {', '.join(reader.fieldnames)}"
            )

        abdullah: list[int] = []
        notebooklm: list[int] = []
        for row_number, row in enumerate(reader, start=2):
            left = (row.get("Abdullah") or "").strip()
            right = (row.get("NotebookLM") or "").strip()

            if not left and not right:
                continue
            if not left or not right:
                raise ValueError(
                    f"row {row_number}: both Abdullah and NotebookLM require a value"
                )
            if left not in {"0", "1"} or right not in {"0", "1"}:
                raise ValueError(
                    f"row {row_number}: labels must be 0 or 1, got {left!r} and {right!r}"
                )

            abdullah.append(int(left))
            notebooklm.append(int(right))

    if not abdullah:
        raise ValueError("the CSV contains no paired labels")
    return abdullah, notebooklm


def jaccard_overlap(left: list[int], right: list[int]) -> float:
    if len(left) != len(right) or not left:
        raise ValueError("label lists must be non-empty and have equal length")

    intersection = sum(a == 1 and b == 1 for a, b in zip(left, right))
    union = sum(a == 1 or b == 1 for a, b in zip(left, right))
    if union == 0:
        raise ValueError("Jaccard is undefined because neither column contains a positive label")
    return intersection / union


def analyze(csv_path: Path) -> None:
    abdullah, notebooklm = read_labels(csv_path)
    jaccard = jaccard_overlap(abdullah, notebooklm)
    print(f"{csv_path}:")
    print(f"  n = {len(abdullah)}")
    print(f"  Jaccard positive-unit overlap = {jaccard:.4f}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Compute Jaccard overlap from binary Abdullah and NotebookLM CSV columns."
        )
    )
    parser.add_argument("csv", nargs="+", type=Path, help="one or more audit CSV files")
    args = parser.parse_args()

    failed = False
    for index, csv_path in enumerate(args.csv):
        if index:
            print()
        try:
            analyze(csv_path)
        except (OSError, ValueError) as error:
            failed = True
            print(f"{csv_path}: error: {error}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
