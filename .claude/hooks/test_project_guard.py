"""Self-check for project_guard against a throwaway tree. Run: python .claude/hooks/test_project_guard.py"""
import tempfile
from pathlib import Path

import project_guard as g

with tempfile.TemporaryDirectory() as d:
    g.ROOT = root = Path(d).resolve()
    for p in ("build/app-a", "build/app-b", "manage/area-x", "system"):
        (root / p).mkdir(parents=True)
    (root / "build/app-b/CLAUDE.md").write_text("# B\nImports: manage/area-x\n", encoding="utf-8")
    cwd, ALL = str(root), g.SPANS_ALL

    assert g.project_of(root / "build/app-a/STATUS.md", cwd) == "build/app-a"
    assert g.project_of("build/app-a/src/x.py", cwd) == "build/app-a"
    assert g.project_of(root / "build/CLAUDE.md", cwd) is None  # area file = global
    assert g.project_of(root / "system/projects.py", cwd) is None
    assert g.project_of(root, cwd) == ALL and g.project_of(root / "build", cwd) == ALL
    assert g.project_of(Path(d).parent / "elsewhere.txt", cwd) is None

    assert g.touched("Read", {"file_path": str(root / "manage/area-x/notes.md")}, cwd) == {"manage/area-x"}
    assert g.touched("Grep", {"pattern": "x"}, cwd) == {ALL}
    assert g.touched("Bash", {"command": 'cat "build/app-a/x" build\\app-b\\y'}, cwd) == {"build/app-a", "build/app-b"}
    assert g.touched("Bash", {"command": "npm run build"}, cwd) == set()

    assert g.decide(set(), {"build/app-a"}) is None  # first project becomes active
    assert g.decide(set(), {ALL}) is None  # router may survey before choosing
    assert g.decide(set(), {"build/app-a", "build/app-b"})
    assert g.decide({"build/app-a"}, {"build/app-a"}) is None
    assert g.decide({"build/app-a"}, {"build/app-b"})
    assert g.decide({"build/app-a"}, {ALL})
    assert g.decide({"build/app-b"}, {"manage/area-x"}) is None  # declared Imports:
    assert g.decide({"build/app-a"}, {"manage/area-x"})  # not imported by app-a

print("project_guard ok")
