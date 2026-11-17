"""Gene signatures for green2024 claims (claims/SIGNATURES.md).

Sources (raw/supplements/green2024/, the publisher's copies):
  41586_2024_7871_MOESM4_ESM.xlsx  Supplementary Table 2, sheet DEGs: markers of each subpopulation against the other
      subpopulations of its cell type (avg_log2FC, p_val_adj).
  41586_2024_7871_MOESM7_ESM.xlsx  Supplementary Table 5, sheet "Subpopulation communities": community membership.
A claim about a subpopulation's proportion is tested on its markers (top 100 with p_val_adj < 0.05 and avg_log2FC > 0);
a community claim on the markers of its member subpopulations (top 50 each), each in its own cell class.
"""
import pandas as pd

from ad_sc_claims.signatures._common import SUPP, Signatures, top

PAPER = "green2024"
D = SUPP / PAPER
ST2, ST5 = D / "41586_2024_7871_MOESM4_ESM.xlsx", D / "41586_2024_7871_MOESM7_ESM.xlsx"
PREFIX = {"Ast": "Astrocytes", "Mic": "Microglia", "Oli": "Oligodendrocytes", "OPC": "OPCs", "COP": "OPCs",
          "End": "Endothelial", "Peri": "Pericytes", "SMC": "Pericytes", "Fib": "Fibroblasts",
          "Exc": "Excitatory neurons", "Inh": "Inhibitory neurons"}


def cls(state):
    return PREFIX.get(state.split(".")[0])


def main():
    s = Signatures(PAPER)
    deg = pd.read_excel(ST2, sheet_name="DEGs")
    deg = deg[(deg.p_val_adj < 0.05) & (deg.avg_log2FC > 0)]
    src, sel = f"{ST2.name}|DEGs", "markers vs other subpopulations of the type: p_val_adj < 0.05, avg_log2FC > 0, top {n} by avg_log2FC"

    def markers(state, n=100):
        t = top(deg[deg.state.eq(state)], "avg_log2FC", n)
        assert len(t), state
        return t

    for state, claims in {"Mic.12": ["C01", "C08", "C17", "C19"], "Mic.13": ["C02", "C17", "C19"],
                          "Ast.10": ["C03", "C19"], "Oli.7": ["C04", "C19"], "Inh.16": ["C05"],
                          "Inh.6": ["C06"]}.items():
        s.add(f"{state}_markers", claims, "state_markers", cls(state), markers(state), stat="avg_log2FC",
              padj="p_val_adj", cell_state=state, source=src, selection=sel.format(n=100))
    com = pd.read_excel(ST5, sheet_name="Subpopulation communities")
    for community, claim in [("C1", "C22"), ("C2", "C23")]:
        members = com[com.community.eq(community)].subpopulation.tolist()
        skipped = []
        for state in members:
            if cls(state) is None or not len(deg[deg.state.eq(state)]):
                skipped.append(state)
                continue
            s.add(f"community_{community}_markers", [claim], "state_markers", cls(state), markers(state, 50),
                  stat="avg_log2FC", padj="p_val_adj", cell_state=state, source=f"{src}; {ST5.name}|Subpopulation communities",
                  selection=sel.format(n=50) + f", for each member of community {community}")
        print(f"{PAPER}: community {community}: {len(members) - len(skipped)} of {len(members)} members used"
              + (f" (no cell class or markers: {', '.join(skipped)})" if skipped else ""))
    s.unresolved(["C18"], "trajectory structure", "two trajectories inferred from donor composition; no re-test template")
    s.unresolved(["C21"], "order of changes along pseudotime", "a timing claim; the re-tests compare groups, not order")
    s.unresolved(["C20", "C24"], "alternative brain ageing trajectory", "no contrast in these datasets matches it "
                 "(claims/contrast_overrides.tsv)")
    s.unresolved(["C25"], "community proportions in all cells vs cognition",
                 "a whole-tissue shift of many subpopulations' markers would mix composition and expression")
    s.unresolved(["C26"], "sequence of community functions", "pathway programmes ordered along pseudotime")
    s.unresolved(["C28"], "Ast.10 vs Ast.5 signature in Visium", "a comparison of two signatures in spatial data")
    return s.write()


if __name__ == "__main__":
    main()
