# grubman2019: Grubman et al. 2019, Nat Neurosci, doi:10.1038/s41593-019-0539-4, PMID 31768052

**Source used: abstract only, not the full text.**
- PMID checked by title in Europe PMC and PubMed. The paper has no PMCID. Europe PMC marks it "Subscription required" (not open access), so it has no Europe PMC full text.
- Claims come from three sources:
  1. The published abstract (PubMed / Europe PMC).
  2. The abstract and highlights of the bioRxiv preprint, "A single cell brain atlas in human Alzheimer's disease", doi:10.1101/628347, v1 2019-05-14, CC BY-NC-ND. I read these through the bioRxiv API (https://api.biorxiv.org/details/biorxiv/10.1101/628347).
  3. The GEO series record and the deposited cell covariates.
- I tried to download the preprint full text from bioRxiv, but the download was rate-limited and refused, so I did not use it.
- **Effect on the claims:**
  - No claim has a figure location, statistic or gene list.
  - The set is shorter than usual (8 claims) and probably misses Results-level claims of the published paper, such as composition changes, specific DEGs, named subcluster markers and TFs other than TFEB.
  - Re-extract when the full text (or the preprint full text) is available.

**Data**
- Region: entorhinal cortex.
- Brain bank: Victorian Brain Bank. The bank is inferred from author affiliations; it is not stated in the abstract.
- Donors: 6 AD and 6 controls (published abstract, "n = 6 per group").
- Assay: snRNA-seq, 10x Chromium. Chemistry not verified.
- Nuclei: 13,214 high-quality nuclei.
- Data: GEO **GSE138852**, open.
  - `GSE138852_counts.csv.gz` holds the counts.
  - `GSE138852_covariates.csv.gz` holds the author labels for each nucleus:
    - condition (`batchCond` AD / ct)
    - cell type (oligo, astro, OPC, neuron, mg, endo, unID, doublet)
    - subcluster (`subclustID`: a1-a8, m1-m5, o1-o6, O1-O4, n1-n6, e1-e2, u1-u7, d1-d5)
    - subcluster condition (`subclustCond`: AD / ct / undetermined)
  - So author cell labels are available.
- Interactive resource: http://adsn.ddnetbio.com.

**Pooled libraries (important for re-testing)**
- Each 10x library pools 2 donors of the same group, and donors are **not demultiplexed**. Barcode suffixes are AD1_AD2, AD3_AD4, AD5_AD6, Ct1_Ct2, Ct3_Ct4 and Ct5_Ct6.
- GEO lists 8 GSMs, including AD7-AD8 and Ct7-Ct8, and says "n = 16". The deposited covariates contain only the 6 libraries above (3 per group), which matches the published 6 + 6.
- Within this dataset, a donor-level re-test is therefore impossible. At most there are 3 pooled units per group.
- Condition is fully confounded with library.
- In the deposited labels, subclusters are almost perfectly split by condition (for example a1 220 AD / 2 ct nuclei, o1 1877 / 4, m1 74 / 4).
- Cell-type composition is also very unbalanced: astrocytes 472 AD vs 1699 ct nuclei, oligodendrocytes 4655 vs 2777.
- These patterns may partly reflect batch or dissection. I did not record them as claims because the abstract does not assert them.

**Claims left out**
- Preprint only, dropped from the published abstract:
  - "oligodendrocyte and microglia AD subclusters show discordant expression of APOE". Ambiguous: the direction in oligodendrocytes is not stated.
  - Nine gene co-expression clusters between control and AD, including clusters with mixed astrocyte/oligodendrocyte properties ("hybrid" cells, probably the `unID` class).
- Atlas statistics: subcluster counts per cell type (preprint: 5 microglial, 8 astrocyte, 6 neuronal, 6 oligodendrocyte, 4 OPC, 2 endothelial).
- Everything that exists only in the published full text, which I did not access.

**Ambiguities**
- The abstract does not say which AD subclusters carry each result. The `cell_state` values name the AD subclusters from the GEO covariates (astrocytes a1/a2, microglia m1/m2, OPC O1) as a guide for re-testing, not as the authors' attribution.
- `unit_of_analysis` = cells is inferred, not stated, because donors are pooled per library.
- `method` is not available from the abstract.
- TFEB (C08): the abstract says TFEB "regulates multiple disease genes in a specific AD astrocyte subpopulation". The direction of TFEB activity is not stated, so direction = NA.
