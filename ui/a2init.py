'''
Foundation module to host basic info and functionality

Everything thats needed by but itself has no constrains to the user interface.
Such as paths and os tweaks. Mainly this is to thin out the ui module but also
to make functionality available without passing the main ui object.

Created on Mar 11, 2016

@author: eRiC
'''
import os
import logging
from os.path import exists, join, dirname


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class Paths(object):
    def __init__(self):
        self.ui = dirname(__file__)
        if not self.ui:
            cwd = os.getcwd()
            if exists(join(cwd, 'a2ui.py')):
                self.ui = cwd
                log.info('fetched a2ui dir from cwd... %s' % cwd)
            else:
                raise Exception('a2ui start interrupted! '
                                'Could not get main Ui dir!')

        self.a2 = dirname(self.ui)
        self.lib = join(self.a2, 'lib')
        self.starter_exe = join(self.a2, 'a2Starter.exe')
        self.a2_script = join(self.a2, 'a2.ahk')
        self.settings = get_settings_path()
        self.modules = join(self.a2, 'modules')
        
        # test if all necessary directories are present:
        main_items = [self.a2_script, self.starter_exe, self.lib,
                      self.modules, self.settings, self.ui]
        missing = [p for p in main_items if not exists(p)]
        if missing:
            raise Exception('a2ui start interrupted! %s not found in main dir!'
                            % missing)
        if not os.access(self.settings, os.W_OK):
            raise Exception('a2ui start interrupted! %s inaccessable!'
                            % self.settings)
    
        # by default the Autohotkey.exe in the lib should be uses
        # but we need an option for that a user can put it to whatever he wants
        self.autohotkey = join(self.lib, 'AutoHotkey', 'AutoHotkey.exe')
        self.db = join(self.settings, 'a2.db')


def get_settings_path():
    """
    TODO: same shit: make it changable
    """
    return join(dirname(dirname(__file__)), 'settings')


def set_windows_startup(state=True):
    """
    might be doable via python but this is just too easy with AHKs A_Startup
    """
    import ahk
    print('int(state): %s' % int(state))
    ahk.call_cmd('set_windows_startup', paths.a2, int(state))


paths = Paths()
