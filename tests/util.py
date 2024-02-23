# ---------------------------------------------------------------------
# Gufo HTTP: Test utilities
# ---------------------------------------------------------------------
# Copyright (C) 2024, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------

# Python modules
import random

HTTPD_PATH = "/usr/sbin/nginx"
HTTPD_HOST = "local.gufolabs.com"
HTTPD_ADDRESS = "127.0.0.1"
HTTPD_PORT = random.randint(52000, 53999)
URL_PREFIX = f"http://{HTTPD_HOST}:{HTTPD_PORT}"
