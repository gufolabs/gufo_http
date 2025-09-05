// ------------------------------------------------------------------------
// Gufo HTTP: Headers impmentation
// ------------------------------------------------------------------------
// Copyright (C) 2024-25, Gufo Labs
// See LICENSE.md for details
// ------------------------------------------------------------------------
use pyo3::{exceptions::PyKeyError, prelude::*, types::PyBytes};
use reqwest::header::HeaderMap;

#[derive(Clone)]
#[pyclass]
pub struct Headers(HeaderMap);

impl Headers {
    pub fn new(headers: HeaderMap) -> Self {
        Self(headers)
    }
}

#[pymethods]
impl Headers {
    fn __getitem__<'a>(&'a self, key: &str) -> PyResult<&'a [u8]> {
        match self.0.get(key) {
            Some(x) => Ok(x.as_ref()),
            None => Err(PyKeyError::new_err(key.to_owned())),
        }
    }
    fn __contains__(&self, key: &str) -> bool {
        self.0.contains_key(key)
    }
    #[pyo3(signature = (key, default = None))]
    fn get<'a>(
        &'a self,
        key: &str,
        default: Option<&Bound<'a, PyBytes>>,
        py: Python<'a>,
    ) -> PyResult<Option<Bound<'a, PyBytes>>> {
        match self.0.get(key) {
            Some(x) => Ok(Some(PyBytes::new(py, x.as_ref()))),
            None => match default {
                Some(d) => Ok(Some(d.clone())),
                None => Ok(None),
            },
        }
    }
    fn keys(&self) -> KeysIterator {
        KeysIterator(
            self.0
                .keys()
                .map(|x| x.to_string())
                .collect::<Vec<_>>()
                .into_iter(),
        )
    }
    fn values(&self) -> ValuesIterator {
        ValuesIterator(
            self.0
                .values()
                .map(|x| x.as_ref().to_owned().into_boxed_slice())
                .collect::<Vec<_>>()
                .into_iter(),
        )
    }
    fn items(&self) -> ItemsIterator {
        ItemsIterator(
            self.0
                .iter()
                .map(|(k, v)| (k.to_string(), v.as_ref().to_owned().into_boxed_slice()))
                .collect::<Vec<_>>()
                .into_iter(),
        )
    }
}

// Keys iterator
// Very ineffective as pyo3 doesn't support lifetime.
#[pyclass]
pub struct KeysIterator(std::vec::IntoIter<String>);

#[pymethods]
impl KeysIterator {
    fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }
    fn __next__(mut slf: PyRefMut<'_, Self>) -> Option<String> {
        slf.0.next()
    }
}

// Values iterator
// Very ineffective as pyo3 doesn't support lifetime.
#[pyclass]
pub struct ValuesIterator(std::vec::IntoIter<Box<[u8]>>);

#[pymethods]
impl ValuesIterator {
    fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }
    fn __next__(mut slf: PyRefMut<'_, Self>, py: Python) -> Option<Py<PyAny>> {
        slf.0.next().map(|boxed| {
            let bytes = PyBytes::new(py, &boxed);
            bytes.into()
        })
    }
}
// Items iterator
// Very ineffective as pyo3 doesn't support lifetime.
#[pyclass]
pub struct ItemsIterator(std::vec::IntoIter<(String, Box<[u8]>)>);

#[pymethods]
impl ItemsIterator {
    fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }
    fn __next__(mut slf: PyRefMut<'_, Self>, py: Python) -> Option<(String, Py<PyAny>)> {
        slf.0.next().map(|(k, v)| {
            let bytes = PyBytes::new(py, &v);
            (k, bytes.into())
        })
    }
}
