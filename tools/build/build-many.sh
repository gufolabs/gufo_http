#!/bin/sh
# ------------------------------------------------------------------------
# Build wheel in the manylinux
# Usage:
# ./tools/build/build-many 3.9 3.10 3.11 3.11 3.12 3.13 3.14
# expects RUST_VERSION and RUST_ARCH
# ------------------------------------------------------------------------
# Copyright (C) 2022-25, Gufo Labs
# ------------------------------------------------------------------------

# set -x
set -e

empty_dir() {
    local path="$1"
    if [ -d "${path}" ]; then
        echo "Clearing ${path}..."
        rm -rf "${path}"/*
    else
        echo "Creating ${path}..."
        mkdir -p "${path}"
    fi
}

ensure_dir() {
    local path="$1"
    if [ ! -x "${path}" ]; then
        echo "Creating ${path}..."
        mkdir -p "${path}"
    fi
}

line() {
    echo "# ------------------------------------------------------------------------"
}

header() {
    line
    echo "# $1"
    line
}

section() {
    echo "#"
    echo "# $1"
    echo "#"
}

checkpoint() {
    # Store the current time in seconds
    CHECKPOINT_TIME=$(date +%s)
}

elapsed() {
    local now=$(date +%s)
    local diff=$((now - CHECKPOINT_TIME))
    echo "** Elapsed time: $diff seconds"
}

# Detect environment
OSNAME=$(uname -s)
if [ "$OSNAME" == "Linux" ]; then
    SUPPORTS_PGO=true
else
    SUPPORTS_PGO=false
fi
# Save base path
BASE_PATH=$PATH
# Rust settings
export RUSTUP_HOME=${RUSTUP_HOME:-/usr/local/rustup}
export CARGO_HOME=${CARGO_HOME:-/usr/local/cargo}
PATH=$CARGO_HOME/bin:$BASE_PATH

# Paths
BUILD="build"
DIST="dist"
TMP_WHEELHOUSE="/tmp/wheelhouse"
WHEELHOUSE="wheelhouse"
TARGET="target"

if [ $(id -u) -eq 0 ]; then
    SUDO=""
else
    SUDO="sudo"
fi

header "Installing rust"
checkpoint
empty_dir "${TARGET}"
./tools/build/setup-rust.sh
rustup component add llvm-tools-preview
elapsed

header "Installing nginx"
checkpoint
./tools/build/setup-nginx.sh
elapsed

while [ $# -gt 0 ]
do
    header "Building for Python $1"
    # Convert version to ABI
    case "$1" in
        3.9) ABI=cp39-cp39 ;;
        3.10) ABI=cp310-cp310 ;;
        3.11) ABI=cp311-cp311 ;;
        3.12) ABI=cp312-cp312 ;;
        3.13) ABI=cp313-cp313 ;;
        3.14) ABI=cp314-cp314 ;;
        *)
            echo "Unknown Python version $1"
            exit 2
            ;;
    esac
    # Set up paths
    if [ $OSNAME == "Darwin" ]; then
        # MacOS
        PV=$(ls $RUNNER_TOOL_CACHE/Python | grep "^$1" | sort -V | tail -n1)
        PATH=$CARGO_HOME/bin:$RUNNER_TOOL_CACHE/Python/$PV/arm64/bin:$BASE_PATH
        export PYO3_PYTHON=$RUNNER_TOOL_CACHE/Python/$PV/arm64/bin/python3
        pip install build
    else
        # Linux
        PATH=$CARGO_HOME/bin:/opt/python/$ABI/bin:$BASE_PATH
        export PYO3_PYTHON=/opt/python/$ABI/bin/python3
    fi
    # Check python version is supported in file system
    if [ ! -f $PYO3_PYTHON ]; then
        echo "Python version $1 is not supported"
        exit 2
    fi
    # Check python
    PY_VER=$(python3 --version)
    echo "Python version: $PY_VER"
    section "Upgrade pip..."
    checkpoint
    pip install --upgrade pip
    elapsed
    section "Setup build dependencies..."
    checkpoint
    pip install e .[build,test,test-extra]
    elapsed
    if [ "$SUPPORTS_PGO" = true ]; then
        section "Collecting PGO..."
        checkpoint
        PGO_DATA_DIR=`mktemp -d`
        ./tools/build/build-pgo.sh $PGO_DATA_DIR
        elapsed
    fi
    section "Building wheel..."
    checkpoint
    empty_dir "${DIST}"
    empty_dir "${BUILD}"
    python3 -m build --wheel
    elapsed
    if [ "$SUPPORTS_PGO" = true ]; then
        section "Clearing PGO..."
        rm -rf $PGO_DATA_DIR
    fi
    section "Auditing wheel..."
    checkpoint
    empty_dir "${TMP_WHEELHOUSE}"
    auditwheel repair --wheel-dir="${TMP_WHEELHOUSE}" "${DIST}"/*.whl
    elapsed
    section "Installing wheel..."
    checkpoint
    pip install "${TMP_WHEELHOUSE}"/*.whl
    elapsed
    section "Testing..."
    checkpoint
    pytest tests/
    elapsed
    section "Saving..."
    ensure_dir "${WHEELHOUSE}"
    cp "${TMP_WHEELHOUSE}"/*.whl "${WHEELHOUSE}"/
    empty_dir "${DIST}"
    empty_dir "${TMP_WHEELHOUSE}"
    echo "... done"
    shift
done

echo "##"
echo "## Done"
echo "##"
ls -lh wheelhouse/
