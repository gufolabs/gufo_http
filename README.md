# Gufo HTTP

*The accelerated Python HTTP client library.*

[![PyPi version](https://img.shields.io/pypi/v/gufo_http.svg)](https://pypi.python.org/pypi/gufo_http/)
![Python Versions](https://img.shields.io/pypi/pyversions/gufo_http)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
![Build](https://img.shields.io/github/actions/workflow/status/gufolabs/gufo_http/tests.yml?branch=master)
![Sponsors](https://img.shields.io/github/sponsors/gufolabs)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json)](https://github.com/charliermarsh/ruff)

---

**Documentation**: [https://docs.gufolabs.com/gufo_http/](https://docs.gufolabs.com/gufo_http/)

**Source Code**: [https://github.com/gufolabs/gufo_http/](https://github.com/gufolabs/gufo_http/)

---

WARNING: Initial release, work in progress. Coming soon...

*Gufo HTTP* is a high-performance Python HTTP client library that handles both asynchronous and synchronous modes.
It wraps famous [Reqwest][Reqwest] HTTP client, written in
[Rust][Rust] language with [PyO3][PyO3] wrapper.

The getting of single URL is a simple task:

``` python
async with HttpClient() as client:
    resp = client.get("https://docs.gufolabs.com")
    assert resp.status == 200
    data = await resp.read()
```

The `HttpClient` is highly customizable, for example,
to set request headers:

``` python
async with HttpClient(headers={"X-My-Header": b"test"}) as client:
    resp = client.get("https://docs.gufolabs.com")
    ...
```

Gufo HTTP supports common authentication methods out-of-box:

``` python
async with HttpClient(auth=BasicAuth("scott", "tiger")) as client:
    resp = client.get("https://docs.gufolabs.com")
    ...
```


## On Gufo Stack

This product is a part of [Gufo Stack][Gufo Stack] - the collaborative effort 
led by [Gufo Labs][Gufo Labs]. Our goal is to create a robust and flexible 
set of tools to create network management software and automate 
routine administration tasks.

To do this, we extract the key technologies that have proven themselves 
in the [NOC][NOC] and bring them as separate packages. Then we work on API,
performance tuning, documentation, and testing. The [NOC][NOC] uses the final result
as the external dependencies.

[Gufo Stack][Gufo Stack] makes the [NOC][NOC] better, and this is our primary task. But other products
can benefit from [Gufo Stack][Gufo Stack] too. So we believe that our effort will make 
the other network management products better.

[Gufo Labs]: https://gufolabs.com/
[Gufo Stack]: https://gufolabs.com/products/gufo-stack/
[NOC]: https://getnoc.com/
[Rust]: https://rust-lang.org/
[PyO3]: https://pyo3.rs/
[Reqwest]: https://github.com/seanmonstar/reqwest