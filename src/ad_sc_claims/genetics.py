"""Genetic claims of the AD field. The engine's claim re-tests call `genetic_test` for every genetic_enrichment claim
([tests] genetic_test in config/project.toml).

TWAS genes and differential expression: a claim that genes with a TWAS association to AD overlap the AD DEGs of a cell
type is tested in every dataset, in the claim's cell classes and contrast, by a competitive test: the mean |z| of the
TWAS genes in the edgeR table against N_RANDOM random gene sets of the same size, each gene drawn from the same
expression decile (logCPM). The TWAS genes are the claim's signature rows of kind `twas_genes`
(src/ad_sc_claims/signatures/<paper>.py). Positive z: the TWAS genes change more than expression-matched genes.

Claims about the GWAS heritability of gene sets need AD GWAS summary statistics, which this project does not have
(decided 2026-11-18): they are not testable.
"""
import numpy as np
import pandas as pd
from scipy import stats

from oktopy.retest import de_table, map_genes, signatures, summarise

N_RANDOM = 2000
MIN_GENES = 10


def twas_de_test(ctx, dataset, genes):
    rng = np.random.default_rng(0)  # own stream: the engine's tests keep their random draws
    rows = []
    for reg in [r for r in str(ctx.regions).split(";") if r]:
        for cls in [c for c in str(ctx.cell_classes).split(";") if c] or ["ALL"]:
            for con in str(ctx.contrast).split("+"):
                t = de_table(dataset, reg, cls, con)
                if t is None:
                    continue
                g = map_genes(genes, t.index)
                if len(g) < MIN_GENES:
                    continue
                absz = t.z.abs().values
                dec = pd.qcut(t.logCPM.rank(method="first"), 10, labels=False).values
                pools = {d: np.where(dec == d)[0] for d in range(10)}
                pos = t.index.get_indexer(g)
                obs = absz[pos].mean()
                draws = np.stack([rng.choice(pools[d], N_RANDOM) for d in dec[pos]], axis=1)
                null = absz[draws].mean(1)
                z = (obs - null.mean()) / null.std(ddof=1)
                sig = t.padj.values < 0.05
                rows.append({"region": reg, "cell_class": cls, "z": z, "p": 2 * stats.norm.sf(abs(z)),
                             "effect": float(sig[pos].mean() / max(sig.mean(), 1e-9)), "n_genes": len(g),
                             "n_case": np.nan, "n_ref": np.nan,
                             "test": "TWAS genes: mean |z| vs expression-matched random sets"})
    df = pd.DataFrame(rows)
    if len(df):  # units are the donors of the DE fit
        from oktopy.retest import de_log
        lg = de_log(dataset)
        for i, r in df.iterrows():
            n = lg[(lg.region == r.region) & (lg.cell_class == r.cell_class) & (lg.contrast == ctx.contrast)]
            if len(n):
                df.loc[i, ["n_case", "n_ref"]] = [n.n_case.iloc[0], n.n_ref.iloc[0]]
    return summarise(df, 1, "twas_de_enrichment")


def genetic_test(ctx, dataset, statement, modality, cell_state):
    st = statement.lower()

    def na(why):
        return [{"template_used": "genetic_enrichment", "outcome": "not_testable", "note": why}]

    if "twas" in st:
        sig = signatures()
        genes = sig[sig.claim_id.eq(ctx.claim_id) & sig.kind.eq("twas_genes")].gene.unique()
        if not len(genes):
            return na("no TWAS gene list (signature kind twas_genes)")
        return [twas_de_test(ctx, dataset, list(genes))]
    if "gwas" in st or "heritab" in st:
        return na("needs AD GWAS summary statistics (heritability of gene sets), which this project does not have")
    return na("no genetic test for this claim")
