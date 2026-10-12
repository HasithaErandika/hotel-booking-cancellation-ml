# AI Usage Log: Seneja Ramanayake (Member 2)

Role: Feature / ML Engineer. Owns notebooks 02, 04, 06 and 07. See
[`../docs/team/member-2-seneja-ramanayake.md`](../docs/team/member-2-seneja-ramanayake.md).

## Tool used

**Antigravity** (AI coding agent). Used for code drafting, debugging and explanations in
this member's areas. Policy: [`README.md`](README.md).

## Session log

| Date | Tool / Model | Purpose | Prompt (summary) | Output used? | Verification performed | Notes |
|---|---|---|---|---|---|---|
| 2026-09-16 | Antigravity | Code drafting: stratified Train/Dev/Test split and preprocessing pipeline | Build a stratified 70/15/15 split notebook and a shared preprocessing pipeline (feature engineering, encoding, scaling) | Yes: split and preprocessing notebooks (commits `ab8175b`, `96613a5`) | Checked split sizes and class balance per split, and that no booking appears in two splits | Seneja to add the exact prompt and any extra sessions. The custom transformers from this version could not be loaded in other notebooks, so the pipeline was rebuilt from sklearn parts on 2026-10-11 (decision #24). The split method and feature ideas carried over into notebooks 02 and 04. |

## Note on the initial docs scaffold

The starting structure of `docs/04-preprocessing-feature-engineering.md` and
`docs/team/member-2-seneja-ramanayake.md` was drafted with Claude Code on 2026-09-12
(logged in [`member-4-hasitha-erandika.md`](member-4-hasitha-erandika.md)). The final
feature choices are recorded in `DECISIONS.md` (#6, #7, #8, #22, #23) and checked by the
assertions in notebook 04.
