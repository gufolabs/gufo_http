// ------------------------------------------------------------------------
// Gufo HTTP: Proxy classes
// ------------------------------------------------------------------------
// Copyright (C) 2024, Gufo Labs
// See LICENSE.md for details
// ------------------------------------------------------------------------
use pyo3::{exceptions::PyValueError, prelude::*};

#[derive(Clone)]
#[pyclass]
pub struct Proxy(reqwest::Proxy);

#[pymethods]
impl Proxy {
    #[new]
    fn new(url: &str) -> PyResult<Self> {
        // check schemes. reqwest doesn't do it
        if !url.starts_with("http://") && !url.starts_with("https://") {
            return Err(PyValueError::new_err("invalid scheme"));
        }
        // Create proxy
        let proxy = reqwest::Proxy::all(url).map_err(|x| PyValueError::new_err(x.to_string()))?;
        Ok(Self(proxy))
    }
}

impl From<Proxy> for reqwest::Proxy {
    fn from(value: Proxy) -> Self {
        value.0
    }
}
