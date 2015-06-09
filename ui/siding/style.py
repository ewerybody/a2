###############################################################################
#
# Copyright 2012 Siding Developers (see AUTHORS.txt)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
###############################################################################
"""
An easy to use style system with support for style inheritance, easy icon
loading, relative-URLs in Qt style sheets, Aero Glass on Windows, and
relatively easy hot reloads.
"""

###############################################################################
# Imports
###############################################################################

import argparse
import base64
import ConfigParser
import hashlib
import os
import urllib
import re
import sys
import weakref

from PySide.QtCore import Signal, QUrl, QObject
from PySide.QtGui import QApplication, QIcon, QWidget, QPixmap

from siding import profile

if os.name == 'nt':
    from siding import _aeroglass
else:
    _aeroglass = None

###############################################################################
# Logging
###############################################################################

import logging
log = logging.getLogger("siding.style")

###############################################################################
# Constants and Storage
###############################################################################

STYLE_KEYS = {
    'QMotifStyle': 'motif',
    'QCDEStyle': 'cde',
    'QCleanlooksStyle': 'cleanlooks',
    'QGtkStyle': 'gtk',
    'QMacStyle': 'mac',
    'QPlastiqueStyle': 'plastique',
    'QWindowsStyle': 'windows',
    'QWindowsXPStyle': 'windowsxp',
    'QWindowsVistaStyle': 'windowsvista'
    }

loaded_styles = {}

safe_mode = False

QSS_IMPORT = re.compile(r"@import\s+(.*?)\s*(?:;|$)")
QSS_URL = re.compile(r"url\((.*?)\)", re.DOTALL)
QSS_AERO = re.compile(r"#IFAERO\s*(.*?)\s*(?:#ELSE\s*(.*?)\s*)?#END", re.DOTALL)

###############################################################################
# Style Class
###############################################################################

