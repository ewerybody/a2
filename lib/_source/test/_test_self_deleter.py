"""
We need the self deleter thing for the Uninstaller.
* It should remove itself and
* the directory its contained
  * if it's empty!

So what do we test:
* for both silent and ui versions:
  * create folder with only exe
    * check if it deletes itself + folder
  * create folder with exe + extra stuff
    * check if it deletes itself and keeps other files
"""
import os
import sys
import time
from os.path import join
import shutil
import subprocess

THIS_DIR, NAME = os.path.split(__file__)
NAME = os.path.splitext(NAME)[0]
THIS_DIR = os.path.abspath(THIS_DIR)
SOURCE_DIR = os.path.dirname(THIS_DIR)

TEST_DIR = join(THIS_DIR, f'_ {NAME}')
EXTRA_FILE = join(TEST_DIR, 'random_test_name_4favafvar4var.ext')
TMP_EXE = join(THIS_DIR, f'{NAME}.exe')
TEST_EXE = join(TEST_DIR, f'{NAME}.exe')
AHK_DIR = os.path.abspath(join(THIS_DIR, '..', '..', 'Autohotkey'))
AHK_EXE = join('Autohotkey.exe')
COMPILER = join(AHK_DIR, 'Compiler', 'Ahk2Exe.exe')
TEST_SCRIPT = join(THIS_DIR, NAME + '.ahk')
CHKMK = b'\xe2\x9c\x94'.decode()
EXMRK = b'\xe2\x9c\x96'.decode()
MAX_WAIT = 3
WAIT_STEP = 0.25


def main():
    successes = 0
    run_nr = 0
    for extra_file in True, False:
        for args in ([TEST_EXE], [TEST_EXE, '--silent']):
            run_nr += 1
            print('run_nr: %s' % run_nr)

            if os.path.isdir(TEST_DIR):
                shutil.rmtree(TEST_DIR)
            os.mkdir(TEST_DIR)

            if extra_file:
                with open(EXTRA_FILE, 'w', encoding='utf8') as fileobj:
                    fileobj.write(CHKMK * 50)

            _prnt('Compiling ... ')

            subprocess.call(
                [COMPILER, '/in', TEST_SCRIPT, '/out', TEST_EXE, '/ahk', AHK_EXE], cwd=SOURCE_DIR
            )

            if os.path.isfile(TEST_EXE):
                print(f'{CHKMK} done - {TEST_EXE}')
            else:
                print(f'{EXMRK} Failed! - {TEST_EXE}')
                return

            _prnt('Calling executable ... ')
            pid = subprocess.Popen(args).pid
            print(f'{CHKMK} done - {pid}')

            print('waiting for deletion ...\n')
            waited = 0
            while os.path.isfile(TEST_EXE):
                _prnt('.')
                time.sleep(WAIT_STEP)
                waited += WAIT_STEP
                if waited > MAX_WAIT:
                    break

            time.sleep(WAIT_STEP)

            if os.path.isfile(TEST_EXE):
                print(f'\n{EXMRK} Executable deletion FAILED!')
                return

            if os.path.isdir(TEST_DIR) and not extra_file:
                print(f'\n{EXMRK} Folder deletion FAILED!')
                return
            if not os.path.isdir(TEST_DIR) and extra_file:
                print(f'\n{EXMRK} Keeping Folder FAILED!')
                return
            else:
                print(f'\n{CHKMK} deletion done!')

            print(f'{CHKMK} run_nr: %s' % run_nr)
            successes += 1

    if not successes:
        print(f'\n{EXMRK} FAILED!')
    else:
        print(f'\n{CHKMK} Test PASSED! ({successes})')


_prnt = sys.stdout.write


if __name__ == '__main__':
    main()
