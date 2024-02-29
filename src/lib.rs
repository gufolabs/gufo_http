// ------------------------------------------------------------------------
// Gufo HTTP: Module definition
// ------------------------------------------------------------------------
// Copyright (C) 2024, Gufo Labs
// See LICENSE.md for details
// ------------------------------------------------------------------------

use pyo3::prelude::*;
mod async_client;
mod error;
mod headers;
mod method;

/// Module index
#[pymodule]
#[pyo3(name = "_fast")]
fn gufo_http(py: Python, m: &PyModule) -> PyResult<()> {
    m.add("HttpError", py.get_type::<error::PyHttpError>())?;
    // Request methods
    m.add("GET", method::GET)?;
    m.add("HEAD", method::HEAD)?;
    m.add("OPTIONS", method::OPTIONS)?;
    m.add("DELETE", method::DELETE)?;
    // Compression methods
    m.add("DEFLATE", method::DEFLATE)?;
    m.add("GZIP", method::GZIP)?;
    m.add("BROTLI", method::BROTLI)?;
    m.add_class::<headers::Headers>()?;
    m.add_class::<async_client::AsyncResponse>()?;
    m.add_class::<async_client::AsyncClient>()?;
    Ok(())
}
