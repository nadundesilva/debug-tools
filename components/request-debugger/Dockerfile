FROM node:16.15.0

COPY . /app

WORKDIR /app

EXPOSE 8080

RUN npm i -g npm@8.11.0 && \
    npm ci

ENTRYPOINT ["npm", "run", "start"]
