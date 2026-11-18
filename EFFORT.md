# Effort log: adding the AD field (claims/COMMUNITY_PLAN.md phase 6 of the reference project)

What it takes to add a field with the template and the engine; a headline number for the paper. Times are wall-clock.

| Step | Date | Wall time | Code written | Config / data edited | Notes |
|---|---|---|---|---|---|
| Project from the template (`scripts/63_new_project.py`) | 2026-11-16 | < 1 min | 0 lines | 0 | 5 checks pass at once |
| AD facts: regions, cell classes, contrasts, datasets, examples | 2026-11-16 | ~5 min | 0 lines | config/schema.toml, config/contrasts.toml, config/project.toml | |
| Claims of 8 papers (4 agents, 2 papers each, full text from PMC) | 2026-11-16 | ~16 min (agents in parallel; 48.5 agent-minutes) | 0 lines | 204 claims, 4488 lines of YAML; notes and inventory rows per paper | Grubman 2019 abstract only (paywalled) |
| Consolidation: region codes, inventory, datasets | 2026-11-16 | ~5 min | 0 lines | 42 region codes, 8 papers, 2 datasets | |
| Claim store from the engine: contexts rules for AD comparisons, claims config; `cli.py merge, contexts, store, rating, store, serve` | 2026-11-16 | ~15 min | 0 lines | config/contexts.toml (9 rules, 10 contrast labels), 4 [claims] keys | 204 claims in a store, all Untested (no re-tests yet); knowledge graph and MCP server work |
| Engine update; harmonisation config; loaders for PsychAD and SEA-AD | 2026-11-16 | 16 min | 138 lines (`build/seaad.py` 75, `build/psychad.py` 63, code lines without docstrings) | config/harmonise.toml (55 lines), `[tests]` and `[pipeline]` in project.toml (+10) | example loader removed; project tests from the new template pass (6) |
| Harmonisation (SLURM, both datasets in parallel) | 2026-11-16 | 84 min compute | | | PsychAD 2,577,401 nuclei, 634 donors (440 AD, 194 control), 56 min, peak 179 GiB, label agreement 0.975; SEA-AD 2,545,930 nuclei, 84 donors, 84 min, peak 266 GiB, agreement 0.958 |
| Pseudobulk DE cache, first run | 2026-11-16 | 26 min compute | | | |
| First re-tests | 2026-11-17 | 2 min compute | | | every claim not testable outside its own dataset; the meta-analysis stopped (no cross tests); engine fixes 6-8 below |
| Engine fixes; Braak stage and cognition contrasts | 2026-11-17 | ~40 min (including a failed file copy) | engine: 95 lines (signatures 81 new, claim_meta 10, retest 2, cli 2) | config/contrasts.toml (+10), config/contexts.toml (+1 rule) | |
| DE refit and re-tests | 2026-11-17 | 30 + 100 min compute | | | SEA-AD 72 fits (AD vs control, Braak early/late, cognition); store step stopped (fix 9) |
| Store and rating fixes, store and rating | 2026-11-17 | ~5 min | engine: 4 lines (build_store 3, rating 1) | | 204 claims rated |
| No-difference pattern fixed; re-tests from contexts on | 2026-11-17 | ~15 min (+ 81 min compute) | 0 lines | config/contexts.toml (1 line) | 6 claims now no-difference claims; sun2023-C25 Supported -> Contradicted, lau2020-C02 -> Supported (no effect) |
| Supplementary files: engine `supplements` command; approved downloads | 2026-11-17 | ~45 min (two approval rounds) | engine: supplements.py (~170 lines) | inventory/supplements_manifest.tsv | 19 tables of 6 papers, Mathys 2023 DE results (253 CSV, 435 MB, pinned commit); PMC and Europe PMC refuse scripted downloads of author-manuscript files, so 3 papers came from the publisher |
| Signature curation, one script per paper; per-class signatures (engine); contrast overrides | 2026-11-17 | ~1 h 25 min | 301 lines (`src/ad_sc_claims/signatures/`: 6 papers, helper, runner) | claims/contrast_overrides.tsv (4 claims), `signatures_per_class` | 47 claims curated, 44 unresolved with reasons; Mathys 2019's 11 shared genes reproduced exactly |
| Re-tests with curated signatures | 2026-11-17 | 93 min compute | | | Supported 46 -> 62, Untested 96 -> 81, Contradicted 4 -> 1 |
| Atlas: `atlas` moved into the engine; AD atlas | 2026-11-17 | ~20 min (engine work) | 0 lines of AD code | `[atlas]` in project.toml (13 lines) | reports/atlas.html (1.3 MB): 204 claims, 2 datasets, 481 graph nodes; all 74 pages render |
| Three more datasets: approved downloads, loaders, Sun 2023 signatures | 2026-11-17 | ~25 min | 185 lines (loaders `leng2021` 42, `lau2020` 52, `sun2023` 63; `signatures/sun2023.py` 28) | config/project.toml (dataset list), config/harmonise.toml (`sorted_classes`), inventory/datasets.tsv (+4 rows), claims/contrast_overrides.tsv (+2) | downloads: Leng 2021 CELLxGENE h5ad 363 MB, Lau 2020 GEO tar 1.31 GB, Sun 2023 authors' release ~650 MB and tables 11 MB; Grubman 2019 downloaded and left out |
| Harmonise, DE and re-tests in five datasets (SLURM chain) | 2026-11-17 | 2 h 1 min compute (harmonise 8, DE 6, re-tests 108 min) | | | Leng 106,136 nuclei, 10 donors; Lau 179,392 nuclei, 21 donors; Sun 152,459 microglia |
| Checks of the new datasets; two fixes; Sun re-run | 2026-11-18 | ~20 min (+ 6 min compute) | engine: 3 lines (`pseudobulk`); loader: 2 lines | | fixes 17 and 19 below |
| **Total** | | **~5 h of hands-on work**, of which ~1 h 30 min engine changes AD forced; ~3 h 45 min of compute on the critical path of a clean run (harmonise 84, DE 30, re-tests 108 min); 15 min download for the first two datasets | **635 lines of AD code** (five loaders 295, signature scripts 340; counted again 2026-11-18, code lines without docstrings or comments) | | engine changes forced by AD: ~700 lines with tests, all in the reference project |

