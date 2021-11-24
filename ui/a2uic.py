"""
Handle Qt Designer file updating, compilation and patching.
"""
import os
import sys
import a2core
from importlib import reload
from a2qt import QtCore, QtGui, QtWidgets, QtSvg

log = a2core.get_logger(__name__)

UI_FILE_SUFFIX = '_ui'
PYSIDE_REPLACE = 'a2qt'
OLDSCHOOL_CLASS = '(object):\n'
LINE_LEN = 95
QMEMBERS = {}
MEMBERSQ = {}

for mod in (QtCore, QtGui, QtWidgets, QtSvg):
    name = mod.__name__.split('.')[1]
    QMEMBERS[name] = [n for n in dir(mod) if not n.startswith('_') and n != 'a2qt']
    for member in QMEMBERS[name]:
        if member in MEMBERSQ:
            print(f'{member} already listed in {MEMBERSQ[member]}!!')
            continue
        MEMBERSQ[member] = name


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
    the default uic executable. See #219. Done:
    [x] make use of a2qt wrapper instead of PySideX
    [x] remove main-obj resizes (!!!!!)
    [x] make a proper doc-string instead of comments block
    [x] remove #if/#endif comments
    [x] remove # setupUi and # retranslateUi comments
    [x] remove retranslateUi and its call if empty
    [x] remove unneeded empty lines
    [x] make it class Name: instead of oldschool class Name(object):
    TODO:
    [ ] get rid of broad * imports - this is pretty big. We'd need some LUTs.
    [ ] make it black/brunette compliant - I'd rather leave this to brunette itself.
        but in a separate process that auto-checks for updated ui-files.
    """
    with open(pyfile) as pyfobj:
        lines: list[str] = pyfobj.readlines()

    # find the module doc string
    mod_doc_block = []
    for i, line in enumerate(lines):
        if mod_doc_block and not line.strip():
            mod_doc_block.append(i)
            break
        if line.startswith('##') and not mod_doc_block:
            mod_doc_block = [i]

    # find the imports block
    pyside_import_lines = []
    start = mod_doc_block[1]
    submod_lines = {}
    submods_used = {}
    _submod = ''
    for i, line in enumerate(lines[start:], start):
        # finish when collected and next line is empty
        if pyside_import_lines and not line.strip():
            break

        if line.startswith('from PySide'):
            parts = line.split()
            dot_pos = parts[1].find('.')
            if dot_pos == -1:
                raise RuntimeError('Patching compiled ui failed on line %i:\n  %s' % (i, line))
            _submod = parts[1][dot_pos + 1 :]
            parts[1] = PYSIDE_REPLACE + '.' + _submod
            lines[i] = ' '.join(parts) + '\n'
            pyside_import_lines.append(i)
            submod_lines[_submod] = [i]
        elif _submod:
            submod_lines[_submod].append(i)
            pyside_import_lines.append(i)
    pyside_import_lines[:] = [min(pyside_import_lines), max(pyside_import_lines)]

    if not all(mod in globals() for mod in submod_lines):
        raise RuntimeError('Not all Qt Submodules loaded!')

    # find class block
    class_block_start = None
    start = pyside_import_lines[-1] + 1
    for i, line in enumerate(lines[start:], start):
        if class_block_start is None and line.startswith('class '):
            class_block_start = i
            if line.endswith(OLDSCHOOL_CLASS):
                lines[i] = line[: -len(OLDSCHOOL_CLASS)] + ':\n'
            break

    setup_line = lines[class_block_start + 1]
    parts = setup_line.split()
    assert parts[0] == 'def'
    assert parts[1] == 'setupUi(self,'
    assert parts[2].endswith('):')
    obj_name = parts[2][:-2]

    # prepare the class block
    resize_removed = False
    retranslate_call_line = None
    for i, _line in enumerate(lines[class_block_start + 1 :], class_block_start + 1):
        line = _line.strip()
        if not line:
            lines[i] = ''
        # Remove the resize. All our uis are dynamically sized.
        elif not resize_removed and line.startswith(f'{obj_name}.resize('):
            lines[i] = ''
            resize_removed = True
        # remove comments
        elif line.startswith('#'):
            lines[i] = ''

        # remove translation func if empty
        elif line.startswith('self.retranslateUi('):
            retranslate_call_line = i
        elif (
            line.startswith('def retranslateUi(self, ')
            and lines[i + 1].strip() == 'pass'
            and retranslate_call_line is not None
        ):
            lines[i] = ''
            lines[i + 1] = ''
            lines[retranslate_call_line] = ''

        for word, mod in MEMBERSQ.items():
            if word in line:
                if line[line.find(word) + len(word)] in '(.':
                    submods_used.setdefault(mod, set()).add(word)
                else:
                    log.error(f'Word "{word}" found in line but not handled!\n> {line}')

    new_import_lines = []
    for mod in submods_used:
        members = sorted(submods_used[mod])
        line = f'from {PYSIDE_REPLACE}.{mod} import '

        rest = ', '.join(members)
        if len(line + rest) <= 95:
            new_import_lines.append(line + rest)
            continue

        line += '('
        for word in members[:-1]:
            if len(line + word) <= 95:
                line += word + ', '
                continue
            new_import_lines.append(line)
            line = '    ' + word + ', '
        line += members[-1] + ')'
        new_import_lines.append(line)


    # assemble new lines
    new_lines = lines[: mod_doc_block[0]]
    new_lines.append('"""\n')
    for i in range(mod_doc_block[0] + 1, mod_doc_block[1] - 1):
        line = lines[i].strip('# \n')
        if line:
            new_lines.append(line + '\n')
        else:
            new_lines.append('\n')
    new_lines.append('"""\n\n')
    new_lines.append('\n'.join(new_import_lines) + '\n')
    # these are probably all other imports
    new_lines.extend(lines[pyside_import_lines[1] + 1: class_block_start])
    # this skips all empty lines
    new_lines.extend(l for l in lines[class_block_start:] if l)

    with open(pyfile, 'w') as pyfobj:
        pyfobj.write(''.join(new_lines))


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
