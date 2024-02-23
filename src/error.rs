// ------------------------------------------------------------------------
// Gufo HTTP: Error
// ------------------------------------------------------------------------
// Copyright (C) 2024, Gufo Labs
// See LICENSE.md for details
// ------------------------------------------------------------------------
use pyo3::{create_exception, exceptions::PyException, PyErr};

//pub type HttpResult<T> = Result<T, HttpError>;

#[derive(Debug)]
pub enum HttpError {}

create_exception!(
    _fast,
    PyHttpError,
    PyException,
    "Base class for Gufo HTTP Errors"
);

impl From<HttpError> for PyErr {
    fn from(value: HttpError) -> Self {
        match value {}
    }
}
