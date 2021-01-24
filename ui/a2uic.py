"""
Handle Qt Designer file updating, compilation and patching.
"""
import os
import sys
import a2core
from importlib import reload

UI_FILE_SUFFIX = '_ui'
PYSIDE_REPLACE = 'a2qt'
log = a2core.get_logger(__name__)


def check_module(module, force=False):
    """
    Recompile a ui xml file to Python if out-of-date.

    :param module module: Module object to check.
    """
    if not a2core.is_dev_mode():
        return

    if getattr(sys, 'frozen', False):
        # log.info('frozen! no need to compile %s' % module)
        return

    pyfile = module.__file__
    folder, pybase = os.path.split(pyfile)
    uiname = os.path.splitext(pybase)[0]
    uibase = None

    if uiname.endswith(UI_FILE_SUFFIX):
        uibase = uiname[: -len(UI_FILE_SUFFIX)] + '.ui'
    else:
        uibase = _get_ui_basename_from_header(pyfile)

    if uibase is None:
        raise RuntimeError(
            'Could not get source ui file from module:\n %s\n  ' 'Not a ui file module??!' % module
        )

    uifile = os.path.join(folder, uibase)
    if not uibase or not os.path.isfile(uifile):
        return

    diff = os.path.getmtime(pyfile) - os.path.getmtime(uifile)
    if not force and os.path.getsize(pyfile) and diff > 0:
        return

    log.debug('%s needs compile! (age: %is)', uibase, diff)

    # Make paths in compiled files project related, not from current user.
    parent_path = os.path.abspath(os.path.join(a2core.__file__, '..', '..'))

    # Newer uic seems to just put the basename in the header... however.
    ui_relative = os.path.relpath(uifile, parent_path)
    curr_cwd = os.getcwd()
    os.chdir(parent_path)

    import subprocess
    import a2qt

    uic_path = os.path.join(a2qt.QT_PATH, 'uic.exe')
    subprocess.call([uic_path, '-g', 'python', ui_relative, '-o', pyfile])

    os.chdir(curr_cwd)

    _patch_ui(uiname, pyfile)

    reload(module)


def _patch_ui(uiname, pyfile):
    """
    Patch compiled ui file to fix a couple of problems there are with
    the default uic executable. See #219. TODO:
    [x] make use of a2qt wrapper instead of PySideX
    [x] remove main-obj resizes (!!!!!)
    [ ] get rid of broad * imports
    [ ] make a proper doc-string instead of comments block
    [ ] remove #if/#endif comments
    [ ] remove # setupUi and # retranslateUi comments
    [ ] remove retranslateUi and its call if empty
    [ ] remove unneeded empty lines
    [ ] make it class Name: instead of oldschool class Name(object):
    [ ] make it black/brunette compliant
    """
    with open(pyfile) as pyfobj:
        lines: list[str] = pyfobj.readlines()

    # find the module doc string
    mod_doc_block = None
    for i, line in enumerate(lines):
        if mod_doc_block is not None and not line.strip():
            mod_doc_block.append(i)
            break
        if line.startswith('##') and mod_doc_block is None:
            mod_doc_block = [i]

    # find the imports block
    pyside_wrapped_line = None
    for i, line in enumerate(lines[mod_doc_block[1] :], mod_doc_block[1]):
        if pyside_wrapped_line and not line.strip():
            break

        if line.startswith('from PySide'):
            parts = line.split()
            dot_pos = parts[1].find('.')
            if dot_pos == -1:
                raise RuntimeError('Patching compiled ui failed on line %i:\n  %s' % (i, line))
            parts[1] = PYSIDE_REPLACE + parts[1][dot_pos:]
            lines[i] = ' '.join(parts) + '\n'
            pyside_wrapped_line = i

    # find class block
    class_block_start = None
    for i, line in enumerate(lines[pyside_wrapped_line + 1 :], pyside_wrapped_line + 1):
        if class_block_start is None and line.startswith('class '):
            class_block_start = i
            break

    setup_line = lines[class_block_start + 1]
    parts = setup_line.split()
    assert parts[0] == 'def'
    assert parts[1] == 'setupUi(self,'
    assert parts[2].endswith('):')
    obj_name = parts[2][:-2]

    # Remove the resize. All our uis are dynamically sized.
    for i, _line in enumerate(lines[class_block_start + 1 :], class_block_start + 1):
        line = _line.strip()
        if line.startswith(f'{obj_name}.resize('):
            lines[i] = '\n'
            break

    with open(pyfile, 'w') as pyfobj:
        pyfobj.write(''.join(lines))


def _get_ui_basename_from_header(py_ui_path):
    """TODO: This is kinda ugly I don't think we need it."""
    uibase = None
    with open(py_ui_path) as fobj:
        line = fobj.readline()
        while line and uibase is not None:
            line = line.strip()
            if line.startswith('# Form implementation '):
                uibase = line[line.rfind("'", 0, -1) + 1 : -1]
                uibase = os.path.basename(uibase.strip())
                log.error('checkUiModule from read: %s', uibase)
                break
            line = fobj.readline()
    return uibase
