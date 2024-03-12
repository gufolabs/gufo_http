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
- [aiohttp][aiohttp] (3.9.3)
- [aiosonic][aiosonic] (0.18.0)
- [httpx][httpx] (0.27)
- [requests][requests] (2.31.0)
- [niquests][niquests] (3.5.2)
- [PycURL][pycurl] (7.45.3)
- [urllib][urllib] from Python standard library
- [urllibb3][urllib3] (2.2.1)

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

## HTTP/1.1 Requests

### Single Requests

Perform http requests to read 1kb text file. This test evaluates:

* The cost of client's initialization.
* The efficiency of the network code.
* The efficiency HTTP/1.1 parser. 

Run tests:
```
pytest benchmarks/test_single_x100_1k.py
```

**Results (lower is better)**
```
================================================================= test session starts =================================================================
platform linux -- Python 3.11.2, pytest-7.4.3, pluggy-1.4.0
benchmark: 4.0.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /home/admin/bench/gufo_http
plugins: anyio-4.3.0, benchmark-4.0.0
collected 11 items                                                                                                                                    

benchmarks/test_single_x100_1k.py ...........                                                                                                   [100%]


----------------------------------------------------------------------------------------------- benchmark: 11 tests -----------------------------------------------------------------------------------------------
Name (time in us)                Min                    Max                   Mean                StdDev                 Median                   IQR            Outliers         OPS            Rounds  Iterations
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_urllib3_sync           559.6880 (1.0)       1,246.9130 (1.67)        612.8979 (1.0)         44.8409 (1.56)        607.6110 (1.0)         25.8205 (1.0)         37;33  1,631.5931 (1.0)         697           1
test_pycurl_sync            572.5990 (1.02)        748.3810 (1.0)         622.1162 (1.02)        34.7881 (1.21)        617.5100 (1.02)        40.2622 (1.56)         20;3  1,607.4169 (0.99)         73           1
test_urllib_sync            658.8650 (1.18)        868.8990 (1.16)        720.5614 (1.18)        28.7254 (1.0)         716.4400 (1.18)        31.2975 (1.21)       208;26  1,387.8069 (0.85)        751           1
test_gufo_http_sync         932.3560 (1.67)      2,139.1020 (2.86)      1,043.3998 (1.70)       177.0928 (6.17)      1,005.6240 (1.66)        62.1935 (2.41)          1;4    958.4054 (0.59)         45           1
test_gufo_http_async      1,330.7690 (2.38)      1,622.9070 (2.17)      1,435.8727 (2.34)        46.7674 (1.63)      1,433.4990 (2.36)        60.2895 (2.33)        119;8    696.4405 (0.43)        405           1
test_niquests_sync        1,542.7730 (2.76)     19,614.0250 (26.21)     1,779.6494 (2.90)       830.0737 (28.90)     1,661.4445 (2.73)       101.0680 (3.91)        8;108    561.9084 (0.34)        494           1
test_requests_sync        1,761.6280 (3.15)      2,453.6630 (3.28)      1,909.8052 (3.12)       140.1992 (4.88)      1,856.9455 (3.06)       112.2350 (4.35)          8;4    523.6136 (0.32)         46           1
test_aiosonic_async       1,959.2180 (3.50)      3,370.8260 (4.50)      2,154.0451 (3.51)       208.8863 (7.27)      2,093.3120 (3.45)        83.0015 (3.21)        40;41    464.2428 (0.28)        404           1
test_aiohttp_async        2,151.3730 (3.84)      8,118.6410 (10.85)     2,292.1203 (3.74)       317.2131 (11.04)     2,267.8740 (3.73)        73.7982 (2.86)          1;7    436.2773 (0.27)        351           1
test_httpx_sync          41,079.3140 (73.40)    54,493.3170 (72.81)    42,657.7260 (69.60)    2,765.8773 (96.29)    41,970.3340 (69.07)      753.7480 (29.19)         1;3     23.4424 (0.01)         22           1
test_httpx_async         42,803.9490 (76.48)    52,177.8810 (69.72)    45,093.8321 (73.57)    2,592.9973 (90.27)    44,251.4320 (72.83)    1,208.5235 (46.80)         2;2     22.1760 (0.01)         15           1
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
================================================================= 11 passed in 9.17s ==================================================================
```

