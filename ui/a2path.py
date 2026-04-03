"""
All things file system paths.
"""
from pathlib import Path

import os
import typing


def iter_dirs(path: str) -> typing.Iterator[DirObj]:
    """Iterate over directory items in a path. Yield DirObj."""
    item = DirObj()
    if not os.path.isdir(path):
        return

    for this in os.scandir(path):
        if not this.is_dir():
            continue
        item._set_path(this.path)
        yield item


def get_dir_names(path: str) -> list[str]:
    """From path return list of subfolder names."""
    if not os.path.isdir(path):
        return []
    return [item.name for item in os.scandir(path) if item.is_dir()]


def get_dir_names_except(path: str, pattern: str) -> list[str]:
    """From path return list of subfolder names that do not match a given pattern."""
    if not os.path.isdir(path):
        return []
    from fnmatch import fnmatch

    return [i.name for i in os.scandir(path) if i.is_dir() and not fnmatch(i.name, pattern)]


def remove_dir(path: str) -> None:
    """
    Safely delete a folder.

    Moves the folder to temp with random name then deletes it.
    Instead of deleting the single items directly this will already
    correctly fail moving to temp if ANY of the containing items is locked.
    So there is no other safeguard needed.
    """
    if not os.path.isdir(path):
        return

    import shutil

    trash_path = temp_path()
    os.rename(path, trash_path)
    shutil.rmtree(trash_path)


def temp_path(prefix: str = '', ext: str = '') -> str:
    import uuid

    if ext and not ext.startswith('.'):
        ext = '.' + ext
    try_path = None
    while try_path is None or os.path.exists(try_path):
        try_path = os.path.join(os.getenv('TEMP', ''), prefix + str(uuid.uuid4()) + ext)
    return try_path


def iter_files(path: str) -> typing.Iterator[FileObj]:
    """Loop over all files in a directory."""
    if not os.path.isdir(path):
        return
    item = FileObj()
    for this in os.scandir(path):
        if not this.is_file():
            continue
        item._set_path(this.path)
        yield item


def get_file_names(path: str) -> list[str]:
    """Get list of all file names in given directory `path`."""
    return [item.name for item in os.scandir(path) if item.is_file()]


def iter_types(path, types: list[str] | tuple[str, ...]) -> typing.Iterator[FileObj]:
    """Loop over files of given types in a directory."""
    item = FileObj()
    for this in os.scandir(path):
        if not this.is_file():
            continue
        item._set_path(this.path)
        if item.is_type(types):
            yield item


def add_slash(url):
    """Make sure there is a slash/ at the end of given url."""
    return ensure_ending(url, '/')


def ensure_ending(path, ending):
    """Make sure there is a given ending the end of a path string."""
    if not path.endswith(ending):
        path += ending
    return path


def is_same(path1, path2):
    """Return True if two normalized paths are identical."""
    return os.path.normcase(path1) == os.path.normcase(path2)


class _PathObj:
    def __init__(self, path: str = ''):
        self._path = path
        self._name = ''
        self._dir = ''

    def _set_path(self, path: str):
        self._path = path
        self._name = ''
        self._dir = ''

    @property
    def path(self):
        if not self._path:
            if not self._name or not self._dir:
                raise RuntimeError('Cannot build path without both dir and name!')
            self._path = os.path.join(self._dir, self._name)
        return self._path

    def _set_name(self, name: str):
        self._name = name
        if not self._dir:
            self._dir, _ = os.path.split(self._path)
        self._path = ''

    @property
    def name(self):
        """Give the name aka tail part of the directories path."""
        if not self._name:
            self._set_dir_name()
        return self._name

    def _set_dir_name(self):
        self._dir, self._name = os.path.split(self._path)

    @property
    def dir(self) -> str:
        """Give the parent path above the current directory."""
        if not self._dir:
            self._set_dir_name()
        return self._dir


class DirObj(_PathObj):
    """A basic path primitive object."""

    def join(self, *sub_path):
        """Join the directories path with another given `sub_path` or paths."""
        return os.path.join(self._path, *sub_path)


class FileObj(_PathObj):
    """A file specific path primitive object.
    Featuring `ext` to identify file types, alongside `is_type`, and `base` to
    get a files name without path and extension.
    """

    def __init__(self) -> None:
        super(FileObj, self).__init__()
        self._ext = None  # type str | None
        self._base = ''

    @property
    def ext(self) -> str:
        """Get the files extension. Such as '.jpg'."""
        if self._ext is None:
            _, ext = self._set_base_ext()
            return ext
        return self._ext

    def _set_base_ext(self):
        self._base, self._ext = os.path.splitext(self.name)
        self._ext = self._ext.lower()
        return self._base, self._ext

    def is_type(self, type_list: list[str] | tuple[str, ...]) -> bool:
        """Tell if the file is of the given `type_list`."""
        return self.ext in type_list

    @property
    def base(self) -> str:
        """Get the files base name without path and extension."""
        if not self._base:
            self._set_base_ext()
        return self._base

    def _set_name(self, name: str) -> None:
        super(FileObj, self)._set_name(name)
        self._ext = None
        self._base = ''

    def _set_path(self, path: str) -> None:
        super(FileObj, self)._set_path(path)
        self._ext = None
        self._base = ''


def build_dir_map(path: str | Path | list[str | Path] | tuple[str | Path, ...]) -> dict[str, list[str]]:
    """From given path (or list of paths) build flat dictionary of directory: files.
    Directory path keys will be unique this way.
    Empty directories will still have an empty list attached.
    """
    paths = [path] if not isinstance(path, (list, tuple)) else path
    dir_map = {}
    for path in paths:
        path = os.path.abspath(path)
        if os.path.isdir(path):
            dir_map.setdefault(path, [])
        elif os.path.isfile(path):
            dir_path, base = os.path.split(path)
            dir_map.setdefault(dir_path, []).append(base)
    return dir_map


if __name__ == '__main__':
    import pytest
    from test import test_a2path

    pytest.main([test_a2path.__file__, '-v'])
