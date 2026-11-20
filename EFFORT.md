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
| Curated tests: the authors' labels, sex, TWAS genes; donor and region check; region glossary; Leng contrasts | 2026-11-18 | ~3 h hands-on, spread over the day between job runs | AD: 62 lines (`genetics.py` 53, signature scripts 9) and a 10-line project test; engine: 243 lines and 142 test lines | claims/state_labels.tsv (13 rows), claims/sex_claims.tsv (5), claims/contrast_overrides.tsv (+3), claims/REGIONS.md, config/project.toml (`[tests]` +2 keys, `[rating]` +4 templates) | SEA-AD Supplementary Table 4 (26 MB) downloaded after approval; items 19-26 below |
| Re-tests in five datasets, four runs | 2026-11-18 | ~80 min compute per run (SEA-AD 68-77 min) | | | run 1 stopped on a missing column (item 22); runs 2-4 after the sun2023-C25, Leng contrast and both-sexes fixes (items 21, 25, 26) |
| Phase 7a engine: method registry, shuffled-label calibration, power; 2-4-gene sets by the donor score; re-tests, store, rating | 2026-11-19/20 | ~10 min here (engine work in the reference project) | 0 lines of AD code | 0 | calibration 15-91 min per dataset, re-tests 44 min (SEA-AD cross); 5 verdicts moved (results below) |
| **Total** | | **~5 h of hands-on work** for five datasets, of which ~1 h 30 min engine changes AD forced, and ~3 h more for the curated tests; ~3 h 45 min of compute on the critical path of a clean run (harmonise 84, DE 30, re-tests 108 min); 15 min download for the first two datasets | **697 lines of AD code** (five loaders 295, signature scripts 349, genetic test 53; code lines without docstrings or comments) | | engine changes forced by AD: ~1,100 lines with tests, all in the reference project |

## What the AD field forced back into the template or the engine
1. The extraction brief (how to get full text and code claims) should ship with the template, generalised: Europe PMC
   `fullTextXML` fails for NIH author manuscripts outside the open-access subset; NCBI `efetch db=pmc` or the PMC
   OAI-PMH service return the same text. To do: `template/claims/EXTRACTION.md`.
2. Region codes need a glossary next to the vocabulary: the brief mapped Brodmann area 10 to DLPFC (wrong: frontopolar),
   and three files followed it; fixed here by hand. Done 2026-11-18: `claims/REGIONS.md` here and in the template,
   with a project test that every region code has a row.
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
    turned them into one donor "nan" (pooling many donors, AD and non-AD). No test used it; fixed in the loader. Done
    2026-11-18: `harmonise.finalise` stops on a missing donor or region.
20. The authors' labels as a composition test (`claims/state_labels.tsv`, template `claims/CURATED_TESTS.md`): a
    state's share among the nuclei of `within` per donor x region, from the labels a dataset carries (SEA-AD
    supertypes, Sun's MG states). Marker tests stood in for shares before.
21. A label claim whose state exists in one dataset only must stay out of the others (`other_datasets = none`):
    sun2023-C25 names P2RY12 and CX3CR1, so PsychAD and SEA-AD tested their expression (contradicted) instead of the
    share the claim is about.
22. Claims comparing the sexes (`claims/sex_claims.tsv`, `[tests] sex`): tested within each sex, as a class share or as
    the mean correlation of all genes with a pathology measure (donors permuted). The test skips datasets without the
    measure; a first run stopped on Leng's and Lau's missing `thal_phase`.
23. A genetic test is project code (`[tests] genetic_test`, `src/ad_sc_claims/genetics.py`): TWAS genes against the AD
    DEGs, with expression-matched random gene sets and its own random stream.
24. Every engine test draws from one random stream. Adding or removing tests shifts the random nulls of the tests
    after them in a dataset: 8 untargeted AD claims moved in the second decimal of z, no verdict. In PD a new
    whole-tissue table moved 25 tests (two outcomes, no verdict). A seed per test would remove it, at the price of
    changing every stored result once; not done.
