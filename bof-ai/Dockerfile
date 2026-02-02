FROM ubuntu:22.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential socat \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN make -C /app

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
