import os
import codecs
import importlib
from pprint import pprint

import PySide2 as pyside_package

IMPORT_STR = ' import '
FROM_IMPORT = 'from PySide2 import '


def main():
    pypaks = pyside_package.__all__
    print('pypaks:', pypaks)
    pak_members = {}
    member_paks = {}
    for pakname in pypaks:
        qmod = importlib.import_module(f'{pyside_package.__name__}.{pakname}')
        members = [m for m in dir(qmod) if not m.startswith('_')]
        pak_members[pakname] = members
        for m in members:
            member_paks[m] = pakname

    uipath = os.path.abspath(os.path.join(__file__, '..', '..', '..', 'ui'))
    numpys, pydirs, qlines, numqfiles, changed_files, change_count = 0, 0, 0, 0, 0, 0
    for dirpath, folders, files in os.walk(uipath):
        pyfiles = [f for f in files if os.path.splitext(f)[1] == '.py']
        if pyfiles:
            pydirs += 1
            numpys += len(pyfiles)
            for pyfile in pyfiles:
                this_q_lines = []
                import_lines = []
                qpacks = []
                try:
                    this_path = os.path.join(dirpath, pyfile)
                    needs_unicode = False
                    try:
                        with open(this_path) as fob:
                            lines = fob.read().split('\n')
                    except UnicodeDecodeError:
                        needs_unicode = True
                        with codecs.open(this_path, encoding='utf-8-sig') as fob:
                            lines = fob.read().split('\n')

                    print(f'checking {len(lines)} lines in file {this_path} ...')

                    change_file = False
                    for i, line in enumerate(lines):
                        line = line.rstrip()
                        # skip empty lines
                        if not line:
                            continue
                        # skip comments
                        if line.lstrip().startswith('#'):
                            continue

                        try:
                            changed, newline, this_qpacks = check_line(line, pypaks, pak_members, member_paks)
                            if changed:
                                change_file = True
                                lines[i] = newline
                                change_count += 1
                            qpacks.extend(this_qpacks)
                        except Exception as error:
                            print(f'problems with File: "{this_path}", line {i}')
                            raise error

                        if line.strip().startswith(FROM_IMPORT):
                            import_lines.append(i)

                    if import_lines:
                        if len(import_lines) > 1:
                            raise RuntimeError('Multiple import lines?!?!', import_lines, this_path)
                        current_paks = [p.strip() for p in lines[import_lines[0]][len(FROM_IMPORT):].split(',')]
                        new_paks = set(qpacks)
                        if new_paks != set(current_paks):
                            lines[import_lines[0]] = FROM_IMPORT + ', '.join(new_paks)
                            change_file = True
                            change_count += 1

                    if change_file:
                        if needs_unicode:
                            with codecs.open(this_path, 'w', encoding='utf-8-sig') as fob:
                                fob.write('\n'.join(lines))
                        else:
                            with open(this_path, 'w') as fob:
                                fob.write('\n'.join(lines))
                        print(f'changed file: {this_path}')
                        changed_files += 1

                except Exception as error:
                    print(f'problems with file: {this_path}')
                    raise error

                if this_q_lines:
                    numqfiles += 1
                    print('Qt lines in file: %s\n  %s' % (pyfile, '  \n'.join(this_q_lines)))

    print('numpys:', numpys)
    print('pydirs:', pydirs)
    print('numqfiles:', numqfiles)
    print('qlines:', qlines)
    print('changed_files', changed_files)
    print('change_count', change_count)


def check_line(line, pypaks, pak_members, member_paks):
    any_changed = False

    if 'PySide' in line:
        pos0 = 0
        changed = True
        while changed:
            changed, line, pos0 = fix_pyside1(line, pos0)
            if changed:
                any_changed = True

    qpacks = []
    for pak in pypaks:
        if pak not in line:
            continue
        if '\n' in line:
            break

        qpacks.append(pak)

        num_tries = 0
        pos0 = 0
        changed = True
        while changed:
            if num_tries > 23:
                break
            changed, line, pos0, changed_packs = fix_moved_members(pak, line, pos0, pak_members, member_paks)
            if changed:
                qpacks.extend(changed_packs)
                num_tries += 1
                any_changed = True
                if '\n' in line:
                    break

    return any_changed, line, qpacks


def fix_pyside1(line, pos0):
    pyside1 = 'PySide'
    pos1 = line.find(pyside1, pos0)
    if pos1 == -1:
        return False, line, pos0

    changed = False
    pos0 = pos1 + len(pyside1)
    if len(line) == pos0 or line[pos0] != '2':
        line = line[:pos0] + '2' + line[pos0:]
        changed = True

    return changed, line, pos0


def fix_moved_members(pak, line, pos0, pak_members, member_paks):
    pos1 = line.find(pak, pos0)
    changed = False
    if pos1 == -1:
        return changed, line, pos0, []

    pos2 = pos1 + len(pak)
    if pos2 == len(line):
        return changed, line, pos0, []

    qpacks = []

    if line[pos2] == '.':
        rest_of_line = line[pos2 + 1:]
        member_name = get_member(rest_of_line)
        if member_name not in pak_members[pak]:
            try:
                new_pak = member_paks[member_name]
            except KeyError:
                raise RuntimeError(f'Name "{member_name}" not under any of the paks!')

            line = line[:pos1] + new_pak + line[pos2:]
            changed = True
            pos0 = pos1 + len(new_pak)
            qpacks.append(new_pak)
        else:
            pos0 = pos2

    if 'from' in line and IMPORT_STR in line:
        pos3 = pos2 + len(IMPORT_STR)
        if line[pos2:pos3] == IMPORT_STR:
            import_members = [m.strip() for m in line[pos3:].split(',')]
            not_in_pak = [m not in pak_members[pak] for m in import_members]
            if any(not_in_pak):
                lines = {}
                for m in import_members:
                    lines.setdefault(member_paks[m], []).append(m)
                new_lines = []
                for new_pak, members in lines.items():
                    new_lines.append(line[:pos1] + new_pak + IMPORT_STR + ', '.join(members))
                    qpacks.append(new_pak)
                line = '\n'.join(new_lines)
                changed = True
                # to avoid seeking through the line again
                pos0 = len(line)

    return changed, line, pos0, qpacks


def get_member(string):
    member = ''
    for l in string:
        if l.isalpha():
            member += l
        else:
            return member


if __name__ == '__main__':
    main()
