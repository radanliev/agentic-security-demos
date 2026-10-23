# Demo 34: Visual Injection

## Learning Objectives

- Explain typographic visual injection (rendered text in an image the agent acts on)
- Show the baseline acts on all 3/3 injections in the untrusted region
- Show a region defense (ignore untrusted) blocks 3/3 injections at a cost of 1 benign
- Distinguish the visual channel from text detectors (Demo 37)

## Conceptual Explanation

Vision-language agents read text rendered inside images. This toy uses eight hand-built images: three injections (typographic, untrusted, acted) and five benign, of which one benign in the untrusted region is also acted upon.

| Policy | Injections blocked | Benign cost |
|--------|--------------------|-------------|
| Baseline (act on all typographic) | 0/3 (3/3 succeed) | 0 |
| Region defense (ignore untrusted) | 3/3 | 1 (v07) |

The defense is perfect on injections but not free: it also drops one benign image the baseline handled.

Boundary: this demo covers the visual channel only, not text detectors (Demo 37). Different question, data, and claims.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real images, models, screenshots, or credentials
- No network access (standard library only)
- All images and verdicts are hand-built toys

## Run It

```bash
cd demo-34-visual-injection
python3 -m pytest tests/ -v          # 5 tests, <1 min
python3 student/run_visual.py        # writes results/visual.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-34-visual-injection/INSTRUCTIONS.md).
