"""Write every paper's claim signatures (claims/signatures/), then run `oktopy signatures` to merge them.

Usage: python -I src/ad_sc_claims/signatures/run.py [paper ...]
"""
import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # src/

from ad_sc_claims.signatures._common import Signatures  # noqa: E402

PAPERS = ["gabitto2024", "green2024", "lau2020", "leng2021", "mathys2019", "mathys2023", "sun2023"]
# papers whose supplementary tables could not be fetched: their claims stay on the genes they name
NO_SUPPLEMENT = {
    "grubman2019": (["C01"], "AD and control subclusters", "not in PMC; full text not accessed"),
}


def main(argv=None):
    papers = (sys.argv[1:] if argv is None else argv) or PAPERS + list(NO_SUPPLEMENT)
    for p in papers:
        if p in NO_SUPPLEMENT:
            s = Signatures(p)
            claims, term, reason = NO_SUPPLEMENT[p]
            s.unresolved(claims, term, reason)
            s.write()
        else:
            importlib.import_module(f"ad_sc_claims.signatures.{p}").main()
    return 0


if __name__ == "__main__":
    sys.exit(main())
