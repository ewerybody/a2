Plugins
*******

siding's plugin system does its best to make no assumptions about the structure
of your application while providing a simple, clean way to easilly extend your
application.


Plugin Basics
=============

Plugins are simple subclasses of :class:`siding.plugins.IPlugin`, which is
itself a subclass of :class:`PySide.QtCore.QObject`. Plugins are meant to
interact with the rest of an application primarily through Signals and Slots.
However, there's nothing to stop you from doing whatever you'd like.

