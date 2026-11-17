# mathys2023: Mathys et al. 2023, Cell 186(20):4365-4385.e27, doi:10.1016/j.cell.2023.08.039, PMID 37774677

**Source used**
- PMID checked by title in Europe PMC: "Single-cell atlas reveals correlates of high cognitive function, dementia, and resilience to Alzheimer's disease pathology", Cell 2023. PMCID PMC10601493 (NIH author manuscript NIHMS1933514).
- The Europe PMC `fullTextXML` endpoint returned HTTP 500. I used the PMC OAI-PMH JATS record of the author manuscript instead: https://pmc.ncbi.nlm.nih.gov/api/oai/v1/mh/?verb=GetRecord&identifier=oai:pubmedcentral.nih.gov:10601493&metadataPrefix=pmc
- From that record I read the Summary, all ten Results sections, the Discussion, Limitations, STAR Methods, and the main and supplementary (S1-S7) figure legends.
- Data S1 and Methods S1 (supplementary PDFs with many validation panels) were not read. Results that rest only on them are cited by page.
- Quotes come from the author manuscript.

**Data**
- Cohort: ROSMAP (ROS and MAP), 427 participants, 212 men and 215 women.
- Pathologic AD (modified NIA-Reagan): 238 AD and 189 non-AD. In the inventory these are n_pd = 238 and n_ctrl = 189.
- Braak stage: 115 at 0-II, 198 at III-IV, 114 at V-VI.
- Clinical consensus diagnosis at death: 146 no cognitive impairment, 102 mild cognitive impairment, 144 AD dementia; the rest other.
- Region: prefrontal cortex. No Brodmann area is given in this paper, so it is coded `PFC`. The same lab coded BA10 in 2019; see the mathys2019 note on harmonising.
- Assay: snRNA-seq with 10x Chromium 3' v3.
  - 2,359,994 nuclei after QC and Scrublet doublet removal.
  - 54 high-resolution cell types in 12 major groups: 14 excitatory, 25 inhibitory and 3 astrocyte subtypes, 5 immune and several vascular types.
- DE: muscat pseudobulk (sum per donor and cell type), edgeR, with covariates age at death and PMI. BH correction within each cell type.
- Robustness checks: RUVseq factors, sex, DecontX ambient-RNA removal, random half-cohorts.
- Where the data are:
  - Synapse via the AD Knowledge Portal, controlled access under a data use agreement with Rush or Sage. The Data availability text gives syn52293417; the key resources table gives syn51015750 (doi:10.7303/syn51015750). Both are listed in the inventory.
  - Browsable at the UCSC Cell Browser (ad-aging-brain) and http://compbio.mit.edu/ad_aging_brain/.
  - DE results on GitHub: mathyslab7/ROSMAP_snRNAseq_PFC.
- External validation data, not generated in this paper:
  - The De Jager ROSMAP DLPFC snRNA-seq (Synapse syn51123521). Results say 424 donors and Methods say 465.
  - SEA-AD MTG.
  - Multi-region ROSMAP data (MTG, angular gyrus, entorhinal cortex, hippocampus, thalamus), used for the cohesin co-expression and resilience-gene panels.
  - A combined PFC dataset of this study plus De Jager, 615 donors, used to confirm composition results.

**Claims left out**
- The cell-type atlas itself (Fig. 1). It is not an AD comparison.
- A diabetes-specific oligodendrocyte signature (Fig. 2A). It is not about AD.
- Sex-specific responses to AD pathology (Data S1 page 2H). Mentioned only in passing.
- Several validation statements: the overlap of DEGs between AD pathology measures within cell types and the correlated effect sizes (Fig. 2B-F, S2A-C); agreement with earlier snRNA-seq studies, with De Jager DLPFC and with SEA-AD MTG; and random half-cohort replication. They are robustness checks, recorded in the notes of C01. The MTG confirmation of the synaptic, splicing, lipid and mitochondrial changes (Fig. 3D) is likewise a validation in a non-own dataset.
- Cell-type-restricted DEGs (Methods S1 page 4). The text only says "a considerable fraction", with no specific claim.
- Cohesin in excitatory neurons of other regions (Fig. 4A) and across tertiles of gpath (Fig. 5D). Folded into the notes of C08.
- An excitatory-neuron decrease, significant only for neocortical gpath. Folded into the notes of C25.
- Composition of inhibitory and excitatory neurons by cognitive domain (Data S1 page 14). Folded into the notes of C28.
- Exc L2-3 CBLN2 LINC02306 abundance positively associated with perceptual orientation (Data S1 page 16). Secondary, and only in the supplement.
- Discussion speculation: VGF, FGF17, brain oscillations, and LAMP5 interneurons in mouse models. These are mouse or literature points, not single-cell findings.

**Ambiguities**
- Most DE claims are associations with continuous global AD pathology (gpath) rather than case vs control. Comparisons are written as "along global AD pathology". Stage claims (C11-C16) compare tertiles of the pathology measure.
- Composition tests mix two units: cell-level hypergeometric overrepresentation across quartile groups, and donor-level Mann-Whitney and quasi-binomial regression (age, sex, PMI).
- Several statements say "across multiple cell types" without listing them (C05, C11). For C11 I listed the major classes analysed; for C05 only excitatory neurons and astrocytes are coded.
- Gene lists for pathways and complexes (cohesin components, MIB genes, cholesterol genes, oligodendrocyte DNA damage response genes) are mainly in figures. Only the named genes are listed; STAG1 is the only cohesin gene named, in the RT-qPCR legend.
- The text cites "Figures 8I and 8J", but the manuscript has only 7 main figures; probably Fig. 7I,J (C29).
- Cognitive resilience scores (CR/CDR) are residuals of cognition, or of its slope, regressed on one of four pathology measures. Re-tests need the same construction.
