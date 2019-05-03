# adding a2 paths for imports
import os
import sys


this_path = os.path.dirname(__file__)
a2path = os.path.abspath(os.path.join(this_path, '..', '..', '..'))
uipath = os.path.join(a2path, 'ui')
sys.path.append(uipath)