class Style(object):
    """
    This class stores all information on any given style, and provides
    functions for working with style files and applying styles.

    In most cases, you won't have to work with this class directly.
    """

    inherits = None
    """ The name of the style being inherited. """

    def __init__(self, name, path=None):
        self.name = name

        # Make sure we've got a path.
        if path and os.path.isabs(path):
            if not os.path.exists(path):
                log.error('Cannot find style: %s' % name)
                raise IOError('Cannot find style: %s' % name)
            source = 0

        else:
            if not path:
                path = profile.join(u'styles', name)

            if not profile.exists(path):
                log.error('Cannot find style: %s' % name)
                raise IOError('Cannot find style: %s' % name)

            source = profile.get_source(path)

        # Store the path.
        self.path = path
        self.path_source = source

        # Now, load the theme.
        self.reload(False)

    def __str__(self):
        return '<Style(%r)>' % self.name

    @property
    def active(self):
        """ Whether or not this is the active style. """
        return self is loaded_styles.get(None)

    ##### Qt Style Sheet Loading ##############################################

    def _import_qss(self, path, match):
        """ Parse an @import statement within QSS. """
        url = match.group(1)
        if url.startswith('url('):
            if not url.endswith(')'):
                return match.group(0)
            url = url[4:-1]

        # Try parsing the URL. Make sure not to allow inheritance for that
        # step, as we want to use the style we're inheriting to load the
        # QSS in that case.
        url = self._qss_url(path, url, False, True, True)
        if not url or not self.has_file(url):
            if self.inherits:
                data = loaded_styles[self.inherits]._import_qss(path, match)
                if not data:
                    log.warning('Cannot find %r in style %r.' % (
                            url, self.name))
                return data
            return ''

        return self.load_qss(url)

    def _qss_url(self, path, url, allow_inheritance=True, _suppress=False,
                 for_import=False):
        """
        Process a url() and return an absolute URL, or None if the URL isn't
        valid.
        """
        if (url.startswith('"') and url.endswith('"')) or \
                (url.startswith("'") and url.endswith("'")):
            url = url[1:-1]

        # Make a QUrl.
        url = QUrl(url.decode('unicode_escape'))

        # Is it a data uri?
        if url.scheme() == 'data':
            # Extract the useful information from the path.
            format, sep, data = url.path().partition(',')
            if not sep and not data:
                data = format
                format = ''

            mimetype, _, format = format.partition(';')
            if not mimetype:
                ext = 'txt'
            else:
                _, _, ext = mimetype.rpartition('/')
            if not format:
                format = 'charset=US-ASCII'

            # Build the filename.
            fn = os.path.join(profile.cache_path, u'data-uris',
                    '%s.%s' % (hashlib.md5(data).hexdigest(), ext))

            # Ensure the path exists and write the file.
            try:
                if not os.path.exists(os.path.dirname(fn)):
                    os.makedirs(os.path.dirname(fn))
                with open(fn, 'wb') as f:
                    if format == 'base64':
                        f.write(base64.b64decode(data))
                    elif format.startswith('charset='):
                        data = urllib.unquote(data).encode('latin1')
                        cs = format[8:]
                        if cs and cs.lower() not in ('utf-8','utf8'):
                            data = data.decode(cs).encode('utf-8')
                        f.write(data)
                    else:
                        return
            except (ValueError, OSError, IOError, TypeError):
                log.debug('Error parsing data URI.', exc_info=1)
                return

            # Substitute the right / on Windows, and return the path.
            if os.name == 'nt':
                fn = fn.replace('\\', '/')
            return fn

        # If it's relative, build an absolute URL. If not, return.
        if not url.isRelative():
            return

        url = url.toLocalFile()
        if url.startswith('/'):
            url = url[1:]
        else:
            url = profile.join(path, url)

        # If we're dealing with import, return a relative path.
        if for_import:
            return url

        return self.get_path(url, allow_inheritance, False, _suppress)

    def _update_url(self, path, match):
        """
        Process a url() in QSS, handling relative URLs and returning absolute
        paths.
        """
        url = self._qss_url(path, match.group(1))
        if not url:
            return match.group(0)
        if os.name == 'nt':
            url = url.replace('\\','/')
        return 'url("%s")' % url.encode('unicode_escape')

    def _qss_aero(self, match):
        """ Process a block of #IFAERO ... #ELSE ... #END in QSS. """
        if _aeroglass and _aeroglass.manager.status:
            return match.group(1)
        return match.group(2)

    def load_qss(self, path):
        """
        Load a Qt style sheet from a source file and do some simple
        pre-processing to allow the use of relative URLs and an @import
        statement. Examples:

        .. code-block:: css

            QPushButton {
                @import 'button_base.qss';

                some-invalid-property: url('relative/url.png');
                background-image: url('/images/button.png');
            }

        Assuming that ``button_base.qss`` contains ``"color: red;"``, and this
        style lives in ``/path/to/example`` while the Qt style sheet we're
        processing is at ``/path/to/example/qss/file.qss``, the following would
        result:

        .. code-block:: css

            QPushButton {
                color: red;

                some-invalid-property: url('/path/to/example/qss/relative/url.png');
                background-image: url('/path/to/example/images/button.png');
            }

        """
        if not self.has_file(path):
            return ''

        # Build the relative path for relative URLs.
        start_path = os.path.dirname(path)
        if start_path.startswith(self.path):
            start_path = start_path[len(self.path)+1:]

        start_path = profile.join(start_path, 'test')

        # Get the file.
        f = self.get_file(path, 'rU')
        if not f:
            return ''
        qss = f.read()
        f.close()

        log.debug('Begin Loading QSS: %s' % path)
        log.debug('---- Before ----')
        log.debug(qss)
        
        # Process #IFAERO .. #ELSE .. #END
        qss = QSS_AERO.sub(self._qss_aero, qss)

        # Process the @import statement.
        qss = QSS_IMPORT.sub(lambda m: self._import_qss(start_path, m), qss)

        # Process the rest of the urls.
        qss = QSS_URL.sub(lambda m: self._update_url(start_path, m), qss)

        log.debug('---- After ----')
        log.debug(qss)
        log.debug('End Loading QSS: %s' % path)

        return qss

    ##### Loading #############################################################

    def apply(self):
        """ Apply this style to the application. """
        log.info('Applying style: %s' % self.name)

        app = QApplication.instance()

        if self.data.get('aero'):
            self._enable_aero()
        else:
            self._disable_aero()

        # The Widget Style
        ui = self.data.get('ui', profile.get('siding/widget-style'))
        app.setStyle(ui)

        # Now, load the application QSS.
        qss = self.load_qss('application.qss')
        app.setStyleSheet(qss)

        # Restyle every styled widget.
        for ref in _managed_widgets.keys():
            self.style_widget(None, ref)

        # Set this as the current style.
        if not self.active:
            loaded_styles[None] = self

    def reload(self, apply=True, _chain=None):
        """
        Reload this style's INI file and reapply the style if requested.
        """
        if hasattr(self, 'data'):
            log.info('Reloading style: %s (%s)' % (self.name, self.path))
        else:
            log.info('Loading style: %s (%s)' % (self.name, self.path))

        file = self.get_file('style.ini', use_inheritance=False)
        if not file:
            log.error('Cannot open style.ini for style: %s' % self.name)
            raise IOError('Cannot open style.ini for style: %s' % self.name)

        parser = ConfigParser.SafeConfigParser()
        parser.readfp(file)
        file.close()

        if not parser.has_section('Style'):
            log.error('Invalid style.ini for style: %s' % self.name)
            raise ValueError('No Style section in style.ini for style: %s' %
                        self.name)

        # If this style inherits, reload the style it inherits from. Be sure
        # not to start an infinite loop.
        if parser.has_option('Style', 'inherit'):
            self.inherits = inherits = parser.get('Style', 'inherit')
        else:
            self.inherits = inherits = None
        if inherits:
            if inherits == self.name:
                log.warning('Style %r tries to inherit itself.' % self.name)
                log.debug('Disabling inheritance for style: %s' % self.name)
                self.inherits = inherits = None
            elif _chain and self.name in _chain:
                log.warning('Style inheritance loop: %r' % _chain)
                log.debug('Disabling inheritance for style: %s' % self.name)
                self.inherits = inherits = None
            elif not _chain:
                _chain = []

            if inherits:
                _chain.append(self.name)

                if inherits in loaded_styles:
                    loaded_styles[inherits].reload(False, _chain=_chain)
                else:
                    try:
                        load(inherits, False)
                    except IOError:
                        log.warning(
                            'Style %r tries to inherit unknown style %r.' % (
                                self.name, inherits))
                        log.debug('Disabling inheritance for style: %s' %
                                self.name)
                        self.inherits = inherits = None

        # Reset the style data, inheriting it if we can.
        if inherits:
            self.data = loaded_styles[inherits].data.copy()
        else:
            self.data = {}

        # Now load all the data we have from the actual style.
        for key, value in parser.items('Style'):
            key = key.lower()
            if key == 'inherit':
                continue
            self.data[key] = value

        # Delete the settings object.
        del parser

        # Reapply the style if requested.
        if apply:
            self.apply()

    def style_widget(self, widget, _ref=None):
        """
        Reapply the styles associated with the :class:`~PySide.QtGui.QWidget`
        ``widget``. In almost all cases, you'll want to use
        :func:`siding.style.apply_stylesheet` and
        :func:`siding.style.remove_stylesheet` rather than calling this
        directly.
        """
        if not _ref:
            _ref = _find_widget(widget)
        if not _ref:
            return
        if not widget:
            widget = _ref()
        if not widget:
            del _managed_widgets[_ref]
            return

        # Get the list of styles, and make a list to store the QSS in
        # temporarily.
        widget_styles = _managed_widgets[_ref]
        qss = []

        log.debug('Begin rebuilding styles on widget %r.' % widget)

        for style in widget_styles:
            # If it starts with "data:", just chop that off and add it,
            # otherwise load the QSS with the appropriate function.
            if style.startswith("data:"):
                qss.append(style[5:])
                continue

            qss.append(self.load_qss(style))

        # Now, apply the styles.
        log.debug('Applying new styles to widget %r.' % widget)
        widget.setStyleSheet('\n'.join(qss))

        log.debug('End rebuilding styles on widget %r.' % widget)

    ##### Aero Helpers ########################################################

    def _enable_aero(self):
        """ Enable Aero Glass. """
        if _aeroglass:
            _aeroglass.enable()

    def _disable_aero(self):
        """ Disable Aero Glass. """
        if _aeroglass:
            _aeroglass.disable()

    ##### Path Helpers ########################################################

    def icon(self, name, extension='png', use_inheritance=True,
             allow_theme=True):
        """
        Find an icon with the given ``name`` and return a
        :class:`~PySide.QtGui.QIcon` of that icon. If ``use_inheritance`` is
        True and this style doesn't have an icon with the given name, the
        icon will be searched for in the style this style inherits.
        
        If ``allow_theme`` is True and the icon can't be located in a style, it
        will be retrieved with :func:`PySide.QtGui.QIcon.fromTheme` as a last
        resort as long as the style allows the use of system icons.
        """
        icon = None

        fn = '%s.%s' % (name, extension)
        path = profile.join('images', fn)

        if self.path_source != profile.SOURCE_PKG_RESOURCES:
            file = self.get_path(path, use_inheritance)
            if file and os.path.exists(file):
                icon = QIcon(file)
        else:
            if self.has_file(path, use_inheritance):
                f = self.get_file(path, use_inheritance=use_inheritance)
                if f:
                    pixmap = QPixmap()
                    pixmap.loadFromData(f.read())
                    icon = QIcon(pixmap)
                    del pixmap
                    f.close()

        if not icon and use_inheritance and self.inherits:
            icon = loaded_styles[self.inherits].icon(name, extension,
                                                  use_inheritance, allow_theme)

        if not icon and allow_theme:
            if QIcon.hasThemeIcon(name):
                icon = QIcon.fromTheme(name)

        if not icon:
            icon = QIcon()

        return icon

    def has_file(self, file, use_inheritance=True, secure=True,
                 _suppress=False):
        """
        Return True if the given file exists in this style, otherwise False. If
        ``use_inheritance`` is True, styles this style inherits from will be
        checked as well.
        """
        path = profile.normpath(profile.join(self.path, file))
        if secure and not path.startswith(self.path):
            raise ValueError("File path not within style.")

        if not profile.exists(path, source=self.path_source):
            if use_inheritance and self.inherits:
                return loaded_styles[self.inherits].has_file(file,
                                                             secure=secure)
            return False

        return True

    def get_file(self, file, mode='rb', use_inheritance=True, secure=True,
                 _suppress=False):
        """
        Return a file or file-like object for the given ``file`` in this
        style. If ``secure`` is True, the path will be checked before the
        file is opened to ensure it resides within the root of this style.

        If ``use_inheritance`` is True and the file doesn't exist within this
        style, it will be searched for in the style this style inherits.

        If the file cannot be found at all, returns ``None``.
        """
        path = profile.normpath(profile.join(self.path, file))
        if secure and not path.startswith(self.path):
            raise ValueError("File path not within style.")

        if not profile.exists(path, source=self.path_source):
            if use_inheritance and self.inherits:
                return loaded_styles[self.inherits].get_file(file, mode,
                                                             secure=secure)
            if not _suppress:
                log.warning('Cannot find %r in style: %s' % (file, self.name))
            return None

        return profile.get_file(path, mode, source=self.path_source)

    def get_path(self, file, use_inheritance=True, secure=True,
                 _suppress=False):
        """
        Return a path to the given ``file`` relative to this style. If
        ``secure`` is True, the path will be checked to ensure it resides
        within the root of this style.
        
        If ``use_inheritance`` is True and the file doesn't exist within this
        style, it will be searched for in the style this style inherits.
        
        If the file cannot be found at all, returns ``None``.
        """
        path = profile.normpath(profile.join(self.path, file))
        if secure and not path.startswith(self.path):
            raise ValueError("File path not within style.")

        if not profile.exists(path, source=self.path_source):
            if use_inheritance and self.inherits:
                return loaded_styles[self.inherits].get_path(file,
                                                             secure=secure)
            if not _suppress:
                log.warning('Cannot find %r in style: %s' % (file, self.name))
            return None

        return profile.get_filename(path, source=self.path_source)

