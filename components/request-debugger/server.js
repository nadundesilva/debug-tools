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
const bodyParser = require("body-parser");
const cookieParser = require("cookie-parser");

const HOST = process.env.SERVER_HOST || "0.0.0.0";
const PORT = process.env.SERVER_PORT || 8080;
const STATUS_CODE = parseInt(process.env.STATUS_CODE, 10) || 200

var app = express();

app.use(bodyParser.text({
    type: "*/*"
}));
app.use(cookieParser());

app.all("/*", (req, res) => {
    const requestLog = {
        method: req.method,
        protocol: req.protocol,
        path: req.originalUrl,
        headers: req.headers,
        body: req.body,
        cookies: req.cookies,
        signedCookies: req.signedCookies
    };
    console.log(JSON.stringify(requestLog));
    res.status(STATUS_CODE);
    res.send("Hello from Request Debugger");
});

const server = app.listen(PORT, HOST, () => {
    console.log(`Running on http://${HOST}:${PORT}`);
});

process.on("SIGTERM", () => {
    console.log("Shutting down HTTP server");
    server.close(() => {
      console.log("HTTP server successfully shutdown");
    });
});
