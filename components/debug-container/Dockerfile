#checkov:skip=CKV_DOCKER_2: Not required since nothing is running
FROM ubuntu:24.04

# renovate: datasource=repology depName=ubuntu_24_04/curl
ARG CURL_VERSION="8.5.0-2ubuntu10.6"
# renovate: datasource=repology depName=ubuntu_24_04/wget
ARG WGET_VERSION="1.21.4-1ubuntu4.1"
# renovate: datasource=repology depName=ubuntu_24_04/telnet
ARG TELNET_VERSION="0.17+2.5-3ubuntu4"

# hadolint ignore=DL3008
RUN <<EOF
set -eu

apt-get update -y
apt-get upgrade -y

apt-get install -y --no-install-recommends \
    curl="${CURL_VERSION}" \
    wget="${WGET_VERSION}" \
    telnet="${TELNET_VERSION}"

echo "Creating Users"
groupadd -r \
    -g 30000 \
    debug-tools
useradd -r -m \
    -u 10000 \
    -g debug-tools \
    -s /bin/bash \
    -d /home/request-debugger \
    debug-user

echo "Cleaning Up"
apt-get clean -y
rm -rf /var/lib/apt/lists/*
EOF

USER 10000:30000

ENTRYPOINT ["sleep", "infinity"]
