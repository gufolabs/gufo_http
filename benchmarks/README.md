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

Both synchronous and asynchronous tests are conducted if supported by the library.
Libraries are tested against a local nginx installation provided by the `gufo.http.httpd` wrapper.
We're using median value to rank the benchmarks.

## Preparing

We're using AWS EC2 t2.xlarge instance with Debian 12 instance.

Clone repo:
```
git clone https://github.com/gufolabs/gufo_http.git
cd gufo_http
```

Install local nginx:
```
./tools/build/setup-nginx.sh
```

Install dependencies:

```
pip3 install -r .requirements/test.txt -r .requirements/bench.txt gufo-http
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
================================================================= test session starts =================================================================
platform linux -- Python 3.11.2, pytest-7.4.3, pluggy-1.4.0
benchmark: 4.0.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /home/admin/gufo_http
plugins: anyio-4.3.0, benchmark-4.0.0
collected 8 items                                                                                                                                     

benchmarks/test_linear_x100_1k.py ........                                                                                                      [100%]


------------------------------------------------------------------------------------ benchmark: 8 tests ------------------------------------------------------------------------------------
Name (time in ms)             Min                 Max                Mean            StdDev              Median               IQR            Outliers      OPS            Rounds  Iterations
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_gufo_http_sync       18.6511 (1.0)       22.0578 (1.0)       20.7532 (1.0)      0.7476 (1.06)      20.8302 (1.0)      1.0786 (1.66)          7;0  48.1852 (1.0)          25           1
test_aiohttp_async        45.3278 (2.43)      48.0793 (2.18)      46.4353 (2.24)     0.7075 (1.0)       46.3188 (2.22)     0.6506 (1.0)           5;2  21.5354 (0.45)         21           1
test_aiosonic_async       48.2223 (2.59)      53.3538 (2.42)      49.6425 (2.39)     1.0922 (1.54)      49.5367 (2.38)     0.9324 (1.43)          4;1  20.1440 (0.42)         20           1
test_gufo_http_async      51.3218 (2.75)      55.0385 (2.50)      53.1424 (2.56)     1.0471 (1.48)      53.0693 (2.55)     1.3117 (2.02)          6;0  18.8174 (0.39)         18           1
test_urllib_sync          78.6088 (4.21)      82.4507 (3.74)      79.8657 (3.85)     1.0909 (1.54)      80.0389 (3.84)     1.5550 (2.39)          3;0  12.5210 (0.26)         13           1
test_httpx_sync          118.4881 (6.35)     122.2384 (5.54)     120.2949 (5.80)     1.1943 (1.69)     120.4083 (5.78)     1.3665 (2.10)          4;0   8.3129 (0.17)          9           1
test_requests_sync       163.7536 (8.78)     166.6170 (7.55)     164.9666 (7.95)     1.1180 (1.58)     164.9403 (7.92)     1.9717 (3.03)          3;0   6.0618 (0.13)          6           1
test_httpx_async         174.7670 (9.37)     182.8303 (8.29)     178.9327 (8.62)     3.6452 (5.15)     180.7324 (8.68)     6.2842 (9.66)          2;0   5.5887 (0.12)          5           1
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
================================================================= 8 passed in 11.26s ==================================================================
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
================================================================= test session starts =================================================================
platform linux -- Python 3.11.2, pytest-7.4.3, pluggy-1.4.0
benchmark: 4.0.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /home/admin/gufo_http
plugins: anyio-4.3.0, benchmark-4.0.0
collected 8 items                                                                                                                                     

benchmarks/test_p4_x100_1k.py ........                                                                                                          [100%]


------------------------------------------------------------------------------------------- benchmark: 8 tests ------------------------------------------------------------------------------------------
Name (time in ms)               Min                   Max                  Mean                StdDev                Median                IQR            Outliers      OPS            Rounds  Iterations
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_gufo_http_sync         47.1888 (1.0)      5,045.7544 (87.58)      299.6138 (5.74)     1,117.1265 (>1000.0)     49.7281 (1.0)       1.6933 (1.22)          1;2   3.3376 (0.17)         20           1
test_urllib_sync            49.2343 (1.04)        57.6137 (1.0)         52.1996 (1.0)          2.0458 (1.87)        51.6310 (1.04)      1.4353 (1.03)          5;3  19.1572 (1.0)          19           1
test_gufo_http_async        58.4397 (1.24)        61.6751 (1.07)        60.1698 (1.15)         1.0913 (1.0)         60.3053 (1.21)      1.9670 (1.42)          6;0  16.6196 (0.87)         17           1
test_aiosonic_async         97.0841 (2.06)       125.0035 (2.17)       103.6111 (1.98)         9.8370 (9.01)        99.8978 (2.01)      3.9392 (2.84)          2;2   9.6515 (0.50)         11           1
test_aiohttp_async         111.5709 (2.36)       116.7556 (2.03)       114.6789 (2.20)         1.9406 (1.78)       114.8500 (2.31)      3.2414 (2.34)          4;0   8.7200 (0.46)          8           1
test_requests_sync         143.6128 (3.04)       165.8280 (2.88)       147.7651 (2.83)         7.9978 (7.33)       144.8788 (2.91)      1.3873 (1.0)           1;1   6.7675 (0.35)          7           1
test_httpx_sync          3,297.1338 (69.87)    3,341.2073 (57.99)    3,324.2242 (63.68)       18.7042 (17.14)    3,332.4440 (67.01)    29.6245 (21.35)         1;0   0.3008 (0.02)          5           1
test_httpx_async         4,304.5593 (91.22)    4,358.0231 (75.64)    4,324.6237 (82.85)       24.2366 (22.21)    4,311.7061 (86.71)    40.7096 (29.34)         1;0   0.2312 (0.01)          5           1
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
============================================================ 8 passed in 68.05s (0:01:08) =============================================================
```

## Feedback

If you have any ideas, comment, or thoughts on benchmark suite,
feel free to [discuss it on GitHub][discussion].

[Gufo Labs]: https://gufolabs.com/
[Gufo Stack]: https://docs.gufolabs.com/
[Gufo HTTP]: https://docs.gufolabs.com/gufo_http/
[aiohttp]: https://docs.aiohttp.org/en/stable/
[aiosonic]: https://aiosonic.readthedocs.io/en/latest/
[httpx]: https://www.python-httpx.org
[requests]: https://requests.readthedocs.io/en/latest/
[urllib]: https://docs.python.org/3/library/urllib.request.html#module-urllib.request
[discussion]: https://github.com/gufolabs/gufo_http/discussions/2