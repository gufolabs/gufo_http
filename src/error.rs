// ------------------------------------------------------------------------
// Gufo HTTP: Error
// ------------------------------------------------------------------------
// Copyright (C) 2024, Gufo Labs
// See LICENSE.md for details
// ------------------------------------------------------------------------
use pyo3::{create_exception, exceptions::PyException, PyErr};

//pub type HttpResult<T> = Result<T, HttpError>;

#[derive(Debug)]
pub enum HttpError {
    RequestError(String),
    RedirectError,
    ConnectError,
    AlreadyReadError,
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
create_exception!(_fast, PyAlreadyReadError, PyHttpError, "Already read");

impl From<HttpError> for PyErr {
    fn from(value: HttpError) -> Self {
        match value {
            HttpError::RequestError(x) => PyRequestError::new_err(x),
            HttpError::RedirectError => PyRedirectError::new_err("redirects limit exceeded"),
            HttpError::ConnectError => PyConnectError::new_err("connect error"),
            HttpError::AlreadyReadError => PyAlreadyReadError::new_err("already read"),
        }
    }
}

impl From<reqwest::Error> for HttpError {
    fn from(value: reqwest::Error) -> Self {
        if value.is_connect() {
            return HttpError::ConnectError;
        }
        if value.is_redirect() {
            return HttpError::RedirectError;
        }
        HttpError::RequestError(value.to_string())
    }
}
