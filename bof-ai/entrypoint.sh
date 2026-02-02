#!/bin/sh
set -eu

FLAG_VALUE="${FLAG:-CTF{test_flag}}"
PORT_VALUE="${PORT:-1337}"

echo "$FLAG_VALUE" > /app/build/flag.txt
chmod 444 /app/build/flag.txt

exec socat TCP-LISTEN:${PORT_VALUE},reuseaddr,fork EXEC:/app/build/chat_ai,pty,rawer,stderr
