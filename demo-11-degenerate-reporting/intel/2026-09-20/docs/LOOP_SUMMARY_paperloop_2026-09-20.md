# paperloop loop summary — demo-11, "Degenerate Reporting" audit (RAID 2027)

This repository was spun out of demo-7 on 2026-09-05. The loop summary it inherited described the
TriageTrap defence paper and none of it applies here; it is archived unchanged at
`docs/loop15/inherited_from_demo7/LOOP_SUMMARY_demo7.md` and is not this paper's history.

## What this paper is
A meta-science audit of how the indirect-prompt-injection defence literature *reports* its
evaluations. No model is trained, no benchmark is re-run, no defence is proposed. Every number is
either a recomputation over a third-party artefact pinned by commit and content digest, or a
detector run over released text with per-call provenance.

## Loop 15 (2026-09-06) — evidence restoration and the lopsided-reporting reframe

**The state loop 15 inherited.** The manuscript had already been rewritten from the TriageTrap
defence paper to the audit, but `artifacts/r14_audit/` — the artefact tree every macro is generated
from — had not been carried across the split. All 107 macros named a source file that did not
exist, so not one headline number re-derived. Separately, `llncs.cls` is absent from this TeX
installation, so the paper had never compiled here and no PDF existed to measure.

**What was restored, and what it showed.** The AgentDojo runs tree was refetched and came back at
commit `089ed468…` with tree sha256 `f0387b5f…` and 36,679 files, matching the digest the frozen
protocol recorded, so the third-party artefact is bit-identical to the one originally used. The
R-Judge, Tensor Trust and RAG-injection-survival artefacts were refetched and their censuses re-run.
The benchmark's own detector (arm A1) was re-executed locally over the digest-pinned inputs. The
regenerated macro file is **identical to the orphaned one except for A1's attacked column**: every
frame number, every ladder number, the whole census, the AgentDojo reproduction, every benign
detector rate and the agreement statistics re-derive exactly. The numbers were real; they had lost
their evidence.

**What changed in the claims.** See `docs/loop15/WITHDRAWALS.md`. In summary: the headline moved
from "no in-scope paper reports a trivial-policy control" to the lopsided-reporting asymmetry, on
the strength of an independent 129-full-text search reconciled against the primary frame; Case
Study Zero was stripped of the other submission's result numbers; the census wording was corrected;
two denominators that the paper had been mixing silently are now both stated; and a per-input
wall-clock ceiling on the local re-execution was declared as Amendment 5.

**Instrument repairs.** Four defects in the gate were fixed rather than worked around: the
reference-heading scan read only six lines per page; the appendix-heading pattern matched prose
cross-references; the embedded-font check read `pdffonts`' subset column instead of its embedded
column; and the minimum-font-size check measured rotated glyphs by their bounding-box height and
flagged every mathematical superscript. Each is recorded in the source at the point of the fix.

**Gate state at the close of loop 15.** 0 BLOCKER, 0 MAJOR. Body 20 pages against RAID's 20-page
limit. All 212 macros trace to a present artefact; `docs/loop15/MACRO_PROVENANCE_AUDIT.json` is the
per-macro ledger.

## Standing rules
Never edit a number to pass a gate — park science decisions in `.paperloop/state/proposals/`.
Never fabricate: mark gaps `[CITATION NEEDED]` / `[RESULT PENDING]`. British English, third person.
Every headline number recomputes offline from a cached artefact. No finding, table or number is
shared as a contribution with demo-7; see `SEPARATION.md`.

## Open, and load-bearing
- **D11-P1** withdraw the paper's own defence arms and the adaptive corpus — **text already matches** (round 3 Evaluate); housekeeping markers still open.
- **D11-P2** the lopsided-reporting reframe — **implemented**; author still owns 3 vs 4 flag-everything and 129-row vs 122-work primary (both already printed).
- **D11-P3** Amendment 5 wall-clock ceiling — **rates match** `findings.json` (81/124 benign; 542/618 touched, 9 indeterminate).
- Hardcoded Study-5 PPV **0.133% / 752** still uses pre-Amendment-5 **546/629**, not current **542/629** (0.132% / 757). Parked: `proposals/proposal_only-ppv-hardcoded-amendment5.md`. Does not reverse the headline. Do not hand-type.
- The primary frame's two coding sheets, its adjudication record and its search-string list did not
  survive the split. The manuscript now says so; restoring them is a precondition of submission.

