import json
import pytest
import urllib.error

import a2dl

RAW_REPO = 'https://raw.githubusercontent.com/ewerybody/a2'
BRANCH = 'master'  # that's gonna change!
TEST_URL_JSON = f'{RAW_REPO}/{BRANCH}/lib/defaults/tags.json'
TEST_URL_TEXT = f'{RAW_REPO}/{BRANCH}/README.md'


class Test:
    def test_read(self):
        """README.md should be non-empty and look like markdown."""
        data = a2dl.read(TEST_URL_TEXT)
        assert len(data) > 0
        assert isinstance(data, str)
        assert '#' in data

    def test_read_json(self):
        data = a2dl.read_json(TEST_URL_JSON)
        assert isinstance(data, dict)
        assert all(isinstance(k, str) for k in data)
        assert all(isinstance(v, str) for v in data.values())

    def test_read_raw_returns_bytes(self):
        data = a2dl.read_raw(TEST_URL_TEXT)
        assert isinstance(data, bytes)
        assert len(data) > 0

    def test_read_raw_size(self):
        """Passing size= should limit the number of bytes returned."""
        data = a2dl.read_raw(TEST_URL_TEXT, size=16)
        assert isinstance(data, bytes)
        assert len(data) == 16

    def test_read_raw_size_bad_type(self):
        with pytest.raises(RuntimeError, match='Integer'):
            a2dl.read_raw(TEST_URL_TEXT, size='a lot')  # type: ignore[arg-type]

    def test_progress_callback(self):
        """Progress callback should be called at least once with sane values."""
        calls = []

        def on_progress(current: int, total: int):
            calls.append((current, total))

        a2dl.read_raw(TEST_URL_TEXT, progress_callback=on_progress)

        assert len(calls) > 0
        # current should always be positive and never exceed total (when known)
        for current, total in calls:
            assert current > 0
            if total != -1:
                assert current <= total

    def test_progress_callback_final_value(self):
        """Last progress call should report current == total (when Content-Length known)."""
        calls = []

        def on_progress(current: int, total: int):
            calls.append((current, total))

        a2dl.read(TEST_URL_JSON, progress_callback=on_progress)

        assert calls, 'Expected at least one progress call'
        last_current, last_total = calls[-1]
        if last_total != -1:
            assert last_current == last_total

    def test_progress_increases_monotonically(self):
        """Reported byte counts should never go backwards."""
        calls = []
        a2dl.read_raw(TEST_URL_TEXT, progress_callback=lambda c, t: calls.append(c))
        for a, b in zip(calls, calls[1:]):
            assert b >= a

    def test_broken_url(self):
        with pytest.raises((json.JSONDecodeError, Exception)):
            a2dl.read_json('http://vVsdfbsdfgbvsdfvdsafvbsdfvgAdDsad')

    def test_broken_url_raw(self):
        with pytest.raises((urllib.error.URLError, OSError)):
            a2dl.read_raw('http://this.domain.does.not.exist.invalid/file.bin')

    def test_404_raises(self):
        with pytest.raises(urllib.error.HTTPError):
            a2dl.read('https://raw.githubusercontent.com/ewerybody/a2/master/DOES_NOT_EXIST.md')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
