---
hide:
    - navigation
---
# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

To see unreleased changes, please see the [CHANGELOG on the main branch guide](https://github.com/gufolabs/gufo_http/blob/main/CHANGELOG.md).

## [Unreleased]

### Added

* `RequestMethod` enum.

### Changed

* `HttpClient.request` accepts `RequestMethod`.

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

