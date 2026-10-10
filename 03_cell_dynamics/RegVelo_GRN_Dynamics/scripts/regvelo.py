"""Run without installing the repository as a package."""
import sys
from pathlib import Path

script_dir = Path(__file__).resolve().parent
sys.path = [entry for entry in sys.path if Path(entry).resolve() != script_dir]
sys.path.insert(0, str(script_dir.parent / "src"))
from regvelo_workflow.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
