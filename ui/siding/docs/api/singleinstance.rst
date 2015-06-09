``siding.singleinstance``
*************************

.. automodule:: siding.singleinstance

QSingleApplication
==================

.. autoclass:: QSingleApplication

    .. attribute:: messageReceived

        This signal is emitted whenever the application receives a message from
        another instance. The message is encoded as JSON as it's sent, so this
        can potentially be any basic type. Example::

            @app.messageReceived.connect
            def handle_message(args):
                print 'We just got:', args

    .. attribute:: compositionChanged

        This signal is emitted on Windows when we receive the
        ``WM_DWMCOMPOSITIONCHANGED`` message.

    .. autoattribute:: already_running

    .. automethod:: ensure_single
    .. automethod:: send_message
