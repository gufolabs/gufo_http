#!/bin/sh
# ------------------------------------------------------------------------
# Build version which collects PGO data
# ------------------------------------------------------------------------
# Copyright (C) 2022-24, Gufo Labs
# ------------------------------------------------------------------------

PGO_DATA_DIR=$1
if [ "$PGO_DATA_DIR" = "" ]; then
    echo "PGO data dir must be set"
    exit 1
fi

# Collect PGO
echo "Building profiling version"
RUSTFLAGS="-Cprofile-generate=$PGO_DATA_DIR" python3 -m pip install --editable .
echo "Collecting PGO data"
PYTHONPATH=src/:$PYTHONPATH python3 ./tools/build/pgo-runner.py
echo "Merging profdata"
$(./tools/build/get-rustup-bin.sh)/llvm-profdata merge -o $PGO_DATA_DIR/merged.profdata $PGO_DATA_DIR
echo "PGO profile is written into $PGO_DATA_DIR/merged.profdata"