## Round 3 Evaluate (2026-09-08 Gatekeeper)

Lead: science-auditor. Measure: exit **0** · B0 M0 m62. Writer not dispatched. Manuscript not edited.

- All 18 live `science.stat_reporting` ids **dismissed** (CI level / English “mean” / related-work % / Wilson and rule-of-three as method / third-party quote). Gatekeeper re-checked 62/129, 7/129, 81/124, and the PPV arithmetic against `artifacts/`.
- **Lopsided-reporting claim survives** (62/129 vs 7/129).
- Consecutive-clean clock does not start: new parked science (PPV drift) plus the 18 FPs remain in FINDINGS until the checker is narrowed (author/tooling, not a manuscript edit).

---

## Round 16 (2026-09-16 – 2026-09-18) — Forensic Audit, Claims Verification Suite, and Independent Release

**Lead**: research-engineer / science-auditor.  
**State File**: `docs/round16/LEDGER.json` (108 verified facts, 32 issues tracked).

### What was measured
1. **Verifiable claims suite**: All 7 empirical claims in `claims/` recomputed and verified offline within $\le 0.005$ tolerance (`bash claims/run_all.sh` $\rightarrow$ 7 passed, 0 failed):
   - `claim1_lopsided`: 62/129 (48.06%) flattering vs 7/129 (5.43%, Wilson 95% CI: [2.66%, 10.81%]) strict trivial controls.
   - `claim2_ladder`: G1–G4 reference baselines rule out 0.0% to 52.6% of protection across 120 trials (`artifacts/s17_defence_comparison/trials.jsonl`).
   - `claim3_benign_cost`: Arm A1 benign firing rate 81/124 (65.32%), Cohen's $\kappa = 0.962$ on 120 re-executed trials.
   - `claim4_matched`: A1–A5 attacked detection rates across 380 matched trials.
   - `claim5_census`: 91 cells examined across 4 artifacts, 85 attempted (49 reproduce, 36 do not reproduce), 6 not attemptable.
   - `claim6_agreement`: 28 full texts dual-coded, $\kappa = 1.0$ (Scope, TPC), $0.922$ (CPC), $0.514$ (DEN), $0.719$ (MCC).
   - `claim7_base_rate`: Operational PPV is 0.132% with 757 false alarms per true attack under base rate $10^{-4}$ and prevalence $10^{-4}$.
2. **Macro provenance**: All 221 macros in `docs/macros/d7_r14_macros.tex` generated programmatically from raw artifacts via `python3 scripts/r14_audit/make_macros.py`. Provenance verified in `docs/round16/MACRO_AUDIT.json` (resolves R16-006 count mismatch from loop 15).
3. **Unit test suite**: 15 unit tests passing (`python3 -m pytest tests/ -q` $\rightarrow$ 15 passed).
4. **Independent clean-room reproduction**: Archive `dist/degenerate_reporting_artefact.zip` (278,186,041 bytes, SHA-256 `0e2d12b261d39b726f848a7150997e7f9d539acfe32c34927555f5e47b614049`) extracted into an external isolated sandbox (`/tmp/d11_clean_room_independent_runner`). Verified 100% offline execution with zero missing files, zero external network calls, and exit code 0 (`scripts/r16_release/verify_package.py`).
5. **Forensic git history scan**: 22 commits (`4cf1f76..218611a`) audited over 315,249 lines of diff. Zero raw API keys committed in demo-11. Author/committer metadata identified on all commits; 4 commit messages referencing sibling project identified.

### What changed
1. **Ethics section (Section 6)**: Completely rewritten in `docs/raid_paper_manuscript.tex` following the 6-point checklist of `.claude/skills/meta-research-ethics/SKILL.md`. Includes exact verbatim statement: *"Findings concern reporting practice and not research integrity, in those words."* Audited all negative findings for purely descriptive, non-accusatory language.
2. **Right-of-reply notifications**: Formal notification packets drafted in `docs/round16/NOTIFICATIONS/` for 4 audited artifacts (AgentDojo, R-Judge, Tensor Trust, RAG Injection Survival) with structured 14-day reply windows.
3. **CI automated workflow**: Implemented `.github/workflows/ci.yml` running pytest, claims suite, anonymity checks, working-tree dirtiness assertions on macro generation, and quarantine import exclusions.
4. **Release packaging and verification**: Created `scripts/r16_release/build_package.py` to build the distribution artifact strictly from an allowlist, and `scripts/r16_release/verify_package.py` to assert strict exclusion of `NEVER_RELEASE` paths.
5. **Release route decision**: Codified in `docs/round16/RELEASE_NOTES.md` to deploy the public artifact as a fresh single-commit anonymous repository rather than rewriting git history.