###############################################################################
# The Null Style
###############################################################################

class NullStyle(Style):
    """
    The NullStyle provides a default style if no styles are available. It
    doesn't load anything.
    """
    def __init__(self, name='null', path=None):
        self.name = name
        self.path = path
        self.path_source = 0

        self.data = {
            'name': 'Null Style',
            'description': 'The not-a-style-at-all style.',
        }

    def reload(self, apply=True, _chain=None):
        """ Do nothing but, possibly, apply the style. """
        if apply:
            self.apply()

    def has_file(self, file, use_inheritance=True, secure=True,
                 _suppress=False):
        """ Return False, as the NullStyle has no files. """
        return False

    def get_file(self, file, mode='rb', use_inheritance=True, secure=True,
                 _suppress=False):
        """ Return None, as the NullStyle has no files. """
        return None

    def get_path(self, file, use_inheritance=True, secure=True,
                 _suppress=False):
        """ Return None, as the NullStyle has no files. """
        return None

loaded_styles[None] = NullStyle()

###############################################################################
# Widget Management
###############################################################################

_managed_widgets = {}

def _find_widget(widget):
    """
    Find the widget in our list of tracked widgets and return the weak
    reference.
    """
    for ref in _managed_widgets.keys():
        wid = ref()
        if not wid:
            del _managed_widgets[ref]
            continue
        if wid is widget:
            return ref

