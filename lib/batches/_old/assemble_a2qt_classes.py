import os
import sys
import json
import datetime
import importlib

import PySide2 as pack1
import PySide6 as pack2

P1, P2 = 'PySide2', 'PySide6'
SIDES = [P1, P2]
IND = '    '
IMPORT_LINE = IND + 'from {side}.{pack} import {mod}\n'
THIS_DIR, THISBASE = os.path.split(os.path.abspath(__file__))
RENAMES_NAME = 'members_renamed.json'
FUNC_RENAME_TMP = '{i}{member}.{new_name} = {member}.{old_name}\n'
CHANGES_NAME = 'member_changes.json'
WRAPPER_DIR = os.path.abspath(os.path.join(THIS_DIR, *['..'] * 3, 'ui', 'a2qt'))


def main():
    p1_all, p2_all = get__all__lists()

    imp_all__(pack2, p2_all)
    imp_all__(pack1, p1_all)

    allnames = gather_allnames(p1_all, p2_all)
    p1s, p2s = check_uniqueness(allnames)
    items_in_both = check_same_name_items(allnames, p1s, p2s)
    get_function_changes(items_in_both)
    packs = gather_packs(allnames)
    files = get_file_contents(packs)
    add_renames(files)
    write_files = check_write_files(files)

    if write_files:
        handle_files(write_files, files)
    else:
        print('Nothing to write! All files up-to-date!')


def check_write_files(files):
    write_files = []
    for fname, content in files.items():
        if os.path.isfile(fname):
            with open(fname) as fob:
                unchanged = fob.read() == content
            if unchanged:
                continue
        write_files.append(fname)
    return write_files


def handle_files(write_files, files):
    print('Writing files ...')
    for file_path in write_files:
        with open(file_path, 'w') as fobj:
            print(f'  {os.path.basename(file_path)}')
            fobj.write(files[file_path])


def get_file_contents(packs):
    temp_path = os.path.join(THIS_DIR, THISBASE.replace('.py', '.template'))
    with open(temp_path) as fobj:
        template = fobj.read()

    files = {}
    for qpack, p1items in packs.items():
        p2code = IMPORT_LINE.format(side=P2, pack=qpack, mod='*')
        p1code = ''

        packname = qpack + '.py'
        pack_path = os.path.join(WRAPPER_DIR, packname)
        print('%s' % qpack)
        for subpack, items in p1items.items():
            if items == '*':
                print('  %s: * everything' % (subpack))
                p1code += IMPORT_LINE.format(side=P1, pack=subpack, mod='*')

                if qpack == 'QtCore':
                    p2code += IMPORT_LINE.format(side=P2, pack=qpack, mod='__version__')
                    p2code += IMPORT_LINE.format(side=P2, pack=qpack, mod='__version_info__')
                    p1code += IMPORT_LINE.format(side=P1, pack=qpack, mod='__version__')
                    p1code += IMPORT_LINE.format(side=P1, pack=qpack, mod='__version_info__')

            else:
                p1code += IMPORT_LINE.format(side=P1, pack=subpack, mod=get_wrapped_string(items))
                print('  %s: %i' % (subpack, len(items)))

        files[pack_path] = template.format(pyside2=p2code, pyside1=p1code)
    print('... Assembling finished!\n')
    return files


def get_wrapped_string(items, indents=2, linelen=80):
    if len(items) == 1:
        return items[0]

    items.sort()
    lines = ['(']
    thisline = indents * IND + items[0]
    for item in items[1:]:
        if len(thisline) + 2 + len(item) > linelen:
            lines.append(thisline + ',')
            thisline = indents * IND + item
        else:
            thisline += ', ' + item
    thisline += ')'
    lines.append(thisline)
    return '\n'.join(lines)


def get_imported_pyside_modules():
    psmods = []
    for s in sys.modules.keys():
        if s.startswith(P1):
            parts = s.split('.', 1)
            if len(parts) == 1 or len(parts) == 2 and parts[1].startswith('Q'):
                psmods.append(s)
    return sorted(psmods)


def imp_all__(pack, modlist):
    print('Importing: %s' % pack.__name__)
    psmods = get_imported_pyside_modules()
    for qmod in modlist:
        modpath = pack.__name__ + '.' + qmod
        if modpath not in psmods:
            try:
                importlib.import_module(modpath)
                print('  Imported: %s' % modpath)
            except ImportError as error:
                print(' Error importing: %s\n  %s' % (modpath, error))
        else:
            print('  Already imported: %s' % modpath)


def get__all__lists():
    p1_all = list(pack1.__all__)
    p2_all = list(pack2.__all__)

    # add new pyside2 packages
    for pack in ['QtWidgets', 'QtPrintSupport']:
        if pack not in p2_all:
            p2_all.append(pack)

    for pack in [p1_all, p2_all]:
        # remove QtWebKit and QtScript if in
        for qmod in ['QtScript', 'QtWebKit']:
            if qmod in pack:
                pack.remove(qmod)
        if 'QtUiTools' not in pack:
            pack.append('QtUiTools')

    print('p1_all:\n  %s' % p1_all)
    print('p2_all:\n  %s' % p2_all)
    return p1_all, p2_all


def gather_allnames(p1_all, p2_all):
    allnames = {P1: {'__all__': p1_all}, P2: {'__all__': p2_all}}

    for packname in SIDES:
        uniques, multiples, qpacks = {}, {}, {}
        for qpack in allnames[packname]['__all__']:
            modpath = packname + '.' + qpack
            for name in dir(sys.modules.get(modpath, [])):
                if name.startswith('__'):
                    continue
                if name in uniques:
                    multiples.setdefault(name, []).append(qpack)
                uniques[name] = qpack
                qpacks.setdefault(qpack, []).append(name)
        allnames[packname]['uniques'] = uniques
        allnames[packname]['qpacks'] = qpacks
        if multiples:
            allnames[packname]['multiples'] = multiples
    return allnames


