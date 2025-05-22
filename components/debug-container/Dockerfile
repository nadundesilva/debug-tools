FROM ubuntu:24.04

RUN useradd -m -u 10000 -g 30000 debug-container
USER debug-container

# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends curl wget telnet && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["sleep", "infinity"]
