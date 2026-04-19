import os
import sys
import logging

# Only spot where this is set! Use `a2log.get()`` anywhere else!
LOG_LEVEL = logging.INFO
log = logging.getLogger(__name__)
log.setLevel(LOG_LEVEL)

NAME = 'a2'


def get(name: str | None = None) -> logging.Logger:
    """Get a logger for calling module."""
    # make sure logging is initialized
    if not logging.root.handlers:
        logging.basicConfig()
    # make bend name == __main__-runs to actual module name
    if name is None or name == '__main__':
        try:
            frame = sys._getframe(1)
            # print('frame.f_code.co_filename: %s' % frame.f_code.co_filename)
            dirpath, base = os.path.split(frame.f_code.co_filename)
            name = os.path.splitext(base)[0]
            if name == '__init__':
                name = os.path.basename(dirpath)
        except AttributeError:
            pass

    new_log = logging.getLogger(name)
    new_log.setLevel(LOG_LEVEL)
    return new_log


def set_level(debug: bool = False) -> None:
    """Set all our loggers to standard INFO or debug mode."""
    level = [logging.INFO, logging.DEBUG][debug]
    for name, logger in log.manager.loggerDict.items():
        if not name.startswith(NAME) or not isinstance(logger, logging.Logger):
            continue
        try:
            logger.setLevel(level)
            log.debug('"%s" Log level DEBUG: active', name)
            log.info('"%s" Log level INFO: active', name)
        except AttributeError as error:
            if isinstance(logger, logging.PlaceHolder):
                continue
            log.info('Could not set log level on logger object "%s": %s', name, str(logger))
            log.error(error)
