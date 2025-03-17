// ------------------------------------------------------------------------
// Gufo HTTP: Error
// ------------------------------------------------------------------------
// Copyright (C) 2024, Gufo Labs
// See LICENSE.md for details
// ------------------------------------------------------------------------
use pyo3::{
    DowncastError, PyErr, create_exception,
    exceptions::{PyConnectionError, PyException, PyTimeoutError, PyValueError},
};

pub type HttpResult<T> = Result<T, GufoHttpError>;

#[derive(Debug)]
pub enum GufoHttpError {
    Request(String),
    Redirect,
    Connect(String),
    ValueError(String),
    Timeout,
    Downcast,
}

create_exception!(
    _fast,
    HttpError,
    PyException,
    "Base class for Gufo HTTP Errors"
);

create_exception!(_fast, RequestError, HttpError, "Request error");

create_exception!(_fast, RedirectError, HttpError, "Redirects limit exceeded");

impl From<GufoHttpError> for PyErr {
    fn from(value: GufoHttpError) -> Self {
        match value {
            GufoHttpError::Request(x) => RequestError::new_err(x),
            GufoHttpError::Redirect => RedirectError::new_err("redirects limit exceeded"),
            GufoHttpError::Connect(x) => PyConnectionError::new_err(x),
            GufoHttpError::ValueError(x) => PyValueError::new_err(x),
            GufoHttpError::Timeout => PyTimeoutError::new_err("timed out"),
            GufoHttpError::Downcast => PyValueError::new_err("downcast error"),
        }
    }
}

impl From<reqwest::Error> for GufoHttpError {
    fn from(value: reqwest::Error) -> Self {
        if value.is_connect() {
            return GufoHttpError::Connect(value.to_string());
        }
        if value.is_timeout() {
            return GufoHttpError::Timeout;
        }
        if value.is_redirect() {
            return GufoHttpError::Redirect;
        }
        GufoHttpError::Request(value.to_string())
    }
}

impl From<DowncastError<'_, '_>> for GufoHttpError {
    fn from(_value: DowncastError) -> Self {
        GufoHttpError::Downcast
    }
}
