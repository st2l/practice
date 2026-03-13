#!/bin/sh
set -eu

FLAG_VALUE="${FLAG:-practice{test_flag}}"
PORT_VALUE="${PORT:-1337}"

echo "$FLAG_VALUE" >/app/flag.txt
chmod 444 /app/flag.txt

exec socat TCP-LISTEN:${PORT_VALUE},reuseaddr,fork EXEC:/app/build/got_overwrite_exit,stderr
