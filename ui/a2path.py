"""
All things file system.
"""
import os
import shutil
import fnmatch


def iter_dirs(path):
    """
    Iterate over directory items in a path. Yield DirObj.
    """
    item = DirObj()
    if not os.path.isdir(path):
        return

    for this in os.scandir(path):
        if this.is_dir():
            item.set_path(this.path)
            yield item


def get_dir_names(path):
    """
    From path return list of subfolder names.
    """
    if not os.path.isdir(path):
        return []
    return [item.name for item in os.scandir(path) if item.is_dir()]


def get_dir_names_except(path, pattern):
    """
    From path return list of subfolder names that do not match a given pattern.
    """
    if not os.path.isdir(path):
        return []
    from fnmatch import fnmatch
    return [i.name for i in os.scandir(path) if i.is_dir() and not fnmatch(i.name, pattern)]


def remove_dir(path):
    """
    Savely delete a folder.

    Moves the folder to temp with random name then deletes it.
    Instead of deleting the single items directly this will already
    correctly fail moving to temp if ANY of the containing items is locked.
    So there is no other safeguard needed.
    """
    import uuid
    trash_path = os.path.join(os.getenv('TEMP'), str(uuid.uuid4()))
    os.rename(path, trash_path)
    shutil.rmtree(trash_path)


def iter_files(path):
    item = FileObj()
    for this in os.scandir(path):
        if this.is_file():
            item.set_path(this.path)
            yield item


def get_file_names(path):
    return [item.name for item in os.scandir(path) if item.is_file()]


def iter_types(path, types):
    item = FileObj()
    for this in os.scandir(path):
        if this.is_file():
            item.set_path(this.path)
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
    """
    Return True if two normalised paths are identical.
    """
    return os.path.normcase(path1) == os.path.normcase(path2)


class _PathObj:
    def __init__(self, path=None):
        self._path = path
        self._name = None
        self._dir = None

    def set_path(self, path):
        self._path = path
        self._name = None
        self._dir = None

    @property
    def path(self):
        if self._path is None:
            if self._name is None or self._dir is None:
                raise RuntimeError('Cannot build path without both dir and name!')
            self._path = os.path.join(self._dir, self._name)
        return self._path

    def set_name(self, name):
        self._name = name
        if self._dir is None:
            self._dir, _ = os.path.split(self._path)
        self._path = None

    @property
    def name(self):
        if self._name is None:
            self._set_dir_name()
        return self._name

    def _set_dir_name(self):
        self._dir, self._name = os.path.split(self._path)

    @property
    def dir(self):
        if self._dir is None:
            self._set_dir_name()
        return self._dir


class DirObj(_PathObj):
    def join(self, *sub_path):
        return os.path.join(self._path, *sub_path)


class FileObj(_PathObj):
    def __init__(self):
        super(FileObj, self).__init__()
        self._ext = None
        self._base = None

    @property
    def ext(self):
        if self._ext is None:
            self._set_base_ext()
        return self._ext

    def _set_base_ext(self):
        self._base, self._ext = os.path.splitext(self._name)
        self._ext = self._ext.lower()

    def is_type(self, type_list):
        return self.ext in type_list

    @property
    def base(self):
        if self._base is None:
            self._set_base_ext()
        return self._base

    def set_name(self, name):
        super(FileObj, self).set_name(name)
        self._ext = None
        self._base = None

    def set_path(self, path):
        super(FileObj, self).set_path(path)
        self._ext = None
        self._base = None
