import typer
import sys

app = typer.Typer(
    name="Super app",
    help="some help here",
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)


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


def main():
    app()


if __name__ == "__main__":
    sys.exit(main())
