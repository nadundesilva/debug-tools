FROM node:24.7.0-alpine3.22@sha256:be4d5e92ac68483ec71440bf5934865b4b7fcb93588f17a24d411d15f0204e4f AS builder

# renovate: datasource=npm depName=npm
ARG NPM_VERSION="11.5.2"

RUN npm i -g npm@${NPM_VERSION}

WORKDIR /app
COPY . .
RUN npm ci

FROM node:24.7.0-alpine3.22@sha256:be4d5e92ac68483ec71440bf5934865b4b7fcb93588f17a24d411d15f0204e4f

# renovate: datasource=repology depName=alpine_3_22/curl versioning=deb
ARG CURL_VERSION="8.14.1-r1"

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

WORKDIR /server
COPY --from=builder --chown=${USER_ID}:${GROUP_ID} /app .

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
