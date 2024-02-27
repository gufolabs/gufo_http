// ------------------------------------------------------------------------
// Gufo HTTP: AsyncClient implementation
// ------------------------------------------------------------------------
// Copyright (C) 2024, Gufo Labs
// See LICENSE.md for details
// ------------------------------------------------------------------------
use super::response::AsyncResponse;
use pyo3::{
    exceptions::{PyRuntimeError, PyValueError},
    prelude::*,
};
use pyo3_asyncio::tokio::future_into_py;
use reqwest::{
    header::{HeaderMap, HeaderName, HeaderValue},
    redirect::Policy,
    RequestBuilder,
};
use std::collections::HashMap;

#[pyclass(module = "gufo.http.async_client")]
pub struct AsyncClient {
    client: reqwest::Client,
}

#[pymethods]
impl AsyncClient {
    #[new]
    fn new(max_redirect: Option<usize>, headers: Option<HashMap<&str, &[u8]>>) -> PyResult<Self> {
        let builder = reqwest::Client::builder();
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
        //
        let client = builder
            .build()
            .map_err(|x| PyValueError::new_err(x.to_string()))?;
        Ok(AsyncClient { client })
    }
    fn get<'a>(
        &self,
        py: Python<'a>,
        url: String,
        headers: Option<HashMap<&str, &[u8]>>,
    ) -> PyResult<&'a PyAny> {
        let mut builder = self.client.get(url);
        if let Some(h) = headers {
            for (k, v) in h {
                builder = builder.header(
                    HeaderName::from_bytes(k.as_ref())
                        .map_err(|e| PyValueError::new_err(e.to_string()))?,
                    HeaderValue::from_bytes(v).map_err(|e| PyValueError::new_err(e.to_string()))?,
                )
            }
        }
        self.process_request(py, builder)
    }
}

impl AsyncClient {
    fn process_request<'a>(&self, py: Python<'a>, req: RequestBuilder) -> PyResult<&'a PyAny> {
        future_into_py(py, async move {
            // Send request and wait for response
            let response = req
                .send()
                .await
                .map_err(|x| PyRuntimeError::new_err(x.to_string()))?;
            Python::with_gil(|py| Py::new(py, AsyncResponse::new(response)))
        })
    }
}
