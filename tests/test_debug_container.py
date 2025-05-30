import pytest


@pytest.fixture(scope="module")
def debug_container_image(docker_client):
    image, build_logs = docker_client.images.build(
        path="../components/debug-container/",
        tag="debug-container:test",
        nocache=True,
        rm=True,
        forcerm=True,
        pull=True,
    )
    for line in build_logs:
        print(line)
    yield image
    docker_client.images.remove(image.id, force=True)


def test_debug_container(docker_client, debug_container_image):
    container = docker_client.containers.run(
        image=debug_container_image.id, detach=True
    )

    container.stop()
    container.wait()
    container.remove()
