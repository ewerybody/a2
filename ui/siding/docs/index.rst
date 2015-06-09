siding
******

siding is a lightweight framework to assist in the creation of PySide
applications with support for multiple-instance detection, multiple profiles,
easy to use styles, and a flexible plugins system.

siding is available under the
`Apache License, Version 2.0 <http://www.apache.org/licenses/LICENSE-2.0.html>`_.

Installation
============

siding isn't finished yet, but you can still download it if you'd like. You
can use pip::

    pip install siding

Or if you still like the old ways::

    easy_install siding

And, of course, you can always grab the latest code off
`GitHub <https://github.com/stendec/siding/>`_::

    git clone git://github.com/stendec/siding.git

siding requires Python 2.7 for now, with possible support for Python 3 later
on.

Short Example
=============

Why use siding? Here's why. The following application has support for only
running a single instance, profiles, styles, and plugins::

    import siding

    # Create the application.
    app = siding.QSingleApplication()

    app.setOrganizationName("StenCorp")
    app.setApplicationName("My Awesome App")

    # Initialize everything.
    siding.profile.initialize(True)
    app.ensure_single()
    siding.plugins.initialize(True)
    siding.style.initialize(True)

    # Load my code, whatever it is.
    import my_window
    my_window.show()

    # Connect a simple signal so we can receive arguments from any other
    # instances that try to open.
    app.messageReceived.connect(my_window.handle_args)

    # And run the application.
    app.exec_()

Documentation
=============

Documentation is still being written.

.. toctree::
    :maxdepth: 2

    guides/index

API
===

.. toctree::
    :maxdepth: 2

    api/addons
    api/path
    api/profile
    api/singleinstance
    api/style
    api/version
