FROM python:3.13-slim-bullseye AS dev
COPY . /workspaces/gufo_http
WORKDIR /workspaces/gufo_http
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
    && pip install -e .[build,docs,ipython,lint,test,bench]
