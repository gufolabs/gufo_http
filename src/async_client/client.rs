// ------------------------------------------------------------------------
// Gufo HTTP: AsyncClient implementation
// ------------------------------------------------------------------------
// Copyright (C) 2024, Gufo Labs
// See LICENSE.md for details
// ------------------------------------------------------------------------
use super::response::AsyncResponse;
use crate::error::HttpError;
use crate::method::{BROTLI, DEFLATE, DELETE, GET, GZIP, HEAD, OPTIONS, PATCH, POST, PUT};
use pyo3::{exceptions::PyValueError, prelude::*};
use pyo3_asyncio::tokio::future_into_py;
use reqwest::{
    header::{HeaderMap, HeaderName, HeaderValue},
    redirect::Policy,
    Method,
};
use std::collections::HashMap;
use std::time::Duration;

#[pyclass(module = "gufo.http.async_client")]
pub struct AsyncClient {
    client: reqwest::Client,
}

#[pymethods]
impl AsyncClient {
    #[new]
    fn new(
        validate_cert: bool,
        connect_timeout: u64,
        timeout: u64,
        max_redirect: Option<usize>,
        headers: Option<HashMap<&str, &[u8]>>,
        compression: Option<u8>,
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
        // Build client
        let client = builder
            .build()
            .map_err(|x| PyValueError::new_err(x.to_string()))?;
        Ok(AsyncClient { client })
    }
    fn request<'a>(
        &self,
        py: Python<'a>,
        method: usize,
        url: String,
        headers: Option<HashMap<&str, &[u8]>>,
        body: Option<Vec<u8>>,
    ) -> PyResult<&'a PyAny> {
        // Get method
        let m = match method {
            GET => Method::GET,
            HEAD => Method::HEAD,
            OPTIONS => Method::OPTIONS,
            DELETE => Method::DELETE,
            POST => Method::POST,
            PUT => Method::PUT,
            PATCH => Method::PATCH,
            _ => return Err(PyValueError::new_err("invalid method")),
        };
        // Build request for method
        let mut req = self.client.request(m, url);
        // Add headers
        if let Some(h) = headers {
            for (k, v) in h {
                req = req.header(
                    HeaderName::from_bytes(k.as_ref())
                        .map_err(|e| PyValueError::new_err(e.to_string()))?,
                    HeaderValue::from_bytes(v).map_err(|e| PyValueError::new_err(e.to_string()))?,
                )
            }
        }
        // Add body
        if let Some(b) = body {
            req = req.body(b);
        }
        // Create future
        future_into_py(py, async move {
            // Send request and wait for response
            let response = req.send().await.map_err(HttpError::from)?;
            Python::with_gil(|py| Py::new(py, AsyncResponse::new(response)))
        })
    }
}
