FROM node:24.1.0-alpine3.21

# renovate: datasource=npm packageName=npm
ARG NPM_VERSION="10.9.2"

RUN <<EOF
apk update
apk upgrade

addgroup -S -g 30000 request-debugger
adduser -S -u 10000 -G request-debugger request-debugger
EOF

COPY --chown=request-debugger . /app
WORKDIR /app

RUN npm i -g "npm@${NPM_VERSION}" && \
    npm ci

ENV SERVER_BIND_HOST="0.0.0.0"
ENV SERVER_BIND_PORT="8080"
ENV HEALTHCHECK_PATH="/_internal/health"
    
HEALTHCHECK --start-period=10s \
    --retries=3 \
    --interval=10s \
    --timeout=10s \
    CMD curl -f "http://${SERVER_BIND_HOST}:${SERVER_BIND_PORT}${HEALTHCHECK_PATH}" || exit 1

USER request-debugger
EXPOSE 8080

ENTRYPOINT ["npm", "run", "start"]
