FROM python:3.12-slim-bullseye AS dev
COPY .requirements tools/build/setup-rust.sh tools/build/setup-nginx.sh /tmp
ENV \
    PATH=/usr/local/cargo/bin:$PATH\
    RUSTUP_HOME=/usr/local/rustup\
    CARGO_HOME=/usr/local/cargo
RUN \
    set -x \
    && apt-get clean \
    && apt-get update \
    && apt-get install -y --no-install-recommends\
    git\
    ca-certificates\
    gcc\
    libc6-dev\
    curl\
    && /tmp/setup-nginx.sh \
    && /tmp/setup-rust.sh \
    && rustup component add\
    rust-analysis\
    rust-src\
    rls\
    clippy\
    rustfmt\
    llvm-tools-preview \
    && pip install --upgrade pip\
    && pip install --upgrade build\
    && pip install\
    -r /tmp/build.txt\
    -r /tmp/docs.txt\
    -r /tmp/ipython.txt\
    -r /tmp/lint.txt\
    -r /tmp/test.txt\
    -r /tmp/bench.txt