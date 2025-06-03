from typing import Generator

import docker
import docker.models
import docker.models.images
import pytest


@pytest.fixture(scope="module")
def request_debugger_image(
    docker_client: docker.DockerClient,
) -> Generator[docker.models.images.Image, None, None]:
    image, build_logs = docker_client.images.build(
        path="../components/request-debugger/",
        tag="request-debugger:test",
        nocache=True,
        rm=True,
        forcerm=True,
        pull=True,
    )
    for line in build_logs:
        print(line)
    yield image
    docker_client.images.remove(image.id, force=True)


def test_request_debugger(
    docker_client: docker.DockerClient,
    request_debugger_image: docker.models.images.Image,
) -> None:
    server_bind_port = 18080

    container = docker_client.containers.run(
        image=request_debugger_image,
        detach=True,
        ports={str(server_bind_port): server_bind_port},
        environment={"SERVER_BIND_PORT": str(server_bind_port)},
    )

    container.stop()
    container.wait()
    container.remove()
