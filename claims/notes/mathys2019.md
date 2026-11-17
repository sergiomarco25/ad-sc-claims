# mathys2019: Mathys et al. 2019, Nature 570:332-337, doi:10.1038/s41586-019-1195-2, PMID 31042697

**Source used**
- PMID checked by title in Europe PMC: "Single-cell transcriptomic analysis of Alzheimer's disease", Nature 2019. PMCID PMC6865822 (NIH author manuscript NIHMS1049060).
- The Europe PMC `fullTextXML` endpoint returned HTTP 500 for this PMCID (it is not in the open-access subset). I used the PMC OAI-PMH JATS record of the author manuscript instead: https://pmc.ncbi.nlm.nih.gov/api/oai/v1/mh/?verb=GetRecord&identifier=oai:pubmedcentral.nih.gov:6865822&metadataPrefix=pmc
- From that record I read the abstract, all Results sections, the Discussion, the Methods and the main and Extended Data figure legends.
- The Extended Data / Supplementary Tables (S1-S8: DEGs, module genes, subcluster markers) are separate files and were not read.
- Quotes come from the author manuscript. The published version may differ slightly in wording.
- An Author Correction exists (PMC9009526, doi:10.1038/s41586-019-1329-6). It changes only the funding acknowledgements and does not affect the claims.

**Data**
- Cohort: ROSMAP (Religious Orders Study participants only, as stated in the paper).
- Region: prefrontal cortex, Brodmann area 10. Coded as `DLPFC` following the project rule "Brodmann 10/9/46 = DLPFC". BA10 is strictly frontopolar, so this may need harmonising with mathys2023, which says only "prefrontal cortex" and is coded `PFC`.
- 48 donors:
  - 24 with AD pathology ("AD-pathology": elevated amyloid plus other AD pathology).
  - 24 with no or very low amyloid or other pathology ("no-pathology"). This group includes some cognitively impaired donors, because selection was on pathology only.
  - 12 women and 12 men in each group, matched for age (median 86.7 vs 87.1) and education.
- Subgroups: early-pathology and late-pathology donors were defined by k-means (k=3) on quantitative traits (tangles, nft, gpath, plaq_n, amyloid, cognition). The group sizes are not given in the text.
- Assay: snRNA-seq with 10x Chromium 3' v2.
  - 80,660 nuclei profiled.
  - 75,060 nuclei after QC, with 17,926 protein-coding genes.
  - 70,634 nuclei after doublet and low-quality subcluster removal.
- Validation: RT-qPCR on NeuN+ FACS nuclei (8 vs 8 donors), RNAscope (4 vs 4), and immunohistochemistry (performed once).
- Bulk comparison: ROSMAP bulk RNA-seq, n=484.
- Where the data are: Synapse syn18485175 (doi:10.7303/syn18485175); ROSMAP metadata doi:10.7303/syn3157322. This is the AD Knowledge Portal, controlled access under a ROSMAP data use agreement.

**Claims left out**
- The cell-type atlas and annotation, with 8 broad types and 20 pre-clusters. It is not an AD comparison.
- The statement that cell-type proportions match Lake et al. 2018 (Extended Data Fig. 3). It is a methods/robustness point, and the paper makes no AD composition claim.
- RT-qPCR confirmation of 5 of 6 neuronal DEGs (Fig. 1c). It is validation, recorded in the notes of C01 and C06.
- MRI white-matter hyperintensities linked to lower cognition in women but not men (n=505 ROSMAP). These are not single-cell data; the authors use them only as support for the sex claims (C25-C28).
- The point that marker genes of AD-associated subpopulations are more highly expressed in female AD donors (Extended Data Fig. 10b,c). It is folded into C25.
- Discussion interpretations: that changes reflect cell-state shifts rather than loss, and that the sex differences could mean greater female disease burden or resilience. These are speculation, not tested.

**Ambiguities**
- Main differential expression (DE) is cell-level Wilcoxon, with a Poisson mixed model (donor random effect) required for the DEG counts. Subcluster enrichment uses a cell-level hypergeometric test, robust to subsampling 3 women + 3 men per group. Gene-trait modules (SOM) use cell-level Spearman correlations, checked at donor level.
- Fig. 1g gives P = 0.001 and P = 0.05 for APOE in microglia and astrocytes without saying which is which (C03, C04).
- Opc0 and Mic2 are the depleted counterparts in Extended Data Fig. 8 but are not discussed in the text, so they are not recorded as claims.
- Opc1 (C22) is called AD-associated only in passing.
- Gene lists for most subpopulations and modules (In0, Opc1, M3, M7, M9) are only in the Supplementary Tables, so `genes` is empty for those claims.
- C09 (bulk RNA-seq dominated by Ex/Oli changes) is a single-nucleus vs bulk comparison and is marked `not_testable` by the standard templates.
- The paper calls the cohort "ROS" in Results and "ROSMAP" in the data-availability text.

## Consolidation (2026-11-16)
- 28 claims recoded from DLPFC to PFC: ROSMAP prefrontal cortex is Brodmann area 10 (frontopolar) or unspecified prefrontal cortex, not dorsolateral; DLPFC is kept for explicitly dorsolateral samples (green2024; SEA-AD area 9 in gabitto2024).
