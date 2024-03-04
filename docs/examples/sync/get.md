# Gufo HTTP Example: Get Request

`Get` is one of the basic HTTP operations allowing to download
single page.

``` py title="get.py" linenums="1"
--8<-- "examples/sync/get.py"
```

Let's see the details.

``` py title="get.py" linenums="1" hl_lines="1"
--8<-- "examples/sync/get.py"
```
Import `sys` module to parse the CLI argument.

!!! warning

    We use `sys.argv` only for demonstration purposes. Use `argsparse` or alternatives
    in real-world applications.

``` py title="get.py" linenums="1" hl_lines="3"
--8<-- "examples/sync/get.py"
```

`HttpClient` object holds all necessary API. We're using a synchronous
version from `gufo.http.sync_client`.

``` py title="get.py" linenums="1" hl_lines="6"
--8<-- "examples/sync/get.py"
```

We define our main function and expect resource URL.

``` py title="get.py" linenums="1" hl_lines="7"
--8<-- "examples/sync/get.py"
```

First, we need to create `HttpClient` object which wraps the client's session.
The `HttpClient` may be used as an instance directly or operated as context manager
using the `with` clause. When used as a context manager,
the client automatically closes all connections on the exit of context,
so its lifetime is defined explicitly.

`HttpClient` constructor offers lots of configuration variables for fine-tuning. Refer to the 
[HttpClient reference][gufo.http.sync_client.HttpClient]
for further details. In our example we use default settings.

``` py title="get.py" linenums="1" hl_lines="8"
--8<-- "examples/sync/get.py"
```
`.get()` method starts a HTTP GET request and await for response headers.
It assepts an url as mandatary argument and returns a `SyncResponse` instance.

``` py title="get.py" linenums="1" hl_lines="9"
--8<-- "examples/sync/get.py"
```
We can inspect response code and headers without reading whole response body.
For our example we just check the status code is 200 OK.

``` py title="get.py" linenums="1" hl_lines="10 11"
--8<-- "examples/sync/get.py"
```
If status code is not OK, we print and error message and terminate our function.

``` py title="get.py" linenums="1" hl_lines="12"
--8<-- "examples/sync/get.py"
```
`.read()` method waits and returns a whole response body.
``` py title="get.py" linenums="1" hl_lines="13"
--8<-- "examples/sync/get.py"
```
Here we print our response body. Note, `.read()` returns a `bytes` type,
so we convert it into `str` using `.decode()` method. In our example
we consider the response is encoding using UTF-8 encoding.

``` py title="get.py" linenums="1" hl_lines="16"
--8<-- "examples/sync/get.py"
```
Lets run our `main()` function pass first command-line parameter as url.

## Running

Let's check our script. Run example as:

```
$ python3 examples/sync/get.py https://gufolabs.com/
<!DOCTYPE html>
<html>
...
```