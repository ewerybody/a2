import os
import json
import urllib.request
from typing import Any, Callable

import a2core

log = a2core.get_logger(__name__)
__version__ = (0, 1, 0)
__version_info__ = '0.1.0'

_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0'}
_CHUNK_SIZE = 8192


def read(url: str, progress_callback: Callable | None = None, size: int | None = None) -> str:
    """Fetch the contents of a URL and return them as a decoded string.

    :param url: The URL to fetch.
    :param progress_callback: Optional callable receiving (current: int, total: int) byte counts
        as the download progresses. Falls back to debug logging if not provided.
    :param size: If given, read only this many bytes from the response.
    :return: The response body decoded as a UTF-8 string.
    """
    return read_raw(url, progress_callback, size).decode()


def read_json(url: str, progress_callback: Callable | None = None) -> Any:
    """Fetch the contents of a URL and return them as a parsed JSON object.

    :param url: The URL to fetch. The response is expected to be valid JSON.
    :param progress_callback: Optional callable receiving (current: int, total: int) byte counts
        as the download progresses. Falls back to debug logging if not provided.
    :return: The parsed JSON value (dict, list, str, int, etc.).
    :raises json.JSONDecodeError: If the response body is not valid JSON.
    """
    return json.loads(read_raw(url, progress_callback))


def read_raw(url: str, progress_callback: Callable | None = None, size: int | None = None) -> bytes:
    """Fetch the contents of a URL and return them as raw bytes.

    Downloads the response in chunks of :data:`_CHUNK_SIZE` bytes, calling
    ``progress_callback(current, total)`` after each chunk. If ``total`` is
    unknown the server did not send a ``Content-Length`` header and ``total``
    will be ``-1``.

    :param url: The URL to fetch.
    :param progress_callback: Optional callable receiving (current: int, total: int) byte counts
        as the download progresses. Falls back to debug logging if not provided.
    :param size: If given, read only this many bytes from the response instead
        of consuming the full body. Must be an :class:`int`.
    :return: The raw response body as bytes.
    :raises RuntimeError: If ``size`` is provided but is not an :class:`int`.
    :raises urllib.error.URLError: If the URL cannot be reached.
    """
    if progress_callback is None:
        progress_callback = _backup_report
    request = urllib.request.Request(url, headers=_HEADERS)
    block_nr = 0
    with urllib.request.urlopen(request) as response:
        total = int(response.headers.get('Content-Length', -1))
        if size is not None:
            if not isinstance(size, int):
                raise RuntimeError('Value `size` needs to be Integer!')
            return response.read(size)

        chunks = []
        current = 0
        while True:
            chunk = response.read(_CHUNK_SIZE)
            if not chunk:
                break
            chunks.append(chunk)
            current += len(chunk)
            progress_callback(current, total)

        return b''.join(chunks)


def download(url: str, target_path: str, overwrite: bool = False, progress_callback: Callable | None = None) -> None:
    """Download a file from a URL to disk.

    If ``target_path`` is a directory the filename is derived from the URL.
    The file is first written to a temporary location in ``%TEMP%`` and only
    considered complete once it exists on disk.  If the temporary file already
    exists the download is skipped entirely.

    :param url: The URL of the file to download.
    :param target_path: Destination file path or directory.
    :param overwrite: If ``False`` (default) and ``target_path`` already exists
        as a file, raises :class:`FileExistsError`.
    :param progress_callback: Optional callable receiving (current: int, total: int)
        byte counts as the download progresses.
    :raises FileExistsError: If the target file already exists and ``overwrite`` is ``False``.
    :raises RuntimeError: If the download completes but the temporary file is not found on disk.
    """
    base_name = os.path.basename(url)
    if os.path.isdir(target_path):
        target_path = os.path.join(target_path, base_name)

    if os.path.isfile(target_path) and not overwrite:
        raise FileExistsError('The target file path already exists!')

    tmp_file = os.path.join(os.getenv('TEMP', ''), f'__tmp_dl_{base_name}')
    if not os.path.isfile(tmp_file):
        data = read_raw(url, progress_callback)
        with open(tmp_file, 'wb') as f:
            f.write(data)

    if not os.path.isfile(tmp_file):
        raise RuntimeError('Download failed!')

    if os.path.isfile(target_path):
        os.unlink(target_path)
    os.rename(tmp_file, target_path)


def _backup_report(current: int, total: int) -> None:
    """Default progress callback that logs download progress at DEBUG level.

    Silent when ``total`` is unknown (``-1``) or when the final chunk arrives
    (``current == total``) to avoid noise at the boundaries.

    :param current: Number of bytes received so far.
    :param total: Total expected bytes, or ``-1`` if unknown.
    """
    if current not in (-1, total) and total != -1:
        log.debug('%i/%i', current, total)


if __name__ == '__main__':
    import pytest

    from test import test_a2dl
    pytest.main([test_a2dl.__file__, '-v'])
