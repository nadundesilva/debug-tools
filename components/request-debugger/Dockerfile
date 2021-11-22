FROM node:16.13.0

COPY . /app

WORKDIR /app

RUN npm ci

ENTRYPOINT ["npm", "run", "start"]
