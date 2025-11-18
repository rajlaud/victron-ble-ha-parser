# Release Process

This document describes how to release a new version of `victron-ble-ha-parser` to PyPI.

## Prerequisites

The project uses GitHub Actions for automated PyPI deployment to ensure compliance with Home Assistant's [dependency transparency requirements](https://developers.home-assistant.io/docs/core/integration-quality-scale/rules/dependency-transparency/).

### Setup PyPI Publishing (One-time)

1. Create a PyPI account at https://pypi.org if you don't have one
2. Enable 2FA on your PyPI account (required)
3. Configure Trusted Publisher in PyPI:
   - Go to https://pypi.org/manage/account/publishing/
   - Add a new pending publisher with:
     - PyPI Project Name: `victron-ble-ha-parser`
     - Owner: `rajlaud`
     - Repository name: `victron-ble-ha-parser`
     - Workflow name: `publish.yml`
     - Environment name: `pypi`

4. Create a GitHub environment named `pypi`:
   - Go to repository Settings → Environments → New environment
   - Name it `pypi`
   - Add protection rules if desired (e.g., require approval)

## Release Steps

### 1. Update Version

Update the version number in `pyproject.toml`:

```toml
[project]
version = "X.Y.Z"
```

### 2. Update Changelog

Document changes in the commit messages or update README.md if applicable.

### 3. Commit Changes

```bash
git add pyproject.toml
git commit -m "Bump version to X.Y.Z"
git push origin main
```

### 4. Create and Push a Git Tag

```bash
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin vX.Y.Z
```

The tag **must** follow the pattern `vX.Y.Z` (e.g., `v0.4.9`, `v1.0.0`) to trigger the publish workflow.

### 5. Monitor the Release

1. Go to the [Actions tab](https://github.com/rajlaud/victron-ble-ha-parser/actions)
2. Watch the "Publish to PyPI" workflow
3. Verify the package appears on PyPI: https://pypi.org/project/victron-ble-ha-parser/

## Compliance with Home Assistant Requirements

This release process ensures compliance with Home Assistant's dependency transparency requirements:

- ✅ **OSI-approved license**: Apache-2.0
- ✅ **Public CI pipeline**: GitHub Actions workflow (`.github/workflows/publish.yml`)
- ✅ **Tagged releases**: Git tags match PyPI versions
- ✅ **Source distribution**: Both `sdist` and `wheel` are published
- ✅ **Issue tracker**: GitHub Issues enabled

## Troubleshooting

### Workflow Fails

If the publish workflow fails:

1. Check the [Actions tab](https://github.com/rajlaud/victron-ble-ha-parser/actions) for error details
2. Common issues:
   - PyPI Trusted Publisher not configured correctly
   - Environment name mismatch (must be `pypi`)
   - Tag format incorrect (must be `vX.Y.Z`)

### Manual Publishing (Not Recommended)

For emergency situations only, you can publish manually:

```bash
python -m pip install --upgrade build twine
python -m build
python -m twine upload dist/*
```

However, this violates Home Assistant's transparency requirements as it's not built in a public CI pipeline.

## Version History

- **0.4.8**: Initial setup with automated PyPI deployment
