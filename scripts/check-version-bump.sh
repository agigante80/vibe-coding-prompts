#!/usr/bin/env bash
# Fail if any prompt file changed relative to the base ref without a version bump.
#
# Usage: scripts/check-version-bump.sh <base-ref>
# Typically called from CI with the pull request base SHA.
#
# Rules:
# - Modified prompts (M) and renamed-with-edits prompts (R<n>) need a bump.
# - Newly added prompts (A) are exempt; front matter validity is enforced
#   separately by update_prompt_index.py --check.
# - A pure rename passes: its per-file diff carries the version line along.
set -euo pipefail

BASE="${1:?usage: check-version-bump.sh <base-ref>}"
FAILED=0

while IFS=$'\t' read -r status old new; do
  case "$status" in
    M)  file="$old" ;;
    R*) file="$new" ;;
    *)  continue ;;
  esac
  case "$file" in
    prompts/*.md) ;;
    *) continue ;;
  esac
  # Skip files with no content difference (e.g. mode-only changes).
  # Content lines start with + or - but are not the +++/--- file headers.
  if ! git diff --find-renames "$BASE"...HEAD -- "$file" \
      | grep -E '^[+-]' | grep -vE '^\+\+\+|^---' | grep -q .; then
    continue
  fi
  if git diff --find-renames "$BASE"...HEAD -- "$file" | grep -Eq '^[+-]version:'; then
    echo "ok: $file (version bumped)"
  else
    echo "FAIL: $file changed without a version bump in its front matter" >&2
    FAILED=1
  fi
done < <(git diff --name-status --find-renames "$BASE"...HEAD)

if [ "$FAILED" -ne 0 ]; then
  echo >&2
  echo "Bump the 'version:' field (and 'updated:') in each failing prompt." >&2
  echo "Rules: docs/prompt-creation-guide.md, section 'Front Matter, Versioning and the README Index'." >&2
  exit 1
fi
echo "version bump check: OK"
