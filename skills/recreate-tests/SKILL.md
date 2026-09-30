---
name: recreate-tests
description: Recreate or rewrite tests for a source file, module, or entire project. Reads the source under test, understands its behaviour and edge cases, then rewrites the test files from scratch.
argument-hint: <file, module, or directory>
disable-model-invocation: true
---

Recreate the tests for `$ARGUMENTS`. The target may be a single source file, a module (multiple related files), or an entire project directory. If no target was provided, ask what to target before continuing.

Work through the phases below in order. Phases 3 and 4 run back-to-back without stopping; all other output phases stop for confirmation before continuing. Do not proceed past a stop point until the user confirms.

## Phase 1: Read the source

If the target is a test file rather than a source file, identify the corresponding source file(s) by examining the test file's imports and the units it exercises. Use those as the source files for all subsequent phases.

If the target is a directory or module, first discover which source files it contains. Then read every source file in full. Do not skip any methods or branches.

**Scope rules:** only include source files that are directly under test in the target test file(s). Do not expand scope to transitive dependencies that already have their own separate test files — those are out of scope unless the user explicitly includes them.

## Phase 2: Read the existing tests

Read the existing test files in full. If no test files can be found for the target, record this and proceed to Phase 3 with an empty inventory.

## Phase 3: Map existing coverage from tests

Produce a dot-point inventory of what is currently tested. **Format:** See `references/inventory-format.md`. Group by test file (the top-level key is each test file path).

## Phase 4: Map expected cases from source

Launch a read-only subagent (Explore-type). Give it only the source file paths from Phase 1 — pass the paths, not the file contents, and let the subagent read them directly. Do not pass it the existing tests or the Phase 3 inventory.
Instruct it to:

- Read each source file in full
- Walk every public method or function and enumerate what should be tested:
  - The happy path (expected return value, side effects)
  - Each distinct failure path (exception, error return, None, etc.)
  - Edge cases and boundary conditions (empty input, zero, None, concurrent access, etc.)
  - Behaviour that depends on external state (flag enabled/disabled, clock, cache populated vs empty)
- Return the inventory in the same dot-point format as Phase 3 (see `references/inventory-format.md`), grouped by source file (the top-level key is each source file path)

The subagent must not be given any context about the existing tests. Its inventory is derived purely from the source code.

## Phase 4.5: Review both inventories

Present the Phase 3 and Phase 4 inventories together. For each unit, call out:

- Cases in Phase 3 that are **missing** from Phase 4's expected list (tests that cover behaviour the source doesn't appear to have — likely stale or testing the wrong thing)
- Cases in Phase 4 that are **absent** from Phase 3 (coverage gaps worth adding)
- Cases that exist in both (no action needed)

Match cases by **semantic equivalence**, not exact wording. Two bullets describe the same case if they test the same condition and expected outcome, regardless of phrasing. When uncertain whether two cases match, treat them as distinct.

**Stop here.** Ask: "Do these inventories look right? Any cases I've missed or should deprioritise?" Wait for confirmation before continuing.

## Phase 5: Evaluate structural fit

Using the Phase 3 inventory (what is currently tested), check whether each existing test case is in the right place given the current source structure. The goal here is **placement only** — not coverage gaps. Do not flag cases that are missing from the tests; only flag cases that exist in the tests but are in the wrong file or testing at the wrong boundary.

Look for:

- Units that have been split (e.g. a class broken into multiple classes or modules) but tests still treat them as one — the mock boundaries may now be wrong
- Units that were merged but tests duplicate setup across them
- Tests mocking internal collaborators that are now implementation details, rather than the true external boundary

The Phase 4 inventory (expected cases from source) is context for understanding boundaries — not a gap list. Do not flag missing coverage here.

<!-- The photographs skip lines 66–74 here, beginning with "For example, given this source layout:". The example's introductory layout is not recoverable verbatim; its visible evaluation is preserved below. -->

The structural fit evaluation would look like:

**`test_order_processor.py`**
- ✅ `OrderProcessor.submit` — correctly placed
- ✅ `OrderProcessor.cancel` — correctly placed
- ⚠️ `OrderProcessor.charge_payment_gateway` — **misplaced**. `payment_gateway.py` now exists as a standalone module, so `PaymentGateway` is no longer an internal implementation detail of `OrderProcessor` — it's a separate unit with its own boundary. These tests should move to `test_payment_gateway.py`. In `test_order_processor.py`, `PaymentGateway` should be mocked, and `OrderProcessor.submit` tests should assert it is called correctly, not test charge behaviour directly.
- ❌ `test_payment_gateway.py` — **missing entirely**. `payment_gateway.py` has no test file.

Call out each misplaced test explicitly before writing any tests. Do not call out missing coverage — that is handled in Phase 7.

**Stop here.** Ask: "Do these structural findings look right? Any misplacements I've missed or any you want to ignore?" Wait for confirmation before continuing.

## Phase 6: Evaluate semantic fit

Go through each existing test case one by one and assess whether its **implementation** is scoped correctly for where it sits. A test can be in the right file but still reach through the wrong boundary — mocking too deep, not mocking at all, or asserting on internals that should be opaque.

For each test, check:

- **Mock boundaries:** does the test mock at the true external boundary of the unit under test? A test for `OrderProcessor.submit` should mock `PaymentGateway`, not the HTTP client inside `PaymentGateway`
- **Assertion scope:** does the test assert on the unit's observable output or side effects, rather than internal state or the behaviour of a dependency?
- **Setup leakage:** does the test arrange state that belongs to a collaborator rather than the unit itself?

