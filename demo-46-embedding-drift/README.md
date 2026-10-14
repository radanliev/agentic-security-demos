# Demo 46: Embedding-swap cosine shift

## Learning Objectives

- Compute cosine shift `1 - cosine(baseline, replacement)` for one artefact
- Compare a toy swap with a frozen study mean (0.1222)
- See that an orthogonal swap moves farther than that frozen mean

## Safety Notice

Synthetic 4-dimensional vectors only. No models, no network, no package corpus.
The frozen mean is a label copied from the simulated study so the comparison is reproducible. It is not a new measurement.

## Reproducibility Metadata

| Field | Value |
|-------|-------|
| Python | 3.11+ (stdlib only) |
| Command | `make demo DEMO=46` |

## Research Connection

Distilled from `radanliev/demo-46-simulated-embedding-drift-aibom` (private).
That study still uses simulated representation spaces. This folder teaches the shift formula on two hand-built vectors.
