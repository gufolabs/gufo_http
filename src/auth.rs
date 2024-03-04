// ------------------------------------------------------------------------
// Gufo HTTP: Authentication primitives
// ------------------------------------------------------------------------
// Copyright (C) 2024, Gufo Labs
// See LICENSE.md for details
// ------------------------------------------------------------------------

use pyo3::prelude::*;

#[derive(Debug, Clone)]
pub enum AuthMethod {
    None,
    Basic {
        user: String,
        password: Option<String>,
    },
    Bearer {
        token: String,
    },
}

#[derive(Debug)]
#[pyclass(subclass)]
pub struct AuthBase {}

#[derive(Debug, Clone)]
#[pyclass(extends = AuthBase, subclass)]
pub struct BasicAuth(AuthMethod);

#[derive(Debug, Clone)]
#[pyclass(extends = AuthBase, subclass)]
pub struct BearerAuth(AuthMethod);

pub trait GetAuthMethod {
    fn get_method(&self) -> AuthMethod;
}

#[pymethods]
impl AuthBase {
    #[new]
    fn new() -> Self {
        Self {}
    }
}

#[pymethods]
impl BasicAuth {
    #[new]
    fn new(user: &str, password: Option<&str>) -> (Self, AuthBase) {
        (
            Self(AuthMethod::Basic {
                user: user.into(),
                password: password.map(|x| x.into()),
            }),
            AuthBase::new(),
        )
    }
}

impl GetAuthMethod for BasicAuth {
    fn get_method(&self) -> AuthMethod {
        self.0.clone()
    }
}

#[pymethods]
impl BearerAuth {
    #[new]
    fn new(token: &str) -> (Self, AuthBase) {
        (
            Self(AuthMethod::Bearer {
                token: token.into(),
            }),
            AuthBase::new(),
        )
    }
}

impl GetAuthMethod for BearerAuth {
    fn get_method(&self) -> AuthMethod {
        self.0.clone()
    }
}
