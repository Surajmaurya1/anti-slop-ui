# Changelog

All notable changes to this repository are documented here.

The skill content itself is preserved as authored. This file records packaging and repository changes, not rewrites of `SKILL.md` or its references.

## [Unreleased]

### Added

- MIT License (`LICENSE`), copyright (c) 2026 Suraj Maurya.

### Changed

- Updated `skills/anti-slop-ui/SKILL.md` frontmatter to `license: MIT`; no skill instructions or other metadata were changed.
- Updated the README License section and removed the previous "no license chosen" statements.
- Regenerated `dist/anti-slop-ui-v1.0.0.zip` so the distribution includes the MIT license and updated skill metadata. The archive extracts to `anti-slop-ui/` containing `SKILL.md`, `LICENSE`, `references/`, and `scripts/`; development tests are not shipped in the ZIP.

## [1.0.0] - 2026-11-25

### Added

- First public packaging of Anti-Slop UI.
- `skills/anti-slop-ui/` as the discoverable skill source:
  - `SKILL.md` (byte-identical to the author's archive)
  - `references/` — accessibility, components, design intake, styles catalog, tokens, workflows
  - `scripts/` — `contrast.py`, `diff_guard.py`
  - `tests/` — contrast and diff-guard test suites, token pairs, and the React/TypeScript sample-app fixture
- `dist/anti-slop-ui-v1.0.0.zip` — installable archive that extracts to a single `anti-slop-ui/` folder.
- Public README with installation, manual ZIP, contribution, and license information.

### Validation

- Local Skills CLI discovery: `npx skills add ./skills/anti-slop-ui --list` → 1 skill found (`anti-slop-ui`).
- Python test suite: 22 of 23 tests pass. See known gaps below.

### Known gaps inherited from the source archive

The source archive (`files.zip`, 16 files) was a flattened export and omitted dotfiles. It did not contain every document that `SKILL.md` references. Nothing was invented to fill these gaps.

- **Missing reference documents** referenced by `SKILL.md`:
  - `references/implementation.md`
  - `references/responsive.md`
  - `references/reference-analysis.md`
  - `references/anti-slop-patterns.md`
  - `references/visual-qa.md`
  - `references/provenance.md`
- **Missing test documentation:** `tests/scenarios.md` (referenced by the skill metadata and test docstring).
- **Missing test fixture:** `tests/fixtures/sample-app/.env.example` (a dotfile dropped by the export). As a result, `test_diff_guard.py::test_dependency_and_env_files` errors; the other 22 tests pass.
- **No license file at the time of release:** resolved in Unreleased by adding the MIT License.

### Notes

- `SKILL.md` still carries the author's own metadata version (`0.2.0`) and pre-release status note. The repository release is `v1.0.0`; the skill text was not modified.
- The original `files.zip` used for this release is kept locally and is not published.
