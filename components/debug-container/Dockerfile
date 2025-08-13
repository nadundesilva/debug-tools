#checkov:skip=CKV_DOCKER_2: Not required since nothing is running
FROM ubuntu:24.04@sha256:7c06e91f61fa88c08cc74f7e1b7c69ae24910d745357e0dfe1d2c0322aaf20f9

# renovate: datasource=repology depName=ubuntu_24_04/curl versioning=deb
ARG CURL_VERSION="8.5.0-2ubuntu10.6"
# renovate: datasource=repology depName=ubuntu_24_04/wget versioning=deb
ARG WGET_VERSION="1.21.4-1ubuntu4.1"
# renovate: datasource=repology depName=ubuntu_24_04/inetutils versioning=deb
ARG INETUTILS_VERSION="2:2.5-3ubuntu4"

ARG USER_ID="10000"
ARG GROUP_ID="30000"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl="${CURL_VERSION}" \
        wget="${WGET_VERSION}" \
        inetutils-telnet="${INETUTILS_VERSION}" && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/* && \
    groupadd -r \
        -g ${GROUP_ID} \
        debug-tools && \
    useradd -r -m -l \
        -u ${USER_ID} \
        -g ${GROUP_ID} \
        -s /bin/bash \
        -d /home/request-debugger \
        debug-user

SHELL ["/bin/bash", "-c"]
USER ${USER_ID}:${GROUP_ID}

ENTRYPOINT ["sleep", "infinity"]