###############################################################################
# Styling Functions
###############################################################################

def enable_aero(widget, margin=(-1, -1, -1, -1)):
    """
    Enable Aero Glass for the provided widget. This only functions on Windows
    and when Aero Glass is enabled system-wide.
    """
    if _aeroglass:
        _aeroglass.add(widget, margin)

def disable_aero(widget):
    """ Disable Aero Glass for the provided widget. """
    if _aeroglass:
        _aeroglass.remove(widget)

def icon(name, extension='png', style=None):
    """
    Get an icon with the given name from the active style, or a style with the
    name given in style.
    """
    if not style in loaded_styles:
        style = None

    return loaded_styles[style].icon(name, extension=extension)

def apply_stylesheet(widget, *paths):
    """
    Apply the stylesheet at the provided path(s) to the
    :class:`~PySide.QtGui.QWidget` ``widget``. More than one path can be
    supplied to apply more than one stylesheet to a widget.

    The stylesheet will be processed with the :func:`~Style.load_qss` function
    of the active style whenever it's reloaded, allowing for the use of the
    ``@import`` statement as well as relative URLs.

    In addition, this function will remember the widget and restyle it
    whenever the current style is reloaded or a new style is activated.

    If you want to include a raw Qt style sheet, rather than loading from a
    file, prefix the string with ``"data:"``. Example::

        siding.style.apply_stylesheet(my_widget, "data:* { color: red; }")

    Any pre-set styles on a widget will be saved as such an entry the first
    time this function is used on any given widget to preserve those styles.
    """
    if not isinstance(widget, QWidget):
        raise TypeError("widget not a QWidget.")

    ref = _find_widget(widget)
    if not ref:
        # Make a new entry for our new widget.
        ref = weakref.ref(widget)
        _managed_widgets[ref] = []

        # If there are existing styles, store them.
        qss = widget.styleSheet()
        if qss:
            _managed_widgets[ref].append('data:%s' % qss)

    # Extend the list of styles with the new paths.
    _managed_widgets[ref].extend(paths)

    # Now, restyle the widget.
    active().style_widget(widget, ref)

