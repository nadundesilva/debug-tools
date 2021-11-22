FROM node:16.13.0

COPY . /app

WORKDIR /app

EXPOSE 8080

RUN npm ci

ENTRYPOINT ["npm", "run", "start"]
