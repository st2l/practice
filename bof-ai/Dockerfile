FROM ubuntu:22.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends socat \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY build/chat_ai /app/build/chat_ai

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh /app/build/chat_ai

ENTRYPOINT ["/app/entrypoint.sh"]
