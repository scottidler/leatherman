#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sh
import pwd
import sys
import glob

from doit import get_var
from pathlib import Path
from subprocess import check_call, check_output, CalledProcessError, PIPE

from leatherman.cfg import CFG

LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

DOIT_CONFIG = {"default_tasks": ["pull", "deploy", "count"], "verbosity": 2}

SPACE = " "
NEWLINE = "\n"


def envs(sep):
    return sep.join(
        [
            f"APP_PROJNAME={CFG.APP_PROJNAME}",
            f"APP_DEPENV={CFG.APP_DEPENV}",
            f"APP_VERSION={CFG.APP_VERSION}",
            f"APP_BRANCH={CFG.APP_BRANCH}",
            f"APP_DEPENV={CFG.APP_DEPENV}",
            f"APP_REVISION={CFG.APP_REVISION}",
            f"APP_REMOTE_ORIGIN_URL={CFG.APP_REMOTE_ORIGIN_URL}",
            f"APP_INSTALLPATH={CFG.APP_INSTALLPATH}",
        ]
    )


def docstr_format(*args, **kwargs):
    def wrapper(func):
        func.__doc__ = func.__doc__.format(*args, **kwargs)
        return func

    return wrapper


class UnknownPkgmgrError(Exception):
    def __init__(self):
        super(UnknownPkgmgrError, self).__init__("unknown pkgmgr!")


def check_hash(program):
    try:
        check_call(f"hash {program}", shell=True, stdout=PIPE, stderr=PIPE)
        return True
    except CalledProcessError:
        return False


def get_pkgmgr():
    if check_hash("dpkg"):
        return "deb"
    elif check_hash("rpm"):
        return "rpm"
    elif check_hash("brew"):
        return "brew"
    raise UnknownPkgmgrError


def pyfiles(path, exclude=None):
    pyfiles = set(Path(path).rglob("*.py")) - set(
        Path(exclude).rglob("*.py") if exclude else []
    )
    return [pyfile.as_posix() for pyfile in pyfiles]


def task_count():
    """
    use the cloc utility to count lines of code
    """
    excludes = ["dist", "venv", "__pycache__", "*.egg-info"]
    excludes = "--exclude-dir=" + ",".join(excludes)
    scandir = os.path.dirname(__file__)
    return {
        "actions": [f"cloc {excludes} {scandir}"],
        "uptodate": [lambda: not check_hash("cloc")],
    }


def task_noroot():
    """
    make sure script isn't run as root
    """
    then = 'echo "   DO NOT RUN AS ROOT!"; echo; exit 1'
    bash = f"if [[ $(id -u) -eq 0 ]]; then {then}; fi"
    return {"actions": [f"bash -c '{bash}'"]}


def task_pull():
    """
    do a safe git pull
    """
    submods = (
        check_output("git submodule status | awk '{print $2}'", shell=True)
        .decode("utf-8")
        .split()
    )
    test = "`git diff-index --quiet HEAD --`"
    pull = "git pull --rebase"
    update = "git submodule update --remote"
    dirty = "echo \"refusing to '{cmd}' because the tree is dirty\""
    dirty_pull, dirty_update = [dirty.format(cmd=cmd) for cmd in (pull, update)]

    yield {
        "name": "mozilla-it/props-bot",
        "actions": [f"if {test}; then {pull}; else {dirty_pull}; exit 1; fi"],
    }

    for submod in submods:
        yield {
            "name": submod,
            "actions": [
                f"cd {submod} && if {test}; then {update}; else {dirty_update}; exit 1; fi"
            ],
        }


def task_test():
    """
    run tox in tests/
    """
    return {"task_dep": ["noroot"], "actions": [f"cd {CFG.APP_REPOROOT} && tox"]}


def task_rmcache():
    """
    recursively delete python cache files
    """
    rmrf = 'rm -rf "{}" \;'
    names_types = {
        "__pycache__": "d",
        ".pytest_cache": "d",
        "node_modules": "d",
        ".serverless": "d",
        ".venv": "d",
        ".eggs": "d",
        ".tox": "d",
        "*.pyc": "f",
        ".coverage": "f",
        ".doit.db": "f",
    }
    return {
        "actions": [
            f"sudo find {CFG.APP_REPOROOT} -depth -name {name} -type {type} -exec {rmrf}"
            for name, type in names_types.items()
        ]
    }


def task_tidy():
    """
    delete cached files
    """
    TIDY_FILES = [".doit.db", "venv/", ".pytest_cache/"]
    return {
        "actions": [
            "rm -rf " + " ".join(TIDY_FILES),
            'find . | grep -E "(__pycache__|\.pyc$)" | xargs rm -rf',
        ]
    }


if __name__ == "__main__":
    print("should be run with doit installed")
    import doit

    doit.run(globals())
