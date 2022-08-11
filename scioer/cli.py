import typer
import sys
import yaml
import click
import scioer.config.load as load
import scioer.config.parse as parser
import os
import re
from typing import Optional
from pathlib import Path

from scioer.__version__ import __version__  # noqa: I900

import scioer.docker as docker

app = typer.Typer(
    name="Super app",
    help="some help here",
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)


# Global options get tossed in here
state = {"verbose": False}


def conf_callback(ctx: typer.Context, param: typer.CallbackParam, value: Path):

    if not value:
        ctx.default_map = ctx.default_map or {}  # Initialize the default map
        return None

    typer.echo(f"Loading config file:: {value}")
    configFiles = load.get_config_files(value)
    config = value or load.filter_config_files(configFiles)

    if config:
        typer.echo(f"Loading from config file: {config}")

        data = parser.load_config_file(config)

        ctx.default_map = ctx.default_map or {}  # Initialize the default map
        ctx.default_map.update(data)  # Merge the config dict into default_map

    return config


def version_callback(value: bool):
    if value:
        typer.echo(f"scioer CLI Version: {__version__}")
        raise typer.Exit()


configOption = typer.Option(
    None,
    "--config",
    "-c",
    metavar="FILE",
    dir_okay=False,
    resolve_path=True,
    readable=True,
    writable=True,
    callback=conf_callback,
    is_eager=True,
    help="Path to the yaml config file",
)


def load_course(config: dict, courseName: str, ask: bool = True):

    course = config.get(courseName, {})

    while ask and not course:
        typer.secho(
            f'Course "{courseName} is not found. use `scioer config` if you want to create it.',
            fg=typer.colors.YELLOW,
        )
        courses = [k for k in config.keys() if isinstance(config[k], dict)]
        courseName = click.prompt(
            "Course not found, did you mean one of:", type=click.Choice(courses)
        )

        course = config.get(courseName, {})

    if course:
        course["name"] = courseName
    return course


@app.command()
def start(
    ctx: typer.Context,
    name: str,
    pull: bool = False,
    configFile: Optional[Path] = configOption,
):
    """Function to start a new oer container"""

    client = docker.setup()

    config = ctx.default_map
    course = load_course(config, name)
    typer.secho(f"{course}", fg=typer.colors.YELLOW)

    if pull:
        typer.secho("pull", fg=typer.colors.GREEN)
        docker.fetch_latest(client, course["image"])

    docker.start_container(client, course)

    print(f"Hello {name}!")


@app.command()
def stop(
    ctx: typer.Context,
    name: str,
    keep: Optional[bool] = typer.Option(False, "--no-remove", "-k"),
    configFile: Optional[Path] = configOption,
):
    """Function to stop a running oer container"""

    client = docker.setup()

    config = ctx.default_map
    course = load_course(config, name, ask=False)
    typer.secho(f"{course}", fg=typer.colors.YELLOW)

    if course:
        docker.stop_container(client, course["name"], keep)
    else:
        typer.secho(f'Course "{name}" is not running.', fg=typer.colors.YELLOW)


@app.command()
def shell(
    ctx: typer.Context,
    name: str,
    configFile: Optional[Path] = configOption,
):
    """Function to drop the caller into the shell of the running oer container"""

    client = docker.setup()

    config = ctx.default_map
    course = load_course(config, name, ask=False)
    typer.secho(f"{course}", fg=typer.colors.YELLOW)

    if course:
        docker.attach(client, course["name"])
    else:
        typer.secho(f'Course "{name}" is not running.', fg=typer.colors.YELLOW)


@app.command()
def about(name: str):
    """Prints all the information about the running container"""

    print(f"bye {name}!")


def prompt_port(message: str, default: int) -> int:
    value = typer.prompt(
        message,
        default=default,
        type=int,
    )

    while value < 0 or value > 65535:
        typer.secho(
            f"`{value}` is not a valid port number.",
            fg=typer.colors.RED,
        )

        value = typer.prompt(
            message,
            default=default,
            type=int,
        )
    return value


