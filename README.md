# AD single-cell claim store

Claims of human post-mortem brain Alzheimer's disease single-nucleus studies, each re-tested donor-level across harmonised datasets and rated for certainty.

A claim store for one field: published conclusions extracted as structured claims (`claims/<paper>.yaml`), re-tested
in every harmonised dataset, rated for certainty (`claims/RATING.md`) and served to people and AI tools. Created from
the claim-store template of the PD single-cell claim store (https://github.com/sergiomarco25/pd-sc-claims) on
2026-11-16; the engine is kept in `src/claimstore/` (its source commit in `src/claimstore/ENGINE.txt`).

- Browse: the atlas at https://sergiomarco25.github.io/ad-sc-claims/ (`docs/index.html`): every claim with its
  rating and its re-tests in five datasets (SEA-AD, PsychAD, Leng 2021, Lau 2020 and the microglia of Sun 2023), the
  datasets, genes and a knowledge graph.
- Ask: open an issue with the question form; answers enter the evidence base as rated findings.
- Results and the effort it took to add this field: `EFFORT.md`. Data paths: `data_root` in `config/project.toml`
  (`data/`, usually a link to the data area) or `AD_SC_CLAIMS_DATA_ROOT`.

## Layout
| Path | What |
|---|---|
| `config/project.toml` | every path, the dataset list, release rules and facts about this field (`claimstore.config`) |
| `config/schema.toml` | the claim schema: required fields and vocabularies; set `region` and `cell_type` for this field |
| `config/contrasts.toml` | case and reference groups of each contrast, and the disease stage |
| `config/server_instructions.md` | what the MCP server tells AI clients about this store |
| `claims/` | one YAML file of claims per paper (`example2024.yaml` shows the format), findings, reference knowledge |
| `inventory/` | papers screened (`papers.tsv`) and datasets (`datasets.tsv`) |
| `src/claimstore/` | the engine (do not edit here; update it from the template) |
| `src/ad_sc_claims/` | what is specific to this field: dataset loaders (`build/`), harmonisation, analyses |
| `tests/` | checks run by CI: the config, the schema, every claim file |

## First steps
1. Set `region` and `cell_type` in `config/schema.toml`, then `python3 -I claims/schema/build_schemas.py`.
2. Add papers to `inventory/papers.tsv` and their claims to `claims/<paper>.yaml`; `pytest tests` validates them.
3. Define contrasts in `config/contrasts.toml` and write one loader per dataset in `src/ad_sc_claims/build/`.
4. Set paths in `config/project.toml` (or `AD_SC_CLAIMS_DATA_ROOT` and friends) and the release rules.

## Commands
`python3 -I src/claimstore/cli.py COMMAND` (`--help` lists them all), in the order a project runs them:

| Step | Commands |
|---|---|
| claims | `schema`, `merge` (validate and merge claim files), `contexts` (claim -> dataset, regions, cell classes, contrast), `supplements` (list or download the papers' supplementary files), `signatures` (each claim's genes for the re-tests) |
| per dataset | `harmonise DATASET` (loader, schema check, cell classes), `pseudobulk DATASET`, `de-cache DATASET` (edgeR) |
| re-tests | `tests internal DATASET`, `tests cross DATASET`, then `meta` (combine each claim's tests) |
| store | `store`, `rating` (verdict and certainty), `store` again (load the ratings), `serve` / `http` (MCP server), `atlas` (the browsable page, reports/atlas.html; wording in `[atlas]`) |
| release | `release VERSION`, `config --show` |

Steps from `contexts` on need pandas; `harmonise` and `pseudobulk` also anndata and scanpy; `de-cache` needs R with
edgeR and data.table (`[envs]` in `config/project.toml`).

Signatures curated from the papers' supplementary tables: `python -I src/ad_sc_claims/signatures/run.py`, then
`signatures` (rules in the reference project's template, `claims/SIGNATURES.md`). Effort and results: `EFFORT.md`.

## Licence
Code: Apache-2.0 (`LICENSE`). Claims and other data and text created here: CC BY 4.0 (`LICENSE-DATA.md`).
