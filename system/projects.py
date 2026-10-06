"""Routing index: one line per project (area/name — title: purpose). Deterministic, always current."""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")  # Windows console defaults to cp1252

ROOT = Path(__file__).resolve().parent.parent

for area in ("explore", "build", "manage"):
    for d in sorted(p for p in (ROOT / area).glob("*") if p.is_dir() and not p.name.startswith(".")):
        md = d / "CLAUDE.md"
        lines = [l.strip() for l in md.read_text(encoding="utf-8").splitlines() if l.strip()] if md.exists() else []
        title = lines[0].lstrip("# ") if lines else "(no CLAUDE.md)"
        purpose = next((l for l in lines[1:] if not l.startswith("#")), "")
        print(f"{area}/{d.name} - {title}: {purpose[:100]}")
