# Demo 50: Budget-Bounded Delegation

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output.

## Learning Objectives

- Explain why delegated spend must be conserved across a whole delegation tree
- Apply five budget invariants (B1–B5) to a synthetic multi-agent plan
- Distinguish a fail-closed denial from a ledger violation
- Explain why partial grants are opt-in rather than the default
- Distinguish teaching demonstrations from validated research benchmarks

**Status:** design stage, created 6 November 2026. The repository holds an offline ledger,
synthetic fixtures and tests. It holds no results; every empirical statement in a future paper is
[RESULT PENDING] until a committed analysis script derives it.

## Research question

In multi-agent pipelines where agents delegate sub-tasks to other agents, can token and cost
budgets be carried as attenuating capabilities, so that no chain of delegation spends more than
its root principal's budget, and what does that enforcement cost in completed benign work?

## Why it matters

Delegation multiplies model calls. A pipeline that fans work out to several agents, each of which
may delegate again, can consume quota and money far faster than its designers planned, whether
through faults, poorly bounded retries or manipulated inputs. For public bodies with fixed budgets,
exhausted quota is also a security event, because it forces a fall-back to other model tiers
(demo 49). Agent frameworks commonly expose per-call limits rather than budgets that are conserved
across a delegation tree [CITATION NEEDED: independent sources on multi-agent frameworks,
agent-to-agent protocols and resource-exhaustion risks].

## Invariants enforced by the ledger

| Key | Invariant |
|---|---|
| B1 | a node's own spend plus what it has delegated never exceeds its grant |
| B2 | delegation depth never exceeds the configured maximum |
| B3 | no node delegates to more children than the fan-out cap |
| B4 | every child's grant was within its parent's remaining budget when it was made |
| B5 | total spend across the tree never exceeds the root budget |

Requests that would break an invariant are denied (fail-closed). `tests/` includes a seeded
randomised test that replays 300 random plans and checks that B1 to B5 always hold.

## What is here now

| Path | Contents |
|---|---|
| `student/delegation_budget/` | `BudgetLedger`, plan replay and requested-spend accounting |
| `fixtures/synthetic_plans.json` | four synthetic formative-feedback pipeline plans; placeholders, not measurements |
| `student/run_budget.py` | prints requested versus enforced spend and writes `results/delegation_budget.json` |
| `tests/` | unit and randomised invariant tests (standard library `unittest`; also collected by pytest) |

```bash
python3 student/run_budget.py
python3 -m pytest tests/ -v
```

Everything runs offline with the Python standard library.

## Safety Notice

⚠️ **This is a teaching demonstration using synthetic fixtures only.**
- No real agents, providers, tools, or credentials
- No network access (standard library only)
- All plans and budgets are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real pipelines

## Distinctness

- Demo 16 (infection spread) models how injected content propagates between agents; demo 50 is
  about bounding the resources a delegation tree can consume, whatever the cause.
- Demo 24 (delegation checks) analyses who may authorise what between agents; demo 50 adds cost as
  a conserved quantity that travels with delegated authority.
- Demo 23 (fault injection) measures dependability under pipeline faults; demo 50 provides a
  control and asks what it costs.

## Venue plan

Plan A (proposal): IEEE/IFIP DSN 2027, abstract 25 November 2026 and papers 2 December 2026 AoE, 11-page regular papers excluding references ([CFP](https://dsn2027-berlin.github.io/call-for-contributions), checked 9 November 2026). Plan B: ACM AsiaCCS 2027 round 2, papers 11 December 2026 ([CFP](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html), checked 9 November 2026). Plan C: USENIX Security 2027 Cycle 2, registration 19 January 2027 and papers 26 January 2027 ([CFP](https://www.usenix.org/conference/usenixsecurity27/call-for-papers), checked 9 November 2026). ESORICS 2027 and ACSAC 2027 calls were not verified as published at the time of checking.

## Reproducibility Metadata

| Field | Value |
|-------|-------|
| Seed | 50 (fixed; no randomness used unless a test says otherwise) |
| Python | 3.11+ (stdlib only) |
| OS | Linux/macOS/Windows |
| Command | `make demo DEMO=50` |

## Reproducibility

```bash
python3 -m pytest tests/ -v      # 5 tests
python3 student/run_budget.py    # writes results/delegation_budget.json
```

Python 3.11 or newer, standard library only, fully offline and deterministic.

## Licence

MIT (see the repository [LICENSE](../../LICENSE)).
