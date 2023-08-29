"""git module."""

import os

from etils import epath
import git

from ml_croissant._src.core.path import Path


def is_git_lfs_file(filepath: epath.Path) -> bool:
    """Returns whether a file a non-downloaded git-lfs file by checking its header.

    An optimization of this function would be to only read the file if there is a git
    repository in the distribution.
    """
    with open(filepath, "rb") as file:
        # Only read the first line of the file. In the future, this could be a problem,
        # e.g. if we accept *.txt files and the file starts with the same header.
        first_line = file.readline()
        if first_line.startswith(b"version https://git-lfs.github.com/spec"):
            return True
    return False


def download_git_lfs_file(file: Path):
    """Downloads a specific git-lfs file within its repo."""
    # Path(filepath="/tmp/full/path.json", fullpath="path.json")
    # => working_dir = "/tmp/full"
    working_dir = os.fspath(file.filepath).rsplit(os.fspath(file.fullpath))[0]
    repo = git.Git(working_dir)
    repo.execute(["git", "lfs", "pull", "--include", os.fspath(file.fullpath)])