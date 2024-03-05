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

Perform 100 HTTP/1.1 requests to read 1kb text file with concurrency of 4. Along with the
efficiency of the implementation of the client, this test also evaluates an efficiency
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


------------------------------------------------------------------------------------ benchmark: 8 tests ------------------------------------------------------------------------------------
Name (time in ms)             Min                 Max                Mean            StdDev              Median               IQR            Outliers      OPS            Rounds  Iterations
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_gufo_http_sync        8.9127 (1.0)       11.6549 (1.0)       10.4452 (1.0)      0.6743 (1.0)       10.5441 (1.0)      0.5976 (1.0)           5;3  95.7379 (1.0)          21           1
test_gufo_http_async      34.0677 (3.82)      42.7470 (3.67)      35.6436 (3.41)     1.6357 (2.43)      35.2255 (3.34)     0.9045 (1.51)          2;2  28.0556 (0.29)         28           1
test_aiosonic_async       34.8327 (3.91)      40.8665 (3.51)      37.7288 (3.61)     1.4914 (2.21)      37.7008 (3.58)     2.2096 (3.70)          8;0  26.5049 (0.28)         26           1
test_aiohttp_async        38.1524 (4.28)      46.9943 (4.03)      40.2307 (3.85)     1.7668 (2.62)      39.7903 (3.77)     1.8416 (3.08)          3;1  24.8566 (0.26)         24           1
test_urllib_sync          44.8055 (5.03)      48.4236 (4.15)      46.7769 (4.48)     1.0305 (1.53)      46.8137 (4.44)     1.4473 (2.42)          8;0  21.3781 (0.22)         21           1
test_requests_sync       138.5247 (15.54)    141.5943 (12.15)    140.3800 (13.44)    1.1060 (1.64)     140.6570 (13.34)    1.6775 (2.81)          2;0   7.1235 (0.07)          7           1
test_httpx_sync          218.9799 (24.57)    227.6729 (19.53)    222.5712 (21.31)    3.2829 (4.87)     221.7710 (21.03)    4.0976 (6.86)          2;0   4.4929 (0.05)          5           1
test_httpx_async         287.6360 (32.27)    301.8868 (25.90)    294.2786 (28.17)    5.7851 (8.58)     291.8509 (27.68)    8.8554 (14.82)         2;0   3.3981 (0.04)          5           1
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
================================================================= 8 passed in 12.00s ==================================================================
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