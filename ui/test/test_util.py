import os
import unittest
import a2util


class Test(unittest.TestCase):
    def test_set_archive(self):
        file_path = __file__
        a2util.set_archive(file_path, False)
        attrs1 = os.stat(file_path).st_file_attributes
        a2util.set_archive(file_path, True)
        attrs2 = os.stat(file_path).st_file_attributes
        self.assertNotEqual(attrs1, attrs2)

    def test_unroll_seconds(self):
        for seconds, control in ((29030400.0, '1 year'),(179, '3 minutes')):
            time_string = a2util.unroll_seconds(seconds, 0)
            self.assertEqual(time_string, control)


if __name__ == "__main__":
    unittest.main()
