"""test_qdl"""
import json
import pytest

import qdl

TEST_URL_JSON = 'https://raw.githubusercontent.com/ewerybody/a2/master/package.json'
TEST_URL_TEXT = 'https://raw.githubusercontent.com/ewerybody/a2/master/README.md'


class Test:
    def test_read(self):
        data = qdl.read_json(TEST_URL_JSON)
        assert isinstance(data, dict)
        data = qdl.read(TEST_URL_TEXT)
        assert isinstance(data, str)

    def test_broken_url(self):
        with pytest.raises((json.JSONDecodeError, Exception)):
            qdl.read_json('http://vVsdfbsdfgbvsdfvdsafvbsdfvgAdDsad')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
