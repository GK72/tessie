#!/usr/bin/env bash
set -euo pipefail

COLOR_DEF='\033[0m'
COLOR_PURPLE='\033[1;35m'

function log() {
    >&2 echo -e "${COLOR_PURPLE}${1}${COLOR_DEF}"
}

function activate-venv() {
    if [[ -e ~/.venv/def ]]; then
        source ~/.venv/def/bin/activate
    fi
}

function run-checkers() {
    log "Running MyPy..."
    mypy "${PROJECT_DIR}/tessie"

    log "Running PyLint..."
    pylint "${PROJECT_DIR}/tessie"
}

PROJECT_DIR=$(git -C "${0%/*}" rev-parse --show-toplevel)
activate-venv

set +e
run-checkers
set -e
