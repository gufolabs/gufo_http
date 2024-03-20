# ---------------------------------------------------------------------
# Gufo HTTP: async HttpClient tests
# ---------------------------------------------------------------------
# Copyright (C) 2024, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------

# Python modules
from collections.abc import Iterable
from typing import ClassVar, Dict, Optional, Type

# Third-party modules
import pytest

# Gufo HTTP Modules
from gufo.http import (
    GZIP,
    AuthBase,
    BasicAuth,
    BearerAuth,
    HttpError,
    RedirectError,
    RequestError,
    RequestMethod,
)
from gufo.http.httpd import Httpd
from gufo.http.sync_client import HttpClient

from .util import UNROUTABLE_PROXY, UNROUTABLE_URL, with_env


def test_get(httpd: Httpd) -> None:
    client = HttpClient()
    resp = client.get(f"{httpd.prefix}/")
    assert resp.status == 200
    data = resp.content
    assert data
    assert b"</html>" in data


def test_head(httpd: Httpd) -> None:
    client = HttpClient()
    resp = client.head(f"{httpd.prefix}/")
    assert resp.status == 200
    data = resp.content
    assert data == b""


def test_options(httpd: Httpd) -> None:
    with HttpClient() as client:
        resp = client.options(f"{httpd.prefix}/options")
        assert resp.status == 204
        allow = resp.headers["Allow"]
        for m in (b"OPTIONS", b"GET", b"HEAD"):
            assert m in allow


def test_delete(httpd: Httpd) -> None:
    with HttpClient() as client:
        resp = client.delete(f"{httpd.prefix}/delete")
        assert resp.status == 200
        data = resp.content
        assert data == b"OK"


def test_post(httpd: Httpd) -> None:
    with HttpClient() as client:
        resp = client.post(f"{httpd.prefix}/post", b"TEST")
        assert resp.status == 200
        data = resp.content
        assert data == b"OK"


def test_put(httpd: Httpd) -> None:
    with HttpClient() as client:
        resp = client.put(f"{httpd.prefix}/put", b"TEST")
        assert resp.status == 200
        data = resp.content
        assert data == b"OK"


def test_patch(httpd: Httpd) -> None:
    with HttpClient() as client:
        resp = client.patch(f"{httpd.prefix}/patch", b"TEST")
        assert resp.status == 200
        data = resp.content
        assert data == b"OK"


@pytest.mark.parametrize(
    ("method", "path", "body"),
    [
        (RequestMethod.GET, "/", None),
        (RequestMethod.HEAD, "/", None),
        (RequestMethod.OPTIONS, "/options", None),
        (RequestMethod.DELETE, "/delete", None),
        (RequestMethod.POST, "/post", b"TEST"),
        (RequestMethod.PUT, "/put", b"TEST"),
        (RequestMethod.PATCH, "/patch", b"TEST"),
    ],
)
def test_request(
    method: RequestMethod, path: str, body: Optional[bytes], httpd: Httpd
) -> None:
    with HttpClient() as client:
        resp = client.request(method, f"{httpd.prefix}{path}", body=body)
        assert 200 <= resp.status <= 299


@pytest.mark.parametrize(
    ("method", "path", "body"),
    [
        ("GET", "/", None),
        ("HEAD", "/", None),
        ("OPTIONS", "/options", None),
        ("DELETE", "/delete", None),
        ("POST", "/post", b"TEST"),
        ("PUT", "/put", b"TEST"),
        ("PATCH", "/patch", b"TEST"),
    ],
)
def test_request_by_str(
    method: str, path: str, body: Optional[bytes], httpd: Httpd
) -> None:
    with HttpClient() as client:
        resp = client.request(
            RequestMethod.get(method), f"{httpd.prefix}{path}", body=body
        )
        assert 200 <= resp.status <= 299


def test_not_found(httpd: Httpd) -> None:
    with HttpClient() as client:
        resp = client.get(f"{httpd.prefix}/not_found")
        assert resp.status == 404


@pytest.mark.parametrize(
    "url", ["ldap://127.0.0.1/", "http://700.700:202020/"]
)
def test_invalid_url(httpd: Httpd, url: str) -> None:
    with HttpClient() as client, pytest.raises(RequestError):
        client.get(url)


