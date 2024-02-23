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

/// Module index
#[pymodule]
#[pyo3(name = "_fast")]
fn gufo_http(py: Python, m: &PyModule) -> PyResult<()> {
    m.add("HttpError", py.get_type::<error::PyHttpError>())?;
    m.add_class::<headers::Headers>()?;
    m.add_class::<async_client::AsyncResponse>()?;
    m.add_class::<async_client::AsyncClient>()?;
    Ok(())
}
