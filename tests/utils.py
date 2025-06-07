import time

import docker
import docker.errors
import docker.models
import docker.models.containers
import docker.models.images
import pytest


def build_image(
    context_path: str, image_tag: str, docker_client: docker.client.DockerClient
) -> docker.models.images.Image:
    try:
        print(f"Building Docker image '{image_tag}' from '{context_path}'...")
        image, build_logs = docker_client.images.build(
            path=context_path,
            tag=image_tag,
            nocache=True,
            pull=True,
            rm=True,
            forcerm=True,
        )
        print(f"Image built successfully: {image.id}")

        for build_log_line in build_logs:
            if isinstance(build_log_line, dict) and "stream" in build_log_line:
                stream = build_log_line["stream"]
                if isinstance(stream, str):
                    print(stream.strip())

        return image
    except docker.errors.BuildError as e:
        print(f"Error building image: {e}")
        for err_log_line in e.build_log:
            if "stream" in err_log_line:
                print(err_log_line["stream"].strip())
            else:
                print(err_log_line)
        raise e


def wait_for_container(
    container: docker.models.containers.Container,
) -> None:
    timeout = 30
    interval = 5
    start_time = time.time()

    print(f"Waiting for container {container.id} to start running")
    while time.time() - start_time < timeout:
        container.reload()
        if container.attrs["State"]["Status"] == "running":
            print(f"Container {container.id} running")
            break
        print(f"Container {container.id} not yet running")
        time.sleep(interval)

    print("Waiting for container to become healthy")
    while time.time() - start_time < timeout:
        container.reload()
        if "Health" not in container.attrs["State"]:
            print(
                f"Container {container.id} assumed to be healthy (no health probe configured)"
            )
            return
        elif container.attrs["State"]["Health"]["Status"] == "healthy":
            print(f"Container {container.id} healthy")
            return
        print(f"Container {container.id} not yet healthy")
        time.sleep(interval)

    pytest.fail(f"Container {container.id} did not started up {timeout} seconds")
