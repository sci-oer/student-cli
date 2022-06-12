import typer
import sys
import yaml
import click
import scioer.config.load as load
import scioer.config.parse as parser

from scioer.__version__ import __version__  # noqa: I900


app = typer.Typer(
    name="Super app",
    help="some help here",
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)


# Global options get tossed in here
state = {"verbose": False}


def conf_callback(ctx: typer.Context, param: typer.CallbackParam, value: str):
    typer.echo(f"Loading config file")
    configFiles = load.get_config_files(value)
    config = load.filter_config_files(configFiles)

    if config:
        typer.echo(f"Loading from config file: {config}")

        data = parser.load_config_file(config)

        ctx.default_map = ctx.default_map or {}  # Initialize the default map
        ctx.default_map.update(data)  # Merge the config dict into default_map

    return config


@app.command()
def test(
    config: str = typer.Option("", callback=conf_callback, is_eager=True),
    opt1: str = typer.Option(...),
    opt2: str = typer.Option("hello"),
):
    """Function to start a new oer container"""

    if state["verbose"]:
        typer.echo("verbose", color=typer.colors.GREEN)

    print(f"Hello {opt1} - {opt2} - {config}!")


@app.command()
def start(name: str):
    """Function to start a new oer container"""

    print(f"Hello {name}!")


@app.command()
def stop(name: str):
    """Function to stop a running oer container"""

    print(f"bye {name}!")


@app.command()
def shell(name: str):
    """Function to drop the caller into the shell of the running oer container"""

    print(f"bye {name}!")


@app.command()
def about(name: str):
    """Prints all the information about the running container"""

    print(f"bye {name}!")


@app.callback()
def setup(verbose: bool = False):
    if verbose:
        typer.echo("Will write verbose output")
        state["verbose"] = True


def main():
    app()


if __name__ == "__main__":
    sys.exit(main())
