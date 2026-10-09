#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
TARGET="${1:-$DIR/../index.html}"
cp -- "$DIR/index.original.html" "$TARGET"
cmp -- "$DIR/index.original.html" "$TARGET"
echo 'ROLLBACK: original bytes restored; PASS'
