/*
 * Copyright (c) 2021, Deep Net. All Rights Reserved.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *   http://www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

const express = require("express");
const cookieParser = require("cookie-parser");

const RESPONSE_CONTENT_HELLO = "HELLO";
const RESPONSE_CONTENT_REQUEST_PROPERTIES = "REQUEST_PROPERTIES";

const BIND_HOST = process.env.SERVER_BIND_HOST || "0.0.0.0";
const BIND_PORT = process.env.SERVER_BIND_PORT || 8080;
const HEALTHCHECK_PATH = process.env.HEALTH_CHECK_PATH || "/_internal/health";
const RESPONSE_STATUS_CODE =
  parseInt(process.env.RESPONSE_STATUS_CODE, 10) || 200;
const RESPONSE_CONTENT = process.env.RESPONSE_CONTENT || RESPONSE_CONTENT_HELLO;

const buildDebugRequestObject = (req) => {
  return {
    protocol: req.protocol,
    method: req.method,
    path: req.originalUrl,

    headers: req.headers,
    cookies: req.cookies,
    body: req.body,
  };
};

let respond = (req, res) => {
  res.status(500);
  res.json({ message: "Response not supported" });
};
switch (RESPONSE_CONTENT) {
  case RESPONSE_CONTENT_HELLO:
    respond = (req, res) => {
      res.status(RESPONSE_STATUS_CODE);
      res.json({ message: "Hello from Request Debugger" });
    };
    break;
  case RESPONSE_CONTENT_REQUEST_PROPERTIES:
    respond = (req, res) => {
      res.status(RESPONSE_STATUS_CODE);
      res.json(buildDebugRequestObject(req));
    };
    break;
  default:
    throw Error(
      `Unknown value for environment variable RESPONSE_CONTENT: ${RESPONSE_CONTENT}`,
    );
}

const app = express();

app.use(express.json());

app.get(HEALTHCHECK_PATH, (req, res) => {
  res.status(200);
  res.send({ status: "OK" });
});

app.use(
  express.text({
    type: "*/*",
  }),
);
app.use(cookieParser());

app.all("*path", (req, res) => {
  console.log(JSON.stringify(buildDebugRequestObject(req)));
  respond(req, res);
});

const server = app.listen(BIND_PORT, BIND_HOST, (err) => {
  if (err) {
    console.log(`Error starting server: ${err}`);
  } else {
    console.log(`Running on http://${BIND_HOST}:${BIND_PORT}`);
  }
});

process.on("SIGTERM", () => {
  console.log("SIGTERM Received: Shutting down HTTP server");
  server.close(() => {
    console.log("HTTP server successfully shutdown");
  });
});
