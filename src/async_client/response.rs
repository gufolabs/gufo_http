// ------------------------------------------------------------------------
// Gufo HTTP: AsyncResponse impmentation
// ------------------------------------------------------------------------
// Copyright (C) 2024, Gufo Labs
// See LICENSE.md for details
// ------------------------------------------------------------------------
use crate::headers::Headers;
use pyo3::{exceptions::PyRuntimeError, prelude::*, types::PyBytes, ToPyObject};
use pyo3_asyncio::tokio::future_into_py;
use std::cell::RefCell;

#[pyclass(module = "gufo.http.async_client")]
pub struct AsyncResponse {
    #[pyo3(get)]
    status: u16,
    response: RefCell<Option<reqwest::Response>>,
    headers: Headers,
}

impl AsyncResponse {
    pub fn new(response: reqwest::Response) -> Self {
        let headers = Headers::new(response.headers().clone());
        AsyncResponse {
            status: response.status().into(),
            response: RefCell::new(Some(response)),
            headers,
        }
    }
}

#[pymethods]
impl AsyncResponse {
    #[getter]
    fn headers(&self) -> PyResult<Headers> {
        Ok(self.headers.clone())
    }
    fn read<'a>(&'a self, py: Python<'a>) -> PyResult<&'a PyAny> {
        match self
            .response
            .try_borrow_mut()
            .map_err(|e| PyRuntimeError::new_err(e.to_string()))?
            .take()
        {
            Some(response) => future_into_py(py, async move {
                let buf = response
                    .bytes()
                    .await
                    .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;
                Python::with_gil(|py| Ok(PyBytes::new(py, buf.as_ref()).to_object(py)))
            }),
            None => Err(PyRuntimeError::new_err("Already read")),
        }
    }
}