![Median chart](single_x100_1k.png)
*Lower is better*

### 100 Linear Requests

Perform set of 100 linear http requests to read 1kb text file using single client session
whenever possible. This test evaluates:

* The efficiency of the network code.
* The efficency of the HTTP/1.1 parser.
* An ability to maintain connection pools.

Run tests:
```
pytest benchmarks/test_linear_x100_1k.py
```

**Results (lower is better)**
```
================================================================= test session starts =================================================================
platform linux -- Python 3.11.2, pytest-7.4.3, pluggy-1.4.0
benchmark: 4.0.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /home/admin/bench/gufo_http
plugins: anyio-4.3.0, benchmark-4.0.0
collected 11 items                                                                                                                                    

benchmarks/test_linear_x100_1k.py ...........                                                                                                   [100%]


----------------------------------------------------------------------------------- benchmark: 11 tests ------------------------------------------------------------------------------------
Name (time in ms)             Min                 Max                Mean            StdDev              Median               IQR            Outliers      OPS            Rounds  Iterations
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_pycurl_sync          14.8365 (1.0)       16.3861 (1.0)       15.5327 (1.0)      0.3498 (1.0)       15.5279 (1.0)      0.4758 (1.0)          20;0  64.3803 (1.0)          59           1
test_gufo_http_sync       15.6296 (1.05)      18.9774 (1.16)      17.0747 (1.10)     0.6889 (1.97)      16.9616 (1.09)     0.9595 (2.02)         18;0  58.5661 (0.91)         58           1
test_aiohttp_async        41.4606 (2.79)      43.2958 (2.64)      42.4532 (2.73)     0.5326 (1.52)      42.4940 (2.74)     0.7613 (1.60)          9;0  23.5553 (0.37)         23           1
test_gufo_http_async      44.5912 (3.01)      49.0183 (2.99)      46.2745 (2.98)     1.1522 (3.29)      46.1390 (2.97)     1.0644 (2.24)          7;2  21.6102 (0.34)         22           1
test_aiosonic_async       44.7362 (3.02)      48.9211 (2.99)      46.3734 (2.99)     0.8680 (2.48)      46.3936 (2.99)     0.7834 (1.65)          5;2  21.5641 (0.33)         22           1
test_urllib3_sync         58.2859 (3.93)      59.8772 (3.65)      59.0778 (3.80)     0.4955 (1.42)      59.0435 (3.80)     0.5773 (1.21)          6;0  16.9268 (0.26)         17           1
test_urllib_sync          70.2436 (4.73)      72.3247 (4.41)      71.5258 (4.60)     0.5289 (1.51)      71.4880 (4.60)     0.5479 (1.15)          4;1  13.9810 (0.22)         14           1
test_niquests_sync        91.8051 (6.19)     109.4231 (6.68)      94.9622 (6.11)     4.8379 (13.83)     93.7023 (6.03)     0.6003 (1.26)          1;2  10.5305 (0.16)         11           1
test_httpx_sync          112.5345 (7.58)     116.1791 (7.09)     114.3526 (7.36)     1.2965 (3.71)     113.8844 (7.33)     2.2858 (4.80)          4;0   8.7449 (0.14)          9           1
test_httpx_async         167.3883 (11.28)    172.2522 (10.51)    168.7584 (10.86)    1.7953 (5.13)     168.3583 (10.84)    1.1404 (2.40)          1;1   5.9256 (0.09)          6           1
test_requests_sync       180.1325 (12.14)    183.1228 (11.18)    182.1927 (11.73)    1.1785 (3.37)     182.7465 (11.77)    1.5222 (3.20)          1;0   5.4887 (0.09)          6           1
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
================================================================= 11 passed in 15.21s =================================================================
```

