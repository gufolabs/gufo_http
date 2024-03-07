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
- [niquests][niquests]
- [PycURL][pycurl]
- [urllib][urllib] from Python standard library

Both synchronous and asynchronous tests are conducted if supported by the library.
Libraries are tested against a local nginx installation provided by the `gufo.http.httpd` wrapper.
We're using median value to rank the benchmarks.

## Preparing

We're using AWS EC2 t2.xlarge (64 bit) instance with Debian 12.

Prepare node:
```
sudo apt-get update
sudo apt-get install --yes git python3.11-venv
python3 -m venv bench
cd bench
. bin/activate
```

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

## Single HTTP/1.1 Requests

Perform http requests to read 1kb text file. This test evaluates:

* The cost of client's initialization.
* The efficiency of the network code.
* The efficiency HTTP/1.1 parser. 

Run tests:
```
pytest benchmarks/test_single_x100_1k.py
```

Results:
```
================================================================= test session starts =================================================================
platform linux -- Python 3.11.2, pytest-7.4.3, pluggy-1.4.0
benchmark: 4.0.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /home/admin/bench/gufo_http
plugins: anyio-4.3.0, benchmark-4.0.0
collected 10 items                                                                                                                                    

benchmarks/test_single_x100_1k.py ..........                                                                                                    [100%]


----------------------------------------------------------------------------------------------- benchmark: 10 tests -----------------------------------------------------------------------------------------------
Name (time in us)                Min                    Max                   Mean                StdDev                 Median                   IQR            Outliers         OPS            Rounds  Iterations
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_pycurl_sync            552.7600 (1.0)         912.4570 (1.0)         627.4404 (1.0)         47.1721 (1.06)        614.9810 (1.0)         50.2328 (1.00)       121;29  1,593.7769 (1.0)         577           1
test_urllib_sync            642.2560 (1.16)        942.6400 (1.03)        716.9010 (1.14)        44.3196 (1.0)         707.1500 (1.15)        50.1018 (1.0)         83;13  1,394.8927 (0.88)        319           1
test_gufo_http_sync         974.8750 (1.76)      2,369.4640 (2.60)      1,078.5705 (1.72)        84.3947 (1.90)      1,064.8040 (1.73)        68.3635 (1.36)        43;13    927.1531 (0.58)        449           1
test_gufo_http_async      1,412.6310 (2.56)      2,331.5960 (2.56)      1,563.8148 (2.49)        96.4462 (2.18)      1,545.4200 (2.51)        95.4475 (1.91)        58;14    639.4619 (0.40)        377           1
test_niquests_sync        1,550.6730 (2.81)     21,700.8490 (23.78)     1,816.3988 (2.89)       936.3856 (21.13)     1,684.6870 (2.74)       165.0163 (3.29)         3;74    550.5399 (0.35)        479           1
test_requests_sync        1,739.7430 (3.15)      3,095.1940 (3.39)      1,887.8259 (3.01)       125.4138 (2.83)      1,861.5670 (3.03)        81.0945 (1.62)        20;16    529.7099 (0.33)        205           1
test_aiosonic_async       1,946.5800 (3.52)      3,595.9540 (3.94)      2,181.6655 (3.48)       228.6378 (5.16)      2,110.4205 (3.43)       106.0000 (2.12)        41;42    458.3654 (0.29)        394           1
test_aiohttp_async        2,177.3450 (3.94)      6,310.3440 (6.92)      2,371.1405 (3.78)       287.4802 (6.49)      2,336.2120 (3.80)       112.2787 (2.24)          4;6    421.7380 (0.26)        339           1
test_httpx_sync          45,358.3610 (82.06)    59,893.9320 (65.64)    48,566.7703 (77.40)    3,721.1132 (83.96)    47,275.3950 (76.87)    1,676.9437 (33.47)         2;2     20.5902 (0.01)         21           1
test_httpx_async         47,650.0620 (86.20)    60,349.6870 (66.14)    50,683.2971 (80.78)    3,316.6865 (74.84)    49,802.8250 (80.98)    2,193.1260 (43.77)         2;2     19.7304 (0.01)         17           1
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
================================================================= 10 passed in 9.12s ==================================================================
```

## 100 Linear HTTP/1.1 Requests

Perform set of 100 linear http requests to read 1kb text file using single client session
whenever possible. This test evaluates:

* The efficiency of the network code.
* The efficency of the HTTP/1.1 parser.
* An ability to maintain connection pools.

Run tests:
```
pytest benchmarks/test_linear_x100_1k.py
```

