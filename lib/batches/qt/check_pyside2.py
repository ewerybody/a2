"""
Script to search the code for usage of a PySide package
to prepare for porting to a new PySide package ...
"""

import os
import codecs
import importlib
from pprint import pprint

# rename to unique `pyside_package`
import PySide6 as pyside_package

OLD_PACK = 'PySide6'
NEW_PACK = 'a2qt'
IMPORT_STR = ' import '
FROM_IMPORT = 'from a2qt import '
IGNORE_MEMBERS = ('qApp', '__package__', '__path__')
IGNORE_DIRS = (NEW_PACK, 'singlesiding')
PYPAKS = pyside_package.__all__
PAK_MEMBERS = {}
MEMBER_PAKS = {}


def main():
    print('pypaks:', PYPAKS)
    global PAK_MEMBERS, MEMBER_PAKS
    for pakname in PYPAKS:
        qmod = importlib.import_module(f'{pyside_package.__name__}.{pakname}')
        members = [m for m in dir(qmod) if not m.startswith('_')]
        PAK_MEMBERS[pakname] = members
        for m in members:
            MEMBER_PAKS[m] = pakname

    stats = {
        'py_dirs': 0,
        'num_py_files': 0,
        'changed_files': 0,
        'change_count': 0,
        'member_changes': 0,
        'pack_changes': 0,
        'packs_used': set()
    }

    # ui_path = os.path.abspath(os.path.join(__file__, '..', '..', '..', 'ui'))
    ui_path = os.path.abspath(os.path.join(__file__, '..', '..', '..', '..', 'ui'))
    check_files(ui_path, stats)

    pprint(stats)


def check_files(path, stats):
    pyfiles = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path) and not item.startswith('_') and item not in IGNORE_DIRS:
            check_files(item_path, stats)
        elif os.path.isfile(item_path) and os.path.splitext(item)[1] == '.py':
            pyfiles.append(item_path)

    if not pyfiles:
        return

    stats['py_dirs'] += 1
    stats['num_py_files'] += len(pyfiles)

    for this_path in pyfiles:
        import_lines = []
        qpacks = set()
        try:
            lines, needs_unicode = get_lines(this_path)
            # print(f'checking {len(lines)} lines in file {this_path} ...')
            change_file = False
            for i, line in iter_lines(lines):
                try:
                    changes, new_line, this_qpacks = check_line(line)
                    if changes:
                        change_file = True
                        lines[i] = new_line
                        stats['change_count'] += 1
                        stats['member_changes'] += changes.get('member', 0)
                        stats['pack_changes'] += changes.get('pack', 0)
                        if not line.startswith('from'):
                            print('line changed:\n  %s\n  %s' % (line, new_line))

                    if this_qpacks:
                        qpacks.update(this_qpacks)

                except Exception as error:
                    print(f'problems with File: "{this_path}", line {i}')
                    raise error

                if line.strip().startswith(FROM_IMPORT):
                    import_lines.append(i)

            if import_lines:
                if len(import_lines) > 1:
                    raise RuntimeError('Multiple import lines?!?!', import_lines, this_path)

                current_paks = [
                    p.strip() for p in lines[import_lines[0]][len(FROM_IMPORT) :].split(',')
                ]

                if qpacks != set(current_paks):
                    new_line  = FROM_IMPORT + ', '.join(qpacks)
                    print('imports line changed:\n  %s\n  %s' % (lines[import_lines[0]], new_line))
                    lines[import_lines[0]] = new_line
                    change_file = True
                    stats['change_count'] += 1
                    stats['pack_changes'] += 1

            if change_file:
                if needs_unicode:
                    with codecs.open(this_path, 'w', encoding='utf-8-sig') as fob:
                        fob.write('\n'.join(lines))
                else:
                    with open(this_path, 'w') as fob:
                        fob.write('\n'.join(lines))

                print(f'changed file: {this_path}')
                stats['changed_files'] += 1

        except Exception as error:
            print(f'problems with File: {this_path}')
            raise error

        stats['packs_used'].update(qpacks)