![Median chart](linear_x100_1k.png)
*Lower is better*

### 100 Parallel Requests

Perform 100 HTTP/1.1 requests to read 1kb text file with concurrency of 4 maintaininng
single client session per thread/coroutine.

* The efficiency of the network code.
* The efficency of the HTTP/1.1 parser.
* An ability to maintain connection pools.
* Granularity of the internal locks.
* Ability to release GIL when runnning native code.

Run tests:
```
pytest benchmarks/test_p4_x100_1k.py
```

**Results (lower is better)**
```
================================================================= test session starts =================================================================
platform linux -- Python 3.11.2, pytest-7.4.3, pluggy-1.4.0
benchmark: 4.0.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /home/admin/bench/gufo_http
plugins: anyio-4.3.0, benchmark-4.0.0
collected 11 items                                                                                                                                    

benchmarks/test_p4_x100_1k.py ...........                                                                                                       [100%]


------------------------------------------------------------------------------------ benchmark: 11 tests ------------------------------------------------------------------------------------
Name (time in ms)             Min                 Max                Mean            StdDev              Median               IQR            Outliers       OPS            Rounds  Iterations
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_gufo_http_sync        7.2836 (1.0)       10.8954 (1.0)        9.1802 (1.0)      0.5346 (1.03)       9.1541 (1.0)      0.5174 (1.04)         25;6  108.9302 (1.0)          92           1
test_pycurl_sync           8.2186 (1.13)      11.0696 (1.02)       9.3183 (1.02)     0.5181 (1.0)        9.2534 (1.01)     0.4962 (1.0)          26;6  107.3162 (0.99)         87           1
test_gufo_http_async      30.1939 (4.15)      40.5446 (3.72)      31.6853 (3.45)     1.8262 (3.52)      31.3115 (3.42)     1.0123 (2.04)          2;2   31.5604 (0.29)         31           1
test_aiosonic_async       34.1517 (4.69)      38.6213 (3.54)      36.0843 (3.93)     1.3087 (2.53)      35.6595 (3.90)     1.8279 (3.68)          9;0   27.7129 (0.25)         27           1
test_aiohttp_async        37.4081 (5.14)      47.7629 (4.38)      39.4416 (4.30)     1.9344 (3.73)      39.0971 (4.27)     0.9056 (1.82)          3;2   25.3539 (0.23)         25           1
test_urllib_sync          41.5838 (5.71)      44.7744 (4.11)      43.2369 (4.71)     0.7841 (1.51)      43.2862 (4.73)     1.1149 (2.25)          7;0   23.1284 (0.21)         23           1
test_urllib3_sync         63.4683 (8.71)      66.6725 (6.12)      64.5508 (7.03)     0.8025 (1.55)      64.5220 (7.05)     1.1252 (2.27)          4;0   15.4917 (0.14)         16           1
test_niquests_sync        99.8689 (13.71)    118.2912 (10.86)    102.6201 (11.18)    5.5534 (10.72)    100.9334 (11.03)    1.6546 (3.33)          1;1    9.7447 (0.09)         10           1
test_requests_sync       161.9760 (22.24)    164.8976 (15.13)    163.5207 (17.81)    1.3422 (2.59)     163.7541 (17.89)    2.5137 (5.07)          3;0    6.1154 (0.06)          6           1
test_httpx_sync          210.2389 (28.86)    225.5404 (20.70)    217.2855 (23.67)    5.8637 (11.32)    218.2690 (23.84)    8.1161 (16.36)         2;0    4.6022 (0.04)          5           1
test_httpx_async         280.2248 (38.47)    290.9817 (26.71)    285.0176 (31.05)    4.2305 (8.17)     284.1745 (31.04)    6.4064 (12.91)         2;0    3.5086 (0.03)          5           1
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
================================================================= 11 passed in 15.52s =================================================================
```

