import a2dev.dependency.autohotkey
import a2dev.dependency.rc_edit
import a2dev.dependency.seven_zip
import a2dev.dependency.sqlite


def main():
    from a2dev.build import CHK_MK
    print('Checking a2 binary dependencies ...')
    a2dev.dependency.autohotkey.check()
    a2dev.dependency.rc_edit.check()
    a2dev.dependency.seven_zip.check()
    a2dev.dependency.sqlite.check()
    print(f'{CHK_MK} Done!')


if __name__ == '__main__':
    main()
