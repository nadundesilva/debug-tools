from typing import Generator

import docker
import pytest


@pytest.fixture(scope="module")
def docker_client() -> Generator[docker.DockerClient, None, None]:
    client = docker.from_env()
    yield client
    client.close()
