// ------------------------------------------------------------------------
// Gufo HTTP=>Some(HTTP Methods
// ------------------------------------------------------------------------
// Copyright (C) 2024, Gufo Labs
// See LICENSE.md for details
// ------------------------------------------------------------------------

use pyo3::{exceptions::PyKeyError, prelude::*};
use reqwest::Method;

// Request methods
#[allow(clippy::upper_case_acronyms)]
#[pyclass(module = "gufo.http", eq)]
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum RequestMethod {
    GET,
    HEAD,
    OPTIONS,
    DELETE,
    POST,
    PUT,
    PATCH,
}

// Compression methods
pub const DEFLATE: u8 = 1;
pub const GZIP: u8 = 1 << 1;
pub const BROTLI: u8 = 1 << 2;
pub const ZSTD: u8 = 1 << 3;

// All request methods
static METHODS: [Method; 7] = [
    Method::GET,
    Method::HEAD,
    Method::OPTIONS,
    Method::DELETE,
    Method::POST,
    Method::PUT,
    Method::PATCH,
];

impl From<RequestMethod> for Method {
    fn from(val: RequestMethod) -> Self {
        METHODS[val as usize].clone()
    }
}

#[pymethods]
impl RequestMethod {
    // __getitem__ for enum is not implemented. Not working
    // See issue: https://github.com/PyO3/pyo3/issues/2887
    pub fn __getitem__(&self, name: &str) -> PyResult<Self> {
        match name {
            "GET" => Ok(RequestMethod::GET),
            "HEAD" => Ok(RequestMethod::HEAD),
            "OPTIONS" => Ok(RequestMethod::OPTIONS),
            "DELETE" => Ok(RequestMethod::DELETE),
            "POST" => Ok(RequestMethod::POST),
            "PUT" => Ok(RequestMethod::PUT),
            "PATCH" => Ok(RequestMethod::PATCH),
            _ => Err(PyKeyError::new_err(name.to_string())),
        }
    }
    #[staticmethod]
    pub fn get(name: &str) -> Option<Self> {
        match name {
            "GET" => Some(RequestMethod::GET),
            "HEAD" => Some(RequestMethod::HEAD),
            "OPTIONS" => Some(RequestMethod::OPTIONS),
            "DELETE" => Some(RequestMethod::DELETE),
            "POST" => Some(RequestMethod::POST),
            "PUT" => Some(RequestMethod::PUT),
            "PATCH" => Some(RequestMethod::PATCH),
            _ => None,
        }
    }
}
