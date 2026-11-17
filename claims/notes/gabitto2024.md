# gabitto2024: Gabitto, Travaglini et al. 2024, Nat Neurosci, doi:10.1038/s41593-024-01774-5, PMID 39402379

**Source used:** Europe PMC full-text XML for PMC11614693 (https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11614693/fullTextXML). The PMID was checked by title in Europe PMC ("Integrated multimodal cell atlas of Alzheimer's disease", Nature Neuroscience 2024, CC BY). I read the abstract, all Results subsections, the Discussion, the main and Extended Data figure legends, and the Methods (cohort, FANS, scCODA, patch-seq, data availability). The Supplementary Note (NEBULA DE, gene family tests) and the Supplementary Tables were not read.

**This paper's data are the SEA-AD dataset of this project (dataset id `seaad`).**

**Cohort as reported (SEA-AD)**
- 84 aged donors from the ACT study and the UW ADRC: 51 female, 33 male, age at death 65-102 (mean 88), mean PMI 7.0 h.
- ADNC: 9 not AD, 12 low, 21 intermediate, 42 high.
  - In the inventory, n_pd = 63 (intermediate + high) and n_ctrl = 21 (not AD + low). The paper does not use a case-control split; it models a continuum.
- Comorbidities were not excluded: LBD, LATE-NC, vascular. 42 of 84 donors had one or more severe copathologies.
- 2 donors were excluded for low RIN or pH, leaving 82 donors in the composition models.
- 11 of the 42 high-ADNC donors are "severely affected". They have lower data quality, NeuN-ir loss and the steepest memory decline, and were excluded from all gene expression tests.

**Regions**
- MTG: area 21, intermediate subdivision.
- A9: tissue from the superior frontal gyrus, in the rostrodorsal PFC. The claims label it `DLPFC`, following the brief's Brodmann rule. It could also be labelled `SFG`.

**Assays and sizes**
- MTG: snRNA-seq (10x v3.1), snATAC-seq and 10x Multiome. 3.4 million high-quality nuclei across all modalities, mapped to 139 supertypes (125 from the BRAIN Initiative MTG reference plus 14 new non-neuronal types/states).
- Nuclei were FANS-sorted to 70% NeuN+ and 30% NeuN-. Neuronal and non-neuronal compositions were therefore modelled separately, and all proportions are relative within those groups.
- MERFISH: 140-gene panel, 69 sections from 27 donors, about 350k cells with cortical depth.
- A9: snRNA-seq of the same donors, 1.2 million nuclei, mapped to a matched A9 taxonomy.
- Quantitative neuropathology: IHC for AT8, 6E10, pTDP-43, α-Syn, IBA1, GFAP and NeuN, quantified with HALO. These measurements feed the continuous pseudoprogression score (CPS, 0-1).
- Ten public PFC datasets (707 donors, 4.3 million nuclei) were reprocessed and mapped to the A9 taxonomy. Only refs 13 (Green et al., ROSMAP DLPFC = green2024) and 14 (Mathys et al. 2023) were large enough for composition replication.

**Data access**
- Processed snRNA-seq and Multiome h5ad files are open: AWS Open Data bucket `sea-ad-single-cell-profiling`, CELLxGENE and the Allen Brain Cell Atlas.
- snATAC peak matrices are in the same bucket.
- MERFISH data are open: AWS bucket `sea-ad-spatial-transcriptomics`.
- Neuropathology images are open: `sea-ad-quantitative-neuropathology`. Derived variables and donor metadata are at https://portal.brain-map.org/explore/seattle-alzheimers-disease.
- FASTQ files are controlled access at Synapse syn26223298.
- The supertype labels of the reprocessed public datasets are in the AWS bucket, without expression or metadata.
- Code: https://github.com/AllenInstitute/SEA-AD_2024.
- Author cell labels (supertypes) and CPS are in the public objects.

**Claims left out, and why**
- CPS construction and the two neuropathological epochs: Aβ plaques and pTau-bearing neurons rise exponentially after CPS of about 0.4-0.6, plaque diameter rises early, NeuN-ir falls linearly, and CPS correlates with Braak, Thal, ADNC and CASI but not with age. This rests on IHC only (not single-nucleus data) and serves as the comparison axis of every claim here.
- The summary count "36 of 139 supertypes affected", and "32 of 58 MTG-affected supertypes also change in A9". These are covered by the cell-type-specific claims C03-C11.
- Taxonomy, mapping and integration methods, and the concordance of the SEA-AD microglial, astrocyte and oligodendrocyte taxonomies with Green and Mathys (Figs. 6b,h and 7c). These are atlas comparisons, not disease contrasts.
- Patch-seq electrophysiology and morphology of vulnerable Sst and Pvalb types (higher Sag, lower Tau, morphological range). This comes from neurosurgical non-AD tissue and is noted under C16.
- Hundreds of genes selectively expressed in vulnerable Sst and Pvalb types (Supplementary Table 7). This is a property of the types, with no disease contrast.
- Oligodendrocytes having the highest APP and PSEN1 expression. No disease contrast; noted under C26.
- L5 IT neurons lost late. This appears only in the Fig. 8a schematic legend.
- Severely affected donors' steeper memory decline and NeuN-ir loss. Clinical and IHC data; part of the context of C01.
- No mouse or iPSC claims in this paper.

**Ambiguities and caveats**
- scCODA used the sequencing library as the sample in SEA-AD, so donors with several libraries contribute more than once. The authors checked donor grouping in Extended Data Fig. 7j. For refs 13 and 14 the unit was the donor.
- The "credible" threshold is a mean inclusion probability above 0.8 across 139 reference-rotated models. No FDR is used.
- Most named vulnerable supertypes appear only in Fig. 3b and Supplementary Table 4. The text names only Sst_20, Sst_25, micro-PVM_3, Astro_2, Oligo_2, Oligo_4 and OPC_2. A re-test needs label transfer to the SEA-AD/BRAIN Initiative supertypes; the SEA-AD reference makes this possible.
- The early/late epochs are defined on CPS, which only SEA-AD has. Other datasets need ADNC, Braak or quantitative pathology as a proxy, and the authors show that effect sizes are smaller with ADNC.
- DE used NEBULA (a negative binomial mixed model) along CPS per supertype. Most claims are from the MTG; A9 DE is not reported in the main text. The early and late effect sizes come from fits on donors in each epoch (Extended Data Fig. 8a,d).
- Gene symbols are given as printed: "CDRH3" (C23) is not an HGNC symbol, and "FDFT" (C27) is presumably FDFT1. The EGF ligand and receptor in C24 are not named.
- The oligodendrocyte loss (C10) is contradicted in the Green and Mathys data, as the authors themselves report.
