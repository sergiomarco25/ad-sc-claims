"""Gene signatures for mathys2023 claims (claims/SIGNATURES.md).

Source: the authors' DE results, raw/supplements/mathys2023/github/ (github.com/mathyslab7/ROSMAP_snRNAseq_PFC at the
commit in SOURCE.txt), Results/Differential_gene_expression_analysis/:
  gpath/<subtype>_gpath.csv                    association with global AD pathology per cell subtype (muscat edgeR)
  cogn_global_lv/<subtype>_cogn_global_lv.csv  association with global cognition at the last visit
A consensus signature, as in the paper, is the genes significant (p_adj.loc < 0.05) in the same direction in at least
3 of the excitatory neuron subtypes.
"""
import pandas as pd

from ad_sc_claims.signatures._common import SUPP, Signatures, top

PAPER = "mathys2023"
R = SUPP / PAPER / "github" / "Results" / "Differential_gene_expression_analysis"
EXC = "Excitatory neurons"


def consensus(trait):
    fs = sorted((R / trait).glob(f"Exc *_{trait}.csv"))
    d = pd.concat([pd.read_csv(f) for f in fs])
    d = d[d.p_adj_loc < 0.05] if "p_adj_loc" in d else d[d["p_adj.loc"] < 0.05]
    g = d.assign(sign=d.logFC.gt(0)).groupby(["gene", "sign"]).agg(n=("cluster_id", "nunique"),
                                                                   logFC=("logFC", "mean")).reset_index()
    g = g[g.n >= 3]
    g = g[~g.gene.duplicated(keep=False)]  # significant both ways in different subtypes: no direction
    print(f"{PAPER}: {trait}: {len(fs)} excitatory subtypes; consensus up {g.sign.sum()}, down {(~g.sign).sum()}")
    return g


def main():
    s = Signatures(PAPER)
    sel = "significant (p_adj.loc < 0.05) in the same direction in >= 3 excitatory subtypes"
    g = consensus("gpath")
    s.add("Exc_consensus_gpath_up", ["C02"], "de_up", EXC, top(g[g.sign], "n", 100000), stat="n",
          comparison="along global AD pathology", source="github|gpath", selection=sel)
    s.add("Exc_consensus_gpath_down", ["C04"], "de_down", EXC, top(g[~g.sign], "n", 100000), stat="n",
          comparison="along global AD pathology", source="github|gpath", selection=sel)
    c = consensus("cogn_global_lv")
    s.add("Exc_consensus_cognition_down", ["C20"], "de_down", EXC, top(c[~c.sign], "n", 100000), stat="n",
          comparison="along global cognition (negative association: lower with better cognition)",
          source="github|cogn_global_lv", selection=sel)
    s.unresolved(["C01", "C18"], "overlap of DEG sets", "the claim is about how DEG sets overlap (between subtypes, or "
                 "between cognition and pathology); a direction re-test of the genes would not test it")
    s.unresolved(["C10", "C11", "C13", "C14", "C15", "C16", "C19", "C21"], "pathway named only",
                 "the claim names pathways (GO terms, gene families) whose member genes are shown only in figures")
    s.unresolved(["C17"], "PFC late vs MTG early changes", "a comparison across regions and stages of two studies")
    return s.write()


if __name__ == "__main__":
    main()
