import random
from typing import Generator

import docker
import docker.models
import docker.models.images
import pytest
import requests

from .utils import build_image, wait_for_container

hello_world_response_body = {"message": "Hello from Request Debugger"}


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
    image.remove()


def test_request_debugger_with_hello_response(
    docker_client: docker.DockerClient,
    request_debugger_image: docker.models.images.Image,
) -> None:
    server_bind_port = 18080

    container = docker_client.containers.run(
        image=request_debugger_image,
        detach=True,
        ports={str(server_bind_port): server_bind_port},
        environment={
            "SERVER_BIND_PORT": str(server_bind_port),
            "RESPONSE_CONTENT": "HELLO",
        },
    )
    wait_for_container(container)

    resp = requests.get(
        f"http://localhost:{server_bind_port}/test-url-{random.randint(0, 1000)}"
    )
    assert resp.status_code == 200
    assert resp.json() == hello_world_response_body

    container.stop()
    container.wait()
    container.remove()


def test_request_debugger_with_echo_request_response(
    docker_client: docker.DockerClient,
    request_debugger_image: docker.models.images.Image,
) -> None:
    server_bind_port = 18081

    container = docker_client.containers.run(
        image=request_debugger_image,
        detach=True,
        ports={str(server_bind_port): server_bind_port},
        environment={
            "SERVER_BIND_PORT": str(server_bind_port),
            "RESPONSE_CONTENT": "REQUEST_PROPERTIES",
        },
    )
    wait_for_container(container)

    req_path = f"/test-url-{random.randint(0, 1000)}"
    body_content = {"test-property": "debug-tools-test-property-value"}
    req_headers = {
        "x-test-header": "debug-tools-test-header",
    }
    req_cookies = {
        "x-test-cookie": "debug-tools-test-cookie",
    }
    resp = requests.post(
        f"http://localhost:{server_bind_port}{req_path}",
        headers=req_headers,
        cookies=req_cookies,
        json=body_content,
    )
    assert resp.status_code == 200
    resp_content = resp.json()

    assert resp_content["protocol"] == "http"
    assert resp_content["method"] == "POST"
    assert resp_content["path"] == req_path

    assert req_headers.items() <= dict(resp_content["headers"]).items()
    assert req_cookies.items() <= dict(resp_content["cookies"]).items()
    assert resp_content["body"] == body_content

    container.stop()
    container.wait()
    container.remove()


@pytest.mark.parametrize(
    "server_bind_port,status_code", [(18181, 200), (18182, 401), (18183, 502)]
)
def test_request_debugger_with_different_status_code(
    docker_client: docker.DockerClient,
    request_debugger_image: docker.models.images.Image,
    server_bind_port: int,
    status_code: int,
) -> None:
    container = docker_client.containers.run(
        image=request_debugger_image,
        detach=True,
        ports={str(server_bind_port): server_bind_port},
        environment={
            "SERVER_BIND_PORT": str(server_bind_port),
            "RESPONSE_STATUS_CODE": str(status_code),
        },
    )
    wait_for_container(container)

    resp = requests.get(
        f"http://localhost:{server_bind_port}/test-url-{random.randint(0, 1000)}"
    )
    assert resp.status_code == status_code
    assert resp.json() == hello_world_response_body

    container.stop()
    container.wait()
    container.remove()
