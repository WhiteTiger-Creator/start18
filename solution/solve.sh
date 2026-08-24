#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export GOCACHE=/tmp/gocache GO111MODULE=off GOPATH=/tmp/gopath

# --- Step 1: rebuild the authoritative gauge series (#BAS-8170) -------------
# The telemetry migration left /app/data/gauge_readings.json holding a truncated
# prefix. Replay the telemetry journal onto the pre-migration snapshot, bring
# every reading onto the basin datum, and write the result back to that path.

go run "${SCRIPT_DIR}/recover_gauges.go"

# --- Step 2: restore the scheduler and produce the release artifacts --------

cp "${SCRIPT_DIR}/schedule_releases_fixed.go" /app/workflow/schedule_releases.go
go run /app/workflow/schedule_releases.go --output-dir /app/output
