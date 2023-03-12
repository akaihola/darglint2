"""Containts the repository class representing a git repo."""

import os
import subprocess
import tempfile
from typing import Dict, Iterator


class Repository(object):
    """Represents a git repository containing a python project."""

    def __init__(self, path: str) -> None:
        self.files: Dict[str, str] = dict()
        try:
            with tempfile.TemporaryDirectory() as tempdir:
                subprocess.run(["git", "clone", path, tempdir])
                for filename in self._get_files(tempdir):
                    try:
                        with open(filename, "r") as fin:
                            self.files[filename] = fin.read()
                    except Exception as ex:
                        print(f"Unable to read from file {filename}: {ex}")
        except Exception as ex:
            print(f"Unable to create temporary directory: {ex}")

    def _get_files(self, tempdir: str) -> Iterator[str]:
        for dirpath, _, filenames in os.walk(tempdir):
            for filename in filenames:
                if filename.endswith(".py"):
                    yield os.path.join(dirpath, filename)

    @property
    def python_files(self) -> Dict[str, str]:
        return self.files
