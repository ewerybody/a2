import os
import json
import time
import logging
from a2qt import QtCore, QtWidgets, QtNetwork

if __name__ == '__main__':
    NAME = os.path.splitext(os.path.basename(__file__))[0]
    logging.basicConfig()
else:
    NAME = __name__
log = logging.getLogger(NAME)
log.setLevel(10)


def read(url, progress_callback=None):
    return read_raw(url, progress_callback).decode()


def read_json(url, progress_callback=None):
    return json.loads(read_raw(url, progress_callback))


def read_raw(url, progress_callback=None):
    app = _check_app()
    downloader = QDownload()
    downloader.read_raw(url, progress_callback)
    return downloader.data


class QDownload(QtCore.QObject):
    progress = QtCore.Signal(int, int)

    def __init__(self):
        super(QDownload, self).__init__()
        self.manager = QtNetwork.QNetworkAccessManager(self)
        self._progress_callback = None
        self._finished = False
        self._data = b''
        self._file = None
        self._progress = None
        self._user_agent = None

    @property
    def data(self):
        return self._data

    def read_raw(self, url, progress_callback=None):
        """Get raw binary contents from given url into memory."""
        reply = self._prepare_request(url, progress_callback)
        self.wait()
        self._data = reply.readAll().data()
        return self._data

    def download(self, url, target_path, overwrite=False, progress_callback=None):
        """Download contents from given url to disk."""
        if os.path.isdir(target_path):
            target_path = os.path.join(os.path.basename(url), target_path)

        if os.path.isfile(target_path) and not overwrite:
            raise FileExistsError('The target file path alredy exists!')


        tmp_file = os.path.join(os.getenv('TEMP'), f'_{PROJECT}_tmp_dl_{version}.zip')
        if not os.path.isfile(tmp_file):
            self._file = QtCore.QSaveFile(tmp_file)
            if self._file.open(QtCore.QIODevice.OpenModeFlag.WriteOnly):
                log.info('Looking up "%s" ...' % pack_nfo['url'])
                reply = self._prepare_request(pack_nfo['url'], progress_callback)
                reply.finished.connect(self._on_download_finished)
                reply.readyRead.connect(self._on_download_ready)
            else:
                error = self._file.errorString()
                log.error(f'Cannot open device: {error}')

            self.wait()
            if os.path.isfile(tmp_file):
                log.info('Downloaded: %s', tmp_file)
            else:
                raise RuntimeError('Download failed!')

    def _on_download_ready(self):
        reply = self.sender()
        if reply.error() == QtNetwork.QNetworkReply.NoError:
            self._file.write(reply.readAll())

    def _on_download_finished(self):
        self._file.commit()

    def _prepare_request(self, url, progress_callback=None):
        self._progress_callback = progress_callback

        request = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
        request.setRawHeader(b'User-Agent', b'MyOwnBrowser 1.0')

        reply = self.manager.get(request)
        reply.finished.connect(self._on_finish)
        reply.downloadProgress.connect(self._on_progress)
        reply.errorOccurred.connect(self._on_error)
        reply.sslErrors.connect(self._on_error)
        return reply

    def _on_error(self, x):
        log.error(x)

    def _on_progress(self, current, total):
        if self._progress_callback is None:
            self._progress_callback = self._backup_report
        self._progress_callback(current, total)

    def _backup_report(self, current, total):
        # if self._progress is None and total != -1:
            # self._progress = tqdm(total=total, unit='bytes')
        print('%i/%i' % (current, total))

        if self._progress is not None:
            self._progress.update(current)

    def wait(self):
        while not self._finished:
            QtWidgets.QApplication.instance().processEvents()
            time.sleep(0.01)
        self._finished = False
        self._progress = None
        self._progress_callback = None

    def _on_finish(self):
        self._finished = True


def _check_app():
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])
    return app


if __name__ == '__main__':
    import unittest
    import test.test_qdl

    unittest.main(test.test_qdl, verbosity=2)
