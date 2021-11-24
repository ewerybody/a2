import os
import sys

_this_dir = os.path.dirname(__file__)
while 'a2.exe' not in [i.name for i in os.scandir(_this_dir)]:
    _this_dir = os.path.dirname(_this_dir)
A2_PATH = _this_dir
A2UI_PATH = os.path.join(A2_PATH, 'ui')
if A2UI_PATH not in sys.path:
    print(f'adding path: {A2UI_PATH} ...')
    sys.path.insert(0, A2UI_PATH)
