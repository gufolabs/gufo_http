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
- [aiosonic][aiosonic]
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
collected 8 items

benchmarks/test_linear_x100_1k.py ........                               [100%]

=============================== warnings summary ===============================
benchmarks/test_linear_x100_1k.py: 21 warnings
  /usr/local/lib/python3.12/site-packages/onecache/__init__.py:52: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    expire_at = datetime.utcnow() + timedelta(milliseconds=self.timeout)

benchmarks/test_linear_x100_1k.py: 2079 warnings
  /usr/local/lib/python3.12/site-packages/onecache/cache_value.py:24: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return datetime.utcnow() > self.expire_at

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html

------------------------------------------------------------------------------------- benchmark: 8 tests -------------------------------------------------------------------------------------
Name (time in ms)             Min                 Max                Mean             StdDev              Median                IQR            Outliers      OPS            Rounds  Iterations
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_gufo_http_sync       35.6027 (1.0)       57.0926 (1.0)       38.6746 (1.0)       5.1270 (3.04)      36.7502 (1.0)       2.1020 (1.0)           3;3  25.8568 (1.0)          22           1
test_aiosonic_async       51.3582 (1.44)      58.3746 (1.02)      54.0190 (1.40)      2.0410 (1.21)      53.6762 (1.46)      3.1153 (1.48)          6;0  18.5120 (0.72)         19           1
test_aiohttp_async        53.5090 (1.50)      67.6734 (1.19)      57.2506 (1.48)      5.1600 (3.06)      54.5661 (1.48)      3.6663 (1.74)          3;3  17.4671 (0.68)         16           1
test_gufo_http_async      73.2533 (2.06)      95.7414 (1.68)      84.9870 (2.20)      6.3187 (3.75)      84.3580 (2.30)      6.5765 (3.13)          4;0  11.7665 (0.46)         14           1
test_httpx_sync           95.3519 (2.68)     109.9267 (1.93)      99.6925 (2.58)      4.1980 (2.49)      98.1954 (2.67)      4.2843 (2.04)          2;1  10.0308 (0.39)         10           1
test_httpx_async         134.3467 (3.77)     138.9999 (2.43)     135.9656 (3.52)      1.6861 (1.0)      135.9719 (3.70)      2.2768 (1.08)          1;0   7.3548 (0.28)          7           1
test_urllib_sync         297.0125 (8.34)     312.4287 (5.47)     303.6417 (7.85)      5.8391 (3.46)     301.5891 (8.21)      7.3726 (3.51)          2;0   3.2934 (0.13)          5           1
test_requests_sync       301.0885 (8.46)     375.3247 (6.57)     335.4169 (8.67)     34.8310 (20.66)    321.6770 (8.75)     64.2984 (30.59)         1;0   2.9814 (0.12)          5           1
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
====================== 8 passed, 2100 warnings in 13.72s =======================
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
collected 8 items

benchmarks/test_p4_x100_1k.py ........                                   [100%]

=============================== warnings summary ===============================
benchmarks/test_p4_x100_1k.py: 800 warnings
  /usr/local/lib/python3.12/site-packages/onecache/__init__.py:52: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    expire_at = datetime.utcnow() + timedelta(milliseconds=self.timeout)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html

----------------------------------------------------------------------------------------- benchmark: 8 tests ----------------------------------------------------------------------------------------
Name (time in ms)               Min                   Max                  Mean             StdDev                Median                IQR            Outliers     OPS            Rounds  Iterations
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_gufo_http_sync        132.5631 (1.0)        344.4145 (1.72)       179.2132 (1.08)     81.5289 (6.97)       152.2771 (1.0)      21.1733 (1.88)          1;1  5.5799 (0.93)          6           1
test_urllib_sync           150.1315 (1.13)       212.0684 (1.06)       166.0132 (1.0)      21.9235 (1.87)       159.7634 (1.05)     19.4154 (1.72)          1;1  6.0236 (1.0)           7           1
test_aiosonic_async        165.5646 (1.25)       200.5206 (1.0)        182.2157 (1.10)     14.5718 (1.25)       179.2602 (1.18)     29.0415 (2.58)          3;0  5.4880 (0.91)          6           1
test_gufo_http_async       170.1850 (1.28)       268.8782 (1.34)       198.5795 (1.20)     36.2697 (3.10)       187.6347 (1.23)     27.9033 (2.48)          1;1  5.0358 (0.84)          6           1
test_aiohttp_async         189.8499 (1.43)       219.4065 (1.09)       199.2248 (1.20)     11.6994 (1.0)        195.3674 (1.28)     11.2554 (1.0)           1;0  5.0195 (0.83)          5           1
test_requests_sync         252.8026 (1.91)       297.9527 (1.49)       274.3723 (1.65)     16.5973 (1.42)       275.1445 (1.81)     20.5420 (1.83)          2;0  3.6447 (0.61)          5           1
test_httpx_sync            541.3474 (4.08)       688.1268 (3.43)       638.5117 (3.85)     58.8306 (5.03)       652.4500 (4.28)     73.1675 (6.50)          1;0  1.5661 (0.26)          5           1
test_httpx_async         1,190.3004 (8.98)     1,271.5708 (6.34)     1,220.3579 (7.35)     33.6008 (2.87)     1,202.2185 (7.89)     47.4888 (4.22)          1;0  0.8194 (0.14)          5           1
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
======================= 8 passed, 800 warnings in 24.73s =======================
```

[Gufo Labs]: https://gufolabs.com/
[Gufo Stack]: https://docs.gufolabs.com/
[Gufo HTTP]: https://docs.gufolabs.com/gufo_http/
[aiohttp]: https://docs.aiohttp.org/en/stable/
[aiosonic]: https://aiosonic.readthedocs.io/en/latest/
[httpx]: https://www.python-httpx.org
[requests]: https://requests.readthedocs.io/en/latest/
[urllib]: https://docs.python.org/3/library/urllib.request.html#module-urllib.request