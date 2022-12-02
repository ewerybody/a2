"""test_qdl"""
import json
import unittest
import qdl

TEST_URL_JSON = 'https://raw.githubusercontent.com/ewerybody/a2/master/package.json'
TEST_URL_TEXT = 'https://raw.githubusercontent.com/ewerybody/a2/master/README.md'


class Test(unittest.TestCase):
    def test_read(self):
        data = qdl.read_json(TEST_URL_JSON)
        self.assertTrue(isinstance(data, dict))
        data = qdl.read(TEST_URL_TEXT)
        self.assertTrue(isinstance(data, str))


if __name__ == "__main__":
    unittest.main(verbosity=2)
