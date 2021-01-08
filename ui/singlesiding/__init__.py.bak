from singlesiding.singleinstance import QSingleApplication


def initialize(organization_name=None, application_name=None, version=None):
    """
    If you're feeling particularly lazy, this function will handle all the
    initialization for you and return a :class:`QSingleApplication` instance.

    :rtype: QSingleApplication
    """
    # Make the app.
    app = QSingleApplication()

    # Store our info.
    if organization_name:
        app.setOrganizationName(organization_name)
    if application_name:
        app.setApplicationName(application_name)
    if version:
        app.setApplicationVersion(version)

    app.ensure_single()

    return app
