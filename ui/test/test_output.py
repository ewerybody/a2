import unittest
import a2output


class Test(unittest.TestCase):
    def test_get_set_vars(self):
        bucket = []
        def test(msg, bucket=bucket):
            bucket.append(msg)
        a2output.connect(test)
        self.assertEqual(bucket, [])
        print('something')
        self.assertNotEqual(bucket, [])


if __name__ == "__main__":
    unittest.main()
