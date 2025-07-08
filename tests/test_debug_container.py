from typing import Callable, Generator

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


@pytest.fixture
def debug_container_container(
    docker_client: docker.DockerClient,
    debug_container_image: docker.models.images.Image,
) -> Generator[Callable[[], docker.models.containers.Container], None, None]:
    created_containers: list[docker.models.containers.Container] = []

    def _container_creator() -> docker.models.containers.Container:
        container = docker_client.containers.run(
            image=debug_container_image, detach=True
        )
        wait_for_container(container)
        created_containers.append(container)
        return container

    yield _container_creator

    for container in created_containers:
        container.stop()
        container.wait()
        container.remove()


def test_debug_container(
    debug_container_container: Callable[[], docker.models.containers.Container],
) -> None:
    container = debug_container_container()
    for tool in installed_tools:
        print(f"Checking if {tool} is installed")
        exit_code, output = container.exec_run(
            ["/bin/bash", "-c", f"command -v {tool}"],
            user=(
                container.image.attrs["Config"]["User"]
                if container.image is not None
                else "root"
            ),
        )
        print(output.decode("utf-8"))
        assert exit_code == 0