def test_no_proxy(httpd: Httpd) -> None:
    with with_env({"HTTP_PROXY": UNROUTABLE_PROXY}), HttpClient() as client:
        resp = client.get(f"{httpd.prefix}/")
        assert resp.status == 200
        data = resp.content
        assert data
        assert b"</html>" in data


@pytest.mark.parametrize(
    ("header", "expected"),
    [
        ("Content-Type", b"text/html"),
        ("content-type", b"text/html"),
    ],
)
def test_headers_getitem(header: str, expected: bytes, httpd: Httpd) -> None:
    client = HttpClient()
    resp = client.get(f"{httpd.prefix}/")
    h = resp.headers[header]
    assert h == expected


def test_headers_getitem_key_error(httpd: Httpd) -> None:
    client = HttpClient()
    resp = client.get(f"{httpd.prefix}/")
    with pytest.raises(KeyError):
        resp.headers["ctype"]


@pytest.mark.parametrize(
    ("header", "expected"),
    [
        ("Content-Type", b"text/html"),
        ("content-type", b"text/html"),
        ("ctype", None),
    ],
)
def test_headers_get(
    header: str, expected: Optional[bytes], httpd: Httpd
) -> None:
    client = HttpClient()
    resp = client.get(f"{httpd.prefix}/")
    h = resp.headers.get(header)
    assert h == expected


def test_headers_get_default(httpd: Httpd) -> None:
    client = HttpClient()
    resp = client.get(f"{httpd.prefix}/")
    default = b"default/value"
    h = resp.headers.get("ctype", default)
    assert h == default
    # assert h is default


@pytest.mark.parametrize(
    ("header", "expected"),
    [
        ("Content-Type", True),
        ("content-type", True),
        ("ctype", False),
    ],
)
def test_headers_in(header: str, expected: bool, httpd: Httpd) -> None:
    client = HttpClient()
    resp = client.get(f"{httpd.prefix}/")
    r = header in resp.headers
    assert r is expected


def test_headers_keys(httpd: Httpd) -> None:
    client = HttpClient()
    resp = client.get(f"{httpd.prefix}/")
    keys = resp.headers.keys()
    assert isinstance(keys, Iterable)
    k = list(keys)
    assert len(k) > 0
    assert "content-type" in k
    assert "server" in k
    assert isinstance(k[0], str)


def test_headers_values(httpd: Httpd) -> None:
    client = HttpClient()
    resp = client.get(f"{httpd.prefix}/")
    values = resp.headers.values()
    assert isinstance(values, Iterable)
    k = list(values)
    assert len(k) > 0
    assert isinstance(k[0], bytes)
    has_nginx = False
    has_html = False
    for v in k:
        if b"nginx" in v:
            has_nginx = True
        elif b"text/html" in v:
            has_html = True
    assert has_nginx
    assert has_html


def test_headers_items(httpd: Httpd) -> None:
    client = HttpClient()
    resp = client.get(f"{httpd.prefix}/")
    items = resp.headers.items()
    assert isinstance(items, Iterable)
    k = list(items)
    assert len(k) > 0
    assert isinstance(k[0], tuple)
    assert len(k[0]) == 2
    assert isinstance(k[0][0], str)
    assert isinstance(k[0][1], bytes)
    data = dict(resp.headers.items())
    assert "content-type" in data
    assert b"text/html" in data["content-type"]


def test_redirect_to_root(httpd: Httpd) -> None:
    with HttpClient() as client:
        resp = client.get(f"{httpd.prefix}/redirect/root")
        assert resp.status == 200
        data = resp.content
        assert data
        assert b"</html>" in data


def test_no_redirect_to_root(httpd: Httpd) -> None:
    with HttpClient(max_redirects=None) as client:
        resp = client.get(f"{httpd.prefix}/redirect/root")
        assert resp.status == 302


def test_redirects_forbidden(httpd: Httpd) -> None:
    with HttpClient(max_redirects=0) as client, pytest.raises(RedirectError):
        client.get(f"{httpd.prefix}/redirect/root")


@pytest.mark.parametrize("x", [HttpError, RedirectError])
def test_redirect_to_loop(httpd: Httpd, x: Type[BaseException]) -> None:
    with HttpClient() as client, pytest.raises(x):
        client.get(f"{httpd.prefix}/redirect/loop")


