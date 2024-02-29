// ------------------------------------------------------------------------
// Gufo HTTP: HTTP Methods
// ------------------------------------------------------------------------
// Copyright (C) 2024, Gufo Labs
// See LICENSE.md for details
// ------------------------------------------------------------------------

// Request methods
pub const GET: usize = 0;
pub const HEAD: usize = 1;
pub const OPTIONS: usize = 2;
pub const DELETE: usize = 3;

// Compression methods
pub const DEFLATE: u8 = 1;
pub const GZIP: u8 = 1 << 1;
pub const BROTLI: u8 = 1 << 2;
