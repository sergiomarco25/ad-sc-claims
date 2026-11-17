# green2024: Green, Fujita, Yang et al. 2024, Nature, doi:10.1038/s41586-024-07871-6, PMID 39198642

**PMID correction:** the suggested PMID 39265577 is wrong. It belongs to an unrelated Cell 2024 paper (Lascaux et al., "TEX264 drives selective autophagy of DNA lesions..."). A Europe PMC title search for "Cellular communities reveal trajectories of brain ageing and Alzheimer's disease" gives PMID 39198642, PMCID PMC11877878 (NIHMS2051794).

**Source used:** Europe PMC `fullTextXML` for PMC11877878 returned HTTP 500. This is an NIH author manuscript, not in the open-access subset. The same author manuscript (full JATS text, Methods and figure legends) was taken instead from NCBI E-utilities: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=PMC11877878&rettype=xml. It may differ in wording from the final Nature version. I read the abstract, all Results subsections, the Discussion, the Methods (cohort, proportions, trait association, mediation, BEYOND, smFISH, Visium) and the main and Extended Data figure legends. Supplementary Tables 1-6 were not read.

**Cohort as reported**
- ROSMAP (Religious Orders Study and Rush Memory and Aging Project). These are prospective community cohorts of older people without dementia at enrolment, followed with annual cognitive testing.
- Region: DLPFC (BA9), frozen tissue from one hemisphere. Neocortical Aβ and tau were measured in the midfrontal cortex of the opposite, fixed hemisphere.
- 465 participants profiled. 437 were retained for analysis: those with WGS and enough nuclei, each with at least 868 nuclei.
- Of the 465: mean age at death 89.1; 67.3% women; 62.4% pathological AD (NIA-Reagan); 36.3% AD dementia; 26% MCI.
  - In the inventory, n_pd = 290 and n_ctrl = 175. I derived these from 62.4% of 465; the paper gives only percentages. The study is not case-control.
- Assay: 10x snRNA-seq. Eight participants were pooled per library and demultiplexed with demuxlet against WGS genotypes.
- 1,649,672 nuclei, in 95 subpopulations; 91 were used for statistics after dropping rare immune types and erythrocytes. Proportions are computed within 7 cell classes: Exc, Inh, Ast, Mic (including monocytes and macrophages), Oli, OPC, vascular.
- Replication: 673 independent ROSMAP participants with DLPFC bulk RNA-seq. Subpopulation proportions were inferred with CelMod, trained on the 419 participants who have both data types. 62 subpopulations were predicted reliably. The meta-analysis has n = 1,110.
- Validation:
  - smFISH (RNAscope) with IBA1 and AT8 IHC on 15 DLPFC samples from the New York Brain Bank (8 AD, 1 MCI, 6 non-impaired).
  - 10x Visium on 10 discovery participants.
  - PAM histopathology scores for 91 participants.

**Data access**
- Raw and processed snRNA-seq: AD Knowledge Portal, Synapse syn31512863. This is controlled access: ROSMAP data need a Synapse data use certificate.
- Bulk RNA-seq: syn3388564. Visium: syn62110225.
- Browser and code: https://github.com/naomihabiblab/BEYOND_DLPFC. ROSMAP clinical and neuropathology metadata: RADC Resource Sharing Hub (https://www.radc.rush.edu).
- Author subpopulation labels are part of the processed data on Synapse. I have not checked them.
- This dataset is "ref. 13 / Green et al. 2023" in gabitto2024, which remapped it to SEA-AD supertypes and used it to replicate SEA-AD composition changes.
- It is not one of this project's pipeline datasets (psychad, seaad).
- Donors may overlap with other ROSMAP DLPFC/PFC studies (Mathys 2019, Mathys 2023, Cain 2023). This is not verified.

**Claims left out, and why**
- Atlas descriptions: the 16 microglial, 10 astrocyte, 12 oligodendrocyte and 3 OPC subpopulations, vascular and neuronal subtypes, and their matches to published signatures (DAM2, DAA, human Aβ-associated microglia, etc.). These have no disease contrast and are kept only where they define a claimed state (C14).
- Meta-analysis-only associations of more oligodendrocyte and excitatory neuron subpopulations (Fig. 3d, Extended Data Fig. 6c). The subpopulations are not named in the text; they are in Supplementary Table 3.
- Associations with CERAD, Braak and AD dementia (Extended Data Fig. 6c). These are only in the Extended Data heat map.
- BEYOND robustness to algorithm (Palantir vs VIA) and VIA's minor third trajectory. Methods and robustness, noted under C18.
- smFISH finding that CPM-high and TPRG1-high IBA1+ cells are distinct. Folded into C14.
- No mouse or iPSC claims in this paper.

**Ambiguities and caveats**
- All associations use continuous traits: neocortical Aβ, neocortical tau and the person-specific slope of cognitive decline. None uses an AD-vs-control contrast. Re-tests need quantitative pathology, or Braak/CERAD as a weaker proxy.
- Proportions are within cell class and square-root transformed. Associations are adjusted for age, sex, PMI and library quality (nuclei and genes per participant). The unit is the participant.
- The mediation, SEM and BEYOND claims (C07, C09, C11-C13, C18-C26) are model-based orderings on cross-sectional autopsy data. The authors flag this limitation. Re-testing them needs large cohorts with full pathology and cognition.
- Marker genes for most subpopulations are in Supplementary Table 2 and are not given in full in the text.
- C08: the text says Mic.12 has "a strong association with age" without giving the sign. I recorded it as positive from the interpretation.
- The Visium validations (C27, C28) rest on 10 participants, with too few in advanced ABA to test Ast.5 > Ast.10 there.
