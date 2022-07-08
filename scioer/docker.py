import docker
import logging
import os
import typer
import subprocess


_LOGGER = logging.getLogger(__name__)


def fetch_latest(client: docker.client, repository, **kwargs):
    _LOGGER.info(
        f'pulling latest version of the "{repository}" docker image, this may take a while...'
    )
    client.images.pull(repository)
    _LOGGER.info("Done pulling the latest docker image")


def start_container(client: docker.client, course: dict, **kwargs):

    uid = os.getuid()
    gid = os.getgid()

    _LOGGER.info(f"starting `{course['image']}` container as `{course['name']}`...")
    container = client.containers.run(
        course["image"],
        publish_all_ports=True,
        name=f'scioer_{course["name"]}',
        tty=True,
        detach=True,
        user=f"{uid}:{gid}",
        volumes=[f"{course['volume']}:/course"],
    )

    return container


def stop_container(client: docker.client, courseName: str, keep: bool, **kwargs):
    _LOGGER.info("stopping docker container...")

    try:
        container = client.containers.get(f"scioer_{courseName}")
    except:
        typer.secho(
            f"Container for course '{courseName}' is not running",
            fg=typer.colors.YELLOW,
        )
        return

    container.stop()
    typer.secho(
        f"Container for course '{courseName}' is has been stopped",
        fg=typer.colors.GREEN,
    )

    if not keep:
        delete_container(container)


def attach(client: docker.client, courseName: str, **kwargs):
    _LOGGER.info("attaching to docker container...")

    try:
        container = client.containers.get(f"scioer_{courseName}")
    except:
        typer.secho(
            f"Container for course '{courseName}' is not running",
            fg=typer.colors.YELLOW,
        )
        return

    typer.echo("Starting interactive shell in the container, type `exit` to quit.")
    os.system(f"docker exec -it scioer_{courseName} bash")


def delete_container(container, **kwargs):
    _LOGGER.info("Deleting container...")
    container.remove()


def setup():
    client = docker.from_env()

    return client
