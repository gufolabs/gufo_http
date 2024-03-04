// ------------------------------------------------------------------------
// Gufo HTTP: SyncResponse impmentation
// ------------------------------------------------------------------------
// Copyright (C) 2024, Gufo Labs
// See LICENSE.md for details
// ------------------------------------------------------------------------
use crate::error::HttpError;
use crate::headers::Headers;
use pyo3::{prelude::*, types::PyBytes};
use std::cell::RefCell;

#[pyclass(module = "gufo.http.sync_client")]
pub struct SyncResponse {
    #[pyo3(get)]
    status: u16,
    response: RefCell<Option<reqwest::blocking::Response>>,
    headers: Headers,
}

impl SyncResponse {
    pub fn new(response: reqwest::blocking::Response) -> Self {
        let headers = Headers::new(response.headers().clone());
        SyncResponse {
            status: response.status().into(),
            response: RefCell::new(Some(response)),
            headers,
        }
    }
}

#[pymethods]
impl SyncResponse {
    #[getter]
    fn headers(&self) -> PyResult<Headers> {
        Ok(self.headers.clone())
    }
    fn read(&self, py: Python) -> PyResult<PyObject> {
        match self
            .response
            .try_borrow_mut()
            .map_err(|_| HttpError::Request("cannot borrow".into()))?
            .take()
        {
            Some(response) => {
                let buf = response.bytes().map_err(HttpError::from)?;
                Ok(PyBytes::new(py, buf.as_ref()).into())
            }
            None => Err(HttpError::AlreadyRead.into()),
        }
    }
}
