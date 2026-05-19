# Roadmap Issue 02: Expand benchmark suite quality and realism

## Problem

Current tests are useful but limited in breadth. More realistic coding tasks can improve confidence in model selection for real projects.

## Proposal

- Add tests for debugging/refactoring with edge cases
- Add one test focused on test-generation quality
- Add one infra-as-code validation-oriented prompt
- Add guidance for deterministic prompt design

## Expected Impact

- Better quality signal across model comparisons
- Reduced risk of overfitting to current prompt set
- Stronger credibility when sharing benchmark outcomes

## Acceptance Criteria

- At least 3 new benchmark tests are added with clear keywords
- benchmark runtime remains acceptable for standard run
- README documents what changed in test coverage

## Labels

enhancement, benchmark, quality