def port_mapping(mapping: str) -> map:
    m = re.fullmatch("^(([0-9]{1,5})(?:\/(?:tcp|udp))?):([0-9]{1,5})$", mapping)
    if not m:
        typer.secho(
            f"Invalid port specification '{mapping}'",
            fg=typer.colors.RED,
        )
        return None

    container = m.group(1)
    srcPort = int(m.group(2))
    hostPort = int(m.group(3))

    if srcPort < 0 or srcPort > 65535 or hostPort < 0 or hostPort > 65535:
        typer.secho(
            "Invalid port number.",
            fg=typer.colors.RED,
        )
        return None

    return {container: hostPort}


def prompt_custom_ports() -> map:
    value = typer.prompt(
        "Custom ports to expose, in the form of 'container:host', or no input to skip ",
        default="",
        value_proc=lambda v: v.strip(),
        type=str,
    )

    mapping = port_mapping(value)
    if value != "" and not mapping:
        typer.secho(
            "Invalid port specification, please try again.",
            fg=typer.colors.RED,
        )

    mappings = mapping if mapping else {}

    while value != "":

        value = typer.prompt(
            "Custom ports to expose, in the form of 'container:host', or no input to skip ",
            default="",
            value_proc=lambda v: v.strip(),
            type=str,
        )

        mapping = port_mapping(value)
        if value != "" and not mapping:
            typer.secho(
                "Invalid port specification, please try again.",
                fg=typer.colors.RED,
            )
            continue

        if mapping:
            mappings = {**mappings, **mapping}

    return mappings


@app.command()
def config(
    ctx: typer.Context,
    configFile: Optional[Path] = configOption,
):
    """Prints all the information about the running container"""

    if not configFile:
        typer.echo(
            f"Config file not found, or not specified. Make sure that file exists or use `--config=FILE` to specify the file"
        )
        raise typer.Exit(1)

    print(f"config file: : {configFile}")

    config = ctx.default_map
    print(f"config contents: : {config}")

    course_name = typer.prompt("What's the name of the course?")
    safe_course_name = "".join(
        x for x in course_name.replace(" ", "_") if x.isalnum() or x == "_"
    )

    default_image = "marshallasch/oo-resource:latest"
    default_volume = os.path.join(load.get_data_directory()[0], safe_course_name)

    course = config.get(safe_course_name, {})

    docker_image = typer.prompt(
        "What docker image does the course use?",
        default=course.get("image", default_image),
    )
    course_storage = typer.prompt(
        "Where should the files for the course be stored?",
        default=course.get("volume", default_volume),
    )

    wiki_port = prompt_port(
        "Wiki port to expose, (0 to publish a random port)",
        3000,
    )

    jupyter_port = prompt_port(
        "Jupyter notebooks port to expose, (0 to publish a random port)",
        8888,
    )

    lectures_port = prompt_port(
        "Lectures port to expose, (0 to publish a random port)",
        8000,
    )

    ssh_port = prompt_port(
        "ssh port to expose, (0 to publish a random port)",
        2222,
    )

    mappings = {
        "3000": wiki_port,
        "8888": jupyter_port,
        "8000": lectures_port,
        "22": ssh_port,
        **prompt_custom_ports(),
    }

    ports = [f"{k}:{v}" for k, v in mappings.items()]

    config[safe_course_name] = {
        "image": docker_image,
        "volume": course_storage,
        "ports": ports,
    }

    parser.save_config_file(configFile, config)

    print(f"config file: '{course_name}', '{docker_image}', '{course_storage}' ")


@app.callback()
def setup(
    verbose: Optional[bool] = typer.Option(False, "--verbose", "-v"),
    version: Optional[bool] = typer.Option(
        None, "--version", "-V", callback=version_callback, is_eager=True
    ),
):
    if verbose:
        typer.echo("Will write verbose output")
        state["verbose"] = True


if __name__ == "__main__":
    app()