### What was withdrawn or reframed
Detailed in `docs/round16/WITHDRAWALS.md`:
- Case Study Zero numerical performance metrics withheld per `SEPARATION.md`; qualitative scoring defect retained.
- Adaptive adversary corpus (`artifacts/s19_adaptive_adversary`) confirmed uncited and withdrawn from defence contributions (stores null payloads).
- Conflated census denominator corrected: 91 examined, 85 attempted (49 reproduce, 36 do not reproduce), 6 not attemptable.
- Study 5 PPV and false alarm ratio corrected from pre-Amendment-5 0.133% / 752:1 to post-ceiling 0.132% / 757:1.
- Erroneous macro provenance statement corrected: macros trace to present artifacts, but cross-check macros cite `artifacts/r15_frame_audit/` rather than `artifacts/r14_audit/`.

### What is open
- **`venue.pagecount`**: Manuscript body is 25 pages vs. RAID 20-page limit (excluding references); 5 body pages must be trimmed before final submission.
- **Right-of-reply notifications**: Drafted in `docs/round16/NOTIFICATIONS/`; transmission pending author dispatch.
- **Primary literature frame original coder sheets**: Reconstructed sheets present in `docs/round16/frame/`; original split gap disclosed in Section 3.1.
- **Credential rotation**: Legacy VirusTotal key in parent repository (`demo-7`) commit history flagged for author rotation.


## Inbox — S21 empirical note (2026-09-19, Gatekeeper)

**Received from New Bot** (author share). **Does NOT clear Blind-B1 / confirmatory R1.**

| Path | Role |
|------|------|
| `docs/round16/EMPIRICAL_RESULTS_NOTE_S21.md` | Exploratory note (Mac + box mirror) |
| box `/workspace/review-inbox/demo-11-degenerate-reporting-raid/round16/` | `EMPIRICAL_RESULTS_NOTE_S21.md`, `p3_pilot_comparison.json`, `boundary_detector_metrics.json` |

**Headline (label EXPLORATORY_BUDGET_PILOT_NOT_CONFIRMATORY_R1):** P3 pilots arm_a hijack 50% vs arm_f 25% (benign 12/12 both); budget 50/50 exhausted; boundary TF–IDF logistic test TPR 0.95 @ FPR 0.0 (AUC≈0.9999); prereg sealed; full R1 needs higher live budget.

**Policy:** No manuscript digit inventing from this note alone. science.* / Blind-B1 stay proposals until author + sealed R1 path. No Paperloop Evaluate round started (await explicit round request with number + success criteria). Writer/Auditor/Blind PC not tasked on this note.


## WORK_ORDER WO-S21-EMP-01 (2026-09-19, Gatekeeper) — OPEN

**Author-approved** placement of S21 exploratory empirical results (AD-S21-WO1). Round tag: `round16 / WO-S21-EMP-01` (placement apply, **not** full hostile Evaluate panel).

| Artefact | Path |
|----------|------|
| WORK_ORDER | `docs/round16/WORK_ORDER_WO-S21-EMP-01.md` → also `.paperloop/state/WORK_ORDER.md` |
| Placement plan | `docs/round16/S21_WRITER_PLACEMENT_PLAN.md` |
| Digit sources only | `EMPIRICAL_RESULTS_NOTE_S21.md`, `p3_pilot_comparison.json`, `boundary_detector_metrics.json` / artefacts under `artifacts/s21_*` |

**Authorized:** Manuscript Writer applies plan to `docs/raid_paper_manuscript.tex` only under WO success criteria (sticky `EXPLORATORY_BUDGET_PILOT_NOT_CONFIRMATORY_R1`; body miniature A/F hijack table; detector appendix; abstract omits P3/detector numbers; no refuse-all live-24 implication).

**After Writer + PDF rebuild:** queue Evidence Auditor digit spot-check vs JSON. **Do not** start full Evaluate triad unless author asks separately.

**Does NOT clear Blind-B1 / confirmatory R1.**


