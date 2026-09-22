#!/usr/bin/env bash
# Fetch the source texts this project verifies against.
#
#   sources/ce/gretil/mbh_NN_u.htm  BORI Critical Edition, GRETIL electronic text
#                                   (not committed: "(C) BORI 1999, for reference
#                                   purposes only"; re-fetched by this script)
#   sources/ganguli/mahaNN.txt      K. M. Ganguli translation, 1883-1896
#                                   (public domain; committed to the repo)
#
# Usage: tools/fetch_sources.sh [--force]
# Safe to run repeatedly: it does nothing when the files are present and match
# the checksums recorded in sources/*.sha256.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CE_DIR="$ROOT/sources/ce/gretil"
GANGULI_DIR="$ROOT/sources/ganguli"

GRETIL_REPO="https://github.com/INDOLOGY/gretil-mirror"
GRETIL_COMMIT="0baf718d8e450821eb0403c03aacc9a4a82316d7"
GRETIL_PATH="gretil.sub.uni-goettingen.de/gretil/1_sanskr/2_epic/mbh"

GANGULI_REPO="https://github.com/aasi-archive/mbh"
GANGULI_COMMIT="3b6591bd1d6e3b10998eb2f7e859e5edb75445d9"

FORCE=0
[[ "${1:-}" == "--force" ]] && FORCE=1

verify() { # verify <dir> <checksum-file>
  (cd "$1" && sha256sum --quiet -c "$2" >/dev/null 2>&1)
}

# Shallow, blob-filtered, sparse clone of one directory at a pinned commit.
# Falls back to the default branch if the pinned commit cannot be fetched.
sparse_fetch() { # sparse_fetch <repo> <commit> <path> <dest>
  local repo="$1" commit="$2" path="$3" dest="$4"
  rm -rf "$dest"
  git init -q "$dest"
  git -C "$dest" remote add origin "$repo"
  git -C "$dest" config core.sparseCheckout true
  echo "$path/" > "$dest/.git/info/sparse-checkout"
  if ! GIT_LFS_SKIP_SMUDGE=1 git -C "$dest" fetch -q --depth 1 --filter=blob:none origin "$commit" 2>/dev/null; then
    echo "  pinned commit unavailable; fetching default branch" >&2
    GIT_LFS_SKIP_SMUDGE=1 git -C "$dest" fetch -q --depth 1 --filter=blob:none origin HEAD
  fi
  GIT_LFS_SKIP_SMUDGE=1 git -C "$dest" checkout -q FETCH_HEAD
}

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# --- Critical Edition (GRETIL) ---------------------------------------------
mkdir -p "$CE_DIR"
if [[ $FORCE -eq 0 ]] && verify "$CE_DIR" "$ROOT/sources/ce.sha256"; then
  echo "CE text present and verified."
else
  echo "Fetching Critical Edition text from $GRETIL_REPO ..."
  sparse_fetch "$GRETIL_REPO" "$GRETIL_COMMIT" "$GRETIL_PATH" "$TMP/gretil"
  cp "$TMP/gretil/$GRETIL_PATH"/mbh_[0-9][0-9]_u.htm "$CE_DIR/"
  if verify "$CE_DIR" "$ROOT/sources/ce.sha256"; then
    echo "CE text fetched and verified."
  else
    echo "WARNING: CE checksums differ from sources/ce.sha256 (upstream changed?)." >&2
    echo "         Review the difference before relying on new text." >&2
  fi
fi

# --- Ganguli translation ------------------------------------------------------
mkdir -p "$GANGULI_DIR"
if [[ $FORCE -eq 0 ]] && verify "$GANGULI_DIR" "$ROOT/sources/ganguli.sha256"; then
  echo "Ganguli text present and verified."
else
  echo "Fetching Ganguli translation from $GANGULI_REPO ..."
  sparse_fetch "$GANGULI_REPO" "$GANGULI_COMMIT" "txt" "$TMP/ganguli"
  cp "$TMP/ganguli/txt"/maha[0-9][0-9].txt "$GANGULI_DIR/"
  verify "$GANGULI_DIR" "$ROOT/sources/ganguli.sha256" \
    && echo "Ganguli text fetched and verified." \
    || echo "WARNING: Ganguli checksums differ from sources/ganguli.sha256." >&2
fi

# --- Parsed cache used by tools/mbh.py -----------------------------------------
python3 "$ROOT/tools/mbh.py" build-cache
