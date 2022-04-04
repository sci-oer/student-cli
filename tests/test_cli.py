from typer.testing import CliRunner

from scioer.cli import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    # assert "Hello name" in result.stdout


# assert "Let's have a coffee in Berlin" in result.stdout
