from typing import Container
import docker
import logging
import os
import typer
import subprocess
import re
from collections.abc import Mapping
import sys

_LOGGER = logging.getLogger(__name__)


def port_mapping(mapping: str, public: bool) -> Mapping:
    m = re.fullmatch("^(([0-9]{1,5})(?:/(?:tcp|udp))?):([0-9]{1,5})$", mapping)
    if not m:
        typer.secho(
            f"Invalid port specification '{mapping}'",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    container = m.group(1)
    srcPort = int(m.group(2))
    hostPort = int(m.group(3))

    if srcPort < 0 or srcPort > 65535:
        typer.secho(
            f"Invalid port number '{srcPort}'",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    if hostPort < 0 or hostPort > 65535:
        typer.secho(
            f"Invalid port number '{srcPort}'",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    host = "0.0.0.0" if public else "127.0.0.1"
    return {container: (host, hostPort) if hostPort != 0 else None}


def port_map(portList: list, public: bool) -> dict:

    portMapping = {}
    for p in portList:
        portMapping.update(port_mapping(p, public))

    return portMapping


def port_env_mapping(mapping: str) -> str:
    m = re.fullmatch("^(([0-9]{1,5})(?:/(?:tcp|udp))?):([0-9]{1,5})$", mapping)
    if not m:
        typer.secho(
            f"Invalid port specification '{mapping}'",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    srcPort = int(m.group(2))
    hostPort = int(m.group(3))

    if srcPort < 0 or srcPort > 65535:
        typer.secho(
            f"Invalid port number '{srcPort}'",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    if hostPort < 0 or hostPort > 65535:
        typer.secho(
            f"Invalid port number '{srcPort}'",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    return f"PORT_{srcPort}={hostPort}"


def port_env_map(portList: list) -> list:
    return [port_env_mapping(p) for p in portList]


def fetch_latest(client: docker.client, repository, **kwargs):
    _LOGGER.info(
        f'pulling latest version of the "{repository}" docker image, this may take a while...'
    )

    oldImage = None
    try:
        oldImage = client.images.get(repository)
    except:
        pass
    image = client.images.pull(repository)
    _LOGGER.info("Done pulling the latest docker image")

    if oldImage and oldImage.id != image.id:
        oldImage.remove()
    return image


def create_container(client: docker.client, course: dict, **kwargs):
    try:
        _LOGGER.info(f"checking if image {course['image']} exists locally...")
        i = client.images.get(course["image"])
        _LOGGER.info("Image exists locally.")
    except docker.errors.ImageNotFound as e:
        _LOGGER.info("Image is not found, start will take a while to pull first.")
        typer.secho(
            f"Course image needs to be downloaded, this may take a while...",
            fg=typer.colors.YELLOW,
        )

    _LOGGER.info(f"starting `{course['image']}` container as `{course['name']}`...")
    try:
        container = client.containers.run(
            course["image"],
            ports=port_map(course["ports"], course.get("public", False)),
            environment=port_env_map(course["ports"]),
            name=f'scioer_{course["name"]}',
            hostname=course["name"],
            tty=True,
            detach=True,
            volumes=[f"{course['volume']}:/course"],
        )
    except docker.errors.ImageNotFound as e:
        _LOGGER.error("Image not found.", e)
        typer.secho(
            f"Course image not found, check the config file that the image name is correct.",
            fg=typer.colors.RED,
        )
        sys.exit(1)
    except docker.errors.APIError as e:
        _LOGGER.debug(f"Failed to start the container: {e}")

        if e.status_code == 409:
            typer.secho(
                f"Container name already in use. Please delete the container with the name `scioer_{course['name']}` before trying again.",
                fg=typer.colors.RED,
            )
            sys.exit(2)
        elif e.status_code == 404:
            typer.secho(
                f"Course image not found, check the config file that the image name is correct.",
                fg=typer.colors.RED,
            )
            sys.exit(3)

        typer.secho(
            f"Unknown error, aborting...",
            fg=typer.colors.RED,
        )
        sys.exit(4)

    return container


def start_container(client: docker.client, course: dict, **kwargs):

    container = None
    try:
        container = client.containers.get(f'scioer_{course["name"]}')
        _LOGGER.info(f'Container for `scioer_{course["name"]}` already exists.')

        if container.status == "running":
            _LOGGER.info("Container is already running, not restarting.")
        else:
            _LOGGER.info("Restarting container")
            container.start()
            _LOGGER.info("Successfully started")

    except:
        _LOGGER.info(f'Container `scioer_{course["name"]}` does not exist, starting...')
        container = create_container(client, course)

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

    os.system(f"docker exec -it scioer_{courseName} cat /scripts/motd.txt")

    typer.echo("Starting interactive shell in the container, type `exit` to quit.")
    os.system(f"docker exec -it scioer_{courseName} bash --login")


def delete_container(container, **kwargs):
    _LOGGER.info("Deleting container...")
    container.remove()


def setup():
    client = None
    try:
        client = docker.from_env()
    except:
        typer.secho(
            "failed to connect to docker, check that Docker is running on the host.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    return client
