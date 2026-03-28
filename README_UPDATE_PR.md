# Update PR #19 Body Script

This directory contains a script to update PR #19's body to include the required metadata for the Phase Validation workflow.

## Problem

PR #19 fails the Phase Validation workflow because its body is missing:
1. A Phase reference (e.g., "Phase: 1.0" or "Closes #123")
2. A "Verification:" section with commands

> Note: All PRs in this repository must include both a Phase/Closes reference and a non-empty
> `Verification:` block to satisfy the validation workflow.

## Solution

The `update_pr_19_body.py` script uses the GitHub API to update PR #19's body with the required metadata.

## Usage

### Prerequisites

- Python 3.x
- `requests` library (`pip install requests`)
- GitHub Personal Access Token with `repo` scope

### Steps

1. **Install required dependencies:**
   ```bash
   pip install requests
   ```

2. **Set your GitHub token:**
   ```bash
   export GITHUB_TOKEN="your_github_token_here"
   ```

3. **Run the script:**
   ```bash
   python3 update_pr_19_body.py
   ```

4. **Verify the update:**
   - Visit https://github.com/neuron7x/Hippocampal-CA1-LAM/pull/19
   - Check that the PR body now includes:
     - "Phase: 1.0" at the beginning
     - "Verification:" section with commands
   - The Phase Validation workflow should now pass

## What the Script Does

The script updates PR #19's body to include:

1. **Phase Reference:** "Phase: 1.0" at the beginning
2. **Verification Section:** Contains the commands that were run:
   - `PYTHONPATH=. pytest -q tests/test_core_contracts.py tests/test_config.py`
   - Reviewed docs/mode_a_audit.md for completeness
   - Verified removal of egg-info artifacts
3. **Original Content:** All original PR content is preserved

## Alternative: Manual Update

If you prefer to update the PR body manually:

1. Go to https://github.com/neuron7x/Hippocampal-CA1-LAM/pull/19
2. Click the "..." menu next to the PR description
3. Click "Edit"
4. Add "Phase: 1.0" at the very beginning
5. Add the following before the "Example harness invocation:" section:

```
Verification:
- PYTHONPATH=. pytest -q tests/test_core_contracts.py tests/test_config.py
- Reviewed docs/mode_a_audit.md for completeness
- Verified removal of egg-info artifacts
```

6. Click "Update comment"

## Validation

After updating, the Phase Validation workflow checks:
- ✓ PR body contains a phase reference (regex: `Phase:[[:space:]]*[0-9]{1,2}\.[0-9]{1,2}` or `Closes #[0-9]+`)
- ✓ PR body contains "Verification:" section (case-insensitive)
- ✓ Verification section has at least one non-empty line

## Troubleshooting

### "GITHUB_TOKEN environment variable not set"
Make sure you've set the environment variable:
```bash
export GITHUB_TOKEN="your_token"
```

### "401 Unauthorized"  
Your token may not have the correct permissions. Ensure it has the `repo` scope.

### "404 Not Found"
The PR number, owner, or repo name may be incorrect. Verify in the script.
