"""Shared helpers for the claim signature scripts (claims/SIGNATURES.md): one script per paper writes
claims/signatures/<paper>.tsv and claims/signatures/<paper>_unresolved.tsv.

Run all of them: python -I src/ad_sc_claims/signatures/run.py [paper ...]; then `oktopy signatures`.
"""
import pandas as pd

from oktopy import config as cfg

SUPP = cfg.RAW / "supplements"
OUT = cfg.REPO / "claims" / "signatures"
COLS = ["signature_id", "paper", "claim_ids", "kind", "cell_type", "cell_state", "comparison", "gene", "rank", "stat",
        "padj", "source", "selection"]


class Signatures:
    def __init__(self, paper):
        self.paper, self.rows, self.unres = paper, [], []

    def add(self, name, claims, kind, cell_type, table, gene="gene", stat=None, padj=None, cell_state="",
            comparison="", source="", selection=""):
        """One signature from `table` (rows in rank order): one row per gene."""
        for i, r in enumerate(table.to_dict("records"), 1):
            self.rows.append({"signature_id": f"{self.paper}__{name}", "paper": self.paper,
                              "claim_ids": ";".join(f"{self.paper}-{c}" for c in claims), "kind": kind,
                              "cell_type": cell_type, "cell_state": cell_state, "comparison": comparison,
                              "gene": str(r[gene]).strip(), "rank": i, "stat": r[stat] if stat else "",
                              "padj": r[padj] if padj else "", "source": source, "selection": selection})

    def unresolved(self, claims, term, reason):
        for c in claims:
            self.unres.append({"claim_id": f"{self.paper}-{c}", "term": term, "reason": reason})

    def write(self):
        OUT.mkdir(exist_ok=True)
        d = pd.DataFrame(self.rows, columns=COLS)
        # a gene listed both up and down in one signature and cell class has no expected direction: drop it
        de = d.kind.isin(["de_up", "de_down"])
        both = d[de].groupby(["signature_id", "cell_type", "gene"]).kind.transform("nunique").gt(1)
        d = d.drop(both[both].index).drop_duplicates(["signature_id", "cell_type", "kind", "gene"])
        if len(d):
            d.to_csv(OUT / f"{self.paper}.tsv", sep="\t", index=False)
        u = pd.DataFrame(self.unres, columns=["claim_id", "term", "reason"])
        if len(u):
            u.to_csv(OUT / f"{self.paper}_unresolved.tsv", sep="\t", index=False)
        claims = d.claim_ids.str.split(";").explode().nunique() if len(d) else 0
        print(f"{self.paper}: {d.signature_id.nunique()} signatures, {len(d)} rows, {claims} claims; "
              f"{u.claim_id.nunique() if len(u) else 0} unresolved claims", flush=True)
        if len(d):
            print(d.groupby(["signature_id", "kind", "cell_type"]).size().to_string(), flush=True)
        return d


def top(d, by, n=100, ascending=False):
    """The first n rows of d by `by` (largest first unless ascending)."""
    return d.sort_values(by, ascending=ascending).head(n)
