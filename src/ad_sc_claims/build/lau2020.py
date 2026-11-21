"""lau2020: Lau et al. 2020 (PNAS), prefrontal cortex of 21 donors, NCBI GEO GSE157827
(raw/lau2020/GSE157827_RAW.tar: one 10x matrix per donor, GSM..._<ID>_{barcodes,features,matrix}).

Donor data from the paper's Dataset S1 (raw/supplements/lau2020/pnas.2008762117.sd01.xlsx, sheet Patient_info):
condition (AD / NC), age, sex, post-mortem delay, Braak tangle stage, APOE genotype. All 21 donors (user decision
2026-11-17): AD = condition AD (12 donors, Braak 4-6), control = NC (9 donors, Braak 1-2).
No author cell labels are released: cell classes come from the engine's marker-based clustering (oktopy.harmonise).
"""
import gzip
import io
import re
import tarfile

import numpy as np
import pandas as pd

from oktopy.config import RAW

TAR = RAW / "lau2020" / "GSE157827_RAW.tar"
DONORS = RAW / "supplements" / "lau2020" / "pnas.2008762117.sd01.xlsx"
AUTHOR_TO_CLASS = {}  # no author labels: labelled by marker clustering


def donors():
    p = pd.read_excel(DONORS, sheet_name="Patient_info")
    p.columns = [str(c).strip() for c in p.columns]
    return pd.DataFrame({
        "disease": p["CONDITION"].map({"AD": "AD", "NC": "control"}).values,
        "disease_raw": p["CONDITION"].astype(str).values,
        "sex": p["SEX"].astype(str).str.strip().values, "age": pd.to_numeric(p["AGE"], errors="coerce").values,
        "pmi": pd.to_numeric(p["PMD"], errors="coerce").values,
        "braak_nft": pd.to_numeric(p["Braak tangle stage"], errors="coerce").values,
        "apoe4": np.where(p["APOE"].astype(str).str.contains("E4"), "Y", "N"),
    }, index=p["ID"].astype(str).str.strip())


def load():
    import anndata as ad
    import scipy.io
    import scipy.sparse as sp

    meta = donors()
    parts, obs, genes = [], [], None
    with tarfile.open(TAR) as t:
        names = t.getnames()
        samples = sorted({re.match(r"^(GSM\d+)_(.+)_matrix\.mtx\.gz$", n).groups() for n in names
                          if n.endswith("_matrix.mtx.gz")})
        for gsm, sid in samples:
            read = lambda kind: gzip.decompress(t.extractfile(f"{gsm}_{sid}_{kind}").read())  # noqa: E731
            m = scipy.io.mmread(io.BytesIO(read("matrix.mtx.gz"))).T.tocsr().astype(np.float32)
            f = pd.read_csv(io.BytesIO(read("features.tsv.gz")), sep="\t", header=None)
            b = pd.read_csv(io.BytesIO(read("barcodes.tsv.gz")), sep="\t", header=None)[0].astype(str)
            if genes is None:
                genes = f
            assert f[0].equals(genes[0]), f"{sid}: genes differ"
            assert sid in meta.index, f"{sid}: no donor row in Dataset S1"
            parts.append(m)
            obs.append(pd.DataFrame({"donor": "lau" + sid, "sample": sid, "region": "PFC",
                                     **{k: meta.loc[sid, k] for k in meta.columns}},
                                    index=sid + ":" + b.values))
            print(f"{sid}: {m.shape[0]} nuclei", flush=True)
    obs = pd.concat(obs)
    X = sp.vstack(parts, format="csr")
    var = pd.DataFrame({"gene_ids": genes[0].astype(str).values}, index=pd.Index(genes[1].astype(str).values))
    print(f"{len(samples)} donors, {X.shape[0]} nuclei: {obs.groupby('disease').donor.nunique().to_dict()}", flush=True)
    a = ad.AnnData(X, obs=obs, var=var)
    a.var_names_make_unique()
    return a