![Median chart](p4_x100_1k.png)
*Lower is better*

## HTTPS Requests

### Single Requests

Perform HTTP/2 requests to read 1kb text file. This test evaluates:

* The cost of client's initialization.
* The efficiency of the network code.
* The efficiency HTTP/1.1 or HTTP/2 parser. 
* The efficency of the crypto.

Run tests:
```
pytest benchmarks/test_https_single_x100_1k.py
```

**Results (lower is better)**
```
================================================================= test session starts =================================================================
platform linux -- Python 3.11.2, pytest-7.4.3, pluggy-1.4.0
benchmark: 4.0.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /home/admin/bench/gufo_http
plugins: anyio-4.3.0, benchmark-4.0.0
collected 11 items                                                                                                                                    

benchmarks/test_https_single_x100_1k.py ...........


--------------------------------------------------------------------------------- benchmark: 11 tests ----------------------------------------------------------------------------------
Name (time in ms)            Min                Max               Mean            StdDev             Median               IQR            Outliers      OPS            Rounds  Iterations
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_pycurl_sync         10.1101 (1.0)      10.5270 (1.0)      10.2586 (1.0)      0.0936 (1.0)      10.2440 (1.0)      0.1147 (1.0)          12;1  97.4796 (1.0)          35           1
test_gufo_http_sync      10.1201 (1.00)     13.3844 (1.27)     10.9279 (1.07)     1.2221 (13.06)    10.3468 (1.01)     0.2738 (2.39)          3;3  91.5086 (0.94)         15           1
test_gufo_http_async     10.5507 (1.04)     12.8932 (1.22)     10.8390 (1.06)     0.2696 (2.88)     10.8037 (1.05)     0.1846 (1.61)          6;3  92.2592 (0.95)         80           1
test_urllib_sync         11.2086 (1.11)     20.0086 (1.90)     11.7377 (1.14)     1.0123 (10.82)    11.5494 (1.13)     0.4450 (3.88)          4;4  85.1954 (0.87)         83           1
test_httpx_sync          11.6343 (1.15)     13.5775 (1.29)     11.9254 (1.16)     0.2859 (3.05)     11.8440 (1.16)     0.1684 (1.47)          9;8  83.8543 (0.86)         78           1
test_aiohttp_async       13.0218 (1.29)     15.0993 (1.43)     13.5596 (1.32)     0.4582 (4.90)     13.4380 (1.31)     0.3692 (3.22)          3;1  73.7485 (0.76)         18           1
test_httpx_async         14.0437 (1.39)     17.7872 (1.69)     14.6871 (1.43)     0.7068 (7.55)     14.4611 (1.41)     0.6279 (5.48)          4;3  68.0869 (0.70)         40           1
test_aiosonic_async      52.5720 (5.20)     59.0495 (5.61)     53.9475 (5.26)     1.4194 (15.17)    53.6496 (5.24)     0.6740 (5.88)          2;2  18.5365 (0.19)         19           1
test_urllib3_sync        52.7468 (5.22)     60.9415 (5.79)     55.0618 (5.37)     1.9572 (20.91)    54.9122 (5.36)     2.6238 (22.88)         6;1  18.1614 (0.19)         20           1
test_niquests_sync       54.0449 (5.35)     57.9727 (5.51)     55.5715 (5.42)     1.0943 (11.69)    55.3307 (5.40)     1.3082 (11.41)         4;0  17.9948 (0.18)         18           1
test_requests_sync       54.1392 (5.35)     57.9534 (5.51)     55.7626 (5.44)     1.2469 (13.32)    55.3186 (5.40)     2.3477 (20.47)         5;0  17.9332 (0.18)         14           1
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
========================================================== 11 passed, 44 warnings in 14.36s ===========================================================
```

![Median chart](https_single_x100_1k.png)
*Lower is better*

