"""leng2021: Leng et al. 2021 (Nat Neurosci), entorhinal cortex (EC) and superior frontal gyrus (SFG) of the same 10
male donors, CELLxGENE collection 180bff9c-c8a5-4539-b13b-ddbc00d643e6 (raw/leng2021/leng2021_{EC,SFG}.h5ad, the two
whole-region datasets; the per-cell-type datasets of the collection are subsets of them).

X holds raw UMI counts; both files share one gene index and are read into one matrix.
Donors (user decision 2026-11-17: all 10): Braak 0 = control (3 donors, aged 50, 60 and 71), Braak 2 and Braak 6 = AD
(4 and 3 donors, labelled Alzheimer disease in the release), so the early-AD (Braak 1-4) and late-AD (Braak >= 5)
contrasts are the paper's Braak 2 vs 0 and Braak 6 vs 0 comparisons.
age: 'NN-year-old stage' -> NN; '80 year-old and over stage' -> 90, flagged in age_censored (as for SEA-AD).
Cell classes from the authors' cell types (clusterCellType); their subclusters (EC:Exc.1 ...) are kept as
subcluster_author.
"""
import re

import numpy as np
import pandas as pd

from claimstore.config import RAW

FILES = {"EC": RAW / "leng2021" / "leng2021_EC.h5ad", "SFG": RAW / "leng2021" / "leng2021_SFG.h5ad"}
AUTHOR_TO_CLASS = {"Exc": "Excitatory neurons", "Inh": "Inhibitory neurons", "Astro": "Astrocytes",
                   "Micro": "Microglia", "Oligo": "Oligodendrocytes", "OPC": "OPCs", "Endo": "Endothelial"}


def _age(s):
    m = re.match(r"^(\d+)-year-old", s)
    if m:
        return float(m.group(1))
    return 90.0 if s.startswith("80 year-old and over") else np.nan


def load():
    import anndata as ad
    from claimstore.h5io import read_csr_many, read_df

    obs, sources, var = [], [], None
    for region, path in FILES.items():
        o, v = read_df(path, "obs"), read_df(path, "var")
        if var is None:
            var = v
        assert v.index.equals(var.index), f"{path.name}: genes differ from {FILES['EC'].name}"
        braak = pd.to_numeric(o["BraakStage"].astype(str), errors="coerce")
        st = o["development_stage"].astype(str)
        obs.append(pd.DataFrame({
            "donor": "leng" + o["donor_id"].astype(str).values, "sample": o["SampleID"].astype(str).values,
            "region": region, "disease": np.where(braak.values > 0, "AD", "control"),
            "disease_raw": ("Braak " + o["BraakStage"].astype(str)).values,
            "sex": o["sex"].astype(str).map({"male": "M", "female": "F"}).values,
            "age": st.map(_age).values, "age_censored": st.str.startswith("80 year-old and over").values,
            "pmi": np.nan, "braak_nft": braak.values,
            "author_cell_type": o["clusterCellType"].astype(str).values,
            "subcluster_author": o["clusterAssignment"].astype(str).values,
            "batch": o["SampleBatch"].astype(str).values,
        }, index=(region + ":" + o.index.astype(str))))
        sources.append((path, "X", np.ones(len(o), bool)))
        print(f"{region}: {len(o)} nuclei, {o.donor_id.nunique()} donors", flush=True)
    obs = pd.concat(obs)
    X = read_csr_many(sources, chunk=100_000)
    genes = pd.DataFrame({"gene_ids": var.index.astype(str)}, index=pd.Index(var["feature_name"].astype(str).values))
    a = ad.AnnData(X, obs=obs, var=genes)
    a.var_names_make_unique()
    return a