## What the AD field forced back into the template or the engine
1. The extraction brief (how to get full text and code claims) should ship with the template, generalised: Europe PMC
   `fullTextXML` fails for NIH author manuscripts outside the open-access subset; NCBI `efetch db=pmc` or the PMC
   OAI-PMH service return the same text. To do: `template/claims/EXTRACTION.md`.
2. Region codes need a glossary next to the vocabulary: the brief mapped Brodmann area 10 to DLPFC (wrong: frontopolar),
   and three files followed it; fixed here by hand. To do: an optional `[region_glossary]` in config/schema.toml.
3. Moved into the engine for AD (reference project, branch engine-store): merging claims, contexts
   (config/contexts.toml) and the store build, which now accepts a project without vocabularies, tests,
   evidence summaries, signatures, consensus statements or datasets; the rating likewise; a command line
   (`src/claimstore/cli.py`) because a template project has no scripts. Outputs of the reference project unchanged.
4. Harmonisation, pseudobulk, the DE cache and the claim re-tests moved into the engine (reference project, branch
   engine-pipeline), so AD needed only its two loaders and config.
5. A reader for large files (`claimstore.h5io.read_csr_many`, branch engine-large-reads, 153 lines with tests): it sizes
   the matrix first and fills it in place, reads several files into one matrix, and switches to 64-bit indices above
   2^31 stored values. SEA-AD's two regions would have needed about 350 GB with the old reader (chunks stacked by
   copying); peak 266 GiB with the new one. Reads of 5 PD files identical to the old reader.
6. Cross-tests now include claims whose own dataset is not harmonised in the project (contexts status "no dataset").
   Before, 174 of the 204 AD claims were tested nowhere, since the papers' own data (ROSMAP and others) are not here.
   In PD every claim's dataset is harmonised, so PD is unaffected.
7. A `signatures` command: a gene table from the genes the claims name, plus any curated per-paper tables in
   `claims/signatures/`. The reference project has its own combining script; a new field had nothing.
8. The meta-analysis runs with no cross-dataset tests and with missing test columns.
9. The store and the rating accept a signature table without ranks, statistics or comparisons, and test tables with
   no claim variants (both crashed on AD).
10. The no-difference pattern (`null_pattern` in config/contexts.toml, copied from PD) missed all six AD claims that
    assert no difference ("do not differ", "does not change", "no ... changes"); sun2023-C25 was rated Supported
    because a change was found. Broadened here and in the template; claims re-tested 2026-11-17.
