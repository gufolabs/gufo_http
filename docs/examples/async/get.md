# Gufo HTTP Example: Get Request

`Get` is one of the basic HTTP operations allowing to download
single page. We have mastered how to process synchronous get
request in our [get.py](../sync/get.md) example. The asynchronous
implementation is only slightly more complicated.

``` py title="get.py" linenums="1"
--8<-- "examples/async/get.py"
```

Let's see the details.
``` py title="get.py" linenums="1" hl_lines="1"
--8<-- "examples/async/get.py"
```

To run async function from our synchronous script,
so we need to import `asyncio` to use `asyncio.run()`.

``` py title="get.py" linenums="1" hl_lines="2"
--8<-- "examples/async/get.py"
```
Import `sys` module to parse the CLI argument.

!!! warning

    We use `sys.argv` only for demonstration purposes. Use `argsparse` or alternatives
    in real-world applications.

``` py title="get.py" linenums="1" hl_lines="4"
--8<-- "examples/async/get.py"
```

`HttpClient` object holds all necessary API. We're using an asynchronous
version from `gufo.http.async_client`.

``` py title="get.py" linenums="1" hl_lines="7"
--8<-- "examples/async/get.py"
```

We define our asychronous main function and expect resource URL.

``` py title="get.py" linenums="1" hl_lines="8"
--8<-- "examples/async/get.py"
```

First, we need to create `HttpClient` object which wraps the client's session.
The `HttpClient` may be used as an instance directly or operated as asynchronous context manager
using the `async with` clause. When used as a context manager,
the client automatically closes all connections on the exit of context,
so its lifetime is defined explicitly.

`HttpClient` constructor offers lots of configuration variables for fine-tuning. Refer to the 
[HttpClient reference][gufo.http.async_client.HttpClient]
for further details. In our example we use default settings.

``` py title="get.py" linenums="1" hl_lines="9"
--8<-- "examples/async/get.py"
```
`.get()` method starts a HTTP GET request and await for response headers.
It assepts an url as mandatary argument and returns a `SyncResponse` instance.
The function is asyncronous and needs to be awaited.

``` py title="get.py" linenums="1" hl_lines="10"
--8<-- "examples/async/get.py"
```
We can inspect response code and headers without reading whole response body.
For our example we just check the status code is 200 OK.

``` py title="get.py" linenums="1" hl_lines="11 12"
--8<-- "examples/async/get.py"
```
If status code is not OK, we print and error message and terminate our function.

``` py title="get.py" linenums="1" hl_lines="13"
--8<-- "examples/async/get.py"
```
`.read()` method waits and returns a whole response body.
This is an asyncronous function which needs to be awaited.


``` py title="get.py" linenums="1" hl_lines="14"
--8<-- "examples/async/get.py"
```
Here we print our response body. Note, `.read()` returns a `bytes` type,
so we convert it into `str` using `.decode()` method. In our example
we consider the response is encoding using UTF-8 encoding.

``` py title="get.py" linenums="1" hl_lines="17"
--8<-- "examples/async/get.py"
```
Lets run our `main()` function pass first command-line parameter as url.

## Running

Let's check our script. Run example as:

```
$ python3 examples/async/get.py https://gufolabs.com/
<!DOCTYPE html>
<html>
...
```