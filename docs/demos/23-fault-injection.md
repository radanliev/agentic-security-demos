# Demo 23: Fault Injection

## Learning Objectives

- Explain four pipeline failure modes: graceful handling, cascade, silent-wrong output, and cost blowup
- Show how a retry budget of 2 absorbs transient faults but not permanent ones
- Read a dependability scorecard: graceful 2/6 without retries, 5/6 with retries
- Distinguish this teaching toy from the pending study it illustrates (no data collected there yet)

## Conceptual Explanation

Agent pipelines meet six classic faults: timeouts, transient errors, permanent failures, malformed inputs, partial writes, and duplicate deliveries. How the pipeline ends depends on whether retries are allowed.

This toy uses 6 hand-built faults:

| Mode | Graceful | Cascade | Silent-wrong | Cost-blowup |
|------|----------|---------|--------------|-------------|
| No retry | 2/6 | 2/6 | 1/6 | 1/6 |
| Retry budget 2 | 5/6 | 1/6 | 0/6 | 0/6 |

Fault `f3` (permanent) is the lesson: retries absorb everything except the fault that will never succeed on re-execution.

Boundary: this toy is dependability under tool faults (timeouts, retries, duplicates); it is not an attack model or an isolation result (Demo 26). Different question, data, and claims.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real pipelines, services, faults, or outages
- No network access (standard library only)
- All faults and outcomes are hand-built toys

## Run It

```bash
cd demo-23-fault-injection
python3 -m pytest tests/ -v          # 5 tests, <1 min
python3 student/run_faults.py        # writes results/faults.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-23-fault-injection/INSTRUCTIONS.md).