def check_uniqueness(allnames):
    print('Analysis: .................................')
    for packname in SIDES:
        print('%s:' % packname)
        if 'multiples' in allnames[packname]:
            print(' items in multiple packs: %i' % len(allnames[packname]['multiples']))
        else:
            print(' No item names in multiple packages!')
        print(' All unique items: %i' % len(allnames[packname]['uniques']))
        print(' across these %i packages:' % len(allnames[packname]['qpacks']))
        for qpack, qpack_list in allnames[packname]['qpacks'].items():
            print('   %s: %i' % (qpack, len(qpack_list)))

    p1s = set(allnames[P1]['uniques'])
    p2s = set(allnames[P2]['uniques'])
    p2only = p2s.difference(p1s)
    print('Items excusive to %s: %i\n  %s' % (P2, len(p2only), ', '.join(p2only)))
    p1only = p1s.difference(p2s)
    print('Items exclusive to %s: %i\n  %s' % (P1, len(p1only), ', '.join(p1only)))

    print('... Analysis finished!\n')
    return p1s, p2s


def check_same_name_items(allnames, p1s, p2s):
    items_in_both = p1s.intersection(p2s)
    print('Items in both: %i' % len(items_in_both))
    still_in_place = {}
    moved = {}
    moved_how = {}
    for item in items_in_both:
        p1pack = allnames[P1]['uniques'][item]
        p2pack = allnames[P2]['uniques'][item]
        if p1pack == p2pack:
            still_in_place[item] = p1pack
        else:
            moved[item] = (p1pack, p2pack)
            key = '>'.join(moved[item])
            moved_how.setdefault(key, 0)
            moved_how[key] += 1
    print('Items still in same package: %i' % len(still_in_place))
    print('Items moved: %i' % len(moved))
    for label, count in moved_how.items():
        print('  %s: %i' % (label, count))

    items_in_both = {'same_pack': still_in_place, 'moved': moved}
    return items_in_both


def gather_packs(allnames):
    side = {}
    for qpack, qpack_list in allnames[P2]['qpacks'].items():
        side[qpack] = {}

        for item in qpack_list:
            qpack1 = allnames[P1]['uniques'].get(item)
            if qpack1:
                side[qpack].setdefault(qpack1, []).append(item)

        for _pack, _packlist in side[qpack].items():
            if sorted(_packlist) == sorted(allnames[P1]['qpacks'][_pack]):
                side[qpack][_pack] = '*'
            else:
                # this means if there are no PySide2 items missing in 1
                if not set(_packlist).difference(allnames[P1]['qpacks'][_pack]):
                    old_items = set(allnames[P1]['qpacks'][_pack]).difference(_packlist)
                    # and if the old items do not belong to PySide2 anyway:
                    if old_items.isdisjoint(allnames[P2]['uniques']):
                        side[qpack][_pack] = '*'

    return side


def get_function_changes(items_in_both):
    changes = {}
    num_changes = 0
    for typ in ['same_pack', 'moved']:
        for name, pack_names in items_in_both[typ].items():
            if isinstance(pack_names, tuple):
                pack_name1, pack_name2 = pack_names
            else:
                pack_name1, pack_name2 = pack_names, pack_names

            p1members = dir(getattr(sys.modules[P1 + '.' + pack_name1], name))
            p2members = dir(getattr(sys.modules[P2 + '.' + pack_name2], name))
            old_members = set(p1members).difference(p2members)
            #            if 'trUtf8' in old_members:
            #                old_members.remove('trUtf8')

            new_members = set(p2members).difference(p1members)
            if old_members or new_members:
                # print('Members changed: %s %s' % (pack_name, name))
                changes.setdefault(pack_name2, {}).setdefault(name, {})
                if old_members:
                    # print('  members removed %i: %s' % (len(old_members), ','.join(old_members)))
                    changes[pack_name2][name]['removed'] = list(old_members)
                    num_changes += len(old_members)
                if new_members:
                    # print('  members added %i: %s' % (len(new_members), ','.join(new_members)))
                    changes[pack_name2][name]['added'] = list(new_members)
                    num_changes += len(new_members)

    print('num_changes tracked: %s' % num_changes)
    file_path = os.path.join(THIS_DIR, CHANGES_NAME)
    with open(file_path, 'w') as fob:
        json.dump(changes, fob, indent=2, sort_keys=True)
    print('  written to: %s\n' % file_path)


def add_renames(files):
    """
    Looks up renames json file in the style::

        {
          "QtWidgets": {
              "QHeaderView": [
                ["setSectionResizeMode", "setResizeMode"]
              ]
          }
        }

    ...
    """
    renames_path = os.path.join(THIS_DIR, RENAMES_NAME)
    if not os.path.isfile(renames_path):
        print(f'No renames file found! ({renames_path})')
        return

    with open(renames_path) as fob:
        renames = json.load(fob)

    for pack, members in renames.items():
        for file_path in files:
            if file_path.endswith(pack + '.py'):
                break
        else:
            continue

        content = files.get(file_path) + '\n'
        for member, renames_list in members.items():
            for new_name, old_name in renames_list:
                content += FUNC_RENAME_TMP.format(
                    i=IND, member=member, new_name=new_name, old_name=old_name
                )
        files[file_path] = content


if __name__ == '__main__':
    main()