25. Two claims had no contrast because no contexts rule matched their Braak wording (leng2021-C16 "Braak 2-4 and 5-6
    vs 0-1", C20 "across Braak stages 0, 2, 6"); fixed with `claims/contrast_overrides.tsv`. The skill now says to
    list claims without a contrast after every `contexts` run.
26. A claim about both sexes first gave one test row per sex. The rating keeps one row per claim x dataset and ranks
    only the variants "both", "revised" and "preprint", so it kept whichever sex came first: leng2021-C19's pooled
    tests went from 4 to 3 between two runs with identical test rows, and PsychAD's male contradiction was never
    seen. Now one row per dataset (`retest.both_sexes`): the sex that tests the claim hardest (for a no-difference
    claim the larger change, p doubled for the two tests), the other sex alongside. With all four datasets pooled,
    C19 came out Contradicted, which exposed that its class-level test measured another quantity than the claim
    (shares within inhibitory neurons): it is now untested. An Inconclusive verdict had hidden the mismatch.

## Results (2026-11-20: 2-4-gene sets by the donor score)
Shuffled-label calibration of the engine's tests (`cli.py calibrate`, `results/robustness/calibration_summary.tsv`):
edgeR per gene 4.1-5.6% of null tests at p < 0.05; donor score 3.5-5.7% at 2-4 and at 5+ genes (1.2% in leng2021,
7 donors: a Mann-Whitney with so few units rarely reaches p < 0.05); composition CLR 3.2-7.3% (0.8% in leng2021;
PsychAD 7.3%, at the top of the band); the random-gene competitive test 9.5-12.8% at 2-4 genes and 43-52% at 5+.
edgeR fits with at least one gene at FDR < 0.05 under shuffled labels: 12-65% (PsychAD 65%, 614 units per fit),
against about 5% expected; a given gene reached FDR < 0.05 in at most 0.32% of null fits (leng2021), so
single-gene claims are not affected. No test counts DE genes per fit.
The 2-4-gene sets moved from the competitive test to the donor score (engine `[tests] min_score_genes`, default 2;
decision in the reference project, 2026-11-19). 63 test rows switched; no other row changed. Among them reproduced
15 -> 18, contradicted 3 -> 4, direction only 24 -> 25, not reproduced 21 -> 16.

| Verdict | Claims | Before |
|---|---|---|
| Supported | 62 | 60 |
| Inconclusive | 67 | 68 |
| Contradicted | 0 | 1 |
| Untested, No effect, Partly supported, Supported (no effect) | 69, 3, 2, 1 | unchanged |

5 claims changed verdict:
- Inconclusive -> Supported: lau2020-C06 (astrocytic NRXN1, NRXN3 down; moderate: Leng's contradiction gone, PsychAD
  now reproduces, p 0.29 -> 0.002, I² 68% -> 0%); gabitto2024-C27 (oligodendrocyte cholesterol genes up late along
  CPS; very low: Leng's opposite result weaker, interval 0.13 to 0.90); mathys2023-C23 (FGF genes with cognition;
  very low: one test, SEA-AD, p 0.07 -> 0.009).
- Contradicted -> Inconclusive: gabitto2024-C22 (microglial transcription factors up early along CPS; very low: Leng's
  contradiction, p 0.03, no longer significant).
- Supported -> Inconclusive: sun2023-C18 (P2RY12, CX3CR1 down in early AD; moderate: Lau's result no longer
  significant, p 0.04 -> 0.28; interval -0.07 to 1.05).

Certainty only: up for gabitto2024-C21 (very low -> low), green2024-C15 (low -> moderate), sun2023-C10 (low -> high)
and sun2023-C21 (low -> moderate), as datasets now agree; down for mathys2019-C08 (high -> low): Leng and Lau now
show NTNG1 falling, PsychAD the other way (I² 32% -> 74%).

Inconclusive claims by reason (`cli.py power`): underpowered 34, heterogeneous 19, small_if_any 13,
pattern_not_detected 1. Median power to detect a standardised effect of 0.5: 0.20 (400 tests, 68% underpowered).

## Results (2026-11-18, evening: curated tests)
The five datasets of the morning, plus tests on the authors' own labels (SEA-AD supertypes, Sun's MG states), tests
within each sex, a TWAS-gene test, and the contrasts of two Leng claims (items 20-26): 996 test rows, 438 informative
(145 reproduced, 181 direction only, 104 not reproduced, 8 contradicted). 135 claims are rated, 118 of them on three or
more independent cohorts.

| Verdict | Claims | Certainty | Morning (five datasets) |
|---|---|---|---|
| Supported | 60 | 12 high, 11 moderate, 24 low, 13 very low | 55 |
| Supported (no effect) | 1 | high | 1 |
| Partly supported | 2 | 2 moderate | 1 |
| Inconclusive | 68 | 5 high, 9 moderate, 22 low, 32 very low | 62 |
| No effect | 3 | 1 high, 2 moderate | 3 |
| Contradicted | 1 | very low | 1 |
| Untested | 69 | | 81 |

