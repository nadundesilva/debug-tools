FROM node:22.16.0

RUN useradd -m -u 10000 -g 30000 request-debugger
USER request-debugger

COPY --chown=request-debugger . /app
WORKDIR /app

EXPOSE 8080

RUN npm i -g npm@10.9.2 && \
    npm ci

ENTRYPOINT ["npm", "run", "start"]
