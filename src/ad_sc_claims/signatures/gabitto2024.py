"""Gene signatures for gabitto2024 claims (claims/SIGNATURES.md).

Source (raw/supplements/gabitto2024/, the publisher's copy): 41593_2024_1774_MOESM3_ESM.xlsx (Supplementary Tables 1-8)
  ST6: curated gene sets (31), among them electron transport chain components and ribosomal genes.
  ST7: genes enriched in the affected (vulnerable) Sst and Pvalb supertypes, mean enrichment score.
ST4 (supertype abundance model) and ST5 (DE per supertype) are only links to the SEA-AD bucket and were not downloaded.
"""
import pandas as pd

from ad_sc_claims.signatures._common import SUPP, Signatures, top

PAPER = "gabitto2024"
F = SUPP / PAPER / "41593_2024_1774_MOESM3_ESM.xlsx"
NEURONS, INH = "Excitatory neurons;Inhibitory neurons", "Inhibitory neurons"


def main():
    s = Signatures(PAPER)
    st6 = pd.read_excel(F, sheet_name="ST6")
    st6.columns = ["set", "gene"]
    sets = sorted(st6.set.unique())
    want = [x for x in sets if "electron transport" in x.lower() or "ribosom" in x.lower()]
    print(f"{PAPER}: ST6 sets used {want} (of {len(sets)})")
    assert want, sets
    s.add("ETC_ribosomal_genes", ["C13"], "pathway_genes", NEURONS,
          st6[st6.set.isin(want)].drop_duplicates("gene"), comparison="along CPS", source=f"{F.name}|ST6",
          selection="all genes of the gene sets: " + "; ".join(want))
    st7 = pd.read_excel(F, sheet_name="ST7")
    st7.columns = ["gene", "sst", "pvalb"]
    for col, claims, state in [("sst", ["C03", "C12"], "vulnerable Sst supertypes"),
                               ("pvalb", ["C05"], "vulnerable Pvalb supertypes")]:
        s.add(f"{col}_vulnerable_markers", claims, "state_markers", INH, top(st7.dropna(subset=[col]), col),
              stat=col, cell_state=state, source=f"{F.name}|ST7",
              selection="genes enriched in the affected supertypes, top 100 by mean enrichment")
    s.unresolved(["C04", "C08", "C09", "C11", "C14"], "supertype markers",
                 "the supertype abundance and DE tables (ST4, ST5) are links to the SEA-AD bucket, not downloaded; "
                 "SEA-AD's own supertype labels could test these claims directly, which the engine cannot yet do")
    s.unresolved(["C17"], "kinase and E3 ligase gene families in vulnerable Sst supertypes",
                 "gene families named in the Supplementary Note; the per-supertype DE (ST5) is not downloaded")
    return s.write()


if __name__ == "__main__":
    main()
