import logging
import os
import sys


def get_config_files(file=None, appname="scioer", **kwargs):
    """
    This will get all the potential file paths on the system for where the config file
    can be

    This will also handle the --config overrides
    """
    files = []
    if file:
        files.append(file)

    if sys.platform == "win32":
        files.append(os.path.join(os.getenv("APPDATA"), appname, "config.yaml"))
        files.append(os.path.join(os.getenv("APPDATA"), appname, "config.yml"))

        files.append(
            os.path.join(os.getenv("LOCALAPPDATA"), appname, "config.yaml")
        )  # not on XP
        files.append(
            os.path.join(os.getenv("LOCALAPPDATA"), appname, "config.yml")
        )  # not on XP

        files.append(
            os.path.join(os.getenv("PROGRAMDATA"), appname, "config.yaml")
        )  # not on XP
        files.append(
            os.path.join(os.getenv("PROGRAMDATA"), appname, "config.yml")
        )  # not on XP
    else:
        XDG_CONFIG_HOME = os.getenv(
            "XDG_CONFIG_HOME", os.path.expanduser(os.path.join("~", ".config"))
        )
        XDG_CONFIG_DIRS = os.getenv("XDG_CONFIG_DIRS", "/etc/xdg")

        files.append(os.path.expanduser(f"./config.yaml"))
        files.append(os.path.expanduser(f"./config.yml"))

        # treat all other platforms as *nix and conform to XDG basedir spec
        files.append(os.path.expanduser(os.path.join("~", f".{appname}.yaml")))
        files.append(os.path.expanduser(os.path.join("~", f".{appname}.yml")))

        files.append(os.path.join(XDG_CONFIG_HOME, appname, "config.yaml"))
        files.append(os.path.join(XDG_CONFIG_HOME, appname, "config.yml"))

        files.append(os.path.join(XDG_CONFIG_DIRS, appname, "config.yaml"))
        files.append(os.path.join(XDG_CONFIG_DIRS, appname, "config.yml"))

    return files


def filter_config_files(files=[], ignore_config=False, **kwargs):
    """
    This will take a list of file paths and return the first one that exists from the list.
    If the ignore config option is set then it will return None even if files do exist.
    """
    if ignore_config:
        return None

    file = None
    for f in files:
        if os.path.isfile(f):
            file = f
            break

    return file
