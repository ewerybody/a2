"""Stuff for downloads from the internets."""
import json
from a2qt import QtCore

import a2core


log = a2core.get_logger(__name__)


# ERROR_FILE_NOT_FOUND = 'File not found (%s)'
GITHUB_URL = 'github.com'
GITHUB_API = 'https://api.github.com/repos/'
GITHUB_COMPARE_TEMPLATE = GITHUB_API + '{owner}/{repo}/compare/{from_tag}...{to_tag}'
GITHUB_RELEASE = GITHUB_API + '{owner}/{repo}/releases'
GITHUB_COMMITS = GITHUB_API + '{owner}/{repo}/commits'
GITHUB_LATEST = GITHUB_RELEASE + '/latest'
GITHUB_RAW_URL = 'https://raw.githubusercontent.com'
DEFAULT_MAIN_BRANCH = 'master'


class GetJSONThread(QtCore.QThread):
    """
    To get a dictionary from a remote url.
    Connect to its Signals:

     - data_fetched(dict) - Remote data as dictionary.
     - error(str) - Error message as string.

    and kick it off by .start()-ing it.
    """

    data_fetched = QtCore.Signal(dict)
    error = QtCore.Signal(str)

    def __init__(self, parent, url):
        super(GetJSONThread, self).__init__(parent)
        self.url = url

    def _error(self, msg):
        self.error.emit(str(msg))
        self.quit()

    def run(self):
        try:
            remote_data = get_remote_data(self.url)
        except Exception as error:
            self._error(str(error))
            return

        self.data_fetched.emit(remote_data)


def read(url):
    """
    Read contents from a file at given url.
    """
    url = url.lower().strip()
    from urllib import request

    try:
        req = request.Request(url, data=None, headers={'User-Agent': 'Mozilla/5.0'})
        data = request.urlopen(req).read()
    except request.HTTPError as error:
        raise RuntimeError('Could not find data at given address!\n%s' % error)

    try:
        data = data.decode(encoding='utf-8-sig')
    except Exception as error:
        log.error(error)
        raise RuntimeError('Error decoding data from given address!:\n%s' % error)
    return data


def get_remote_data(url):
    """
    Download JSON data from a url.

    :param str url: Web address to get the JSON data from.
    :rtype: dict
    """
    data = read(url)
    try:
        remote_data = json.loads(data)
    except Exception as error:
        log.error(error)
        raise RuntimeError('Error loading JSON from given address!:\n%s' % error)
    return remote_data


def get_github_owner_repo(url):
    """
    From a github url extract the owner and repository names.

    :param str url: Web address to a GitHub repository.
    :rtype: tuple[str, str]
    """
    parts = url.split('/')
    i = parts.index(GITHUB_URL)
    owner, repo = parts[i + 1 : i + 3]
    return owner, repo
