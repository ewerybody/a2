import os
import a2path
import pytest

NAME = '_test_a2path_'


def test_iter_dirs():
    tmp_dir = a2path.temp_path(NAME)
    assert tmp_dir.startswith(os.environ['tmp'])
    os.makedirs(tmp_dir)

    num_dirs = 10
    for i in range(num_dirs):
        os.makedirs(os.path.join(tmp_dir, str(i + 1)))

    extra_file = os.path.join(tmp_dir, f'{NAME}.x')
    with open(extra_file, 'w') as file_obj:
        file_obj.write(NAME)

    found_dirs = []
    for item in a2path.iter_dirs(tmp_dir):
        assert item.dir == tmp_dir
        assert item.name.isnumeric()
        joined = item.join('joined')
        assert os.path.relpath(joined, item.path) == 'joined'
        found_dirs.append(item.path)

    assert len(found_dirs) == num_dirs
    assert extra_file not in found_dirs

    dir_names = a2path.get_dir_names(tmp_dir)
    assert len(dir_names) == num_dirs
    assert all(n.isnumeric() for n in dir_names)
    x_dir_names = a2path.get_dir_names_except(tmp_dir, '1*')
    assert not any(n.startswith('1') for n in x_dir_names)

    for dir_path in found_dirs:
        os.rmdir(dir_path)
    os.unlink(extra_file)
    os.rmdir(tmp_dir)


def test_iter_files():
    tmp_dir = a2path.temp_path(NAME)
    assert tmp_dir.startswith(os.environ['tmp'])
    os.makedirs(tmp_dir)

    num_files = 7
    for i in range(num_files):
        fpath = os.path.join(tmp_dir, str(i + 1) + '.X')
        with open(fpath, 'w') as file_obj:
            file_obj.write('x')

    extra_dir = os.path.join(tmp_dir, 'some_dir')
    os.makedirs(extra_dir)

    found_files = []
    for item in a2path.iter_files(tmp_dir):
        assert a2path.is_same(item.dir, tmp_dir.upper())
        assert item.base.isnumeric()
        assert item.ext, '.x'
        found_files.append(item.path)

    extra_file = os.path.join(tmp_dir, f'{NAME}.not')
    with open(extra_file, 'w') as file_obj:
        file_obj.write(NAME)

    x_types = []
    for item in a2path.iter_types(tmp_dir, ['x']):
        x_types.append(item.path)
    assert extra_file not in x_types
    os.unlink(extra_file)

    file_names = a2path.get_file_names(tmp_dir)
    assert len(file_names), num_files

    assert extra_dir not in found_files
    assert len(found_files), num_files

    for file_path in found_files:
        os.unlink(file_path)
    os.rmdir(extra_dir)
    os.rmdir(tmp_dir)


def test_utils():
    tmp_dir = a2path.temp_path(NAME)
    assert not tmp_dir.endswith('/')
    slashed = a2path.add_slash(tmp_dir)
    assert slashed.endswith('/')


def test_remove_dir():
    tmp_dir = a2path.temp_path(NAME)

    sub_dir = os.path.join(tmp_dir, 'subdir')
    os.makedirs(sub_dir)
    sub_file = os.path.join(sub_dir, 'sub_file.x')
    file_obj = open(sub_file, 'w')

    with pytest.raises(PermissionError):
        a2path.remove_dir(tmp_dir)

    file_obj.close()
    a2path.remove_dir(tmp_dir)
    assert not os.path.isdir(tmp_dir)


def test_build_dir_map():
    this_dir = os.path.abspath(os.path.dirname(__file__))
    dir_map = a2path.build_dir_map(__file__)
    assert isinstance(dir_map, dict)
    assert this_dir in dir_map
    assert os.path.basename(__file__) in dir_map[this_dir]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
