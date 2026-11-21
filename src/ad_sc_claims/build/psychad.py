"""psychad: PsychAD (Lee et al.), MSSM cohort CELLxGENE release, DLPFC (4,140,453 nuclei, 1,042 donors), AD donors and
neurotypical controls.

Source: raw/psychad_mssm/0e853475-e298-4b09-881a-ed0b60d5a8c9.h5ad (the file the reference PD project harmonised as
lee2026, linked into this project's raw area). X holds raw integer UMI counts (float32; no raw/ layers). Rows of kept
donors are streamed in chunks.

Donor selection:
- AD = the release's AD_status flag is Yes (447 donors), whatever else the donor carries (Lewy body dementia, vascular
  dementia, schizophrenia, ...); `comorbidity` lists the other diagnoses so they can be excluded later;
- control = disease 'normal' (261 donors; every *_status flag No: neurotypical);
- everything else is left out (other dementias, psychiatric disease without AD);
- donors younger than MIN_AGE are left out: the controls span ages 19-90 and the AD donors are old, and the re-tests do
  not adjust for age (SEA-AD's aged cohort starts at 65).
age: 'NN-year-old stage' -> NN; '80 year-old and over stage' -> 90 (CELLxGENE censoring; ages 81-89 appear explicitly,
so the censored donors are >= 90), flagged in age_censored. pmi, braak_nft and the other AD stagings are not in the
release (NaN), so stage contrasts are not testable here.
Cell classes from the authors' subtypes (AUTHOR_TO_CLASS), as in the reference project.
"""
import re

import numpy as np
import pandas as pd

from oktopy.config import RAW

PATH = RAW / "psychad_mssm" / "0e853475-e298-4b09-881a-ed0b60d5a8c9.h5ad"


def _cls(s):
    for pre, c in [("Oligo", "Oligodendrocytes"), ("OPC", "OPCs"), ("Astro", "Astrocytes"), ("Micro", "Microglia"),
                   ("EN_", "Excitatory neurons"), ("IN_", "Inhibitory neurons"), ("Endo", "Endothelial"),
                   ("PC_", "Pericytes"), ("SMC", "Pericytes"), ("VLMC", "Fibroblasts"), ("PVM", "Immune (other)"),
                   ("Adaptive_T", "T cells"), ("Adaptive", "Immune (other)")]:
        if s.startswith(pre):
            return c
    return "Unknown"


SUBTYPES = ["Oligo_OPALIN", "Oligo_RBFOX1", "Astro_WIF1", "Astro_PLSCR1", "Astro_ADAMTSL3", "Astro_GRIA1", "Micro",
            "OPC", "OPC_HAP1", "OPC_CHRM3", "OPC_GPR17", "EN_L2_3_IT_PDGFD", "EN_L2_3_IT_NTNG1", "EN_L3_5_IT_3",
            "EN_L3_5_IT_2_MET", "EN_L6_IT_1", "EN_L6_CT", "EN_L3_5_IT_1_PLSCR4", "EN_L3_5_IT_2_DACH1", "EN_L6B",
            "EN_L5_6_NP", "EN_L3_5_IT_1_CUX2", "EN_L6_IT_2", "EN_L6_CT_HSPA1A", "EN_L3_5_IT_3_HSPA1A",
            "EN_L6_IT_1_HSPA1A", "EN_L5_ET", "EN_L6_IT_2_HSPA1A", "EN_L3_5_IT_2_HSPA1A", "IN_VIP_TRPC6",
            "IN_PVALB_ANOS1", "IN_SST_EDNRA", "IN_VIP_BCL11B", "IN_LAMP5_RELN", "IN_PVALB_CHRM2", "IN_SST_EYA4",
            "IN_PVALB_CHC", "IN_LAMP5_LHX6", "IN_ADARB2_COL12A1", "IN_ADARB2_SV2C", "IN_ADARB2_SYT10", "IN_VIP_SCML4",
            "IN_SST_PRR16", "IN_ADARB2_RAB37", "IN_SST_MAML3", "IN_PVALB_HSPA1A", "IN_SST_NPY", "IN_LAMP5_RELN_HSPA1A",
            "IN_LAMP5_LHX6_HSPA1A", "IN_PVALB_STUM", "Endo_ITIH5", "Endo_IL1R1", "Endo_PCSK5", "PC_STAC", "PC_ADAMTS4",
            "SMC_MYOCD", "SMC_NRP1", "VLMC_ABCA6", "VLMC_DCDC2", "VLMC_SLC4A4", "PVM", "Adaptive_T", "Adaptive_NK",
            "Adaptive_B", "Adaptive_Plasma"]
AUTHOR_TO_CLASS = {s: _cls(s) for s in SUBTYPES}
AD_TERMS = {"dementia", "Alzheimer disease"}
MIN_AGE = 60


def _age(s):
    m = re.match(r"^(\d+)-year-old", s)
    if m:
        return float(m.group(1))
    return 90.0 if s.startswith("80 year-old and over") else np.nan


def load():
    import anndata as ad
    from oktopy.h5io import read_csr, read_df

    o = read_df(PATH, "obs")
    dis_raw = o["disease"].astype(str)
    disease = pd.Series(np.where(o["AD_status"].astype(str).eq("Yes"), "AD",
                                 np.where(dis_raw.eq("normal"), "control", "")), index=o.index)
    age = o["development_stage"].astype(str).map(_age)
    keep = (disease.ne("") & age.ge(MIN_AGE)).values
    print(f"keeping {keep.sum()} / {len(keep)} nuclei, {o.donor_id[keep].nunique()} donors", flush=True)
    o, disease, dis_raw = o[keep], disease[keep], dis_raw[keep]
    var = read_df(PATH, "var")
    X = read_csr(PATH, "X", rows=keep, chunk=100_000)
    st = o["development_stage"].astype(str)
    donor = o["donor_id"].astype(str)
    obs = pd.DataFrame({
        "donor": donor.values, "sample": donor.values, "region": "DLPFC",
        "disease": disease.values, "disease_raw": dis_raw.values,
        "sex": o["sex"].astype(str).map({"male": "M", "female": "F"}).values,
        "age": st.map(_age).values, "age_censored": st.str.startswith("80 year-old and over").values,
        "pmi": np.nan, "braak_nft": np.nan,
        "author_cell_type": o["subtype"].astype(str).values, "subclass_author": o["subclass"].astype(str).values,
        "comorbidity": dis_raw.map(lambda s: " || ".join(t for t in s.split(" || ") if t not in AD_TERMS
                                                         and t != "normal") or "none").values,
        "genetic_ancestry": o["genetic_ancestry"].astype(str).values, "brain_bank": "MSSM",
    }, index=o.index.astype(str))
    del o
    genes = pd.DataFrame({"gene_ids": var.index.astype(str)}, index=pd.Index(var["feature_name"].astype(str).values))
    a = ad.AnnData(X, obs=obs, var=genes)
    a.var_names_make_unique()
    return a
