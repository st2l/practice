#!/bin/sh
set -eu

FLAG_VALUE="${FLAG:-CTF{test_flag}}"
PORT_VALUE="${PORT:-1337}"

mkdir -p /app/build
echo "$FLAG_VALUE" >/app/flag.txt
chmod 444 /app/flag.txt

exec socat TCP-LISTEN:${PORT_VALUE},reuseaddr,fork EXEC:/app/build/chat_ai,stderr
