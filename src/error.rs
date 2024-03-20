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

pub type HttpResult<T> = Result<T, GufoHttpError>;

#[derive(Debug)]
pub enum GufoHttpError {
    Request(String),
    Redirect,
    Connect,
    ValueError(String),
}

create_exception!(
    _fast,
    HttpError,
    PyException,
    "Base class for Gufo HTTP Errors"
);

create_exception!(_fast, RequestError, HttpError, "Request error");

create_exception!(_fast, RedirectError, HttpError, "Redirects limit exceeded");

create_exception!(_fast, ConnectError, HttpError, "Connect error");

impl From<GufoHttpError> for PyErr {
    fn from(value: GufoHttpError) -> Self {
        match value {
            GufoHttpError::Request(x) => RequestError::new_err(x),
            GufoHttpError::Redirect => RedirectError::new_err("redirects limit exceeded"),
            GufoHttpError::Connect => ConnectError::new_err("connect error"),
            GufoHttpError::ValueError(x) => PyValueError::new_err(x),
        }
    }
}

impl From<reqwest::Error> for GufoHttpError {
    fn from(value: reqwest::Error) -> Self {
        if value.is_connect() {
            return GufoHttpError::Connect;
        }
        if value.is_redirect() {
            return GufoHttpError::Redirect;
        }
        GufoHttpError::Request(value.to_string())
    }
}
