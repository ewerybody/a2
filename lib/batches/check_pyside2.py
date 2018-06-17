import os
import codecs
import importlib
from pprint import pprint

import PySide2 as pyside_package


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

    pprint(member_paks)

    uipath = os.path.abspath(os.path.join(__file__, '..', '..', '..', 'ui'))
    numpys, pydirs, qlines, numqfiles = 0, 0, 0, 0
    for dirpath, folders, files in os.walk(uipath):
        pyfiles = [f for f in files if os.path.splitext(f)[1] == '.py']
        if pyfiles:
            pydirs += 1
            numpys += len(pyfiles)
            for pyfile in pyfiles:
                this_q_lines = []
                try:
                    this_path = os.path.join(dirpath, pyfile)
                    with codecs.open(this_path, encoding='utf-8-sig') as fob:
                        try:
                            lines = fob.read().split('\n')
                        except UnicodeDecodeError:
                            print(f'UnicodeDecodeError file: {this_path}')

                    change_file = False
                    for i, line in enumerate(lines):
                        line = line.rstrip()
                        if not line:
                            continue

                        changed, newline = check_line(line, pypaks, pak_members, member_paks)
                        if changed:
                            change_file = True
                            lines[i] = newline

                    if change_file:
                        with codecs.open(this_path, 'w', encoding='utf-8-sig') as fob:
                            fob.write('\n'.join(lines))
                        print(f'changed file: {this_path}')

                except Exception as error:
                    print(this_path)
                    raise error

                if this_q_lines:
                    numqfiles += 1
                    print('Qt lines in file: %s\n  %s' % (pyfile, '  \n'.join(this_q_lines)))

    print('numpys:', numpys)
    print('pydirs:', pydirs)
    print('numqfiles:', numqfiles)
    print('qlines:', qlines)


def check_line(line, pypaks, pak_members, member_paks):
    changed = False
    pos0 = 0
    for pak in pypaks:
        pos1 = line.find(pak, pos0)
        if pos1 != -1:
            pos2 = pos1 + len(pak)
            if pos2 == len(line):
                break

            if line[pos2] == '.':
                rest_of_line = line[pos2 + 1:]
                member_name = get_member(rest_of_line)
                if member_name not in pak_members[pak]:
                    try:
                        new_pak = member_paks[member_name]
                        line = line[:pos1] + new_pak + line[pos2:]
                        changed = True
                    except:
                        print(member_name)

    return changed, line

def get_member(string):
    member = ''
    for l in string:
        if l.isalpha():
            member += l
        else:
            return member


if __name__ == '__main__':
    main()
