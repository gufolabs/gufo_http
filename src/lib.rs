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

/// Internal implementation in native codes.
///
/// This mode contains an Gufo HTTP internals
/// implemeted in the native codes.
/// You shouldn't import implementations from
/// _fast directly.
///
/// Attributes:
///     DEFLATE: Deflate method for `compression` argument.
///     GZIP: GZIP method for `compression` argument.
///     BROTLI: Brotli method for `compression` argument.
#[pymodule]
#[pyo3(name = "_fast")]
fn gufo_http(py: Python, m: &PyModule) -> PyResult<()> {
    m.add("HttpError", py.get_type::<error::HttpError>())?;
    m.add("RequestError", py.get_type::<error::RequestError>())?;
    m.add("ConnectError", py.get_type::<error::ConnectError>())?;
    m.add("RedirectError", py.get_type::<error::RedirectError>())?;
    // Request methods
    m.add_class::<method::RequestMethod>()?;
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
