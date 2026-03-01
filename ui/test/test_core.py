"""
Headless tests for a2 core — no Qt / PySide6 required.

Run with:  pytest ui/test/test_core.py
"""
import os
import pytest

import a2core


def _reset_a2_singleton():
    """Wipe the A2Obj singleton so each test starts fresh."""
    a2core.A2Obj._instance = None


class TestWriteIfChanged:
    def test_creates_file(self, tmp_path):
        p = str(tmp_path / 'new.txt')
        result = a2core.write_if_changed(p, 'hello')
        assert result is True
        assert open(p).read() == 'hello'

    def test_no_write_when_same(self, tmp_path):
        p = str(tmp_path / 'same.txt')
        a2core.write_if_changed(p, 'hello')
        result = a2core.write_if_changed(p, 'hello')
        assert result is False

    def test_overwrites_when_changed(self, tmp_path):
        p = str(tmp_path / 'changed.txt')
        a2core.write_if_changed(p, 'old')
        result = a2core.write_if_changed(p, 'new')
        assert result is True
        assert open(p).read() == 'new'


class TestPaths:
    def test_ui_path_exists(self):
        paths = a2core.Paths()
        assert os.path.isdir(paths.ui)

    def test_a2_root_exists(self):
        paths = a2core.Paths()
        assert os.path.isdir(paths.a2)

    def test_lib_exists(self):
        paths = a2core.Paths()
        assert os.path.isdir(paths.lib)

    def test_data_path_is_set(self):
        paths = a2core.Paths()
        assert paths.data != ''

    def test_a2_is_parent_of_ui(self):
        paths = a2core.Paths()
        assert paths.ui.startswith(paths.a2)


class TestA2ObjSingleton:
    def setup_method(self):
        _reset_a2_singleton()

    def test_inst_returns_instance(self):
        a2 = a2core.get()
        assert isinstance(a2, a2core.A2Obj)

    def test_inst_is_singleton(self):
        a2a = a2core.get()
        a2b = a2core.get()
        assert a2a is a2b

    def test_double_init_raises(self):
        a2core.get()
        with pytest.raises(RuntimeError):
            a2core.A2Obj()

    def test_has_paths(self):
        a2 = a2core.get()
        assert isinstance(a2.paths, a2core.Paths)

    def test_has_urls(self):
        a2 = a2core.get()
        assert isinstance(a2.urls, a2core.URLs)

    def teardown_method(self):
        _reset_a2_singleton()


class TestHeadless:
    def setup_method(self):
        _reset_a2_singleton()

    def test_start_up_sets_db(self):
        a2 = a2core.get()
        a2.start_up()
        assert a2._db is not None

    def test_module_sources_is_dict(self):
        a2 = a2core.get()
        assert isinstance(a2.module_sources, dict)

    def test_enabled_is_dict(self):
        a2 = a2core.get()
        assert isinstance(a2.enabled, dict)

    def test_version_is_string(self):
        a2 = a2core.get()
        assert isinstance(a2.version, str)
        assert a2.version != ''

    def test_is_git_returns_bool(self):
        a2 = a2core.get()
        assert isinstance(a2.is_git(), bool)

    def teardown_method(self):
        _reset_a2_singleton()