### 100 Linear Requests
Perform set of 100 linear HTTPS requests to read 1kb text file using single client session
whenever possible. This test evaluates:

* The efficiency of the network code.
* The efficency of the HTTP/1.1 parser.
* An ability to maintain connection pools.
* The efficency of the crypto.

Run tests:
```
pytest benchmarks/test_https_linear_x100_1k.py
```

**Results (lower is better)**

```
================================================================= test session starts =================================================================
platform linux -- Python 3.11.2, pytest-7.4.3, pluggy-1.4.0
benchmark: 4.0.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /home/admin/bench/gufo_http
plugins: anyio-4.3.0, benchmark-4.0.0
collected 11 items                                                                                                                                    

benchmarks/test_https_linear_x100_1k.py ...........                                                                                             [100%]


----------------------------------------------------------------------------------------- benchmark: 11 tests -----------------------------------------------------------------------------------------
Name (time in ms)               Min                   Max                  Mean             StdDev                Median                 IQR            Outliers      OPS            Rounds  Iterations
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_pycurl_sync            27.5530 (1.0)         30.2960 (1.0)         28.6996 (1.0)       0.6420 (1.0)         28.5782 (1.0)        0.9508 (1.23)          9;0  34.8437 (1.0)          34           1
test_gufo_http_sync         31.3744 (1.14)        36.4130 (1.20)        32.9570 (1.15)      1.3197 (2.06)        32.5026 (1.14)       1.2681 (1.64)          6;3  30.3426 (0.87)         28           1
test_aiohttp_async          63.8585 (2.32)        66.9743 (2.21)        65.5050 (2.28)      0.9388 (1.46)        65.4824 (2.29)       0.9370 (1.21)          3;0  15.2660 (0.44)         10           1
test_gufo_http_async        64.1737 (2.33)        67.4971 (2.23)        65.7372 (2.29)      1.0170 (1.58)        65.6995 (2.30)       1.2399 (1.61)          5;0  15.2121 (0.44)         15           1
test_httpx_sync             91.8231 (3.33)        94.9401 (3.13)        93.3547 (3.25)      0.9826 (1.53)        93.3101 (3.27)       1.6283 (2.11)          4;0  10.7118 (0.31)         11           1
test_aiosonic_async        106.2416 (3.86)       116.4554 (3.84)       108.6888 (3.79)      3.3076 (5.15)       107.4159 (3.76)       2.4509 (3.17)          2;1   9.2006 (0.26)         10           1
test_urllib3_sync          118.7272 (4.31)       123.1409 (4.06)       120.3286 (4.19)      1.5320 (2.39)       120.2105 (4.21)       2.1491 (2.78)          3;0   8.3106 (0.24)          9           1
test_httpx_async           143.8137 (5.22)       151.3308 (5.00)       146.5398 (5.11)      2.6129 (4.07)       146.2607 (5.12)       3.4013 (4.40)          2;0   6.8241 (0.20)          7           1
test_niquests_sync         169.8794 (6.17)       172.0863 (5.68)       171.1388 (5.96)      0.7578 (1.18)       171.3233 (5.99)       0.7722 (1.0)           2;0   5.8432 (0.17)          6           1
test_urllib_sync         1,139.7685 (41.37)    1,147.2830 (37.87)    1,143.7662 (39.85)     2.9161 (4.54)     1,143.2564 (40.00)      4.2299 (5.48)          2;0   0.8743 (0.03)          5           1
test_requests_sync       5,508.6240 (199.93)   5,639.1937 (186.14)   5,584.9020 (194.60)   60.9650 (94.96)    5,619.8474 (196.65)   106.0952 (137.39)        1;0   0.1791 (0.01)          5           1
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
==================================================== 11 passed, 1215 warnings in 62.47s (0:01:02) =====================================================
```

![Median chart](https_linear_x100_1k.png)
*Lower is better*

### 100 Parralel Requests
Perform 100 HTTPS requests to read 1kb text file with concurrency of 4 maintaininng
single client session per thread/coroutine.

