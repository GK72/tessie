#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR=$(git -C "${0%/*}" rev-parse --show-toplevel)
TMP_FILE=$(mktemp)

"${PROJECT_DIR}/tessie/tess.py" "${PROJECT_DIR}/test/test_regression.py" > "${TMP_FILE}"
diff --report-identical-files "${PROJECT_DIR}/test/reference.txt" "${TMP_FILE}"

rm "${TMP_FILE}"
