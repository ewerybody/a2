import os
import sys

this_dir = os.path.dirname(__file__)
while 'a2.exe' not in [i.name for i in os.scandir(this_dir)]:
    this_dir = os.path.dirname(this_dir)
ui_path = os.path.join(this_dir, 'ui')
if ui_path not in sys.path:
    print(f'adding path: {ui_path} ...')
    sys.path.insert(0, ui_path)
