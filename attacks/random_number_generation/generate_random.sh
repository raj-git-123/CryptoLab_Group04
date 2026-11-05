#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$SCRIPT_DIR/data"

mkdir -p "$DATA_DIR"

dd if=/dev/urandom \
   of="$DATA_DIR/linux_urandom.bin" \
   bs=1M count=1 status=progress

openssl rand \
   -out "$DATA_DIR/openssl_rand.bin" \
   1048576

echo "Linux and OpenSSL datasets generated."

