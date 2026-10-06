"""Project isolation guard (PreToolUse + PostToolUse).

The first project a session touches becomes its active project. Touching any other
project, or searching across all of them, makes Claude Code ask the user. An approved
crossing is remembered for the rest of the session. A project's CLAUDE.md can declare
durable imports with a line `Imports: manage/finances, build/x`.
"""
import json
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AREAS = ("explore", "build", "manage")
SPANS_ALL = "*"
# ponytail: Bash/PowerShell are checked by scanning the command for area/project paths.
# A command that reaches another project without naming it (e.g. `grep -r x .` at root) slips through.
PATH_RE = re.compile(r"(?<![\w.-])(explore|build|manage)[/\\]+([\w.-]+)")


def project_of(path, cwd):
    """'area/name' for a path inside a project, SPANS_ALL for root or an area dir, None for global files."""
    p = Path(path)
    if not p.is_absolute():
        p = Path(cwd) / p
    try:
        parts = p.resolve().relative_to(ROOT).parts
    except ValueError:
        return None  # outside Claude OS
    if not parts or (len(parts) == 1 and parts[0] in AREAS):
        return SPANS_ALL
    if parts[0] in AREAS and len(parts) >= 2 and (ROOT / parts[0] / parts[1]).is_dir():
        return f"{parts[0]}/{parts[1]}"
    return None


def touched(tool, inp, cwd):
    if tool in ("Bash", "PowerShell"):
        return {f"{a}/{n}" for a, n in PATH_RE.findall(inp.get("command", "")) if (ROOT / a / n).is_dir()}
    if tool in ("Grep", "Glob"):
        hit = project_of(inp.get("path") or cwd, cwd)
        return {hit} if hit else set()
    path = inp.get("file_path") or inp.get("notebook_path")
    hit = project_of(path, cwd) if path else None
    return {hit} - {SPANS_ALL} if hit else set()


def imports(project):
    md = ROOT / project / "CLAUDE.md"
    text = md.read_text(encoding="utf-8") if md.exists() else ""
    m = re.search(r"^Imports:\s*(.+)$", text, re.M)
    return {s.strip().strip("/") for s in m.group(1).split(",")} if m else set()


def allowed_set(state):
    allowed = set(state)
    for p in state:
        allowed |= {"/".join(Path(i).parts[:2]) for i in imports(p)}
    return allowed


def decide(state, hits):
    """None = allow; otherwise the reason to ask the user."""
    if not state:  # no active project yet: first single project becomes active
        return "Touches several projects at once." if len(hits - {SPANS_ALL}) > 1 else None
    if SPANS_ALL in hits:
        return f"Searches across every project; active project is {', '.join(sorted(state))}. Scope it, or approve."
    foreign = hits - allowed_set(state)
    if foreign:
        return f"Crosses the project boundary: active {', '.join(sorted(state))} -> {', '.join(sorted(foreign))}."
    return None


def main():
    data = json.load(sys.stdin)
    hits = touched(data.get("tool_name", ""), data.get("tool_input") or {}, data.get("cwd") or str(ROOT))
    if not hits:
        return
    state_file = Path(tempfile.gettempdir()) / f"claude-os-guard-{data.get('session_id', 'x')}.json"
    state = set(json.loads(state_file.read_text())) if state_file.exists() else set()
    if data.get("hook_event_name") == "PostToolUse":  # ran = auto-allowed or user-approved
        state |= hits - {SPANS_ALL}
        state_file.write_text(json.dumps(sorted(state)))
        return
    reason = decide(state, hits)
    if reason:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": f"Project isolation: {reason}",
        }}))


if __name__ == "__main__":
    main()