Results:
```
================================================================= test session starts =================================================================
platform linux -- Python 3.11.2, pytest-7.4.3, pluggy-1.4.0
benchmark: 4.0.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /home/admin/bench/gufo_http
plugins: anyio-4.3.0, benchmark-4.0.0
collected 10 items                                                                                                                                    

benchmarks/test_linear_x100_1k.py ..........                                                                                                    [100%]


----------------------------------------------------------------------------------- benchmark: 10 tests ------------------------------------------------------------------------------------
Name (time in ms)             Min                 Max                Mean            StdDev              Median               IQR            Outliers      OPS            Rounds  Iterations
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_pycurl_sync          14.8286 (1.0)       16.5635 (1.0)       15.5543 (1.0)      0.3471 (1.0)       15.5732 (1.0)      0.3715 (1.0)          16;3  64.2911 (1.0)          60           1
test_gufo_http_sync       16.9257 (1.14)      19.6100 (1.18)      18.3076 (1.18)     0.6682 (1.93)      18.4208 (1.18)     1.0598 (2.85)         20;0  54.6223 (0.85)         52           1
test_aiosonic_async       40.1948 (2.71)      44.1372 (2.66)      42.1504 (2.71)     1.0503 (3.03)      42.0433 (2.70)     1.4114 (3.80)         10;0  23.7246 (0.37)         24           1
test_aiohttp_async        40.7918 (2.75)      43.3388 (2.62)      41.7451 (2.68)     0.7409 (2.13)      41.5796 (2.67)     0.9894 (2.66)          6;0  23.9549 (0.37)         24           1
test_gufo_http_async      45.3282 (3.06)      49.3405 (2.98)      47.8282 (3.07)     0.8637 (2.49)      47.8277 (3.07)     0.7030 (1.89)          4;2  20.9082 (0.33)         21           1
test_urllib_sync          68.0795 (4.59)      70.9134 (4.28)      69.8699 (4.49)     0.8885 (2.56)      69.9497 (4.49)     1.4723 (3.96)          5;0  14.3123 (0.22)         15           1
test_niquests_sync        93.1297 (6.28)     120.2415 (7.26)      97.6183 (6.28)     7.5677 (21.80)     95.3918 (6.13)     1.0791 (2.90)          1;2  10.2440 (0.16)         11           1
test_httpx_sync          116.7218 (7.87)     120.3223 (7.26)     118.3450 (7.61)     1.3440 (3.87)     117.5656 (7.55)     2.3315 (6.28)          3;0   8.4499 (0.13)          9           1
test_httpx_async         172.9347 (11.66)    183.8432 (11.10)    177.3365 (11.40)    3.9560 (11.40)    176.9523 (11.36)    5.5285 (14.88)         2;0   5.6390 (0.09)          6           1
test_requests_sync       181.9891 (12.27)    187.1860 (11.30)    184.6352 (11.87)    2.0526 (5.91)     184.8448 (11.87)    3.3744 (9.08)          2;0   5.4161 (0.08)          6           1
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
================================================================= 10 passed in 14.29s =================================================================
```

## 100 Parallel HTTP/1.1 Requests

Perform 100 HTTP/1.1 requests to read 1kb text file with concurrency of 4 maintaininng
single client session per thread/coroutine.

* The efficiency of the network code.
* The efficency of the HTTP/1.1 parser.
* An ability to maintain connection pools.
* Granularity of the internal locs.
* Ability to release GIL when runnning native code.

Run tests:
```
pytest benchmarks/test_p4_x100_1k.py
```

Results:
```
================================================================= test session starts =================================================================
platform linux -- Python 3.11.2, pytest-7.4.3, pluggy-1.4.0
benchmark: 4.0.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /home/admin/bench/gufo_http
plugins: anyio-4.3.0, benchmark-4.0.0
collected 10 items                                                                                                                                    

benchmarks/test_p4_x100_1k.py ..........                                                                                                        [100%]


------------------------------------------------------------------------------------ benchmark: 10 tests ------------------------------------------------------------------------------------
Name (time in ms)             Min                 Max                Mean            StdDev              Median               IQR            Outliers       OPS            Rounds  Iterations
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_pycurl_sync           8.5505 (1.0)       11.6985 (1.0)        9.7086 (1.0)      0.6270 (1.0)        9.5728 (1.0)      0.8207 (1.66)         28;3  103.0011 (1.0)          99           1
test_gufo_http_sync        8.9141 (1.04)      11.8996 (1.02)      10.2942 (1.06)     0.6789 (1.08)      10.2281 (1.07)     0.8919 (1.80)         27;0   97.1422 (0.94)         80           1
test_gufo_http_async      31.1233 (3.64)      39.0700 (3.34)      32.9239 (3.39)     1.3814 (2.20)      32.5340 (3.40)     1.0728 (2.17)          2;1   30.3731 (0.29)         29           1
test_aiosonic_async       34.5276 (4.04)      39.8711 (3.41)      36.3939 (3.75)     1.1697 (1.87)      36.4312 (3.81)     1.7261 (3.49)          8;1   27.4772 (0.27)         29           1
test_aiohttp_async        38.0094 (4.45)      49.1993 (4.21)      39.3207 (4.05)     2.1364 (3.41)      38.8432 (4.06)     0.4950 (1.0)           1;2   25.4319 (0.25)         25           1
test_urllib_sync          43.8279 (5.13)      48.2060 (4.12)      44.9540 (4.63)     0.9605 (1.53)      44.6689 (4.67)     1.0362 (2.09)          5;1   22.2449 (0.22)         21           1
test_niquests_sync       101.4105 (11.86)    127.8796 (10.93)    105.9729 (10.92)    7.7871 (12.42)    104.0052 (10.86)    1.3018 (2.63)          1;1    9.4364 (0.09)         10           1
test_requests_sync       166.1476 (19.43)    168.5516 (14.41)    167.5796 (17.26)    0.8505 (1.36)     167.7444 (17.52)    0.9684 (1.96)          2;0    5.9673 (0.06)          6           1
test_httpx_sync          215.8258 (25.24)    230.6778 (19.72)    223.7639 (23.05)    5.8582 (9.34)     223.3114 (23.33)    9.0334 (18.25)         2;0    4.4690 (0.04)          5           1
test_httpx_async         298.3353 (34.89)    303.4051 (25.94)    301.2551 (31.03)    2.0818 (3.32)     301.8729 (31.53)    3.3335 (6.73)          2;0    3.3194 (0.03)          5           1
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
================================================================= 10 passed in 14.76s =================================================================
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
[niquests]: https://niquests.readthedocs.io/en/stable/
[pycurl]: http://pycurl.io/
[urllib]: https://docs.python.org/3/library/urllib.request.html#module-urllib.request
[discussion]: https://github.com/gufolabs/gufo_http/discussions/2