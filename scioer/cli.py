import typer
import sys
import yaml
import click
import scioer.config.load as load
import scioer.config.parse as parser
import os
from typing import Optional

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


def conf_callback(ctx: typer.Context, param: typer.CallbackParam, value: str):
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


@app.command()
def test(
    config: str = typer.Option("", callback=conf_callback, is_eager=True),
    opt1: str = typer.Option(...),
    opt2: str = typer.Option("hello"),
):
    """Function to start a new oer container"""

    if state["verbose"]:
        typer.secho("verbose", fg=typer.colors.GREEN)

    print(f"Hello {opt1} - {opt2} - {config}!")


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
    pull: bool = True,
    configFile: str = typer.Option(
        "", "--config-file", callback=conf_callback, is_eager=True
    ),
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
    configFile: str = typer.Option("", callback=conf_callback, is_eager=True),
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
    configFile: str = typer.Option("", callback=conf_callback, is_eager=True),
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


@app.command()
def config(
    ctx: typer.Context,
    configFile: str = typer.Option(
        "", "--config-file", metavar="FILE", callback=conf_callback, is_eager=True
    ),
):
    """Prints all the information about the running container"""

    if not configFile:
        typer.echo(
            f"Config file not found, or not specified. Make sure that file exists or use `--config-file=FILE` to specify the file"
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

    config[safe_course_name] = {"image": docker_image, "volume": course_storage}

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
