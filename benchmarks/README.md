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
benchmarks/test_p4_x100_1k.py: 900 warnings
  /usr/local/lib/python3.12/site-packages/onecache/__init__.py:52: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    expire_at = datetime.utcnow() + timedelta(milliseconds=self.timeout)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html

----------------------------------------------------------------------------------------- benchmark: 8 tests ----------------------------------------------------------------------------------------
Name (time in ms)               Min                   Max                  Mean             StdDev                Median                IQR            Outliers     OPS            Rounds  Iterations
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_gufo_http_async       142.5234 (1.0)        196.4966 (1.0)        154.0920 (1.0)      19.1469 (1.0)        148.1027 (1.0)       9.6178 (1.0)           1;1  6.4896 (1.0)           7           1
test_urllib_sync           150.2020 (1.05)       217.4265 (1.11)       172.5488 (1.12)     26.7115 (1.40)       158.9330 (1.07)     36.5320 (3.80)          1;0  5.7955 (0.89)          6           1
test_aiosonic_async        167.9288 (1.18)       238.5645 (1.21)       194.6592 (1.26)     26.6043 (1.39)       189.2370 (1.28)     42.6969 (4.44)          2;0  5.1372 (0.79)          7           1
test_aiohttp_async         181.5094 (1.27)       247.4179 (1.26)       205.6127 (1.33)     25.0146 (1.31)       202.6352 (1.37)     24.4862 (2.55)          1;0  4.8635 (0.75)          5           1
test_requests_sync         238.4310 (1.67)       372.1797 (1.89)       276.8299 (1.80)     55.4649 (2.90)       254.3191 (1.72)     60.2615 (6.27)          1;0  3.6123 (0.56)          5           1
test_gufo_http_sync        262.9267 (1.84)       326.4619 (1.66)       286.9891 (1.86)     26.7931 (1.40)       282.3365 (1.91)     43.0268 (4.47)          1;0  3.4845 (0.54)          5           1
test_httpx_sync            513.4131 (3.60)       575.2213 (2.93)       533.0847 (3.46)     24.6999 (1.29)       527.0547 (3.56)     26.3952 (2.74)          1;0  1.8759 (0.29)          5           1
test_httpx_async         1,145.9102 (8.04)     1,226.7240 (6.24)     1,175.5272 (7.63)     30.6345 (1.60)     1,168.4489 (7.89)     30.8301 (3.21)          1;0  0.8507 (0.13)          5           1
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
======================= 8 passed, 900 warnings in 24.48s =======================
```

[Gufo Labs]: https://gufolabs.com/
[Gufo Stack]: https://docs.gufolabs.com/
[Gufo HTTP]: https://docs.gufolabs.com/gufo_http/
[aiohttp]: https://docs.aiohttp.org/en/stable/
[aiosonic]: https://aiosonic.readthedocs.io/en/latest/
[httpx]: https://www.python-httpx.org
[requests]: https://requests.readthedocs.io/en/latest/
[urllib]: https://docs.python.org/3/library/urllib.request.html#module-urllib.request