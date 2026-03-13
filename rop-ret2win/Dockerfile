FROM ubuntu:22.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends socat \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY build/rop_ret2win /app/build/rop_ret2win

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh /app/build/rop_ret2win

ENTRYPOINT ["/app/entrypoint.sh"]
