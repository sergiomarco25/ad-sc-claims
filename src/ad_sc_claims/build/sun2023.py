"""sun2023: Sun et al. 2023 (Cell), microglia of 424 ROSMAP donors from six regions, the authors' de-identified processed
release (personal.broadinstitute.org/cboix/sun_victor_et_al_data/, raw/sun2023/; SOURCE.tsv lists the files):
immune-cell counts (ROSMAP.ImmuneCells.6regions.snRNAseq.counts.rds: 16,228 genes x 174,420 nuclei, integer counts) and
the metadata of the 152,459 nuclei the authors kept as microglia, with their states (seurat_clusters 0-12 = MG0-MG12).

Only those microglia are kept. Every nucleus is marked enrichment = "sorted" (an immune-cell release, not whole
tissue): composition tests leave the dataset out, and Microglia is tested on its units (config/harmonise.toml
sorted_classes).
Donors (user decision 2026-11-17): AD = early or late AD (ADdiag3types; 205 donors), control = non-AD (219). The
release has no Braak stage, so the early- and late-AD contrasts are not testable here.
Regions: PFC (all donors), hippocampus, thalamus, entorhinal cortex, middle temporal gyrus, angular gyrus (43 donors).
2,087 hippocampus nuclei have no donor ID (subject empty) and are left out: pooled, they would form one false donor.
The .rds matrix is converted once by R (Matrix package; [envs] r_env or Rscript on PATH) to raw vectors in raw/sun2023/converted/.
"""
import shutil
import subprocess

import numpy as np
import pandas as pd

from claimstore import config as cfg
from claimstore.config import RAW

D = RAW / "sun2023"
RDS = D / "ROSMAP.ImmuneCells.6regions.snRNAseq.counts.rds"
META = D / "ROSMAP.Microglia.6regions.seurat.harmony.selected.deidentified.metadata.txt"
CONV = D / "converted"
REGION = {"PFC": "PFC", "Hippocampus": "hippocampus", "Thalamus": "thalamus", "EntorhinalCortex": "EC",
          "MidtemporalCortex": "MTG", "AngularGyrus": "AG"}
AUTHOR_TO_CLASS = {f"MG{k}": "Microglia" for k in range(13)}

R_CODE = r"""
suppressMessages(library(Matrix))
a <- commandArgs(TRUE); x <- readRDS(a[1]); stopifnot(is(x, "dgCMatrix"))
stopifnot(all(abs(x@x - round(x@x)) < 1e-6))
writeBin(as.integer(x@i), file.path(a[2], "i.bin")); writeBin(as.integer(x@p), file.path(a[2], "p.bin"))
writeBin(as.integer(round(x@x)), file.path(a[2], "x.bin"))
writeLines(rownames(x), file.path(a[2], "genes.txt")); writeLines(colnames(x), file.path(a[2], "cells.txt"))
"""


def convert():
    if (CONV / "cells.txt").exists():
        return
    CONV.mkdir(exist_ok=True)
    env = cfg.R_ENV / "bin" / "Rscript"  # config [envs] r_env, else Rscript on PATH
    rscript = str(env) if env.exists() else shutil.which("Rscript")
    assert rscript, "no Rscript: set [envs] r_env or put R on PATH"
    subprocess.run([rscript, "-e", R_CODE, str(RDS), str(CONV)], check=True)


def load():
    import anndata as ad
    import scipy.sparse as sp

    convert()
    genes = (CONV / "genes.txt").read_text().splitlines()
    cells = (CONV / "cells.txt").read_text().splitlines()
    m = sp.csc_matrix((np.fromfile(CONV / "x.bin", dtype=np.int32).astype(np.float32),
                       np.fromfile(CONV / "i.bin", dtype=np.int32), np.fromfile(CONV / "p.bin", dtype=np.int32)),
                      shape=(len(genes), len(cells)))
    meta = pd.read_csv(META, sep="\t")  # the header lacks the cell-name column: pandas makes it the index
    print(f"{meta.subject.isna().sum()} nuclei without a donor ID left out", flush=True)
    meta = meta[meta.subject.notna()]
    pos = pd.Series(np.arange(len(cells)), index=cells)
    missing = meta.index.difference(pos.index)
    assert not len(missing), f"{len(missing)} microglia of the metadata are not in the counts"
    X = m[:, pos.loc[meta.index].values].T.tocsr()
    del m
    obs = pd.DataFrame({
        "donor": meta["subject"].astype(str).values, "sample": meta["batch"].astype(str).values,
        "region": meta["brainRegion"].map(REGION).values,
        "disease": meta["ADdiag3types"].map({"nonAD": "control", "earlyAD": "AD", "lateAD": "AD"}).values,
        "disease_raw": meta["ADdiag3types"].astype(str).values,
        "sex": meta["msex"].map({"Male": "M", "Female": "F"}).values,
        "age": pd.to_numeric(meta["age_death"], errors="coerce").values,
        "pmi": pd.to_numeric(meta["pmi"], errors="coerce").values, "braak_nft": np.nan,
        "author_cell_type": "MG" + meta["seurat_clusters"].astype(int).astype(str).values,
        "enrichment": "sorted",
    }, index=meta.index.astype(str))
    assert obs.region.notna().all() and obs.disease.notna().all(), "unmapped regions or diagnoses"
    print(f"{X.shape[0]} microglia, {obs.donor.nunique()} donors: {obs.groupby('disease').donor.nunique().to_dict()}",
          flush=True)
    a = ad.AnnData(X, obs=obs, var=pd.DataFrame(index=pd.Index(genes)))
    a.var_names_make_unique()
    return a
