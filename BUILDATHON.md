# Handoff Copilot

## One-sentence summary
Turns an Entire Checkpoint's claimed intent and actual changes into a Markdown handoff brief that never presents incomplete context as complete.

## Problem, intended user and why it matters
Developers picking up an AI agent's work can't easily tell if the code matches the agent's claimed intent. Checkpoints carry that answer, but nothing surfaces it safely.

## Selected Entire track and why Entire is essential
Track 1. Git shows what changed; Entire Checkpoints carry why, what's unresolved, and what was assumed — that's the direct input to this tool.

## Architecture and main workflow
Single Python function `generate_handoff_brief()` in `handoff_copilot.py`. Reads a Checkpoint (dict or JSON string), maps fields via `SECTION_FIELDS` aliases, renders 5 Markdown sections (Intent, Done, Unfinished, Risks, Verification Checklist).

## Entire Graph findings and verification

Ran `entire graph search --repo . --query "handoff brief generator"`. The result identified `generate_handoff_brief` in `handoff_copilot.py` and its only in-repository direct consumer in `test_handoff_copilot.py`; no production callers were found.

Limitation: this is repository-scoped evidence. External scripts or users parsing the Markdown output may still depend on its previous format, so that remains an open compatibility risk.

## Noon Curveball: what changed and how we adapted
Assumption invalidated: the brief generator assumed all Checkpoint fields were always present. Added: detection of `None`, blank strings, or `[REDACTED]` values, per-section `REQUIRED_FIELD_GROUPS`, an `— Incomplete —` heading suffix, and a top-level `Context: COMPLETE`/`PARTIAL` marker. Test added: `test_marks_redacted_reasoning_as_incomplete`.

## Checkpoint links and what each checkpoint proves
[paste your checkpoint links/IDs from `entire status` here]

## Setup, run and test instructions

From `C:\Users\user\t1`:

```powershell
python -m unittest -v
```

The module has no dependencies beyond Python's standard library.

## Known limitations and next steps
- Test coverage: 2 tests confirmed passing (happy path, redaction case). A guard for malformed/non-object input was attempted but not successfully landed due to local file-editing issues during the build session; not included in this submission.
- No CLI wrapper or file I/O layer yet — the function is called directly in Python/tests.
- Graph search was run and verified against source, but not as a full `entire graph impact` analysis before editing.
- Next step: add a CLI entry point and complete the malformed-input validation for production use.