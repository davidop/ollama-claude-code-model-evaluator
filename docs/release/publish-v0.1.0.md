# Publish v0.1.0 (Step by Step)

This guide is the fastest path to publish the first release with reproducible assets.

## 1) Pre-release validation

Run local checks:

```bash
bash scripts/release-check.sh
```

Expected output ends with:

- Release check passed.

## 2) Commit and tag

```bash
git add README.md README.en.md dashboard.html docs/release docs/assets scripts .github/workflows/validate.yml
git commit -m "Prepare v0.1.0 release assets, dashboard, and CI guardrails"
git tag -a v0.1.0 -m "v0.1.0"
```

## 3) Push branch and tag

```bash
git push origin main
git push origin v0.1.0
```

## 4) Create GitHub release (Web UI)

1. Open Releases in GitHub.
2. Click Draft a new release.
3. Select tag: v0.1.0.
4. Title: v0.1.0.
5. Description: paste content from [docs/release/v0.1.0-release-notes.md](docs/release/v0.1.0-release-notes.md).
6. Upload assets:
   - [results/benchmark-standard.json](results/benchmark-standard.json)
   - [results/benchmark-ctx16384-plus14b.json](results/benchmark-ctx16384-plus14b.json)
   - [dashboard.html](dashboard.html) (optional)
7. Publish release.

## 5) Create GitHub release (CLI alternative)

If GitHub CLI is available and authenticated:

```bash
gh release create v0.1.0 \
  results/benchmark-standard.json \
  results/benchmark-ctx16384-plus14b.json \
  dashboard.html \
  --title "v0.1.0" \
  --notes-file docs/release/v0.1.0-release-notes.md
```

## 6) Open roadmap issues

Create issues by copying content from:

- [docs/release/roadmap-01-english-readme-and-global-distribution.md](docs/release/roadmap-01-english-readme-and-global-distribution.md)
- [docs/release/roadmap-02-benchmark-suite-expansion.md](docs/release/roadmap-02-benchmark-suite-expansion.md)
- [docs/release/roadmap-03-dashboard-and-sharing-assets.md](docs/release/roadmap-03-dashboard-and-sharing-assets.md)
- [docs/release/roadmap-04-ci-and-quality-guardrails.md](docs/release/roadmap-04-ci-and-quality-guardrails.md)

## 7) Launch posts

Use templates from:

- [docs/release/launch-pack.md](docs/release/launch-pack.md)

Suggested order:

1. X
2. Reddit
3. Hacker News

## 8) 7-day follow-up metrics

Track:

- Stars per day
- Repo clones
- Unique visitors
- Top referral source

Keep the best performing post format and iterate next release messaging.
