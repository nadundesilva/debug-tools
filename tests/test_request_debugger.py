import pytest


@pytest.fixture(scope="module")
def request_debugger_image(docker_client):
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


def test_request_debugger(docker_client, request_debugger_image):
    server_bind_port = 18080

    container = docker_client.containers.run(
        image=request_debugger_image.id,
        detach=True,
        ports={server_bind_port: server_bind_port},
        environment={"SERVER_BIND_PORT": server_bind_port},
    )

    container.stop()
    container.wait()
    container.remove()
