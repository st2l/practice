FROM ubuntu:22.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends socat \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY build/got_overwrite_exit /app/build/got_overwrite_exit

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh /app/build/got_overwrite_exit

ENTRYPOINT ["/app/entrypoint.sh"]
