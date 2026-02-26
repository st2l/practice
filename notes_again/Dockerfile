FROM ubuntu:22.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libc6-dev socat \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY main.c /app/main.c
RUN mkdir -p /app/bin \
    && gcc -g -O0 /app/main.c -o /app/bin/notes_manager

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh /app/bin/notes_manager

ENTRYPOINT ["/app/entrypoint.sh"]
