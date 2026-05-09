#!/usr/bin/env python3
"""Validate that MMIL_D dynamic state files exist and contain required anchors."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / ".agents" / "state" / "CURRENT_STATE.md"
NEXT = ROOT / ".agents" / "state" / "NEXT_ACTION.md"
LEDGER = ROOT / ".agents" / "state" / "EXPERIMENT_LEDGER.md"

REQUIRED_STATE_TOKENS = [
    "Current scientific claim boundary",
    "Current mainline",
    "Current best trusted results",
    "Active next action",
]


def main() -> int:
    missing = [p for p in (STATE, NEXT, LEDGER) if not p.exists()]
    if missing:
        for p in missing:
            print(f"MISSING: {p}")
        return 1

    text = STATE.read_text(encoding="utf-8")
    failures = [tok for tok in REQUIRED_STATE_TOKENS if tok not in text]
    if failures:
        for tok in failures:
            print(f"CURRENT_STATE.md missing section token: {tok}")
        return 1

    ledger_text = LEDGER.read_text(encoding="utf-8")
    if "| Date | ID | Dataset |" not in ledger_text:
        print("EXPERIMENT_LEDGER.md missing required table header")
        return 1

    print("State files OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
