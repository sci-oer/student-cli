from textwrap import indent
import typer
from collections.abc import Mapping

import sys
import yaml
import click
import platform
import scioer.config.load as load
import scioer.config.parse as parser
import os
import re
from typing import Optional
from pathlib import Path
import logging
from scioer.__version__ import __version__  # noqa: I900

import scioer.docker as docker

_LOGGER = logging.getLogger(__name__)

app = typer.Typer(
    name="Self Contained Interactive Open Educational Resource Helper",
    help=""" A CLI tool to help configure, start, stop course resources.

    \b
    Common usage commands:
    1. `scioer config`
        .... fill in the form
    2. `scioer start <course>`
    3. `scioer shell <course>`
    4. `scioer stop <course>`
    \f
    """,
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)


def conf_callback(ctx: typer.Context, param: typer.CallbackParam, value: Path):

    if value:
        value = os.path.realpath(os.path.expanduser(str(value)))

    configFiles = load.get_config_files(value)
    config = load.filter_config_files(configFiles)

    if not value and not config:
        config = configFiles[0]
        _LOGGER.debug(f"No config file found, using default: {config}")
    elif value and value != config:
        config = value
        _LOGGER.debug(f"Config file does not exist yet, using anyway: {config}")

    _LOGGER.debug(f"Loading config file:: {value}")
    if config:
        _LOGGER.debug(f"Loading from config file: {config}")

        data = parser.load_config_file(config)

        ctx.default_map = ctx.default_map or {}  # Initialize the default map
        ctx.default_map.update(data)  # Merge the config dict into default_map

    return config


def version_callback(value: bool):
    if value:
        typer.echo(f"scioer CLI Version: {__version__}")
        raise typer.Exit()


def verbose_callback(verbose: bool):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)


configOption = typer.Option(
    None,
    "--config",
    "-c",
    metavar="FILE",
    dir_okay=False,
    resolve_path=False,
    readable=True,
    writable=True,
    callback=conf_callback,
    is_eager=True,
    help="Path to the yaml config file",
)

courseNameArgument = typer.Argument(
    None, metavar="COURSE_NAME", help="The name of the course"
)


def load_course(config: Mapping, courseName: str, ask: bool = True):

    course = config.get(courseName, {})

    while ask and not course:

        if courseName:
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


def print_post_start_help(courseName):
    typer.secho(f"Started the {courseName} course resource", fg=typer.colors.GREEN)
    typer.secho(
        f"Login for the wiki: 'admin@example.com' 'password'", fg=typer.colors.GREEN
    )

    typer.echo("-----")
    typer.secho(f"To stop the course: scioer stop {courseName}", fg=typer.colors.YELLOW)
    typer.secho(
        f"To get a shell for the course: scioer shell {courseName}",
        fg=typer.colors.YELLOW,
    )
    typer.secho(
        f"To re-start the course: scioer start {courseName}", fg=typer.colors.YELLOW
    )
    typer.secho(
        f"To get information on the courses: scioer status", fg=typer.colors.YELLOW
    )


@app.command()
def start(
    ctx: typer.Context,
    name: Optional[str] = courseNameArgument,
    pull: bool = False,
    configFile: Optional[Path] = configOption,
):
    """Start a oer container"""

    client = docker.setup()

    config = ctx.default_map
    if not name and len(config.keys()) == 1:
        name = list(config.keys())[0]

    course = load_course(config, name)
    _LOGGER.debug("course content:", course)

    if course.get("auto_pull", False) or pull:
        typer.secho(
            f"Pulling the latest version of the {course['name']}...",
            fg=typer.colors.GREEN,
        )
        docker.fetch_latest(client, course["image"])

    typer.secho("Starting...", fg=typer.colors.GREEN)
    docker.start_container(client, course)
    print_post_start_help(course["name"])


@app.command()
def stop(
    ctx: typer.Context,
    name: Optional[str] = courseNameArgument,
    keep: Optional[bool] = typer.Option(False, "--no-remove", "-k"),
    configFile: Optional[Path] = configOption,
):
    """Stop a running course container"""

    client = docker.setup()

    config = ctx.default_map
    if not name and len(config.keys()) == 1:
        name = list(config.keys())[0]

    course = load_course(config, name, ask=False)
    typer.secho(f"{course}", fg=typer.colors.YELLOW)

    if course:
        docker.stop_container(client, course["name"], keep)
    else:
        typer.secho(f'Course "{name}" is not running.', fg=typer.colors.YELLOW)


