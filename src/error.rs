// ------------------------------------------------------------------------
// Gufo HTTP: Error
// ------------------------------------------------------------------------
// Copyright (C) 2024, Gufo Labs
// See LICENSE.md for details
// ------------------------------------------------------------------------
use pyo3::{
    create_exception,
    exceptions::{PyException, PyValueError},
    PyErr,
};

//pub type HttpResult<T> = Result<T, HttpError>;

#[derive(Debug)]
pub enum HttpError {
    Request(String),
    Redirect,
    Connect,
    ValueError(String),
}

create_exception!(
    _fast,
    PyHttpError,
    PyException,
    "Base class for Gufo HTTP Errors"
);

create_exception!(_fast, PyRequestError, PyHttpError, "Request error");

create_exception!(
    _fast,
    PyRedirectError,
    PyHttpError,
    "Redirects limit exceeded"
);

create_exception!(_fast, PyConnectError, PyHttpError, "Connect error");

impl From<HttpError> for PyErr {
    fn from(value: HttpError) -> Self {
        match value {
            HttpError::Request(x) => PyRequestError::new_err(x),
            HttpError::Redirect => PyRedirectError::new_err("redirects limit exceeded"),
            HttpError::Connect => PyConnectError::new_err("connect error"),
            HttpError::ValueError(x) => PyValueError::new_err(x),
        }
    }
}

impl From<reqwest::Error> for HttpError {
    fn from(value: reqwest::Error) -> Self {
        if value.is_connect() {
            return HttpError::Connect;
        }
        if value.is_redirect() {
            return HttpError::Redirect;
        }
        HttpError::Request(value.to_string())
    }
}
