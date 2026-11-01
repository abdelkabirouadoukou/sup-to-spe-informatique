#!/usr/bin/env bash
# Construit dist/quiz_revision (macOS / Linux) avec quiz/questions embarqué.
# Usage : bash scripts/build_exe.sh
#         PYTHON=.venv/bin/python bash scripts/build_exe.sh
set -euo pipefail

cd "$(dirname "$0")/.."
PYTHON="${PYTHON:-python3}"

# Séparateur de --add-data : ':' sur macOS/Linux (';' sur Windows).
"$PYTHON" -m PyInstaller \
  --noconfirm --clean --onefile \
  --name quiz_revision \
  --add-data "quiz/questions:questions" \
  quiz/quiz_app.py

echo "Build OK : dist/quiz_revision"
