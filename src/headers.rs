// ------------------------------------------------------------------------
// Gufo HTTP: Headers impmentation
// ------------------------------------------------------------------------
// Copyright (C) 2024, Gufo Labs
// See LICENSE.md for details
// ------------------------------------------------------------------------
use pyo3::{exceptions::PyKeyError, prelude::*};
use reqwest::header::HeaderMap;

#[derive(Clone)]
#[pyclass]
pub struct Headers(HeaderMap);

impl Headers {
    pub fn new(headers: HeaderMap) -> Self {
        Self(headers)
    }
}

#[pymethods]
impl Headers {
    fn __getitem__<'a>(&'a self, key: &str) -> PyResult<&'a [u8]> {
        match self.0.get(key) {
            Some(x) => Ok(x.as_ref()),
            None => Err(PyKeyError::new_err(key.to_owned())),
        }
    }
    fn get<'a>(&'a self, key: &str, default: Option<&'a [u8]>) -> PyResult<Option<&'a [u8]>> {
        match self.0.get(key) {
            Some(x) => Ok(Some(x.as_ref())),
            None => match default {
                Some(d) => Ok(Some(d)),
                None => Ok(None),
            },
        }
    }
}
