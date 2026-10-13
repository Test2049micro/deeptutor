#!/bin/bash
set -euo pipefail
APP_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LAUNCHER="$APP_DIR/packaging/launcher"
if [ ! -x "$LAUNCHER" ]; then
  chmod +x "$LAUNCHER"
fi
open "$LAUNCHER"
