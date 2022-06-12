import logging
import os
import sys
import yaml
import typer

_LOGGER = logging.getLogger(__name__)


def load_config_file(file):
    conf = {}
    try:
        with open(file, "r") as f:
            data = yaml.safe_load(f)
    except Exception as ex:
        raise typer.BadParameter(str(ex))

    return data
