# Roadmap Issue 04: CI guardrails for benchmark integrity

## Problem

Current validation is a good baseline, but additional safeguards can prevent accidental benchmark regressions and docs drift.

## Proposal

- Add JSON schema or structural check for benchmark output files
- Add README link checker in CI
- Add lightweight consistency check between README snapshot and JSON values
- Add release checklist automation script

## Expected Impact

- Fewer broken links and stale benchmark summaries
- Higher trust in published benchmark outputs
- Faster, safer release process

## Acceptance Criteria

- CI fails on invalid benchmark JSON shape
- CI detects broken markdown links in README files
- release checklist can be run in one command

## Labels

enhancement, ci, reliability