@app.command()
def shell(
    ctx: typer.Context,
    name: str = courseNameArgument,
    configFile: Optional[Path] = configOption,
):
    """Start a shell in a running course container"""

    client = docker.setup()

    config = ctx.default_map
    if not name and len(config.keys()) == 1:
        name = list(config.keys())[0]

    course = load_course(config, name, ask=False)
    typer.secho(f"{course}", fg=typer.colors.YELLOW)

    if course:
        docker.attach(client, course["name"])
    else:
        typer.secho(f'Course "{name}" is not running.', fg=typer.colors.YELLOW)


def print_container(container):
    indent = 2
    print(f"Course: {container.name[7:]} ({container.status})")

    print(f'{" " * indent }Ports:')
    ports = list(container.ports.items())
    if ports:
        for port in ports[:-1]:
            print(f'{" " * indent }├── {port[1][0]["HostPort"]} -> {port[0][:-4]}')
        port = ports[-1]
        print(f'{" " * indent }└── {port[1][0]["HostPort"]} -> {port[0][:-4]}')

    print(f'{" " * indent }Volumes:')
    volumes = [v for v in container.attrs["Mounts"] if v["Type"] == "bind"]

    home = (
        os.environ["HOMEPATH"] if platform.system() == "Windows" else os.environ["HOME"]
    )
    if volumes:
        for volume in volumes[:-1]:
            hostPath = volume["Source"].replace(home, "~")
            print(f'{" " * indent }├── {hostPath} as {volume["Destination"]}')

        volume = volumes[-1]
        hostPath = volume["Source"].replace(home, "~")
        print(f'{" " * indent }└── {hostPath} as {volume["Destination"]}')


@app.command()
def status(
    ctx: typer.Context,
    configFile: Optional[Path] = configOption,
):
    """Prints all the information about the running container"""
    client = docker.setup()

    config = ctx.default_map
    names = list(config.keys())

    # containers = client.containers.list(all=True)
    # containers = [c for c in containers if c.name.replace('scioer_', '') in names ]

    filtered = []
    notRunning = []
    for n in names:
        try:
            c = client.containers.get(f"scioer_{n}")
            filtered.append(c)
        except:
            notRunning.append(n)

    for c in filtered:
        print_container(c)

    for n in notRunning:
        print(f"Course: {n} (Not Running)")


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


def port_mapping(mapping: str) -> Mapping:
    m = re.fullmatch("^(([0-9]{1,5})(?:/(?:tcp|udp))?)(?::([0-9]{1,5}))?$", mapping)
    if not m:
        return {}

    container = m.group(1)
    srcPort = int(m.group(2))
    hostPort = int(m.group(3) or m.group(2))

    if srcPort < 0 or srcPort > 65535 or hostPort < 0 or hostPort > 65535:
        typer.secho(
            "Invalid port number.",
            fg=typer.colors.RED,
        )
        return {}

    return {container: hostPort}


def prompt_custom_ports() -> Mapping:
    value = typer.prompt(
        "Custom ports to expose, in the form of 'container[:host]', or no input to skip ",
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

    mappings = mapping

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
    """Setup a new course resource, or edit an existing one"""

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
    default_volume = os.path.join(os.path.expanduser("~/Desktop"), safe_course_name)

    course = config.get(safe_course_name, {})

    docker_image = typer.prompt(
        "What docker image does the course use?",
        default=course.get("image", default_image),
    )

    auto_pull = typer.confirm(
        "Automatically fetch new versions", default=course.get("auto_pull", False)
    )

    course_storage = typer.prompt(
        "Where should the files for the course be stored?",
        default=course.get("volume", default_volume),
    )

    useDefaults = typer.confirm("Use the default ports", default=True)

    mappings = {
        "3000": 3000,
        "8888": 8888,
        "8000": 8000,
        "22": 2222,
    }

    if not useDefaults:
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

        customPorts = prompt_custom_ports()

        mappings = {
            "3000": wiki_port,
            "8888": jupyter_port,
            "8000": lectures_port,
            "22": ssh_port,
            **customPorts,
        }

    ports = [f"{k}:{v}" for k, v in mappings.items()]

    config[safe_course_name] = {
        "image": docker_image,
        "volume": os.path.realpath(os.path.expanduser(course_storage)),
        "ports": ports,
        "auto_pull": auto_pull,
        "public": False,
    }

    parser.save_config_file(configFile, config)


@app.callback()
def setup(
    verbose: Optional[bool] = typer.Option(
        False, "--verbose", "-v", callback=verbose_callback, is_eager=True
    ),
    version: Optional[bool] = typer.Option(
        None, "--version", "-V", callback=version_callback, is_eager=True
    ),
):
    pass


if __name__ == "__main__":
    app()
