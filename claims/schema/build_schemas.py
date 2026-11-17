"""Write claims/schema/*.json from config/schema.toml (python3 -I claims/schema/build_schemas.py)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "src"))
from claimstore.schema import *  # noqa: E402,F401,F403
from claimstore.schema import write  # noqa: E402

if __name__ == "__main__":
    for p in write(HERE):
        print(p)
