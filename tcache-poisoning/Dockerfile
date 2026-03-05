FROM ubuntu:22.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends socat make gcc libc6-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY Makefile main.c /app/
COPY libc.so.6 /app/libc.so.6
COPY ld-linux-x86-64.so.2 /app/ld-linux-x86-64.so.2
RUN make

ENV LD_LIBRARY_PATH=/app

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh /app/build/heap_notes /app/libc.so.6 /app/ld-linux-x86-64.so.2

ENTRYPOINT ["/app/entrypoint.sh"]
