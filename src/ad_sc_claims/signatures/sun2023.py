"""Gene signatures for sun2023 claims (claims/SIGNATURES.md).

Source (raw/supplements/sun2023/, the authors' data page personal.broadinstitute.org/cboix/sun_victor_et_al_data/):
  SupplementalTables.combined.xlsx  Table S1; page 2 (StateMarkers): markers of each microglial state MG0-MG12 against
      the other microglia (avg_log2FC, p_val_adj). Page 11 (DEGs with groups) has no gene names, so the gene-group
      claims (G2, G25, G26, G49, G50) stay on the genes they name. Page 13 (TWAS_result): the 1,036 genes with a
      microglia TWAS association to AD (kind twas_genes, read by src/ad_sc_claims/genetics.py).
A claim about a state's share of microglia is tested on the state's top 100 markers (p_val_adj < 0.05, avg_log2FC > 0).
"""
import pandas as pd

from ad_sc_claims.signatures._common import SUPP, Signatures, top

PAPER = "sun2023"
F = SUPP / PAPER / "SupplementalTables.combined.xlsx"


def main():
    s = Signatures(PAPER)
    m = pd.read_excel(F, sheet_name="Page 2.StateMarkers")
    m = m[(m.p_val_adj < 0.05) & (m.avg_log2FC > 0)]
    for state, claims in {"MG4": ["C02"], "MG8": ["C03"], "MG1": ["C04"]}.items():
        t = top(m[m.microgliaState.eq(state)], "avg_log2FC")
        assert len(t), state
        s.add(f"{state}_markers", claims, "state_markers", "Microglia", t, stat="avg_log2FC", padj="p_val_adj",
              cell_state=state, source=f"{F.name}|Page 2.StateMarkers",
              selection="markers vs other microglia: p_val_adj < 0.05, avg_log2FC > 0, top 100 by avg_log2FC")
    tw = pd.read_excel(F, sheet_name="Page 13.TWAS_result").sort_values("p.val").drop_duplicates("hgnc_symbol")
    tw = tw[tw.hgnc_symbol.notna()]
    assert tw.hgnc_symbol.nunique() == 1036, tw.hgnc_symbol.nunique()  # the claim's count
    s.add("microglia_TWAS_genes", ["C27"], "twas_genes", "Microglia", tw, gene="hgnc_symbol", stat="theta",
          source=f"{F.name}|Page 13.TWAS_result", selection="every gene of the TWAS table (1,036), ranked by p")
    s.unresolved(["C05", "C06", "C07"], "comparison between states or between pathology traits",
                 "the claim ranks states (strongest correlation) or traits (plaques vs tangles); the re-tests have no "
                 "ranking test")
    s.unresolved(["C12", "C25"], "share of a state whose marker genes change in expression",
                 "the claim says the state's share is unchanged while its genes change, so a marker shift cannot stand "
                 "in for the share; tested on the authors' state labels (claims/state_labels.tsv)")
    s.unresolved(["C11"], "overlap with the mouse DAM signature", "an overlap with another study's gene set")
    s.unresolved(["C13"], "order and overlap of the inflammatory states", "a ranking of states, not a group difference")
    s.unresolved(["C14", "C17"], "which states and stages change most", "counts and rankings of DEGs across states "
                 "and stages; a direction re-test of the genes would not test them")
    s.unresolved(["C26"], "AD GWAS genes highly expressed in microglial states", "an expression pattern of risk genes")
    return s.write()


if __name__ == "__main__":
    main()
