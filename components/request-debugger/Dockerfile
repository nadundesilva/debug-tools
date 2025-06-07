FROM node:24.1.0-alpine3.22

# renovate: datasource=repology depName=alpine_3_22/curl
ARG CURL_VERSION="8.14.1-r0"
# renovate: datasource=npm packageName=npm
ARG NPM_VERSION="10.9.2"

ARG USER_ID="10000"
ARG GROUP_ID="30000"

RUN apk update && \
    apk add --no-cache \
        curl="${CURL_VERSION}" && \
    rm -rf /var/cache/apk/* && \
    addgroup -S \
        -g ${GROUP_ID} \
        debug-tools && \
    adduser -S \
        -u ${USER_ID} \
        -g ${GROUP_ID} \
        -s /bin/ash \
        request-debugger

COPY --chown=${USER_ID}:${GROUP_ID} . /server
WORKDIR /server

RUN npm i -g "npm@${NPM_VERSION}" && \
    npm ci

ENV SERVER_BIND_HOST="0.0.0.0"
ENV SERVER_BIND_PORT="8080"
ENV HEALTHCHECK_PATH="/_internal/health"

SHELL ["/bin/ash", "-c"]
USER ${USER_ID}:${GROUP_ID}

EXPOSE 8080

HEALTHCHECK --start-period=10s \
    --retries=3 \
    --interval=10s \
    --timeout=10s \
    CMD curl -f "http://${SERVER_BIND_HOST}:${SERVER_BIND_PORT}${HEALTHCHECK_PATH}" || exit 1

ENTRYPOINT ["npm", "run", "start"]
