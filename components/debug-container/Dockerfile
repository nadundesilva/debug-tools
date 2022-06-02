FROM ubuntu:22.10

# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends curl wget telnet && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["sleep", "infinity"]
