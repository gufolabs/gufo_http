// ------------------------------------------------------------------------
// Gufo HTTP: AsyncClient implementation
// ------------------------------------------------------------------------
// Copyright (C) 2024, Gufo Labs
// See LICENSE.md for details
// ------------------------------------------------------------------------
use crate::auth::{AuthMethod, BasicAuth, BearerAuth, GetAuthMethod};
use crate::error::{GufoHttpError, HttpResult};
use crate::headers::Headers;
use crate::method::{RequestMethod, BROTLI, DEFLATE, GZIP, ZSTD};
use crate::proxy::Proxy;
use crate::response::Response;
use pyo3::{
    exceptions::{PyTypeError, PyValueError},
    prelude::*,
    types::PyBytes,
};
use pyo3_asyncio::tokio::future_into_py;
use reqwest::{
    header::{HeaderMap, HeaderName, HeaderValue},
    redirect::Policy,
};
use std::collections::HashMap;
use std::time::Duration;

#[pyclass(module = "gufo.http.async_client")]
pub struct AsyncClient {
    client: reqwest::Client,
    auth: AuthMethod,
}

#[pymethods]
impl AsyncClient {
    #[allow(clippy::too_many_arguments)]
    #[new]
    fn new(
        validate_cert: bool,
        connect_timeout: u64,
        timeout: u64,
        max_redirect: Option<usize>,
        headers: Option<HashMap<&str, &[u8]>>,
        compression: Option<u8>,
        user_agent: Option<&str>,
        auth: Option<&PyAny>,
        proxy: Option<Vec<&PyAny>>,
    ) -> PyResult<Self> {
        let builder = reqwest::Client::builder();
        // Set up redirect policy
        let mut builder = builder.redirect(match max_redirect {
            Some(x) => Policy::limited(x),
            None => Policy::none(),
        });
        // Set headers
        if let Some(h) = headers {
            let mut map = HeaderMap::with_capacity(h.len());
            for (k, v) in h {
                map.insert(
                    HeaderName::from_bytes(k.as_ref())
                        .map_err(|e| PyValueError::new_err(e.to_string()))?,
                    HeaderValue::from_bytes(v).map_err(|e| PyValueError::new_err(e.to_string()))?,
                );
            }
            builder = builder.default_headers(map);
        }
        // Set compression
        if let Some(c) = compression {
            if c | DEFLATE == DEFLATE {
                builder = builder.deflate(true);
            }
            if c | GZIP == GZIP {
                builder = builder.gzip(true);
            }
            if c | BROTLI == BROTLI {
                builder = builder.brotli(true);
            }
            if c | ZSTD == ZSTD {
                builder = builder.zstd(true);
            }
        }
        // Set up certificate validation
        if !validate_cert {
            builder = builder.danger_accept_invalid_certs(true);
        }
        // Set timeouts
        builder = builder
            .connect_timeout(Duration::from_nanos(connect_timeout))
            .timeout(Duration::from_nanos(timeout));
        // Disable proxies
        builder = builder.no_proxy();
        // Set user agent
        if let Some(ua) = user_agent {
            builder = builder.user_agent(ua);
        }
        // Auth
        let auth = match auth {
            Some(auth) => {
                if let Ok(basic_auth) = auth.extract::<BasicAuth>() {
                    basic_auth.get_method()
                } else if let Ok(bearer_auth) = auth.extract::<BearerAuth>() {
                    bearer_auth.get_method()
                } else {
                    return Err(PyTypeError::new_err(
                        "auth must be an instance of subclass of AuthBase",
                    ));
                }
            }
            None => AuthMethod::None,
        };
        // Proxy
        if let Some(proxy) = proxy {
            for p in proxy {
                match p.extract::<Proxy>() {
                    Ok(p) => {
                        builder = builder.proxy(p.into());
                    }
                    Err(_) => {
                        return Err(PyTypeError::new_err("proxy must contain Proxy instances"))
                    }
                }
            }
        }
        // Build client
        let client = builder
            .build()
            .map_err(|x| PyValueError::new_err(x.to_string()))?;
        Ok(AsyncClient { client, auth })
    }
    fn request<'a>(
        &self,
        py: Python<'a>,
        method: &RequestMethod,
        url: String,
        headers: Option<HashMap<&str, &[u8]>>,
        body: Option<Vec<u8>>,
    ) -> PyResult<&'a PyAny> {
        // Get method
        let req = py.allow_threads(|| -> HttpResult<reqwest::RequestBuilder> {
            // Build request for method
            let mut req = self.client.request((*method).into(), url);
            // Add headers
            if let Some(h) = headers {
                for (k, v) in h {
                    req = req.header(
                        HeaderName::from_bytes(k.as_ref())
                            .map_err(|e| GufoHttpError::ValueError(e.to_string()))?,
                        HeaderValue::from_bytes(v)
                            .map_err(|e| GufoHttpError::ValueError(e.to_string()))?,
                    )
                }
            }
            // Add auth
            match &self.auth {
                AuthMethod::None => {}
                AuthMethod::Basic { user, password } => {
                    req = req.basic_auth(user, password.as_ref())
                }
                AuthMethod::Bearer { token } => req = req.bearer_auth(token),
            }
            // Add body
            if let Some(b) = body {
                req = req.body(b);
            }
            Ok(req)
        })?;
        // Create future
        future_into_py(py, async move {
            // Send request and wait for response
            let resp = req.send().await.map_err(GufoHttpError::from)?;
            // Get status
            let status: u16 = resp.status().into();
            // Wrap headers
            let headers = Headers::new(resp.headers().clone());
            // Read body
            let buf = resp.bytes().await.map_err(GufoHttpError::from)?;
            // Return response
            Ok(Response::new(
                status,
                headers,
                Python::with_gil(|py| PyBytes::new(py, buf.as_ref()).into()),
            ))
        })
    }
}
