#checkov:skip=CKV_DOCKER_2: Not required since nothing is running
FROM ubuntu:24.04

# renovate: datasource=repology depName=ubuntu_24_04/curl
ARG CURL_VERSION="8.5.0"
# renovate: datasource=repology depName=ubuntu_24_04/wget
ARG WGET_VERSION="2.1.0"
# renovate: datasource=repology depName=ubuntu_24_04/telnet
ARG TELNET_VERSION="0.21"

RUN groupadd -r -g 30000 debug-container && \
    useradd -m -u 10000 -g 30000 debug-container

USER debug-container

# hadolint ignore=DL3008
RUN <<EOF

apt-get update
apt-get upgrade -y

apt-get install -y --no-install-recommends \
    curl="${CURL_VERSION}" \
    wget="${WGET_VERSION}" \
    telnet="${TELNET_VERSION}"

echo "Cleaning Up"
apt-get clean -y
rm -rf /var/lib/apt/lists/*

EOF

ENTRYPOINT ["sleep", "infinity"]
