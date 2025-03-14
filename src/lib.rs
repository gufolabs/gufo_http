// ------------------------------------------------------------------------
// Gufo HTTP: Module definition
// ------------------------------------------------------------------------
// Copyright (C) 2024-25, Gufo Labs
// See LICENSE.md for details
// ------------------------------------------------------------------------

use pyo3::prelude::*;
mod async_client;
mod auth;
mod error;
mod headers;
mod method;
mod proxy;
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
fn gufo_http(py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add("HttpError", py.get_type::<error::HttpError>())?;
    m.add("RequestError", py.get_type::<error::RequestError>())?;
    m.add("RedirectError", py.get_type::<error::RedirectError>())?;
    // Request methods
    m.add_class::<method::RequestMethod>()?;
    // Compression methods
    m.add("DEFLATE", method::DEFLATE)?;
    m.add("GZIP", method::GZIP)?;
    m.add("BROTLI", method::BROTLI)?;
    m.add("ZSTD", method::ZSTD)?;
    // Auth
    m.add_class::<auth::AuthBase>()?;
    m.add_class::<auth::BasicAuth>()?;
    m.add_class::<auth::BearerAuth>()?;
    // Proxy
    m.add_class::<proxy::Proxy>()?;
    // Other
    m.add_class::<headers::Headers>()?;
    m.add_class::<response::Response>()?;
    // Clients
    m.add_class::<async_client::AsyncClient>()?;
    m.add_class::<sync_client::SyncClient>()?;
    Ok(())
}
