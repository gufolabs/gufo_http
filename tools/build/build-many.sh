#!/bin/sh
# ------------------------------------------------------------------------
# Gufo Labs: Build wheel in the quay.io/pypa/manylinux2014_x86_64:latest
# Usage:
# ./tools/build/build-manylinux 3.8 3.9 3.10 3.11 3.12
# expects RUST_VERSION and RUST_ARCH
# ------------------------------------------------------------------------
# Copyright (C) 2022-24, Gufo Labs
# ------------------------------------------------------------------------

# set -x
set -e

# Save base path
BASE_PATH=$PATH
# Rust settings
export RUSTUP_HOME=${RUSTUP_HOME:-/usr/local/rustup}
export CARGO_HOME=${CARGO_HOME:-/usr/local/cargo}
PATH=$CARGO_HOME/bin:$BASE_PATH

echo "##"
echo "## Installing rust"
echo "##"
./tools/build/setup-rust.sh
rustup component add llvm-tools-preview

echo "##"
echo "## Installing nginx"
echo "##"
./tools/build/setup-nginx.sh

while [ $# -gt 0 ]
do
    echo "##"
    echo "## Building for Python $1"
    echo "##"
    # Convert version to ABI
    case "$1" in
        3.8) ABI=cp38-cp38 ;;
        3.9) ABI=cp39-cp39 ;;
        3.10) ABI=cp310-cp310 ;;
        3.11) ABI=cp311-cp311 ;;
        3.12) ABI=cp312-cp312 ;;
        *)
            echo "Unknown Python version $1"
            exit 2
            ;;
    esac
    # Adjust path
    PATH=$CARGO_HOME/bin:/opt/python/$ABI/bin:$BASE_PATH
    # Check python version is supported in docker image
    export PYO3_PYTHON=/opt/python/$ABI/bin/python3
    if [ ! -f $PYO3_PYTHON ]; then
        echo "Python version $1 is not supported by image"
        exit 2
    fi
    # Check python
    PY_VER=$(python3 --version)
    echo "Python version: $PY_VER"
    echo "Upgrade pip"
    pip install --upgrade pip
    echo "Setup build dependencies"
    pip install -r ./.requirements/build.txt -r ./.requirements/test.txt
    # Collect PGO
    echo "Building profiling version"
    PGO_DATA_DIR="/tmp/pgo-data/$ABI"
    RUSTFLAGS="-Cprofile-generate=$PGO_DATA_DIR" python3 -m pip install --editable .
    echo "Collecting PGO data"
    OLD_PYTHONPATH=$PYTHONPATH
    PYTHONPATH=src/:$PYTHONPATH
    python3 ./tools/build/collect-pgo.py
    PYTHONPATH=$OLD_PYTHONPATH
    $(./tools/build/get-rustup-bin.sh)/llvm-profdata merge -o $PGO_DATA_DIR/merged.profdata $PGO_DATA_DIR
    # Build wheel
    echo "Building wheel"
    RUSTFLAGS="-Cprofile-use=$PGO_DATA_DIR/merged.profdata" python3 -m build --wheel
    # Clean PGO
    rm -rf $PGO_DATA_DIR
    #
    echo "Auditing wheel"
    auditwheel repair dist/*-$ABI-*.whl
    echo "Installing wheel"
    pip install wheelhouse/*-$ABI-*.whl
    echo "Testing"
    pytest -vv tests/
    echo "... done"
    shift
done

echo "##"
echo "## Done"
echo "##"
ls -lh wheelhouse/
