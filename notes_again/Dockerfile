FROM ubuntu:22.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends socat make gcc libc6-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY Makefile main.c /app/
COPY ld-linux-x86-64.so.2 /app/ld-linux-x86-64.so.2
COPY libc.so.6 /app/libc.so.6
RUN make app

ENV LD_LIBRARY_PATH=/app

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh /app/bin/notes_manager /app/ld-linux-x86-64.so.2 /app/libc.so.6

ENTRYPOINT ["/app/entrypoint.sh"]
