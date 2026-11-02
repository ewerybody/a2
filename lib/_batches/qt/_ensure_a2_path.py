import sys
from pathlib import Path

_this_dir = Path(__file__).parent
while not (_this_dir / 'a2.exe').is_file():
    _this_dir = _this_dir.parent
A2_PATH = _this_dir
A2UI_PATH = A2_PATH/ 'ui'
if str(A2UI_PATH) not in sys.path:
    print(f'adding path: {A2UI_PATH} ...')
    sys.path.insert(0, str(A2UI_PATH))
