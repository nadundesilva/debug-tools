# Request Debugger

This container runs a server, which will listen to all HTTP requests and log them, except for the health probe (`/_internal/health`), reserved for internal usage.

## Deploying on Container Environments

- Docker Image - `docker.io/nadunrds/debug-tools-request-debugger:latest`
- [Kubernetes Manifests](../../kubernetes/request-debugger.yaml)

## Configurations

The following environment variables can be used to configure the behaviour of the Docker container.

| Environment Variable   | Description                        | Default Value      |
| ---------------------- | ---------------------------------- | ------------------ |
| `SERVER_BIND_PORT`     | The port the server will bind to   | 8080               |
| `HEALTHCHECK_PATH`     | The internal health check port     | /\_internal/health |
| `RESPONSE_STATUS_CODE` | The status code of the response    | 200                |
| `RESPONSE_CONTENT`     | The content of the response (enum) | `HELLO`            |

### Changing the response

The following env vars can be change the response of the request debugger server.

- `RESPONSE_STATUS_CODE` - Set this to a valid HTTP status code to return.
- `RESPONSE_CONTENT` - Set this to one of the following values.
  - `HELLO` - Return "Hello from Request Debugger" as the response.
  - `REQUEST_PROPERTIES` - Return the request properties (e.g.:- body, headers) as a JSON.
