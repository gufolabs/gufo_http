FROM python:3.13-slim-trixie AS dev
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
    && apt-get -y dist-upgrade \
    && apt-get -y autoremove\
    && apt-get install -y --no-install-recommends\
    git\
    ca-certificates\
    gcc\
    libc6-dev\
    curl\
    && ./tools/build/setup-nginx.sh \
    && ./tools/build/setup-rust.sh \
    && rustup component add\
    rust-analysis\
    rust-src\
    rust-analyzer\
    clippy\
    rustfmt\
    llvm-tools-preview \
    && pip install --upgrade pip\
    && pip install --upgrade build\
    && pip install -e .[build,docs,ipython,lint,test,test-extra]
