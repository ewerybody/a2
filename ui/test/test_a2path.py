from functools import partial
import os
import a2path
import unittest

NAME = '_test_a2path_'


class Test(unittest.TestCase):
    def test_iter_dirs(self):
        tmp_dir = a2path.temp_path(NAME)
        self.assertTrue(tmp_dir.startswith(os.environ['tmp']))
        os.makedirs(tmp_dir)

        num_dirs = 10
        for i in range(num_dirs):
            os.makedirs(os.path.join(tmp_dir, str(i + 1)))

        extra_file = os.path.join(tmp_dir, f'{NAME}.x')
        with open(extra_file, 'w') as fobj:
            fobj.write(NAME)

        found_dirs = []
        for item in a2path.iter_dirs(tmp_dir):
            self.assertEqual(item.dir, tmp_dir)
            self.assertTrue(item.name.isnumeric())
            joined = item.join('joined')
            self.assertEqual(os.path.relpath(joined, item.path), 'joined')
            found_dirs.append(item.path)

        self.assertEqual(len(found_dirs), num_dirs)
        self.assertFalse(extra_file in found_dirs)

        dir_names = a2path.get_dir_names(tmp_dir)
        self.assertEqual(len(dir_names), num_dirs)
        self.assertTrue(all(n.isnumeric() for n in dir_names))
        x_dir_names = a2path.get_dir_names_except(tmp_dir, '1*')
        self.assertFalse(any(n.startswith('1') for n in x_dir_names))

        for dir_path in found_dirs:
            os.rmdir(dir_path)
        os.unlink(extra_file)
        os.rmdir(tmp_dir)

    def test_iter_files(self):
        tmp_dir = a2path.temp_path(NAME)
        self.assertTrue(tmp_dir.startswith(os.environ['tmp']))
        os.makedirs(tmp_dir)

        num_files = 7
        for i in range(num_files):
            fpath = os.path.join(tmp_dir, str(i + 1) + '.X')
            with open(fpath, 'w') as fobj:
                fobj.write('x')

        extra_dir = os.path.join(tmp_dir, 'somedir')
        os.makedirs(extra_dir)

        found_files = []
        for item in a2path.iter_files(tmp_dir):
            self.assertTrue(a2path.is_same(item.dir, tmp_dir.upper()))
            self.assertTrue(item.base.isnumeric())
            self.assertEqual(item.ext, '.x')
            found_files.append(item.path)

        extra_file = os.path.join(tmp_dir, f'{NAME}.not')
        with open(extra_file, 'w') as fobj:
            fobj.write(NAME)

        xtypes = []
        for item in a2path.iter_types(tmp_dir, ['x']):
            xtypes.append(item.path)
        self.assertFalse(extra_file in xtypes)
        os.unlink(extra_file)

        file_names = a2path.get_file_names(tmp_dir)
        self.assertEqual(len(file_names), num_files)

        self.assertFalse(extra_dir in found_files)
        self.assertEqual(len(found_files), num_files)

        for file_path in found_files:
            os.unlink(file_path)
        os.rmdir(extra_dir)
        os.rmdir(tmp_dir)

    def test_utils(self):
        tmp_dir = a2path.temp_path(NAME)
        self.assertFalse(tmp_dir.endswith('/'))
        slashed = a2path.add_slash(tmp_dir)
        self.assertTrue(slashed.endswith('/'))

    def test_remove_dir(self):
        tmp_dir = a2path.temp_path(NAME)

        sub_dir = os.path.join(tmp_dir, 'subdir')
        os.makedirs(sub_dir)
        sub_file = os.path.join(sub_dir, 'sub_file.x')
        fobj = open(sub_file, 'w')

        rmdir_func = partial(a2path.remove_dir, tmp_dir)
        self.assertRaises(PermissionError, rmdir_func)

        fobj.close()
        a2path.remove_dir(tmp_dir)
        self.assertFalse(os.path.isdir(tmp_dir))


if __name__ == '__main__':
    unittest.main()
