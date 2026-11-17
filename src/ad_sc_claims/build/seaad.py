"""seaad: SEA-AD (Gabitto et al. 2024 Nat Neurosci), CELLxGENE whole-taxonomy releases of the middle temporal gyrus
(MTG) and the dorsolateral prefrontal cortex (DLPFC), snRNA-seq of the aged cohort's donors.

Source: raw/seaad/SEAAD_{MTG,DLPFC}_whole_taxonomy.h5ad (CELLxGENE collection 1ca90a2d-2943-483d-b678-b809bf464c30).
Raw UMI counts are raw/X (X is normalised); both files share one gene index. The two regions are read into one matrix
(claimstore.h5io.read_csr_many), so a donor gives one unit per region.

Donors: the aged cohort (84 donors); the young neurotypical reference donors (5 in MTG, 3 in DLPFC: no AD staging,
and the only non-primary nuclei of the release) are left out.
disease: NIA-AA AD neuropathologic change (ADNC) Intermediate or High -> AD (sufficient to explain dementia); Not AD or
Low -> control. disease_raw keeps the ADNC level; ADNC, Thal phase, CERAD score, cognitive status, APOE4 status, Lewy
body and LATE-NC stages are donor columns (config/harmonise.toml donor_extras), as is the continuous pseudo-progression
score (cps; released for MTG only).
braak_nft: 'Braak 0'..'Braak VI' -> 0..6. age: 'NN-year-old stage' -> NN; '80 year-old and over stage' -> 90 (the
release's 90+ donors; ages 81-89 appear explicitly), flagged in age_censored. pmi: midpoint of the released bin, hours.
Cell classes: the authors' subclass (author_cell_type) through SUBCLASS_TO_CLASS; the supertype is kept as
supertype_author. VLMC are counted as fibroblasts, as in PsychAD; the release has no pericyte or lymphocyte types.
"""
import re

import numpy as np
import pandas as pd

from claimstore.config import RAW

FILES = {"MTG": RAW / "seaad" / "SEAAD_MTG_whole_taxonomy.h5ad",
         "DLPFC": RAW / "seaad" / "SEAAD_DLPFC_whole_taxonomy.h5ad"}

EXC, INH = "Excitatory neurons", "Inhibitory neurons"
SUBCLASS_TO_CLASS = {
    "L2/3 IT": EXC, "L4 IT": EXC, "L5 IT": EXC, "L6 IT": EXC, "L6 IT Car3": EXC, "L5 ET": EXC, "L5/6 NP": EXC,
    "L6 CT": EXC, "L6b": EXC,
    "Lamp5": INH, "Lamp5 Lhx6": INH, "Pax6": INH, "Sncg": INH, "Vip": INH, "Sst": INH, "Sst Chodl": INH, "Pvalb": INH,
    "Chandelier": INH,
    "Astrocyte": "Astrocytes", "Oligodendrocyte": "Oligodendrocytes", "OPC": "OPCs", "Microglia-PVM": "Microglia",
    "Endothelial": "Endothelial", "VLMC": "Fibroblasts",
}
AUTHOR_TO_CLASS = SUBCLASS_TO_CLASS
ADNC_TO_DISEASE = {"Not AD": "control", "Low": "control", "Intermediate": "AD", "High": "AD"}
ROMAN = {"0": 0, "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6}


def _age(s):
    m = re.match(r"^(\d+)-year-old", s)
    if m:
        return float(m.group(1))
    return 90.0 if s.startswith("80 year-old and over") else np.nan


def _number(s):
    """'Thal 4' -> 4; 'Braak IV' -> 4; anything else -> NaN."""
    last = str(s).split()[-1] if str(s).strip() else ""
    if last in ROMAN:
        return float(ROMAN[last])
    try:
        return float(last)
    except ValueError:
        return np.nan


def _bin_mid(s):
    """'3.2 to 5.9 hours' -> 4.55; anything else -> NaN."""
    m = re.match(r"^([\d.]+) to ([\d.]+)", str(s))
    return (float(m.group(1)) + float(m.group(2))) / 2 if m else np.nan


def _obs(o, region):
    st = o["development_stage"].astype(str)
    adnc = o["ADNC"].astype(str)
    cps = pd.to_numeric(o["Continuous Pseudo-progression Score"], errors="coerce").values \
        if "Continuous Pseudo-progression Score" in o else np.full(len(o), np.nan)
    return pd.DataFrame({
        "donor": o["donor_id"].astype(str).values, "sample": o["Specimen ID"].astype(str).values, "region": region,
        "disease": adnc.map(ADNC_TO_DISEASE).values, "disease_raw": ("ADNC " + adnc).values,
        "sex": o["sex"].astype(str).map({"male": "M", "female": "F"}).values,
        "age": st.map(_age).values, "age_censored": st.str.startswith("80 year-old and over").values,
        "pmi": o["PMI"].astype(str).map(_bin_mid).values,
        "braak_nft": o["Braak stage"].astype(str).map(_number).values,
        "author_cell_type": o["Subclass"].astype(str).values, "supertype_author": o["Supertype"].astype(str).values,
        "adnc": adnc.values, "thal_phase": o["Thal phase"].astype(str).map(_number).values,
        "cerad": o["CERAD score"].astype(str).values, "apoe4": o["APOE4 status"].astype(str).values,
        "cognitive_status": o["Cognitive status"].astype(str).values,
        "lewy_body_pathology": o["Lewy body disease pathology"].astype(str).values,
        "late_nc": o["LATE-NC stage"].astype(str).values, "cps": np.asarray(cps, dtype=float),
        "assay": o["assay"].astype(str).values,
    }, index=(region + ":" + o.index.astype(str)))


def load():
    import anndata as ad
    from claimstore.h5io import read_csr_many, read_df

    obs, sources, var = [], [], None
    for region, path in FILES.items():
        o = read_df(path, "obs")
        keep = ~o["Neurotypical reference"].astype(str).eq("True").values
        v = read_df(path, "raw/var")
        if var is None:
            var = read_df(path, "var")
        assert v.index.equals(var.index), f"{path.name}: genes differ from {FILES['MTG'].name}"
        obs.append(_obs(o[keep], region))
        sources.append((path, "raw/X", keep))
        print(f"{region}: keeping {keep.sum()} / {len(keep)} nuclei, {o.donor_id[keep].nunique()} donors", flush=True)
    obs = pd.concat(obs)
    assert obs.disease.notna().all(), "ADNC levels without a disease mapping"
    X = read_csr_many(sources, chunk=100_000)
    genes = pd.DataFrame({"gene_ids": var.index.astype(str)}, index=pd.Index(var["feature_name"].astype(str).values))
    a = ad.AnnData(X, obs=obs, var=genes)
    a.var_names_make_unique()
    return a