13 claims changed verdict:
- Supported on SEA-AD's own supertype labels, along CPS (5, all very low certainty: one cohort, the source one):
  gabitto2024-C04 (L2/3 IT supertypes fall, z -4.1), C08 (Micro-PVM_3 rises, z 4.8), C09 (Astro_2 rises, z 3.4) and
  C11 (OPC_2 falls, z -2.7) from Untested; C10 (Oligo_2 and Oligo_4 fall, z -2.7) from Inconclusive. The Sst and Pvalb
  supertype claims (C03, C05, C12) stay Inconclusive.
- Untested -> Inconclusive (8):
  - leng2021-C16 (RORB+ neurons fewer at early and late AD, on the 100 RORB+ markers): reproduced in Leng's own data,
    direction only in Lau, not in SEA-AD; leng2021-C20 (microglia rise along Braak stage): reproduced in Leng and
    SEA-AD, not in Lau. Both had no contrast before (item 25).
  - mathys2019-C26 (male oligodendrocytes shift with pathology; low certainty, I² 61%), C27 and C28 (one test each,
    SEA-AD only).
  - sun2023-C12 and C25 (MG3 and MG0 shares unchanged in AD): reproduced on Sun's labels (p 0.97 and 0.41), one test.
- Untested -> Partly supported (1, moderate): sun2023-C27 (microglial TWAS genes change more in AD than
  expression-matched genes): z 2.0 in PsychAD, direction only in Sun, SEA-AD and Lau, not in Leng.

Sun's labels also confirm sun2023-C02 and C03 (Supported, high) and C04 (Inconclusive, moderate). leng2021-C19 was
tested as the inhibitory class's share within each sex, then left untested when it turned out to measure another
quantity (item 26). 20 more claims moved in the second decimal through the shared random stream (item 24), none in
verdict.

Why 69 claims stay untested (321 test rows; each claim counted by its main reason):
- no signature genes (37 claims): recorded in `claims/signatures/*_unresolved.tsv` (overlap or specificity of gene
  sets, rankings of states, pathways named only in figures, timing along a trajectory);
- templates left to project code (16): within-donor mediation and ordering models on Green's own states (green2024-C07,
  C09, C12, C13), state definitions and chromatin (sun2023-C01, C11, C15, C16, C26, gabitto2024-C02), in-situ and
  morphology claims (sun2023-C13, green2024-C16), spatial neighbourhoods (gabitto2024-C15, green2024-C27) and two
  claims coded for a later pass;
- too few nuclei, units or genes, or no matching contrast (9);
- the authors' subpopulation labels, which no dataset here carries (2: leng2021-C19, mathys2019-C25);
- AD GWAS summary statistics, which the project does not have (3: mathys2019-C15, sun2023-C23, C24; user decision) and
  a module of cognition genes with no genetic test (mathys2019-C16);
- coded not testable at extraction (1).

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
- SEA-AD supertype claims (2026-11-18): tested on SEA-AD's own supertype labels. Supertypes chosen by one rule from
  Supplementary Table 4 (scCODA along CPS): a credible decrease in >= 80% of the reference models in both MTG and A9.
  The share is taken among neurons (neuronal supertypes) or among non-neuronal nuclei (glial ones), and tested along
  CPS (`cps`), the paper's pseudo-progression score, not Braak stage.
- Sun 2023 state claims (2026-11-18): MG states from the authors' labels, among microglia; C12 and C25 (a state's
  share unchanged) only in Sun's data.
- Leng 2021's portal labels are classes only (Exc, Inh, Astro, ...) and its subcluster names are not the paper's:
  claims about EC:Exc subpopulations stay on the RORB+ marker set (C03, C04, C13, C15, C16) or untested (C06, C07).
- Sex claims (2026-11-18): mathys2019-C26 and C28 along Braak stage within one sex, for Mathys' "AD pathology"; C27
  (amyloid) along Thal phase, so only SEA-AD tests it; C25 untested (needs Mathys' subpopulation labels, which no
  dataset here carries). leng2021-C19 (no inhibitory subpopulation changes in AD, in either sex) untested: Leng's
  shares are within inhibitory neurons, so the class share, first used as a check, measures another quantity. As a
  class-level observation, the inhibitory share was lower in AD in one sex or both in all four datasets (PsychAD
  males z -2.5).
- AD genetics (user, 2026-11-18): no AD GWAS summary statistics for now, so the GWAS-heritability claims
  (mathys2019-C15, sun2023-C23, C24) are not testable; sun2023-C27 is tested on Sun's 1,036 microglial TWAS genes.
- Green 2024's mediation and ordering claims (C07, C09, C12, C13) need Green's own states (Mic.12, Mic.13, Ast.10,
  Oli.7), which no dataset here carries: left untested, not forced onto marker genes.

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
