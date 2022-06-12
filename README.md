# Student CLI
![GitHub](https://img.shields.io/github/license/sci-oer/student-cli?style=plastic)


Wrapper script to help start and stop the sci-oer docker container.


## System Requirements
[System Requirements]: #system-requirements

## Installation

The following sections cover the various methods to set up the sci-oer student cli.

### Installing from PyPI or GitHub
[Installing from PyPI or GitHub]: #installing-from-pypi-or-github

[pip] can be used to install scioer from the Python Package Index (PyPI).
It will also install the necessary Python libraries.


```bash
# the latest stable version
python3 -m pip3 install scioer

# a specific version (e.g. 1.0.0)
python3 -m pip3 install scioer==1.0.0
```

If [git] is installed, pip can also install the latest snapshot of the official
scioer source code repository on GitHub.

```bash
# the latest snapshot of the official source code repository (requires git)
python3 -m pip3 install git+https://github.com/sci-oer/student-cli#egg=scioer
```

[git]: https://git-scm.com/
[pip]: https://pip.pypa.io/en/stable/


### Working Locally

When working on the project itself, it is sometimes useful to set up a local development environment, where it is possible to directly run the CLI and the test suite, without building and installing a local package.

For this, start by installing [git] and any system-level dependencies mentioned in [System Requirements]. Then, clone the repository and change into the created directory:

```bash
git clone https://github.com/sci-oer/student-cli
cd student-cli
```

Optionally, set up a [virtual environment].

Finally, if the necessary Python build, test and runtime libraries are not already installed on the environment (virtual or global), manually install them:

```bash
pip3 install .
```

At this point, the environment is set up. To run the test suite, execute:

```bash
python3 -m pytest
```
To run the CLI directly, without building and installing a local package, execute:

```bash
python3 -m scioer [arguments]
```
And to install scioer into the environment:

```bash
pip3 install .
```


#### Creating a virtual environment
[Creating a virtual environment]: #creating-a-virtual-environment

Setting up a virtual environment is an optional step.  Even so, installing
Python packages directly in the global environment is not generally advised.

Instead, it is usual to first set up a [virtual environment]:

```bash
# create virtual enviroment at <path>
python -m venv <path>
```

Once set up, the virtual environment can be activated on the current shell
(more information in the [official documentation][virtual environment]).
Alternatively, the virtual environment can also be used directly, without
activation, by prefixing all `python` and `pip` invocations with the
environment's bin directory.

```bash
# Linux/macOS/BSDs (POSIX)
<path>/bin/python [arguments]
<path>/bin/pip [arguments]

# Windows
<path>\Scripts\python [arguments]
<path>\Scripts\pip [arguments]
```

[virtual environment]: https://docs.python.org/3/library/venv.html

## The Command Line Interface

The complete list of commands and options can be found in `sci-oer --help` and in the man page, but the following topics cover the most common operations.

Brackets `[ ]`, parenthesis `( )`, less than/greater than `< >` and ellipsis `...` are used to describe, respectively, optional, required, positional and repeating elements.
Example commands are prefixed with a number sign `#`, which also serves to indicate that on Linux root permissions (or suitable group membership) may be required.

The `--verbose` option will print some extra information, like automatically made adjustments to user-provided settings.
And if there is a problem, the `--debug` flag will make `sci-oer` output more information to help identify its cause; be sure to include this when opening a new issue.

## Additional Documentation

** TODO **

## Related projects
[Related projects]: #related-projects

### [sci-oer/oo-resources](https://github.com/sci-oer/oo-resources)

The base open educational resource Docker image.


### [sci-oer/automated-builder](https://github.com/sci-oer/automated-builder)

The cli tool and Docker image to create customized versions of the base oo-resource image.

## Contributing

Contributions are more than welcome on this project!
Check out the list of [issues](https://github.com/sci-oer/student-cli) for tasks that you want to try implementing.

Check out the [CONTRIBUTING.md](.github/CONTRIBUTING.md) guide for more information about how to contribute to the project.


## Issues Getting Support

Like any software tool things go wrong and sometimes there are issues.
This section presents some common issues that can arise and solutions to resolve the issue.
If these topics are not able to help you resolve the issue feel free to open a [support request], and we be happy to help.

[support request]: https://github.com/sci-oer/student-cli/issues/new

### I did some work in the container, and now I can't find my files

If Any files that you edited in the `/course` directory within the container will be saved to your computer in one of the following locations:

1. `$XDG_DATA_HOME/scioer/<container name>`
2. `$HOME/.local/share/scioer/<container name>`

Or it will be saved to the location that was specified through the config file or the cli flags that were specified when the container was started.

If your file was not created under the `/course` directory then make sure that you move it into that folder _before_ the container is stopped and removed, otherwise it will be permanently lost.

Do not work on any of your files in the `~` directory from within the container those files will be lost when the container is recreated.

### Permission denied error when trying to edit the files

If you are trying to access the files from your computer that you created or edited from within the container and are now getting permission denied errors.
When this happens it is likely because the container is running as a different user.
This can be checked by running the following commands:

```bash
$ id -u    # This will print the user id of the current user
501

$ id -g    # This will print the group id of the current user
20

$ ls -nd <path to mount >   # The 3rd and 4th columns will be the user id and group id that own the files
drwxr-xr-x  14 501  20  448  3 Apr 13:33 .
                 ^   ^
                 |   |
                 | group Id
                User Id
```

If these do not match you can `sudo chown -R <userId>:<groupId> <volume dir>` to change the ownership of the files.
Then you will need to update the configuration of `sci-oer` to launch the container as the correct user.

### I started the container and all of my work seems to be gone

Make sure that you save all of your work in the `/course` directory, so it can be saved to the persistent volume on your computer.
If you did not save it to the correct spot and the container has not yet been removed then you can still enter the container and move the files, so they can be saved.

### I went to `localhost:3000`, and it says there is no page

- Did you double-check that the container is running? `docker ps`
- Is `3000` the correct port? `docker ps` or `docker inspect <container name>`

