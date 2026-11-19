"""Gene signatures for leng2021 claims (claims/SIGNATURES.md).

Source (raw/supplements/leng2021/, the publisher's copy): 41593_2020_764_MOESM2_ESM.xlsx
  Supplementary Table 1: genes differentially expressed between the RORB+ EC excitatory subpopulations EC:Exc.s2/s4
      and the other EC excitatory neurons (edgeR: logFC, FDR).
  Supplementary Table 2: per EC excitatory subpopulation, Braak stage comparisons (Braak2v0, Braak6v0, ...).
Claims about the RORB+ vulnerable subpopulations (in EC, SFG and the Mathys et al. data, and their share by staining)
are tested on the top 100 genes higher in them (FDR < 0.05). The Braak 6 vs 0 claim on many subpopulations uses the
genes down in any of them (FDR < 0.05), minus genes up in another.
"""
import pandas as pd

from ad_sc_claims.signatures._common import SUPP, Signatures, top

PAPER = "leng2021"
F = SUPP / PAPER / "41593_2020_764_MOESM2_ESM.xlsx"
EXC = "Excitatory neurons"


def main():
    s = Signatures(PAPER)
    t1 = pd.read_excel(F, sheet_name="Supplementary Table 1")
    up = top(t1[(t1.FDR < 0.05) & (t1.logFC > 0)], "logFC")
    s.add("RORB_vulnerable_markers", ["C03", "C04", "C13", "C15", "C16"], "state_markers", EXC, up, stat="logFC",
          padj="FDR", cell_state="EC:Exc.s2; EC:Exc.s4 (RORB+)", source=f"{F.name}|Supplementary Table 1",
          selection="higher in EC:Exc.s2/s4 than other EC excitatory neurons, FDR < 0.05, top 100 by logFC")
    t2 = pd.read_excel(F, sheet_name="Supplementary Table 2")
    print(f"{PAPER}: Supplementary Table 2 comparisons {sorted(t2.comparison.unique())}, "
          f"{t2.subpopulation.nunique()} subpopulations")
    b6 = t2[t2.comparison.eq("Braak6v0") & t2.subpopulation.str.startswith("EC:Exc") & (t2.FDR < 0.05)]
    down = b6[b6.logFC < 0].groupby("gene").agg(logFC=("logFC", "mean"), FDR=("FDR", "min"),
                                                n=("subpopulation", "nunique")).reset_index()
    down = down[~down.gene.isin(b6[b6.logFC > 0].gene)]
    s.add("EC_Exc_Braak6v0_down", ["C11"], "de_down", EXC, top(down, "logFC", 100000, ascending=True), stat="logFC",
          padj="FDR", comparison="Braak 6 vs Braak 0", source=f"{F.name}|Supplementary Table 2",
          selection="down at Braak 6 vs 0 in any EC excitatory subpopulation (FDR < 0.05), not up in another")
    s.unresolved(["C06"], "EC layer genes (Ramsden et al. mouse MEC)", "the layer gene sets are from another study, not "
                 "in this paper's supplement")
    s.unresolved(["C07"], "EC:Exc.s5 markers", "no marker table for EC:Exc.s5 in the supplement")
    s.unresolved(["C09", "C10"], "functions of genes distinguishing a subpopulation",
                 "describes what the genes separating EC:Exc.s2/s4 from other neurons encode; a re-test needs that "
                 "subpopulation labelled in the target data")
    s.unresolved(["C12"], "which subpopulation has the most downregulated genes",
                 "a comparison between subpopulations; the re-tests have no ranking test")
    s.unresolved(["C25"], "overlap with mouse reactive astrocyte genes (Anderson et al. 2016)",
                 "an overlap with another study's gene sets")
    return s.write()


if __name__ == "__main__":
    main()
