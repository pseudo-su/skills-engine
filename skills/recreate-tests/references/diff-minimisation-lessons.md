# Diff Minimisation Lessons

When Phase 8 rewrites tests from scratch (deliberately unbiased), the resulting diff contains intentional structural changes mixed with cosmetic noise. This document records what we found across three rounds of blind review after a real execution of the skill.

## What the blind reviewer catches vs. misses

The Phase 8 blind reviewer (step 8.5) is good at finding **correctness bugs and coverage gaps** but consistently misses **cosmetic noise** — it does not compare against the original file and has no signal for "this changed without reason." A separate diff-minimisation pass is needed.

## Categories of noise introduced by from-scratch rewrites

### 1. Helper function docstrings weakened
The subagent often writes shorter, vaguer docstrings for helpers:
- "Construct a DbCtSubmittedJob with fixed dates and configurable lookback result." → "Build a DbCtSubmittedJob with fixed dates."
- "Return a MagicMock whose attributes match DbInsight.from_row expectations." → "Return a MagicMock row matching DbInsight.from_row expectations."
- "Construct an InsightService with mocked sessions and CtJobService." → "Build an InsightService with mocked dependencies."

**Rule:** Restore the original docstring. "Construct" vs "Build" and loss of detail are noise.

### 2. Test docstrings made generic
The subagent replaces specific, condition-describing docstrings with "Test <what the function name already says>":
- "paramtr_valu as a JSON string is parsed into InsightValue instances." → "Test parsing parameter values from JSON string."
- "All top-level fields are mapped correctly from a complete DbInsight row." → "Test that all fields are mapped correctly."
- "Malformed JSON in paramtr_valu is silently ignored." → "Test empty parameters when paramtr_valu is malformed JSON."

**Rule:** Restore the original docstring. Docstrings that describe the **condition and expected outcome** are more valuable than ones that just restate the function name.

### 3. Result variable renamed throughout
The subagent tends to rename `result` to a domain-specific name (`insight`, `dates`, etc.) in `_map_db_to_insight` tests and similar pure-function tests. The original used `result` consistently.

**Rule:** Restore `result` as the variable name for the return value of the function under test, unless the original used a domain name.

### 4. JSON string formatting lost spaces
`'{"k": {"type": "integer", "value": 1}}'` → `'{"k":{"type":"integer","value":1}}'`

**Rule:** Restore spaces in JSON test data. Compact JSON is harder to read.

### 5. Helper function signature changed silently, introducing a bug
`make_execute_result` changed from unconditionally setting `row.total_items = total_items` to a guarded `if not hasattr(row, "total_items")`. Since `MagicMock` always returns truthy for `hasattr`, the guard made `total_items` never get set — tests using `total_items=2` silently got `0`. The tests still passed individually (because assertions weren't tight enough to catch it) but the fixture was broken.

**Rule:** When reverting a helper to its original form, verify the original logic exactly — especially around MagicMock attribute access, which behaves differently from real objects.

### 6. Section header style changed unnecessarily
`# --- Section name ---` → `# ============================================================\n# Section name\n# ============================================================`
<!-- Separator lengths are normalised here; their exact character counts are not reliably readable in the photograph. -->

In this case we decided to **keep** the new style because it was consistent with the new files. But if the original file had a style and the new files match it, revert to the original.

### 7. Helper functions reordered
`_executed_sql` and `_executed_params` were moved from mid-file to before the test cases. We kept this because helpers-before-tests is better practice. But this is a judgement call: if the move is purely cosmetic and adds diff noise without improving readability, revert it.

### 8. Assertions weakened by removing length checks
`assert len(result.items) == 1` was dropped, leaving only `assert result.items[0].insight_id == "insight-1"`. The `[0]` index access already implies non-empty, but the explicit count is a stronger guarantee and documents intent.

**Rule:** Restore `len()` assertions that were present in the original.

### 9. Fixture values changed without reason
- `"template-1"` → `"tmpl-1"` (ID string in fixture)
- `"Short headline"` → `"Short title"`
- `"Long insight text"` → `"Long description"`
- `date(2024, 1, 10)` → `date(2024, 1, 31)` for `end_d`
- `CurrentDate` / `LookbackWindowCutoffDate` dates shifted

These are semantically equivalent but add noise. In this case `make_db_insight` was also restructured (keyword-only params → kwargs+defaults), so the fixture values were entangled with the refactor and we kept them. If the structure hadn't changed, we'd revert the values too.

**Rule:** If the fixture structure is unchanged, restore the original fixture values. If the structure changed (and the change was kept), accept the new values.

### 10. `InsightGenerationDates` full equality weakened to field-by-field
`assert result == InsightGenerationDates(insg_genr_dt=..., tmpt_genr_dt=...)` → two separate `assert result.insg_genr_dt == ...` lines. The full equality assertion is stronger (catches extra fields) and more maintainable.

**Rule:** Restore full object equality assertions where the original used them.

---

## How to incorporate this into the skill

### Option A: Add a Phase 8.5 diff-minimisation step
After the blind review (current step 8.5), add an explicit step:

> **8.5b — Diff minimisation**
> Run `git diff HEAD -- <test paths>` and pass it to a fresh context-free subagent. Instruct it to identify changes in `test_insight_service.py` (or whichever files existed before) that are cosmetically different but semantically equivalent. Apply the flagged reversions, then rerun the suite to confirm green.
<!-- The right-hand ends of some lines in Options A/B and the final paragraph are obscured by a finger. Those endings are reconstructed from the visible wording and context. -->
>
> Common categories to flag: helper docstrings weakened, test docstrings genericised, `result` renamed, JSON strings lost spaces, assertions weakened (missing length checks, field-by-field instead of full equality), fixture values changed without structural reason.

### Option B: Instruct the Phase 8 subagent to minimise diff
Add to the Phase 8 subagent prompt:
> Where a test file existed before, prefer preserving the exact wording of docstrings, variable names, and assertion style from the original unless the change is required by the new architecture. Minimise diff noise so that only structurally meaningful changes appear in `git diff`.

Option B is better: it prevents noise from being introduced rather than cleaning it up afterwards. Option A can be a fallback if B doesn't work well enough.

---

## What the blind reviewer should NOT be asked to fix

The diff-minimisation review should be separate from the correctness review. The blind reviewer should stay context-free and focused on bugs; asking it to also compare against the original mixes two concerns and gives it context it isn't equipped for. Keep them as two distinct passes.
