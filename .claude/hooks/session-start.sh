#!/bin/bash
# SessionStart hook (Claude Code on the web): fetch and checksum-verify the
# source texts (the BORI Critical Edition text is git-ignored and must be
# re-downloaded in each fresh container), build the parsed caches, and
# regenerate the project index. Idempotent: a no-op fetch when files exist.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
tools/fetch_sources.sh
python3 tools/build_index.py