Flag each case with ✅ (correctly scoped) or ⚠️ (boundary violation — describe what is wrong and what the correct mock/assertion target should be). For example:

**`test_order_processor.py`**
- ✅ `test_submit_returns_order_id_on_success` — mocks `PaymentGateway`, asserts return value
- ⚠️ `test_submit_charges_card` — **reaches through boundary**. This test configures the HTTP client inside `PaymentGateway` directly instead of mocking `PaymentGateway.charge`. The test is asserting on `PaymentGateway`'s internal transport, which is not `OrderProcessor`'s concern. Mock `PaymentGateway.charge` instead.
- ✅ `test_cancel_raises_when_already_fulfilled` — no external dependencies involved, asserts on raised exception

Evaluate every existing test in the file, including any identified as misplaced in Phase 5. Misplaced tests still need a boundary assessment — this directly informs how they should be rewritten in their correct location.

**Stop here.** Ask: "Do these boundary findings look right? Anything you'd like to override or adjust before I write the tests?" Wait for confirmation before continuing.

## Phase 7: Write the test plan

Produce a complete, self-contained test plan and write it to `.test-plan.md` in the current working directory. This file will be used to execute the full test restructure — existing files will be deleted and new files written from scratch, so the plan must contain everything needed without reference to the old tests.

The plan is not a diff. It describes the complete intended state after the operation.

Structure the plan as follows:

### Restructure summary

Open with a clear statement of the file-level changes:

- **Delete:** list every existing test file that will be removed
- **Create:** list every new test file that will be created

For example:

```
Delete:
  tests/test_order_processor.py   # contains misplaced PaymentGateway tests; split below

Create:
  tests/test_order_processor.py   # OrderProcessor unit tests only
  tests/test_payment_gateway.py   # new — PaymentGateway extracted in recent refactor
```

A file may appear in both lists (deleted and recreated with different content). A file may appear only in Delete (if its tests move elsewhere entirely). A file may appear only in Create (if it is brand new).

### Full test scenario summary

A single dot-point inventory across all files being created. **Format:** See `references/inventory-format.md`. Group by new test file (the top-level key is each new test file path). This gives a complete at-a-glance view of everything that will be tested after the restructure.

### Per-file sections

For each file in the Create list, include:

#### `tests/test_order_processor.py`

One-line description of what this file tests.

**Shared fixtures and helpers**

List any helpers or fixtures the tests in this file will share — factories, mock constructors, shared constants.
Describe purpose and signature. No code yet, just intent.

**Test cases**

For each case, the full detail:

- **Test name:** exact function name (e.g. `test_submit_returns_order_id_on_success`)
- **Unit under test:** the class/function being exercised
- **Scenario:** one sentence describing the condition
- **Arrange:** what state or mocks need to be set up
- **Act:** the call being made
- **Assert:** what the test checks

---

Repeat the per-file section for every file in the Create list.

---

Once the plan is written, tell the user its path and ask: "Here is the complete test plan. Review `.test-plan.md` and let me know if you want any changes before I proceed." Wait for explicit approval before continuing.

## Phase 8: Write the tests

1. Ensure the current state is recoverable before proceeding — the next step is destructive. Ask the user to confirm they have a backup or the changes are otherwise reversible (e.g. committed to version control) before continuing.

2. Delete every file listed under **Delete** in the plan. Do this before launching the subagent — it guarantees the subagent can read the codebase freely without risk of seeing the old test implementations.

3. Launch a subagent. Give it:
   - The full content of `.test-plan.md`
   - The source file paths
   - The test runner command
   - Instruction to read any other files it needs for codebase conventions (the old test files are already gone)

   Instruct it to:
   - Create every file listed under **Create**, written from scratch following the plan
   - Run the tests and fix every failure before continuing — do not proceed with a red suite
   - Return a coverage table in the following format:

     | Scenario (from plan) | New test name | Status | Notes |
     |---|---|---|---|
     | returns order ID on success | `test_submit_returns_order_id` | ✓ | |
     | raises error when fields missing | `test_submit_raises_on_missing_fields` | ✓ renamed | clearer name |
     | bypasses validation when flag disabled | — | ⚠ removed | behaviour no longer in source |
     | — | `test_submit_handles_concurrent_access` | ✓ new | gap from Phase 4 |

     Status codes: **✓ present** (same or renamed) · **⚠ removed** intentionally absent, reason required · **✗ missing** unaccounted for, must be flagged

4. Once the subagent reports a green suite and the coverage table, review the diff for cosmetic noise before presenting results. Run `git diff` and revert any changes that are purely cosmetic and do not affect test logic — common examples:
   - Variable renames that carry no semantic meaning (e.g. `mock_result` → `result_obj`)
   - Expressions split across extra lines when a single line is clearer
   - Blank lines added to or removed from existing tests that were not otherwise changed

   Run the suite again after reverting to confirm it is still green.

5. Pass the final `git diff` to a fresh context-free subagent (no prior session context) and ask it to review for bugs, correctness issues, and test quality problems. Address any real findings. Ignore findings that are matters of style preference or that duplicate decisions already made in earlier phases.

6. Present the coverage table and blind review outcome to the user and ask for permission to delete `.test-plan.md`.