* The efficiency of the network code.
* The efficency of the HTTP/1.1 parser.
* An ability to maintain connection pools.
* Granularity of the internal locks.
* Ability to release GIL when runnning native code.

Run tests:
```
pytest benchmarks/test_https_p4_x100_1k.py
```

**Results (lower is better)**
```
================================================================= test session starts =================================================================
platform linux -- Python 3.11.2, pytest-7.4.3, pluggy-1.4.0
benchmark: 4.0.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /home/admin/bench/gufo_http
plugins: anyio-4.3.0, benchmark-4.0.0
collected 11 items                                                                                                                                    

benchmarks/test_https_p4_x100_1k.py ...........                                                                                                 [100%]


---------------------------------------------------------------------------------------- benchmark: 11 tests -----------------------------------------------------------------------------------------
Name (time in ms)               Min                   Max                  Mean             StdDev                Median                IQR            Outliers      OPS            Rounds  Iterations
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_gufo_http_sync         21.1360 (1.0)         29.4575 (1.0)         25.4910 (1.02)      2.3480 (1.19)        25.9351 (1.04)      3.3171 (1.72)         16;0  39.2295 (0.98)         40           1
test_pycurl_sync            21.3382 (1.01)        30.6251 (1.04)        25.0360 (1.0)       1.9783 (1.0)         25.0387 (1.0)       2.2491 (1.17)         11;1  39.9424 (1.0)          34           1
test_gufo_http_async        46.4599 (2.20)        73.1334 (2.48)        56.4327 (2.25)      8.6226 (4.36)        54.3729 (2.17)      1.9234 (1.0)           8;8  17.7202 (0.44)         18           1
test_aiohttp_async          68.1954 (3.23)        75.2719 (2.56)        72.5235 (2.90)      2.8257 (1.43)        73.5960 (2.94)      5.2576 (2.73)          3;0  13.7886 (0.35)          9           1
test_httpx_sync            101.0239 (4.78)       125.3279 (4.25)       104.9345 (4.19)      7.2883 (3.68)       102.2178 (4.08)      2.3788 (1.24)          1;1   9.5298 (0.24)         10           1
test_httpx_async           156.7438 (7.42)       172.7126 (5.86)       168.6394 (6.74)      6.0067 (3.04)       170.6249 (6.81)      2.8955 (1.51)          1;1   5.9298 (0.15)          6           1
test_urllib3_sync          191.3591 (9.05)       218.9681 (7.43)       204.5412 (8.17)     11.2807 (5.70)       202.2406 (8.08)     20.2861 (10.55)         3;0   4.8890 (0.12)          6           1
test_aiosonic_async        219.9907 (10.41)      245.8470 (8.35)       236.3696 (9.44)      9.6836 (4.89)       238.3812 (9.52)      7.5230 (3.91)          1;1   4.2307 (0.11)          5           1
test_niquests_sync         260.7054 (12.33)      287.2331 (9.75)       275.4114 (11.00)    12.1043 (6.12)       282.2942 (11.27)    20.6499 (10.74)         1;0   3.6309 (0.09)          5           1
test_urllib_sync           361.2022 (17.09)      402.9708 (13.68)      389.2026 (15.55)    18.0500 (9.12)       399.6454 (15.96)    25.9360 (13.48)         1;0   2.5694 (0.06)          5           1
test_requests_sync       3,065.0650 (145.02)   3,245.8865 (110.19)   3,151.5214 (125.88)   68.7689 (34.76)    3,154.8421 (126.00)   97.8452 (50.87)         2;0   0.3173 (0.01)          5           1
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
========================================================= 11 passed, 1131 warnings in 41.18s ==========================================================
```

![Median chart](https_p4_x100_1k.png)
*Lower is better*

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
[urllib3]: https://urllib3.readthedocs.io/en/stable/
[discussion]: https://github.com/gufolabs/gufo_http/discussions/2