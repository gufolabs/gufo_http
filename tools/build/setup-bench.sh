#!/bin/sh
# ------------------------------------------------------------------------
# Gufo Labs: Setup benchmark packages
# ------------------------------------------------------------------------
# Copyright (C) 2023-25, Gufo Labs
# ------------------------------------------------------------------------

set -x
set -e
pip3 install --upgrade\
    requests==2.31.0\
    httpx==0.27\
    aiohttp==3.9.3\
    aiosonic==0.18.0\
    niquests==3.5.2\
    pycurl==7.45.3\
    matplotlib==3.8.3
