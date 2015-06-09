``siding.addons``
*****************

.. automodule:: siding.addons

Decorators
==========

.. autofunction:: action

Functions
=========

.. autofunction:: add_type
.. autofunction:: discover
.. autofunction:: get
.. autofunction:: find

.. autofunction:: check_dependencies
.. autofunction:: check_inheritance

AddonInfo
=========

.. autoclass:: AddonInfo

    .. autoattribute:: CORE_VALUES

    .. attribute:: name

        The add-on's name.

    .. attribute:: version

        The add-on's version.

    .. attribute:: file

        The name of the add-on's information file.

    .. attribute:: path

        A :class:`siding.path.PathContext` instance for manipulating paths
        within the add-on's root path. This should most likely be used for all
        file operations involving an add-on, and it's easy to do so. Example::

            with my_addon.path.open(my_addon.file) as info_file:
                info = info_file.read()

            do_something_with_that(info)

    .. attribute:: filedata

        A dictionary of any extra data gathered when matching the add-on's
        filename. For example, if you register your add-on type with the
        ``info_file`` of ``"{category}/{name}.{type"``, then the filedata
        dictionary will contain a single key, ``category``, with that part
        of the path for you to use.

    .. attribute:: data

        A dictionary of miscellaneous data about the add-on, potentially
        including a formatted name, description, author name, author link,
        website, and other such descriptive data.

    .. attribute:: requires

        An :class:`~collections.OrderedDict` of add-ons this add-on requires to
        load and function properly.

        .. seealso:: `Add-on Requirements`


    .. autoattribute:: is_blacklisted


    .. automethod:: load_information
    .. automethod:: update_ui
