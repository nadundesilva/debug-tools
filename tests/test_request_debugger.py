from typing import Generator

import docker
import docker.models
import docker.models.images
import pytest
import requests

from .utils import build_image, wait_for_container


@pytest.fixture(scope="module")
def request_debugger_image(
    docker_client: docker.DockerClient,
) -> Generator[docker.models.images.Image, None, None]:
    image = build_image(
        context_path="../components/request-debugger/",
        image_tag="request-debugger:test",
        docker_client=docker_client,
    )
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
    wait_for_container(container)

    resp = requests.get(f"http://localhost:{server_bind_port}/test-url")
    assert resp.status_code == 200
    assert resp.content.decode("utf-8") == "Hello from Request Debugger"

    container.stop()
    container.wait()
    container.remove()
