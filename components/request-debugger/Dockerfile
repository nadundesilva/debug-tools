FROM node:24.1.0-alpine3.22

# renovate: datasource=repology depName=alpine_3_22/curl
ARG CURL_VERSION="8.14.1-r0"
# renovate: datasource=npm packageName=npm
ARG NPM_VERSION="10.9.2"

RUN <<EOF
set -eu

apk update
apk upgrade

echo "Installing Tools"
apk add --no-cache \
    curl="${CURL_VERSION}"

echo "Creating Users"
addgroup -S \
    -g 30000 \
    debug-tools
adduser -S \
    -u 10000 \
    -G debug-tools \
    -s /bin/ash \
    request-debugger

echo "Cleaning Up"
rm /var/cache/apk/*
EOF

COPY . /server
WORKDIR /server

RUN <<EOF
set -eu

echo "Installing Request Debugger dependencies"
npm i -g "npm@${NPM_VERSION}"
npm ci
chown 10000:30000 /server
EOF

USER 10000:30000

ENV SERVER_BIND_HOST="0.0.0.0"
ENV SERVER_BIND_PORT="8080"
ENV HEALTHCHECK_PATH="/_internal/health"
    
HEALTHCHECK --start-period=10s \
    --retries=3 \
    --interval=10s \
    --timeout=10s \
    CMD curl -f "http://${SERVER_BIND_HOST}:${SERVER_BIND_PORT}${HEALTHCHECK_PATH}" || exit 1

EXPOSE 8080

ENTRYPOINT ["npm", "run", "start"]
