from typing import Generator

import docker
import docker.models
import docker.models.images
import pytest

from .utils import build_image, wait_for_container

installed_tools = ["curl", "wget", "telnet"]


@pytest.fixture(scope="module")
def debug_container_image(
    docker_client: docker.DockerClient,
) -> Generator[docker.models.images.Image, None, None]:
    image = build_image(
        context_path="../components/debug-container/",
        image_tag="debug-container:test",
        docker_client=docker_client,
    )
    yield image
    docker_client.images.remove(image.id, force=True)


def test_debug_container(
    docker_client: docker.DockerClient,
    debug_container_image: docker.models.images.Image,
) -> None:
    container = docker_client.containers.run(image=debug_container_image, detach=True)
    wait_for_container(container)

    for tool in installed_tools:
        print(f"Checking if {tool} is installed")
        exit_code, output = container.exec_run(
            ["/bin/bash", "-c", f"command -v {tool}"],
            user=debug_container_image.attrs["Config"]["User"],
        )
        print(output.decode("utf-8"))
        assert exit_code == 0

    container.stop()
    container.wait()
    container.remove()
