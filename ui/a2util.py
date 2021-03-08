# -*- coding: utf-8 -*-
"""
Misc functions - gathered from the a2core module.
This is all too random to be core.
"""
import os
import time
import stat
import string
import codecs

from a2qt import QtCore

import a2core


UTF8_CODEC = 'utf-8-sig'
JSON_INDENT = 2
ILLEGAL_NAMES = (
    'con prn aux nul com1 com2 com3 com4 com5 com6 com7 com8 '
    'com9 lpt1 lpt2 lpt3 lpt4 lpt5 lpt6 lpt7 lpt8 lpt9'.split()
)
ALLOWED_CHARS = string.ascii_letters + string.digits + '_-.'
EXPLORER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
DEFAULT_NAME_MSG = 'Name "%s" already in use!'


def standard_name_check(name, black_list=None, black_list_msg=None):
    """
    Report about standard naming issues or nothing if all is OK.

    :param str name: Incoming name to check.
    :param list black_list: List of names that are already taken.
    :param str black_list_msg: Optional black list message if its more specific than default.
    :rtype: str
    """
    if not name:
        return 'Name cannot be empty!'

    if black_list_msg is None:
        black_list_msg = DEFAULT_NAME_MSG

    _name = name.lower()
    msg = ''
    if _name == a2core.NAME:
        msg = f'You just cannot name it "{a2core.NAME}"! Ok?'
    elif name.startswith('.'):
        msg = 'Names starting with a dot would be ignored!'
    elif black_list is not None and name in black_list:
        msg = black_list_msg % name
    elif any([(l in string.whitespace) for l in name]):
        msg = 'Name cannot have whitespace! Use _ or - insead!'
    elif not all([(l in ALLOWED_CHARS) for l in name]):
        msg = 'Name can only have letters, digits and "_.-"'
    elif name in ILLEGAL_NAMES:
        msg = 'Name cannot be reserved OS device name!'
    elif not any([(l in string.ascii_letters) for l in name]):
        msg = 'Have at least 1 letter in the name!'

    return msg


def get_cfg_default_name(cfg):
    """

    :param dict cfg: Element configuration dictionary.
    :rtype: str
    """
    cfg_name = cfg.get('name', cfg.get('typ'))
    if cfg_name is None:
        raise RuntimeError(
            'Could not find name for config piece!\n'
            'Make sure "name" or "typ" is given in the config dict!'
        )
    return cfg_name


def get_next_free_number(name, name_list, separator=''):
    """
    Browses a list of names to find a free new version of
    the given name + integer number. Just returns the name if its not even
    in the name_list. Otherwise the first next will be 2.

    Example:

        name = 'trumpet'
        name_list = ['swamp', 'noodle']
        result: 'trumpet'

        name = 'bob'
        name_list = ['bob', 'alice', 'bob 2', 'bob 4']
        result: 'bob 3'

    :param str name: Base name to look up in the list
    :param iterable name_list: List to look for instances of "name"
    :param str separator: string to put between the initial name and
        the integer number.
    :rtype: str
    """
    if name not in name_list:
        return name

    number = 2
    try_name = name + separator + str(number)

    while try_name in name_list:
        number += 1
        try_name = name + separator + str(number)

    return try_name


def json_read(path):
    import json

    with codecs.open(path, encoding=UTF8_CODEC) as fobj:
        return json.load(fobj)


def json_write(path, data):
    import json

    with codecs.open(path, 'w', encoding=UTF8_CODEC) as fobj:
        json.dump(data, fobj, indent=JSON_INDENT, sort_keys=True)


def get_date():
    now = time.localtime()
    return '%i %i %i' % (now.tm_year, now.tm_mon, now.tm_mday)


def surf_to(url):
    import webbrowser

    if url:
        webbrowser.get().open(url)


def load_utf8(path):
    """
    Opens a file with UTF8 codec to return its content in a string
    :param str path: Path to a file to load from.
    :rtype: str
    """
    with codecs.open(path, encoding=UTF8_CODEC) as fobj:
        return fobj.read()


def write_utf8(path, content):
    """
    Opens a file path with UTF8 codec to write string content into.
    :param str path: Path to a file to write to.
    :param str content: String content for the file.
    """
    with codecs.open(path, 'w', encoding=UTF8_CODEC) as fobj:
        fobj.write(content)


def explore(path):
    """
    Opens the Windows Explorer for the given path.
    Selects the file if a file path was passed.

    :param str path: Path to a folder or file.
    """
    # explorer would choke on forward slashes
    path = os.path.normpath(path)

    if os.path.isdir(path):
        args = [path]
    elif os.path.isfile(path):
        args = ['/select,', path]
    else:
        raise FileNotFoundError('Cannot explore to path "%s"' % path)

    start_process_detached(EXPLORER_PATH, args)


def unroll_seconds(value, decimals=2):
    """
    Converts a number of seconds to easily readable values like
    2 minutes
    5 weeks ...

    :param int value: Number of seconds.
    :rtype: str
    """
    current = float(value)
    name = 'seconds'
    if value > 60:
        d = [
            (60, 'minutes'),
            (60, 'hours'),
            (24, 'days'),
            (7, 'weeks'),
            (4, 'months'),
            (12, 'years'),
        ]
        last = current
        for i, (divider, name) in enumerate(d):
            current = current / divider
            # print('%ss is %s %s' % (value, current, name))
            if current == 1.0:
                break
            if current < 1:
                name = d[i - 1][1]
                current = last
                break
            last = current

    v = round(current, decimals)
    if decimals == 0:
        v = int(v)
        if v == 1:
            name = name[:-1]
    return '%s %s' % (v, name)


def start_process_detached(path, args=None, working_dir=None):
    """
    Uses QtCore.QProcess to start off detached processes

    :param str path: Path to the thing to start.
    :param list args: List of argument strings.
    :param str working_dir: Current Working Dir or cwd to set for the process.
    :return: Tuple of process result value and process ID.
    :rtype: tuple
    """
    if args is None:
        args = []
    if not isinstance(args, list):
        args = [args]
    if working_dir is None:
        a2 = a2core.A2Obj.inst()
        working_dir = a2.paths.a2

    process = QtCore.QProcess()
    result, pid = process.startDetached(path, args, working_dir)
    return result, pid


def write_enable(file_path):
    """
    :param str file_path: Path to file to make writable.
    """
    if os.path.isfile(file_path):
        os.chmod(file_path, stat.S_IWRITE)


def rolling_list_add(item, to_list, max_items=10):
    """
    Sort given item to top of a list.

    :param str item: Item to make the first element in given list.
    :param list to_list: List object to treat as rolling list with given item.
    """
    if item in to_list:
        if to_list[0] == item:
            return to_list[:max_items]
        to_list.remove(item)

    to_list.insert(0, item)
    return to_list[:max_items]


def set_archive(file_path, state: bool):
    """
    Change the archive file attribute.

    Pretty weird. There seems to be no built-in solution. Cooked via:
    https://stackoverflow.com/a/40372658/469322
    """
    import ctypes

    attrs = os.stat(file_path).st_file_attributes
    if state:
        changed = attrs | stat.FILE_ATTRIBUTE_ARCHIVE
    else:
        changed = attrs & ~stat.FILE_ATTRIBUTE_ARCHIVE

    if attrs != changed:
        ctypes.windll.kernel32.SetFileAttributesW(file_path, changed)


if __name__ == '__main__':
    x = unroll_seconds(29030400.0, 0)
    print('x: %s' % x)
