# Deployment Checklist

This checklist helps verify that the PyPI deployment pipeline is properly configured.

## Pre-Deployment Verification

- [x] Project has an OSI-approved license (Apache-2.0)
- [x] `pyproject.toml` includes all required metadata:
  - [x] name, version, description
  - [x] readme reference
  - [x] license (SPDX format)
  - [x] authors
  - [x] project URLs (Homepage, Repository, Issues)
  - [x] classifiers
  - [x] dependencies
- [x] `.github/workflows/publish.yml` exists and is configured
- [x] Workflow triggers on tag push (pattern: `v*.*.*`)
- [x] Workflow uses Trusted Publishing (no API tokens needed)
- [x] Package builds successfully with `python -m build`
- [x] Both sdist (`.tar.gz`) and wheel (`.whl`) are generated
- [x] Code passes linting (flake8, black, mypy)

## PyPI Configuration (One-time Setup)

Follow the instructions in `RELEASING.md` to configure:

1. [ ] PyPI Trusted Publisher configured for this repository
2. [ ] GitHub environment `pypi` created in repository settings
3. [ ] (Optional) Environment protection rules configured

## First Release Test

After merging this PR and configuring PyPI:

1. [ ] Update version in `pyproject.toml` to the next version (e.g., `0.4.9`)
2. [ ] Commit and push to main
3. [ ] Create and push a tag: `git tag v0.4.9 && git push origin v0.4.9`
4. [ ] Verify workflow runs successfully in GitHub Actions
5. [ ] Verify package appears on PyPI: https://pypi.org/project/victron-ble-ha-parser/
6. [ ] Test installation: `pip install victron-ble-ha-parser`

## Home Assistant Compliance

Verify compliance with [Home Assistant dependency transparency requirements](https://developers.home-assistant.io/docs/core/integration-quality-scale/rules/dependency-transparency/):

- [x] **OSI-approved license**: Apache-2.0 ✓
- [x] **Available on PyPI**: Will be available after first release
- [x] **Public CI pipeline**: GitHub Actions workflow is public ✓
- [x] **Tagged releases**: Workflow only triggers on version tags ✓
- [x] **Source distribution**: Both sdist and wheel are built ✓
- [x] **Issue tracker**: GitHub Issues enabled ✓

## Post-Release Verification

After each release:

- [ ] Verify package on PyPI has correct version
- [ ] Verify both sdist and wheel are available on PyPI
- [ ] Verify README renders correctly on PyPI
- [ ] Test installation from PyPI in a clean environment
- [ ] Verify the source code tag matches the PyPI version