def list_stylesheets(widget):
    """ List all the Qt stylesheets being applied to ``widget``. """
    if not isinstance(widget, QWidget):
        raise TypeError("widget not a QWidget.")

    ref = _find_widget(widget)
    if not ref:
        return []

    return _managed_widgets[ref][:]

def remove_stylesheet(widget, *paths):
    """
    Remove the stylesheet at the provided path(s) from the ``widget``. More
    than one path can be supplied to remove more than one stylesheet from a
    widget.

    If no paths are provided, all styles will be cleared from the widget.
    """
    if not isinstance(widget, QWidget):
        raise TypeError("widget not a QWidget.")

    ref = _find_widget(widget)
    if not ref:
        return

    widget_styles = _managed_widgets[ref]

    if not paths:
        del widget_styles[:]
    else:
        for path in paths:
            try:
                widget_styles.remove(path)
            except ValueError:
                continue

    # Now, restyle the widget.
    active().style_widget(widget, ref)

    # If we don't have any more styles, remove it from the list for efficiency.
    if not widget_styles:
        del _managed_widgets[ref]

###############################################################################
# Signal Helper
###############################################################################

class Helper(QObject):
    """
    This class's sole purpose in life is providing a QObject to host the
    style_reloaded signal that's exposed as siding.style.style_reloaded
    """
    
    style_reloaded = Signal()

