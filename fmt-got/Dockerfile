FROM ubuntu:22.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends socat make gcc libc6-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY Makefile main.c /app/
RUN make

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh /app/build/voice_coach

ENTRYPOINT ["/app/entrypoint.sh"]
