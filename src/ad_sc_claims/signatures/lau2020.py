"""Gene signatures for lau2020 claims (claims/SIGNATURES.md).

Sources (raw/supplements/lau2020/, PNAS Datasets S1-S5 via Europe PMC):
  pnas.2008762117.sd03.xlsx  Dataset S3: AD vs control DEGs per cell type (sheets Astro, Endo, Excit, Inhit [sic], Mic,
      Oligo; AD_vs_NC_log2fc, Adjusted_p_value).
  pnas.2008762117.sd05.xlsx  Dataset S5: genes distinguishing the AD-up-regulated subpopulations from the
      AD-down-regulated ones (Astro, Mic, Oligo: Up_vs_Down) or from the unchanged ones (Endo: Up_vs_No_change).
DEG claims use the full list in the claimed direction: padj < 0.05 and |log2fc| >= 0.1, which gives 2,139 DEGs
(10 shared by all six cell types) against the paper's 2,190 (11 shared). Subpopulation claims use the top 100 genes higher
in the AD-up subpopulations (enriched claims) or in the AD-down subpopulations (depleted claims).
"""
import pandas as pd

from ad_sc_claims.signatures._common import SUPP, Signatures, top

PAPER = "lau2020"
D = SUPP / PAPER
S3, S5 = D / "pnas.2008762117.sd03.xlsx", D / "pnas.2008762117.sd05.xlsx"
CLASS = {"Astro": "Astrocytes", "Endo": "Endothelial", "Excit": "Excitatory neurons", "Inhit": "Inhibitory neurons",
         "Mic": "Microglia", "Oligo": "Oligodendrocytes"}


def table(f, sheet):
    d = pd.read_excel(f, sheet_name=sheet)
    d.columns = ["gene", "lfc", "padj"]
    return d[d.padj < 0.05]


def main():
    s = Signatures(PAPER)
    for claims, sheets, kind in [(["C04"], ["Excit", "Inhit"], "de_down"), (["C05"], ["Astro"], "de_down"),
                                 (["C07"], ["Mic"], "de_up"), (["C08"], ["Endo"], "de_up"),
                                 (["C10"], ["Oligo"], "de_down")]:
        for sh in sheets:
            d = table(S3, sh)
            d = d[d.lfc >= 0.1] if kind == "de_up" else d[d.lfc <= -0.1]
            s.add(f"{sh}_DEGs_{kind[3:]}", claims, kind, CLASS[sh], top(d.assign(a=d.lfc.abs()), "a", 100000),
                  stat="lfc", padj="padj", comparison="AD vs control", source=f"{S3.name}|{sh}",
                  selection=f"all DEGs with padj < 0.05 and |log2fc| >= 0.1, {'up' if kind == 'de_up' else 'down'} in AD")
    for claims, sh, side, state in [(["C13", "C15"], "Astro", "up", "a1; a6 (AD-up)"), (["C14"], "Astro", "down", "a3 (AD-down)"),
                                    (["C17"], "Oligo", "up", "o1; o2 (AD-up)"), (["C16"], "Oligo", "down", "o3; o5 (AD-down)"),
                                    (["C18"], "Mic", "down", "m6 (AD-down)"), (["C19"], "Endo", "up", "e1; e3; e4 (AD-up)")]:
        d = table(S5, sh)
        d = top(d[d.lfc > 0], "lfc") if side == "up" else top(d[d.lfc < 0], "lfc", ascending=True)
        s.add(f"{sh}_AD{side}_subpopulation_markers", claims, "state_markers", CLASS[sh], d, stat="lfc", padj="padj",
              cell_state=state, source=f"{S5.name}|{sh}",
              selection=f"padj < 0.05, higher in the AD-{side} subpopulations, top 100 by |log2fc|")
    s.unresolved(["C03", "C12"], "overlap of DEG sets", "the claim is about how DEG sets overlap (between cell types, "
                 "or with another study); a direction re-test of the genes would not test it")
    s.unresolved(["C22"], "functions of the angiogenic endothelial signature",
                 "describes the interaction network of the signature genes; nothing to re-test in expression")
    return s.write()


if __name__ == "__main__":
    main()