11. Supplementary files: a new field had no way to fetch them. `cli.py supplements` lists each paper's files first
    (`--list`, nothing downloaded) and fetches only the approved ones (`--only`); a web page served in place of a file
    (an error or a bot check) is refused. PMC and Europe PMC refuse scripted downloads of author-manuscript files; the
    publisher's server has the same tables for Nature-family papers.
12. Signatures per cell class (`[tests] signatures_per_class`): Mathys 2019 and Lau 2020 give DE lists per cell type;
    applied as one gene -> direction map, neuron genes were tested in glia too.
13. Curation rules (`template/claims/SIGNATURES.md`, from the reference project's `claims/SIGNATURES.md`).
14. The atlas (`claimstore.atlas`, `cli.py atlas`): the AD atlas is built from config alone (`[atlas]`).
15. Contexts mapped four claims to the wrong contrast (two disease-progression claims mention cognition, two concern
    the alternative-ageing trajectory); fixed with `claims/contrast_overrides.tsv`. The extraction brief should ask
    for the orientation of each claim (to do with `template/claims/EXTRACTION.md`).
16. Config, not code: a stage contrast needs a name and label that contexts rules can point at (`ad_pathology`, Braak
    NFT stage), and a cognition contrast (no dementia vs dementia).
17. A release of sorted nuclei only (Sun 2023: microglia) is not tissue. The engine built the whole-tissue pseudobulk
    ("ALL") from whatever nuclei a dataset holds, so a whole-tissue claim (lau2020-C11) was tested on Sun's microglia.
    Fixed in the engine (`pseudobulk`: no "ALL" when every nucleus is sorted, branch sorted-only-release); datasets
    mixing sorted and unsorted nuclei (the reference project's kamath2022, its only dataset with sorted nuclei) are
    unchanged.
18. Label agreement depends on sequencing depth. Per nucleus, marker calls agree with the cell class in 0.77 (Leng),
    0.84 (Lau) and 0.70 (Sun) of nuclei, against 0.96-0.98 in PsychAD and SEA-AD; Leng's microglia have a median of
    552 UMIs per nucleus, PsychAD's 4,306. Every author label's majority marker class is still its mapped class
    (`harmonised/<dataset>_label_check.tsv`, `marker_majority`), apart from Sun's MG5 (phagocytic; majority "Immune
    (other)") and two Lau clusters (440 nuclei called microglia, majority oligodendrocyte; 7,331 called "Neurons
    (other)", majority excitatory). The 0.95 rule of thumb holds for deep data only; check the per-label majority for
    shallow data.
19. A missing donor ID must stop a loader: Sun's release has 2,087 hippocampus nuclei without one, and `astype(str)`
    turned them into one donor "nan" (pooling many donors, AD and non-AD). No test used it; fixed in the loader. To do:
    a check in `harmonise.finalise` (donor not empty and not "nan").

## Results (2026-11-18, five datasets)
204 claims, five datasets: SEA-AD, PsychAD, Leng 2021 (EC, SFG), Lau 2020 (PFC) and Sun 2023 (microglia of six
regions). Each paper's claims are tested in its own data where it is here (Gabitto 2024 in SEA-AD; Leng, Lau and Sun in
theirs) and every claim in every other dataset: 976 test rows, 416 of them informative (129 reproduced, 179 direction
only, 100 not reproduced, 8 contradicted). 123 claims are rated, 114 of them on 3-5 independent cohorts.

| Verdict | Claims | Certainty | Two datasets (2026-11-17) |
|---|---|---|---|
| Supported | 55 | 11 high, 12 moderate, 24 low, 8 very low | 62 |
| Supported (no effect) | 1 | high | 1 |
| Partly supported | 1 | moderate | 2 |
| Inconclusive | 62 | 5 high, 9 moderate, 21 low, 27 very low | 57 |
| No effect | 3 | 1 high, 2 moderate | 0 |
| Contradicted | 1 | very low | 1 |
| Untested | 81 | | 81 |

18 claims reach high certainty (none did with two datasets): with three or more independent cohorts the rating starts
from high. 26 claims changed verdict:
- Supported -> Inconclusive (13: gabitto2024-C12, C21, C27, C29; grubman2019-C08; lau2020-C10; mathys2019-C07, C13,
  C14, C20; mathys2023-C02, C04; sun2023-C19). In most, Leng (7 AD donors, 3 controls) or Lau (12 and 9) points the
  other way and the pooled interval now crosses zero. Example: lau2020-C10 (oligodendrocyte myelination genes down) is
  reproduced in Lau's own data and in PsychAD, direction only in SEA-AD, and opposite in Leng. The small cohorts are
  imprecise (standard errors 0.45-0.76 against 0.09 in PsychAD), but they disagree; the claims are not refuted.
- Inconclusive -> Supported (6): leng2021-C01 (fewer excitatory neurons in EC; the same direction in all three
  cohorts tested), mathys2023-C05 and C26, sun2023-C09 and C10 (PPARG+P2RY12+ and FOXP1+LRRK2+ microglia more common in AD,
  tested on those genes: up in Sun's own PFC, 407 donors, and in the same direction in four other cohorts),
  sun2023-C18.
- Inconclusive -> No effect (3): lau2020-C18 (complement-high microglia m6; high certainty), mathys2019-C21 (MHC-II
  microglia Mic1) and C22 (Opc1): their marker sets do not shift in 4-5 cohorts. These test state markers, not state
  proportions.
- Inconclusive -> Contradicted (1, very low): gabitto2024-C22 (microglial transcription factors and their targets up
  early along disease progression): along Braak stage not reproduced in SEA-AD itself, opposite in Leng.
- Partly supported -> Inconclusive (1): gabitto2024-C01, now moderate certainty.
- Untested -> Inconclusive (1): sun2023-C04 (fewer MG1 microglia), tested on the curated MG1 markers; no shift in
  Sun's own PFC.
- Contradicted -> Untested (1): sun2023-C25 (a state's share unchanged while its genes change): a marker test cannot
  stand in for the share (`claims/contrast_overrides.tsv`).

Why 81 claims stay untested (361 test rows over the five datasets; each claim counted by its main reason):
- no signature genes (41 claims, 205 rows): recorded as unresolved in `claims/signatures/*_unresolved.tsv` (overlap or
  specificity of gene sets, rankings of states, pathways named only in figures, timing along a trajectory);
- too few nuclei, units or genes, or no matching contrast (17 claims, 53 rows; Sun has only microglia and AD vs
  non-AD, PsychAD no Braak stage);
- templates the engine leaves to project code (13 claims, 65 rows): correlation with pathology within AD donors, sex
  contrasts, chromatin, spatial neighbourhoods, trajectories;
- coded not testable at extraction (4 claims) and no AD genetic test (4 claims);
- no contrast in the data (2 claims: sun2023-C12, C25).

Three more datasets moved one claim out of Untested (sun2023-C04, through its curated markers) and one in (C25): what
keeps claims untested is their form and the gene lists, not a lack of data.

Next: the authors' state and supertype labels as a composition test (SEA-AD supertypes, Sun's MG states: sun2023-C04,
C12, C25, lau2020-C18 and mathys2019-C21, C22 would be tested as proportions), an AD genetic test, the
pathology-correlation and sex templates, and the donor-ID check (item 19).

## Results with two datasets (2026-11-17, with curated signatures)
204 claims, 2 datasets. Tests: Gabitto 2024's 30 claims in its own data (SEA-AD); the other 174 claims across SEA-AD; all
204 across PsychAD. 140 claims have gene lists: 47 curated from the papers' tables, the rest the genes the claims name.

| Verdict | Claims | Certainty | Before curation |
|---|---|---|---|
| Supported | 62 | 18 moderate, 14 low, 30 very low | 46 |
| Supported (no effect) | 1 | moderate | 1 |
| Partly supported | 2 | 1 low, 1 very low | 2 |
| Inconclusive | 57 | 9 moderate, 4 low, 44 very low | 53 |
| No effect | 0 | | 2 |
| Contradicted | 1 | moderate | 4 |
| Untested | 81 | | 96 |

None reaches high certainty: two datasets, one brain bank each. 32 claims changed verdict, 31 of them through a curated
signature. lau2020-C07 (microglial immune activation) was contradicted on its four example genes and is supported,
moderate certainty, on the paper's 104 microglial DEGs; lau2020-C10 went from No effect to Supported in the same way;
leng2021-C13 and C15 (RORB+ vulnerable neurons) went from Contradicted to Inconclusive on the paper's 100 markers. Four
claims went from Supported to Inconclusive when their 3-5 named genes were replaced by the full marker sets
(mathys2019-C11, C17, C21, lau2020-C19). The one contradiction left is sun2023-C25 (homeostatic microglia proportion
unchanged in AD; a change was found), the paper whose tables could not be fetched.

Why 81 claims stay untested (162 test rows, two datasets each):
- no signature genes (86 rows): Sun 2023's tables are not here (PMC and Europe PMC refuse scripted downloads, the
  publisher's copy was not requested), and claims recorded as unresolved in `claims/signatures/*_unresolved.tsv`
  (overlap or specificity of gene sets, pathways named only in figures, timing along a trajectory, tables on the
  SEA-AD bucket);
- templates the engine leaves to project code (30 rows): correlation with pathology within AD donors, sex contrasts,
  chromatin, spatial neighbourhoods, trajectories;
- too few nuclei, units or genes for the cell type or contrast (28 rows, half in PsychAD, whose release has no Braak
  stage or other AD staging);
- no AD genetic test configured (`[tests] genetic_test`; 10 rows);
- coded not testable at extraction (8 rows).

## Analysis choices to review
- SEA-AD: AD = ADNC Intermediate or High; control = ADNC Not AD or Low; the young neurotypical reference donors are left out.
- PsychAD: AD = the release's AD_status flag (whatever other diagnoses the donor has, listed in `comorbidity`);
  control = neurotypical; donors younger than 60 left out.
- Cognition claims: no dementia vs dementia, all donors.
- Claims about AD pathology traits are tested along Braak NFT stage (SEA-AD only).
- Leng 2021 (2026-11-17): all 10 donors; AD = Braak 2 and 6, control = Braak 0; early AD = Braak 2, late AD = Braak 6.
- Lau 2020 (2026-11-17): all 21 donors; AD (12) vs non-demented controls (9) as in the paper; cell classes by
  marker clustering (no author labels released).
- Sun 2023 (2026-11-17): microglia only, marked sorted; AD = early + late AD vs non-AD; no Braak stage, so the
  early/late-AD contrasts are not tested there. 2,087 hippocampus nuclei without a donor ID left out (2026-11-18).
- Leng 2021 and Sun 2023: the authors' cell labels are kept although per-nucleus marker agreement is 0.77 and 0.70
  (shallow data; item 18).
- Grubman 2019 (2026-11-17): left out; its GEO samples pool two donors each.

## Datasets
- psychad: the MSSM CELLxGENE release (4,140,453 nuclei, 1,042 donors), the file the reference project harmonised as
  lee2026, linked into raw/psychad_mssm and harmonised here with AD donor selection: 2,577,401 nuclei, 634 donors.
- seaad: CELLxGENE whole-taxonomy MTG (50.8 GB, 1.38 M nuclei, 89 donors) and DLPFC (53.2 GB, 1.40 M nuclei, 83 donors) h5ad in raw/seaad: downloaded in 15 min on a compute node (2026-11-16), sizes equal to the published ones to the byte, both open; raw counts in `raw`; donor metadata ADNC, Braak, Thal, CERAD, cognitive status, age, sex, PMI, Lewy-body pathology, LATE-NC; author labels Class / Subclass / Supertype. Harmonised: 2,545,930 nuclei, 84 donors (the aged cohort).
- leng2021: CELLxGENE collection 180bff9c (Leng et al. 2021), the whole-region EC (124.9 MB) and SFG (238.0 MB) h5ad,
  raw UMI counts; 10 male donors (Braak 0: 3, Braak 2: 4, Braak 6: 3), both regions each; 106,136 nuclei (EC 42,528,
  SFG 63,608); the authors' cell types.
- lau2020: NCBI GEO GSE157827 RAW tar (1.31 GB), one filtered 10x matrix per donor, used as released (no further
  nucleus filter); donor data from the paper's Dataset S1; 21 donors (12 AD, 9 control), 179,392 PFC nuclei; cell
  classes by marker clustering (32 Leiden clusters, no author labels released).
- sun2023: the authors' de-identified ROSMAP release (immune-cell counts 631.6 MB as an R matrix, converted once by R;
  metadata of the microglia they kept, with states MG0-MG12): 150,372 microglia, 424 donors (205 AD, 219 non-AD), six
  regions (PFC for all donors, five more for 46-66 donors); marked sorted.
