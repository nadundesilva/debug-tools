# Debug Container

This container contains several tools useful for debugging issues in container environments. The container itself, when run will sleep forever doing nothing. You can use `docker exec` to run commands within the container and debug possible networking and other issues.

The following tools are currently installed in this container.

- cURL
- wget
- telnet

## Deploying on Container Environments

- Docker Image - `docker.io/nadunrds/debug-tools-debug-container:latest`
- [Kubernetes Manifests](./kubernetes/)