def test_get_header(httpd: Httpd) -> None:
    client = HttpClient()
    resp = client.get(f"{httpd.prefix}/headers/get")
    assert resp.status == 200
    assert resp.headers["X-Gufo-HTTP"] == b"TEST"
    data = resp.content
    assert data
    assert data == b'{"status":true}'


def test_get_without_header(httpd: Httpd) -> None:
    client = HttpClient()
    resp = client.get(f"{httpd.prefix}/headers/check")
    assert resp.status == 403
    data = resp.content
    assert data
    assert data == b'{"status":false}'


class MyHttpClient(HttpClient):
    headers: ClassVar[Dict[str, bytes]] = {"X-Gufo-HTTP": b"TEST"}


def test_get_with_header_class(httpd: Httpd) -> None:
    with MyHttpClient() as client:
        resp = client.get(f"{httpd.prefix}/headers/check")
        assert resp.status == 200
        data = resp.content
        assert data
        assert data == b'{"status":true}'


def test_get_with_header_client(httpd: Httpd) -> None:
    with HttpClient(headers={"X-Gufo-HTTP": b"TEST"}) as client:
        resp = client.get(f"{httpd.prefix}/headers/check")
        assert resp.status == 200
        data = resp.content
        assert data
        assert data == b'{"status":true}'


def test_get_with_header_request(httpd: Httpd) -> None:
    with HttpClient() as client:
        resp = client.get(
            f"{httpd.prefix}/headers/check", headers={"X-Gufo-HTTP": b"TEST"}
        )
        assert resp.status == 200
        data = resp.content
        assert data
        assert data == b'{"status":true}'


@pytest.mark.parametrize("compression", [None, GZIP])
def test_compression(httpd: Httpd, compression: Optional[int]) -> None:
    with HttpClient(compression=compression) as client:
        resp = client.get(f"{httpd.prefix}/")
        assert resp.status == 200
        data = resp.content
        assert data
        assert b"</html>" in data


def test_connect_timeout(httpd: Httpd) -> None:
    with (
        HttpClient(connect_timeout=1.0) as client,
        pytest.raises(ConnectionError),
    ):
        client.get(UNROUTABLE_URL)


def test_default_user_agent(httpd: Httpd) -> None:
    with HttpClient() as client:
        resp = client.get(f"{httpd.prefix}/ua/default")
        assert resp.status == 200


def test_set_user_agent(httpd: Httpd) -> None:
    with HttpClient(user_agent="Mozilla like gecko") as client:
        resp = client.get(f"{httpd.prefix}/ua/custom")
        assert resp.status == 200


def test_auth_invalid_class(httpd: Httpd) -> None:
    with pytest.raises(TypeError), HttpClient(auth={}):
        pass


@pytest.mark.parametrize("path", ["/auth/basic", "/auth/bearer"])
def test_auth_basic_fail(httpd: Httpd, path: str) -> None:
    with HttpClient() as client:
        resp = client.get(f"{httpd.prefix}{path}")
        assert resp.status == 401


@pytest.mark.parametrize(
    ("path", "auth", "expected"),
    [
        ("/auth/basic", BasicAuth("scott", "tiger"), 200),
        ("/auth/basic", BasicAuth("scott", "tiger1"), 401),
        ("/auth/bearer", BearerAuth("123456"), 200),
        ("/auth/bearer", BearerAuth("1234567"), 401),
    ],
)
def test_auth(httpd: Httpd, path: str, auth: AuthBase, expected: int) -> None:
    with HttpClient(auth=auth) as client:
        resp = client.get(f"{httpd.prefix}{path}")
        assert resp.status == expected


def test_tls_cert_check_fail(httpd_tls: Httpd) -> None:
    with HttpClient() as client, pytest.raises(ConnectionError):
        client.get(f"{httpd_tls.prefix}/")


def test_tls_get(httpd_tls: Httpd) -> None:
    with HttpClient(validate_cert=False) as client:
        resp = client.get(f"{httpd_tls.prefix}/")
        assert resp.status == 200
        data = resp.content
        assert data
        assert b"</html>" in data
