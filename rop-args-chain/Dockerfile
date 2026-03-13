FROM ubuntu:22.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends socat \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY build/rop_args_chain /app/build/rop_args_chain

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh /app/build/rop_args_chain

ENTRYPOINT ["/app/entrypoint.sh"]
