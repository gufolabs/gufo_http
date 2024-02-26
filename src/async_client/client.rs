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
use reqwest::{redirect::Policy, RequestBuilder};

#[pyclass(module = "gufo.http.async_client")]
pub struct AsyncClient {
    client: reqwest::Client,
}

#[pymethods]
impl AsyncClient {
    #[new]
    fn new(max_redirect: Option<usize>) -> PyResult<Self> {
        let builder = reqwest::Client::builder();
        let client = builder
            .redirect(match max_redirect {
                Some(x) => Policy::limited(x),
                None => Policy::none(),
            })
            .build()
            .map_err(|x| PyValueError::new_err(x.to_string()))?;
        Ok(AsyncClient { client })
    }
    fn get<'a>(&self, py: Python<'a>, url: String) -> PyResult<&'a PyAny> {
        self.process_request(py, self.client.get(url))
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