_helper = Helper()
style_reloaded = _helper.style_reloaded
"""
This signal is emitted whenever the active style is reloaded, or a new
style is loaded. It is recommended that you use this signal to reload
icons and other images for your application. Example::

    class MyWindow(QMainWindow):
        def __init__(self, parent=None):
            ...

            # Connect to the style system, and go ahead and load the icons
            # immediately too.
            siding.style.style_reloaded.connect(self.reload_icons)

        def reload_icons(self):
            self.some_action.setIcon(siding.style.icon('icon-name'))
            self.other_action.setIcon(siding.style.icon('other-icon'))
            self.setWindowIcon(siding.style.icon('window-icon'))
"""

###############################################################################
# Style Loading Functions
###############################################################################

def active():
    """ Return the active style. """
    return loaded_styles[None]


def list_styles():
    """ List all the available styles. """
    styles = []
    for name in profile.listdir('styles'):
        if profile.isfile(profile.join('styles', name, 'style.ini')):
            styles.append(name)

    return styles


def load(name, apply_style=True, path=None):
    """
    Load the style with the given name. If ``apply_style`` is True, it will be
    activated immediately. If ``path`` is specified, the style will be loaded
    from that path. Otherwise, the default style paths will be used.
    """
    if name in loaded_styles:
        style = loaded_styles.get(name)
        style.reload(apply_style or style.active)
        return style

    style = Style(name, path)
    loaded_styles[name] = style

    if apply_style:
        style.apply()

    return style


def reload(style=None):
    """ Reload the active style, or the style with the given name. """
    style = loaded_styles[style]
    style.reload()
    if style.active:
        style_reloaded.emit()

###############################################################################
# Initialization
###############################################################################

def initialize(args=None, **kwargs):
    """
    Initialize the style system. You may use the following arguments to
    configure the style system:
    
    ==============  ============  ============
    Argument        Default       Description
    ==============  ============  ============
    safe_mode       ``False``     When safe mode is enabled, styles won't be loaded automatically.
    style                         The name of the style to load. This overrides the profile value.
    default_style   ``default``   The name of the default style to use if one isn't chosen.
    ==============  ============  ============

    In addition, you can provide a list of command line arguments to have
    siding load them automatically. Example::

        siding.style.initialize(sys.argv[1:])

    The following command line arguments are supported:
    
    ================  ============
    Argument          Description
    ================  ============
    ``--safe-mode``   When safe mode is enabled, styles won't be loaded automatically.
    ``--style``       The name of the style to load.
    ================  ============
    """
    global safe_mode

    # Set the defaults now.
    safe_mode = kwargs.get('safe_mode', safe_mode)
    style = kwargs.get('style')
    default_style = kwargs.get('default_style', 'default')

    # We require the profile for this.
    if not profile.settings:
        raise RuntimeError("siding.style requires you to call siding.profile.initialize() first.")

    # Now, parse the options we've got.
    if args:
        if args is True:
            args = sys.argv[1:]

        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('--safe-mode', action='store_true', default=None)
        parser.add_argument('--style')

        options = parser.parse_known_args(args)[0]

        # Store that then.
        if options.safe_mode is not None:
            safe_mode = options.safe_mode

        if options.style:
            style = options.style

    # If we don't have a style, get it from the profile or fall back to
    if not style:
        style = profile.get('siding/current-style', default_style)

    # Save the current widget style.
    widget_style = QApplication.instance().style().metaObject().className()
    widget_style = STYLE_KEYS.get(widget_style)
    if widget_style:
        profile.set('siding/widget-style', widget_style)

    # Load the style. That is, if safe mode isn't on.
    if safe_mode:
        log.info('Not loading style %r due to safe mode.' % style)
        return

    try:
        load(style)
    except (IOError, ValueError):
        # If we weren't using the default style, then eat the error and try
        # loading the default style.
        if style != default_style:
            try:
                load(default_style)
            except (IOError, ValueError):
                pass
