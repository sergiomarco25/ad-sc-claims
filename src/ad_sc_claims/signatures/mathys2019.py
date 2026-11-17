"""Gene signatures for mathys2019 claims (claims/SIGNATURES.md).

Sources (raw/supplements/mathys2019/, the publisher's copies):
  41586_2019_1195_MOESM4_ESM.xlsx  Supplementary Table 2: DE per cell type (sheets Ex, In, Ast, Oli, Opc, Mic) in three
      column blocks: no-pathology vs pathology, no- vs early-pathology, early- vs late-pathology. A DEG is significant in
      both the cell-level and the mixed model (DEGs.Ind.Mix.models), as in the paper; IndModel.FC > 0 means higher in
      the second group (checked against the group means below).
  41586_2019_1195_MOESM6_ESM.xlsx  Supplementary Table 4: gene-trait correlation modules M1-M10 (first sheet).
  41586_2019_1195_MOESM8_ESM.xlsx  Supplementary Table 6: subpopulation markers (Wilcoxon FDR <= 0.01, logFC >= 0.5).
"""
import numpy as np
import pandas as pd

from ad_sc_claims.signatures._common import SUPP, Signatures, top

PAPER = "mathys2019"
D = SUPP / PAPER
DE, MOD, MARK = D / "41586_2019_1195_MOESM4_ESM.xlsx", D / "41586_2019_1195_MOESM6_ESM.xlsx", D / "41586_2019_1195_MOESM8_ESM.xlsx"
CLASS = {"Ex": "Excitatory neurons", "In": "Inhibitory neurons", "Ast": "Astrocytes", "Oli": "Oligodendrocytes",
         "Opc": "OPCs", "Mic": "Microglia"}
BLOCKS = {"path": 0, "early": 11, "late_vs_early": 22}  # first column of each block


def block(sheet, which):
    raw = pd.read_excel(DE, sheet_name=sheet, header=None)
    s = BLOCKS[which]
    d = raw.iloc[2:, s:s + 9].copy()
    d.columns = ["gene"] + [str(x) for x in raw.iloc[1, s + 1:s + 9]]
    d = d.dropna(subset=["gene"])
    d["FC"] = pd.to_numeric(d["IndModel.FC"], errors="coerce")
    d["padj"] = pd.to_numeric(d["IndModel.adj.pvals"], errors="coerce")
    d["deg"] = d["DEGs.Ind.Mix.models"].astype(str).str.lower().eq("true")
    means = [c for c in d.columns if c.endswith(".mean")]
    first, second = {"path": ("no.pathology.mean", "pathology.mean"), "early": ("no.pathology.mean", "early.pathology.mean"),
                     "late_vs_early": ("early.pathology.mean", "late.pathology.mean")}[which]
    assert {first, second} <= set(means), (sheet, which, means)
    diff = pd.to_numeric(d[second], errors="coerce") - pd.to_numeric(d[first], errors="coerce")
    agree = (np.sign(diff) == np.sign(d.FC))[d.deg].mean()
    assert agree > 0.9, f"{sheet} {which}: FC sign agrees with the group means for only {agree:.2f} of DEGs"
    return d


def main():
    s = Signatures(PAPER)
    src = f"{DE.name}|"
    for name, claims, sheets in [("neuron_DEGs_pathology", ["C01"], ["Ex", "In"]),
                                 ("glia_DEGs_pathology", ["C02"], ["Oli", "Ast", "Mic"])]:
        for sh in sheets:
            d = block(sh, "path")
            for kind, sign in [("de_up", 1), ("de_down", -1)]:
                t = d[d.deg & (np.sign(d.FC) == sign)].assign(a=lambda x: x.FC.abs()).sort_values("a", ascending=False)
                s.add(name, claims, kind, CLASS[sh], t, stat="FC", padj="padj", comparison="pathology vs no-pathology",
                      source=src + sh, selection="DEGs.Ind.Mix.models (cell-level and mixed model); by |IndModel.FC|")
    # genes up in late- vs early-pathology individuals in >= 5 of the 6 cell types (Fig. 2e: 11 genes)
    up = pd.concat([block(sh, "late_vs_early").query("deg and FC > 0").assign(ct=sh) for sh in CLASS])
    shared = up.groupby("gene").agg(n=("ct", "nunique"), FC=("FC", "mean")).query("n >= 5").reset_index()
    print(f"{PAPER}: {len(shared)} genes up in late vs early pathology in >= 5 cell types (paper: 11)")
    s.add("shared_late_vs_early_up", ["C11"], "de_up", "", top(shared, "FC", 1000), stat="n",
          comparison="late- vs early-pathology", source=src + "all sheets",
          selection="DEG (both models) and FC > 0 in >= 5 of 6 cell types")
    # gene-trait correlation modules
    mod = pd.read_excel(MOD, sheet_name=0, header=None)
    for claim, k, ct in [("C13", 7, "Microglia"), ("C14", 9, "Oligodendrocytes")]:
        col = mod.iloc[0].tolist().index(f"Module {k}")
        genes = mod.iloc[2:, col].dropna().astype(str).str.strip()
        s.add(f"module_M{k}", [claim], "pathway_genes", ct, pd.DataFrame({"gene": genes}), cell_state=f"module M{k}",
              source=f"{MOD.name}|Gene-trait correlation modules", selection=f"all genes of module {k}")
    # subpopulation markers
    m = pd.read_excel(MARK, header=1).iloc[:, :4]
    m.columns = ["gene", "padj", "lFC", "subpopulation"]
    m = m.dropna(subset=["gene"])
    for claims, state in [(["C17"], "Ex4"), (["C18"], "In0"), (["C19"], "Ast1"), (["C20"], "Oli0"), (["C21"], "Mic1"),
                          (["C22"], "Opc1"), (["C23"], "Ex6"), (["C23"], "In2"), (["C23"], "Ast0"), (["C23"], "Oli1")]:
        t = top(m[m.subpopulation.eq(state)], "lFC")
        assert len(t), state
        s.add(f"{state}_markers", claims, "state_markers", CLASS[state.rstrip("0123456789")], t, stat="lFC", padj="padj",
              cell_state=state, source=f"{MARK.name}|Subpopulation_markers",
              selection="authors' markers (FDR <= 0.01, logFC >= 0.5), top 100 by logFC")
    s.unresolved(["C05", "C10", "C12"], "cell-type specificity of DEG sets",
                 "the claim is about how DEG sets overlap between cell types; a direction re-test of the genes would "
                 "not test it")
    return s.write()


if __name__ == "__main__":
    main()
