#!/usr/bin/env bash
# Build the Jekyll site offline and turn it into an Artifact preview.
# usage: preview.sh <github-site dir> <work dir>
# Produces <work>/_site (plain build), <work>/preview (Artifact copy) and <work>/preview_files.json.
set -euo pipefail
SITE=$(cd "$1" && pwd); WORK=$(mkdir -p "$2" && cd "$2" && pwd)
TOOLS=$(cd "$(dirname "$0")" && pwd)
VENDOR="$WORK/vendor"; mkdir -p "$VENDOR"
[ -d "$VENDOR/liquid" ]     || git clone -q --depth 1 --branch v4.0.4 https://github.com/Shopify/liquid.git "$VENDOR/liquid"
[ -d "$VENDOR/kramdown" ]   || git clone -q --depth 1 https://github.com/gettalong/kramdown.git "$VENDOR/kramdown"
[ -d "$VENDOR/parser-gfm" ] || git clone -q --depth 1 https://github.com/kramdown/parser-gfm.git "$VENDOR/parser-gfm"
LC_ALL=C.UTF-8 ruby -E UTF-8:UTF-8 -I "$VENDOR/liquid/lib" -I "$VENDOR/kramdown/lib" -I "$VENDOR/parser-gfm/lib" \
  "$TOOLS/minijekyll.rb" "$SITE" "$WORK/_site"
python3 "$TOOLS/build_preview.py" "$WORK/_site" "$WORK/preview" "$WORK/preview_files.json"