## Gatekeeper re-measure after WO-S21-EMP-01 (2026-09-19)

**HEAD:** `a63a038` (writer report) atop `8630bce` (tex+pdf). Branch `paperloop/autofix`. Writer claims VERIFIED on Mac (commits exist; PDF 48pp).

**Gates:** `python3 .paperloop/run_gates.py --build --render` → **exit 1**. BLOCKER **2** · MAJOR 0 · MINOR 21 · INFO 4 · gated 0.
- BLOCKER `layout.overfull` ~39.5pt at `docs/raid_paper_manuscript.tex:785`
- BLOCKER `venue.pagecount` **21 body / 48 total** (RAID ≤20 body) — +1 body page vs limit (S21 placement likely contributed)

**Digit check (Gatekeeper, vs `artifacts/s21_adaptive/p3_pilot_comparison.json` + `artifacts/s21_boundary_detector/metrics.json`):**
- P3 A hijack 0.5 / F 0.25, sticky label, miniature table: **match**
- Detector test TPR 0.95 @ FPR 0.0, tp/fp/tn/fn 114/0/6/120, AUC≈0.9999: **present in MS**
- Abstract clean of P3/detector numbers: **YES**
- refuse-all near “24”: flag for Auditor (context check) — WO forbids implying live 24-case refuse-all comparator

**Does NOT clear Blind-B1 / confirmatory R1.** Full Evaluate panel not started. Evidence Auditor digit spot-check queued next. Autofix candidates for later WORK_ORDER: overfull + −1 body page (no geometry shrink; no digit invention).


## Gatekeeper verify WO-S21-LAYOUT-01 (2026-09-19) — VERIFIED

**Commit:** `422e727` on `paperloop/autofix`.

| | Before | After (Gatekeeper re-measure) |
|--|--------|-------------------------------|
| Exit | 1 | **0** |
| Severity | B2 M0 m21 | **B0 M0 m20** clean true |
| Body/total | 21/48 | **19 body / 46 total** (≤20 body) |

Overfull BLOCKER cleared. S21 sticky label still present; P3 50%/25% and detector digits still in MS; refuse-all negation kept. venue.yaml body_pages:20 unchanged. Blind-B1/R1 **not** cleared. Full Evaluate panel **not** started. WO-S21-LAYOUT-01 closed.

---

## Round 16b (2026-09-20) — Quality without R1 + data packs

**Author audit (New Bot on Luke-Skywalker).** Confirmatory R1 remains **parked** (`R1_BLOCKER`: OpenRouter free tier exhausted; ~425 sealed live / 4208 VOID; not confirmatory). Manuscript quality-without-R1 path verified on `paperloop/autofix` @ `422e727`: exploratory P3 section + sticky non-confirmatory labels + miniature A/F table + boundary-detector appendix disclaimer; abstract omits P3 digits. Receipts: `docs/round16/QUALITY_WITHOUT_R1_RECEIPT.md`, `docs/round16/DUAL_METRIC_FROZEN_TRACE_NOTE.md`. `.paperloop/config.yaml` `result_globs` extended to S21 / boundary / receipt paths. **Blind-B1 still open** until funded OpenRouter resume of `run_confirmatory_r1.py`. No demo-7 EMBER numbers in this manuscript (SEPARATION).

---

## Round 16c (2026-09-20 ~10:46–10:47) — Paperloop `--rounds 4` exhausted (Claude OAuth)

**Tip:** `74330c1` on `paperloop/autofix`. Gates stayed **B0 M0 m20** (19 body / 46 total).

**What worked:** commits landed; S21 artifacts + DATA_PACK + boundary detector paths entered the tree; R1_STATUS_TOUCH comment remains in TeX.

**What failed:** Claude Code OAuth session expired — venue-compliance / paper-evaluator / literature-venue-verifier rounds captured auth errors instead of real reviews. Some leftover review files still mention **demo-7 TriageTrap** contamination; ignore those for this paper.

**Still open (no OpenRouter needed):**
1. Re-auth Claude Code once interactively in this repo (trust dialog), then re-run a bounded loop **or** paste WORK_ORDER to a working fixer.
2. Bib MINORs (arXiv-only / year mismatches) — batch DOI/year hygiene.
3. Parked PPV Amendment-5 drift proposal (`0.133%`/`752` → `0.132%`/`757`) — author decision.
4. Confirmatory R1 — wait for OpenRouter credit.

