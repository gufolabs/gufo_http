#!/bin/sh
# ------------------------------------------------------------------------
# Gufo Labs: Install nginx
# ------------------------------------------------------------------------
# Copyright (C) 2024, Gufo Labs
# ------------------------------------------------------------------------

set -e
OS="unknown"

if  [ -f /etc/redhat-release ]; then
    OS="rhel"
elif [ -f /etc/debian_version ]; then
    OS="debian"
elif [ -f /etc/alpine-release ]; then
    OS="alpine"
else
    echo "Cannot detect OS"
    exit 1
fi

if [ $(id -u) -eq 0 ]; then
    SUDO=""
else
    SUDO="sudo"
fi

echo "Installing nginx for $OS"
case $OS in
    rhel)
        $SUDO yum install -y nginx
        # Test
        /usr/sbin/nginx -v
        ;;
    debian)
        $SUDO apt-get update
        $SUDO apt-get install -y --no-install-recommends nginx
        # Test
        /usr/sbin/nginx -v
        ;;
    alpine)
        $SUDO apk add nginx
        ;;
    *)
        echo "Unsupported OS: $OS"
        exit 1
        ;;
esac