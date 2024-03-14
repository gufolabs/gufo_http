// ------------------------------------------------------------------------
// Gufo HTTP: SyncResponse impmentation
// ------------------------------------------------------------------------
// Copyright (C) 2024, Gufo Labs
// See LICENSE.md for details
// ------------------------------------------------------------------------
use crate::headers::Headers;
use pyo3::{prelude::*, types::PyBytes};

#[pyclass]
pub struct Response {
    #[pyo3(get)]
    status: u16,
    #[pyo3(get)]
    content: Py<PyBytes>,
    #[pyo3(get)]
    headers: Headers,
}

impl Response {
    pub fn new(status: u16, headers: Headers, content: Py<PyBytes>) -> Self {
        Response {
            status,
            headers,
            content,
        }
    }
}
