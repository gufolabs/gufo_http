---
template: index.html
hide:
    - navigation
    - toc
hero:
    title: Gufo HTTP
    subtitle: The accelerated Python HTTP client library
    install_button: Getting Started
    source_button: Source Code
---

*Gufo HTTP* is a high-performance Python HTTP client library that handles both asynchronous and synchronous modes.
It wraps famous [Reqwest][Reqwest] HTTP client, written in
[Rust][Rust] language with [PyO3][PyO3] wrapper.

The getting of single URL is a simple task:

``` python
async with HttpClient() as client:
    resp = client.get("https://docs.gufolabs.com/")
    assert resp.status == 200
    data = await resp.read()
```

The `HttpClient` is highly customizable, for example,
to set request headers:

``` python
async with HttpClient(headers={"X-My-Header": b"test"}) as client:
    resp = client.get("https://docs.gufolabs.com/")
    ...
```

Gufo HTTP supports common authentication methods out-of-box:

``` python
async with HttpClient(auth=BasicAuth("scott", "tiger")) as client:
    resp = client.get("https://protected.example.com/")
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