FROM node:22.16.0

COPY . /app

WORKDIR /app

EXPOSE 8080

RUN npm i -g npm@10.9.2 && \
    npm ci

ENTRYPOINT ["npm", "run", "start"]
