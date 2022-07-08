import logging
import os
import yaml
import typer


def load_config_file(file):

    if not os.path.isfile(file):
        return {}

    try:
        with open(file, "r") as f:
            data = yaml.safe_load(f)
    except Exception as ex:
        raise typer.BadParameter(str(ex))

    return data or {}


def save_config_file(file, config):
    try:
        with open(file, "w") as f:
            data = yaml.dump(config)
            f.write(data)
    except Exception as ex:
        raise "Failed to write to the config"
