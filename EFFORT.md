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
| **Total** | | **~4 h of hands-on work**, of which ~1 h 30 min engine changes AD forced; ~3.5 h of compute on the critical path of a clean run (harmonise 84, DE 30, re-tests 100 min); 15 min download | **439 lines of AD code** (two loaders 138, signature scripts 301) | | engine changes forced by AD: ~700 lines with tests, all in the reference project |

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

## Results (2026-11-17, with curated signatures)
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

Next: Sun 2023's tables (by hand), SEA-AD's supertype labels as a composition test, an AD genetic test, the
pathology-correlation and sex templates in the engine.

## Analysis choices to review
- SEA-AD: AD = ADNC Intermediate or High; control = ADNC Not AD or Low; the young neurotypical reference donors are left out.
- PsychAD: AD = the release's AD_status flag (whatever other diagnoses the donor has, listed in `comorbidity`);
  control = neurotypical; donors younger than 60 left out.
- Cognition claims: no dementia vs dementia, all donors.
- Claims about AD pathology traits are tested along Braak NFT stage (SEA-AD only).

## Datasets
- psychad: the MSSM CELLxGENE release (4,140,453 nuclei, 1,042 donors), the file the reference project harmonised as
  lee2026, linked into raw/psychad_mssm and harmonised here with AD donor selection: 2,577,401 nuclei, 634 donors.
- seaad: CELLxGENE whole-taxonomy MTG (50.8 GB, 1.38 M nuclei, 89 donors) and DLPFC (53.2 GB, 1.40 M nuclei, 83 donors) h5ad in raw/seaad: downloaded in 15 min on a compute node (2026-11-16), sizes equal to the published ones to the byte, both open; raw counts in `raw`; donor metadata ADNC, Braak, Thal, CERAD, cognitive status, age, sex, PMI, Lewy-body pathology, LATE-NC; author labels Class / Subclass / Supertype. Harmonised: 2,545,930 nuclei, 84 donors (the aged cohort).