def check_line(line):
    """
    * Find occurences of old-package in imports or anywhere else.
        * change to new
    * lookup used packs
        * check their members
    """
    changes = {}

    if OLD_PACK in line:
        pos0 = 0
        changed = True
        while changed:
            changed, line, pos0 = fix_pack(line, pos0)
            if changed:
                changes.setdefault('pack', 0)
                changes['pack'] += 1

    qpacks = set()
    for pak in PYPAKS:
        if pak not in line:
            continue
        if '\n' in line:
            break

        qpacks.add(pak)

        num_tries = 0
        pos0 = 0
        changed = True
        while changed:
            if num_tries > 23:
                break

            changed, line, pos0, changed_packs = fix_moved_members(pak, line, pos0)
            if changed:
                qpacks.update(changed_packs)
                num_tries += 1
                changes.setdefault('member', 0)
                changes['member'] += 1
                if '\n' in line:
                    break

    return changes, line, qpacks


def fix_pack(line, pos0):
    """
    Can't remember why I just don't do .replace(OLD_PACK, NEW_PACK) ...
    Well this should work...
    """
    pos1 = line.find(OLD_PACK, pos0)
    if pos1 == -1:
        return False, line, pos0

    changed = False
    pos2 = pos1 + len(OLD_PACK)
    if len(line) == pos2 or line[pos1:pos2] != NEW_PACK:
        line = line[:pos1] + NEW_PACK + line[pos2:]
        changed = True

    return changed, line, pos1 + len(NEW_PACK)


def fix_moved_members(pak, line, pos0):
    pos1 = line.find(pak, pos0)
    changed = False
    if pos1 == -1:
        return changed, line, pos0, []

    pos2 = pos1 + len(pak)
    if pos2 == len(line):
        # end of line, no members accessed
        return changed, line, pos0, []

    qpacks = set()

    if line[pos2] == '.':
        rest_of_line = line[pos2 + 1 :]
        member_name = get_member(rest_of_line)
        if not member_name:
            member_name

        if member_name not in PAK_MEMBERS[pak] and member_name not in IGNORE_MEMBERS:
            try:
                new_pak = MEMBER_PAKS[member_name]
            except KeyError:
                # raise RuntimeError(f'Name "{member_name}" not under any of the paks!')
                print(f'\nWARNING!: Name "{member_name}" not under any of the paks!\n')
                return changed, line, pos0, []

            line = line[:pos1] + new_pak + line[pos2:]
            changed = True
            pos0 = pos1 + len(new_pak)
            qpacks.add(new_pak)
        else:
            pos0 = pos2

    if 'from' in line and IMPORT_STR in line:
        pos3 = pos2 + len(IMPORT_STR)
        if line[pos2:pos3] == IMPORT_STR:
            import_members = [m.strip() for m in line[pos3:].split(',') if m != '*']
            not_in_pak = [m not in PAK_MEMBERS[pak] for m in import_members]
            if any(not_in_pak):
                lines = {}
                for m in import_members:
                    lines.setdefault(MEMBER_PAKS[m], []).append(m)
                new_lines = []
                for new_pak, members in lines.items():
                    new_lines.append(line[:pos1] + new_pak + IMPORT_STR + ', '.join(members))
                    qpacks.add(new_pak)
                line = '\n'.join(new_lines)
                changed = True
                # to avoid seeking through the line again
                pos0 = len(line)

    return changed, line, pos0, qpacks


def get_member(string):
    member = ''
    for l in string:
        if l.isalpha() or l == '_':
            member += l
        else:
            break
    return member


def get_lines(path):
    """
    Return tuple(list,bool) as in:
    (lines of the file, needs_unicode)
    """
    try:
        with open(path) as fob:
            return fob.read().split('\n'), False
    except UnicodeDecodeError:
        needs_unicode = True
        with codecs.open(path, encoding='utf-8-sig') as fob:
            return fob.read().split('\n'), True


def iter_lines(lines):
    for i, line in enumerate(lines):
        line = line.rstrip()
        # skip empty lines
        if not line:
            continue
        # skip comments
        if line.lstrip().startswith('#'):
            continue
        yield i, line


if __name__ == '__main__':
    main()
