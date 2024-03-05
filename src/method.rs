// ------------------------------------------------------------------------
// Gufo HTTP: HTTP Methods
// ------------------------------------------------------------------------
// Copyright (C) 2024, Gufo Labs
// See LICENSE.md for details
// ------------------------------------------------------------------------

use pyo3::{exceptions::PyValueError, prelude::*};
use reqwest::Method;

// Request methods
pub const GET: usize = 0;
pub const HEAD: usize = 1;
pub const OPTIONS: usize = 2;
pub const DELETE: usize = 3;
pub const POST: usize = 4;
pub const PUT: usize = 5;
pub const PATCH: usize = 6;

// Compression methods
pub const DEFLATE: u8 = 1;
pub const GZIP: u8 = 1 << 1;
pub const BROTLI: u8 = 1 << 2;

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

pub fn get_method(method: usize) -> Result<Method, PyErr> {
    METHODS
        .get(method)
        .ok_or_else(|| PyValueError::new_err("invalid method"))
        .cloned()
}
