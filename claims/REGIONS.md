# Region glossary

One row per region code of `config/schema.toml` and `config/harmonise.toml` (written 2026-11-18). Claims and datasets
must agree on what a code means, or a claim is tested in the wrong tissue. `config/contexts.toml` `[region_map]` says
which dataset regions test a claim's region; evidence from another region counts as indirect in the rating.

| code | full name | also called (in papers and datasets) | Brodmann area | datasets |
|---|---|---|---|---|
| `PFC` | prefrontal cortex | "prefrontal cortex" without an area; Mathys 2019 sampled area 10 | various; area 10 is frontopolar | lau2020, sun2023 |
| `DLPFC` | dorsolateral prefrontal cortex | SEA-AD "A9"; PsychAD "DLPFC" | 9, 46 | seaad, psychad |
| `SFG` | superior frontal gyrus | Leng 2021 "SFG" | 8 (Leng 2021) | leng2021 |
| `MTG` | middle temporal gyrus | SEA-AD "MTG"; Sun 2023 "MT" (midtemporal cortex) | 21 | seaad, sun2023 |
| `EC` | entorhinal cortex | Leng 2021 "caudal EC"; Grubman 2019 "EC" | 28, 34 | leng2021, sun2023 |
| `hippocampus` | hippocampus | Sun 2023 "HC" | (not neocortex) | sun2023 |
| `AG` | angular gyrus | Sun 2023 "AG" | 39 | sun2023 |
| `thalamus` | thalamus | Sun 2023 "TH" | (subcortical) | sun2023 |
| `occipital` | occipital cortex | claims only | 17-19 | none |

Notes:
- A claim on `PFC` is tested in `PFC` and `DLPFC` data (`[region_map]`): the same lobe, not always the same area.
  Mathys 2019's area 10 is frontopolar cortex, not dorsolateral prefrontal cortex; its claims tested in DLPFC data are
  tested in a neighbouring area.
- `multiple`: a claim made across several regions; it is tested in every region of each dataset.
