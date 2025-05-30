import docker
import pytest


@pytest.fixture(scope="module")
def docker_client():
    client = docker.from_env()
    yield client
    client.close()
