// ------------------------------------------------------------------------
// Gufo HTTP: Module definition
// ------------------------------------------------------------------------
// Copyright (C) 2024, Gufo Labs
// See LICENSE.md for details
// ------------------------------------------------------------------------

use pyo3::prelude::*;
mod async_client;
mod auth;
mod error;
mod headers;
mod method;
mod response;
mod sync_client;

/// Module index
#[pymodule]
#[pyo3(name = "_fast")]
fn gufo_http(py: Python, m: &PyModule) -> PyResult<()> {
    m.add("HttpError", py.get_type::<error::PyHttpError>())?;
    m.add("RequestError", py.get_type::<error::PyRequestError>())?;
    m.add("ConnectError", py.get_type::<error::PyConnectError>())?;
    m.add("RedirectError", py.get_type::<error::PyRedirectError>())?;
    // Request methods
    m.add("GET", method::GET)?;
    m.add("HEAD", method::HEAD)?;
    m.add("OPTIONS", method::OPTIONS)?;
    m.add("DELETE", method::DELETE)?;
    m.add("POST", method::POST)?;
    m.add("PUT", method::PUT)?;
    m.add("PATCH", method::PATCH)?;
    // Compression methods
    m.add("DEFLATE", method::DEFLATE)?;
    m.add("GZIP", method::GZIP)?;
    m.add("BROTLI", method::BROTLI)?;
    // Auth
    m.add_class::<auth::AuthBase>()?;
    m.add_class::<auth::BasicAuth>()?;
    m.add_class::<auth::BearerAuth>()?;
    // Other
    m.add_class::<headers::Headers>()?;
    m.add_class::<response::Response>()?;
    // Clients
    m.add_class::<async_client::AsyncClient>()?;
    m.add_class::<sync_client::SyncClient>()?;
    Ok(())
}
