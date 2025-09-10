---
hide:
    - navigation
---
# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

To see unreleased changes, please see the [CHANGELOG on the main branch guide](https://github.com/gufolabs/gufo_http/blob/main/CHANGELOG.md).

## 0.6.0

### Added

* `gufo-http` command-line tool.

## 0.5.1

### Security

* Install security updates during devcontainer build.
* Use python:3.13-slim-trixie as base for devcontainer.

### Infrastructure

* Remove `[bench]` dependencies from pyproject.toml

## 0.5.0 - 2025-09-07

### Added

* Python 3.14 support.

### Infrastructure

* Move dependencies to pyproject.toml
* Rust 1.89.0
* PyO3 0.26
* tokio 1.47.1
* reqwest 1.12.23
* devcontainer: Replace `rls` with `rust-analyzer`.

## 0.4.0 - 2025-03-17

### Added

* Python 3.13 support.
* Linux ARM64 binary wheels.
* MUSL AMD64 and ARM64 wheels.

### Removed

* Python 3.8 support.

### Infrastructure
* Rust 1.85.0.
* Rust edition 2024.
* PyO3 0.24.
* Move from `black` to `ruff format`.

## 0.3.1 - 2024-06-03

### Added

* `ZSTD` compression support.

### Fixed

* Include rust files into sdist.

## 0.3.0 - 2024-03-24

### Added

* `RequestMethod` enum.
* Proxy support.

### Fixed

* Raise `TimeoutError` on request timeout, instead of `RequestError`.
* Exception names shown without _Py_ prefix.

### Changed

* `HttpClient.request` accepts `RequestMethod`.
* `HttpClient` accepts optional `proxy` argument.
* `ConnectError` replaced with Python's builtin `ConnectionError`.
* Use Rust 1.77.0.
* Use `reqwest` 0.12.

## 0.2.0 - 2024-03-14

### Added

* `HttpClient.request()` function for both sync and async clients.
* HTTPS benchmarks.
* Httpd: `mode` configuration parameter.
* Httpd: HTTPS mode.

### Changed

* `SyncRequest` and `AsyncRequest` are merged into unified `Request` class.
* `Request.read()` meethod is replaced with `Request.content` property.

## 0.1.2 - 2024-03-09

### Added

* Benchmark results and charts.
* Enable profile-guided optimization (PGO) during packaging stage.

## 0.1.1 - 2024-03-05

### Added

* Benchmarks
  
### Changed

* Improved synchronous client's concurrency.

## 0.1.0 - 2024-03-04

### Added

* Initial implementation

