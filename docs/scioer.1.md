---
title: SCIOER
section: 1
header: User Manual
footer: scioer 0.1.0
date: August 5, 2022
---

# NAME
scioer - Student runner for launching and interacting with self-contained open educational courses

# SYNOPSIS
**scioer** [*OPTION*]...

# DESCRIPTION
**scioer** A python script that is designed to simplify running the course docker containers for the
Self-Contained Open Educational Resource courses.

# OPTIONS
**-h**
: display help message

**-c --config=FILE**
: specify the location of the configuration file to use

# FILES
- A persistent config file is stored in `~/.config/scioer/config.yml`
- The course's persistent files will be stored in the XDG data directory `~/.local/share/scioer/<name>`

# EXAMPLES
**scioer config**
: Creates a new configuration entry for a course

# EXIT STATUS
1 if there was an error, 0 otherwise.

# AUTHORS
Written by Marshall Asch.

# BUGS
Submit bug reports online at: <https://github.com/sci-oer/student-cli/issues>

# SEE ALSO
Full documentation and sources at: <https://github.com/sci-oer/student-cli>