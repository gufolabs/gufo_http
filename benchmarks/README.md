---
hide:
    - navigation
---
# Python HTTP Clients Benchmark

!!! warning

    All following information is provided only for reference.
    These tests are performed by [Gufo Labs][Gufo Labs] to estimate the performance
    of [Gufo HTTP][Gufo HTTP] against major competitors, so they cannot be considered
    independent and unbiased.

    Although performance is an absolute requirement for [Gufo Stack][Gufo Stack],
    other factors such as maturity, community, features, examples, and existing code base
    should also be considered.

We're comparing:

- [Gufo HTTP][Gufo HTTP] (current version)
- [aiohttp][aiohttp]
- [httpx][httpx]
- [requests][requests]
- [urllib][urllib] from Python standard library

Both synchronous and asynchronous tests are conducted if supported by the library. Libraries are tested against a local nginx installation provided by the `gufo.http.httpd` wrapper.

## Preparing

!!! note

    We're utilizing Gufo HTTP's development container,
    so your results may differ. However, the ranking and performance ratios should remain consistent.

Install local nginx:
```
./tools/build/setup-nginx.sh
```

Install Rust toolchain:

```
./tools/build/setup-rust.sh
```

Build Gufo HTTP:

```
python -m pip install --editable .
```

Install dependencies:

```
pip install -r .requirements/test.txt -r .requirements/bench.txt
```

## 100 Linear HTTP/1.1 Requests

Perform set of 100 linear http requests to read 1kb text file. This test evaluates
the efficiency of the network code and HTTP/1.1 parser. It also evaluates an
ability to maintain connection pools.

Run tests:
```
pytest benchmarks/test_linear_x100_1k.py
```

Results:
```
============================= test session starts ==============================
platform linux -- Python 3.12.2, pytest-7.4.3, pluggy-1.4.0
benchmark: 4.0.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /workspaces/gufo_http
plugins: anyio-4.3.0, benchmark-4.0.0
collected 7 items

benchmarks/test_linear_x100_1k.py .......                                [100%]


-------------------------------------------------------------------------------------- benchmark: 7 tests -------------------------------------------------------------------------------------
Name (time in ms)             Min                 Max                Mean             StdDev              Median                 IQR            Outliers      OPS            Rounds  Iterations
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_gufo_http_sync       35.7877 (1.0)       54.3751 (1.0)       38.6503 (1.0)       4.2814 (5.48)      37.4646 (1.0)        2.2753 (3.35)          2;2  25.8730 (1.0)          23           1
test_aiohttp_async        53.8590 (1.50)      57.0090 (1.05)      54.5310 (1.41)      0.7810 (1.0)       54.1197 (1.44)       0.9413 (1.38)          3;1  18.3382 (0.71)         19           1
test_gufo_http_async      71.4257 (2.00)      75.1873 (1.38)      72.6669 (1.88)      0.9725 (1.25)      72.5345 (1.94)       0.6801 (1.0)           4;2  13.7614 (0.53)         14           1
test_httpx_sync           97.6429 (2.73)     134.5522 (2.47)     102.5810 (2.65)     11.2894 (14.46)     98.6623 (2.63)       2.3364 (3.44)          1;1   9.7484 (0.38)         10           1
test_httpx_async         134.4390 (3.76)     158.1822 (2.91)     142.0460 (3.68)      9.0029 (11.53)    138.6336 (3.70)      12.5167 (18.40)         1;0   7.0400 (0.27)          7           1
test_requests_sync       287.1135 (8.02)     408.0361 (7.50)     349.2597 (9.04)     54.6750 (70.01)    343.3154 (9.16)     101.8697 (149.78)        2;0   2.8632 (0.11)          5           1
test_urllib_sync         314.0911 (8.78)     364.8527 (6.71)     333.5485 (8.63)     19.4727 (24.93)    328.2946 (8.76)      23.7571 (34.93)         1;0   2.9981 (0.12)          5           1
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
============================== 7 passed in 12.77s ==============================
```

## 100 Parallel HTTP/1.1 Requests

Perform 100 HTTP/1.1 requests to read 1kb text file with concurrency of 4. This test
disables connection pooling and, along with the
efficiency of the implementation of the client, also evaluates an efficiency
of the internal locks and ability to release GIL.

Run tests:
```
pytest benchmarks/test_p4_x100_1k.py
```

Results:
```
============================= test session starts ==============================
platform linux -- Python 3.12.2, pytest-7.4.3, pluggy-1.4.0
benchmark: 4.0.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /workspaces/gufo_http
plugins: anyio-4.3.0, benchmark-4.0.0
collected 7 items

benchmarks/test_p4_x100_1k.py .......                                    [100%]


----------------------------------------------------------------------------------------- benchmark: 7 tests ----------------------------------------------------------------------------------------
Name (time in ms)               Min                   Max                  Mean             StdDev                Median                IQR            Outliers     OPS            Rounds  Iterations
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_urllib_sync           144.6250 (1.0)        182.3744 (1.0)        158.7986 (1.0)      12.8509 (1.0)        155.2828 (1.00)     16.2050 (1.26)          2;0  6.2973 (1.0)           7           1
test_gufo_http_async       145.4200 (1.01)       317.9843 (1.74)       192.2990 (1.21)     72.6409 (5.65)       155.0639 (1.0)      74.2793 (5.79)          1;0  5.2002 (0.83)          5           1
test_aiohttp_async         199.9764 (1.38)       256.8007 (1.41)       216.0407 (1.36)     24.5505 (1.91)       200.9554 (1.30)     29.8563 (2.33)          1;0  4.6288 (0.74)          5           1
test_requests_sync         233.9884 (1.62)       269.9899 (1.48)       242.5581 (1.53)     15.5051 (1.21)       234.6229 (1.51)     12.8275 (1.0)           1;1  4.1227 (0.65)          5           1
test_gufo_http_sync        269.2625 (1.86)       308.8797 (1.69)       286.9226 (1.81)     15.1410 (1.18)       282.2685 (1.82)     20.5784 (1.60)          2;0  3.4853 (0.55)          5           1
test_httpx_sync            539.9584 (3.73)       642.0066 (3.52)       576.4343 (3.63)     38.7065 (3.01)       567.9095 (3.66)     34.8972 (2.72)          1;0  1.7348 (0.28)          5           1
test_httpx_async         1,141.0411 (7.89)     1,229.2292 (6.74)     1,193.7929 (7.52)     35.0876 (2.73)     1,191.5070 (7.68)     49.8831 (3.89)          2;0  0.8377 (0.13)          5           1
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
============================== 7 passed in 22.71s ==============================
```

[Gufo Labs]: https://gufolabs.com/
[Gufo Stack]: https://docs.gufolabs.com/
[Gufo HTTP]: https://docs.gufolabs.com/gufo_http/
[aiohttp]: https://docs.aiohttp.org/en/stable/
[httpx]: https://www.python-httpx.org
[requests]: https://requests.readthedocs.io/en/latest/
[urllib]: https://docs.python.org/3/library/urllib.request.html#module-urllib.request