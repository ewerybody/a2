__author__ = 'eRiC'
"""
ehmm.. I dunno but somehow simple logging is out or order here :/
import logging
log = logging.getlogger(__name__)
log.info('bla')
... Nothing!! :(
something with python 3.4?!?!
meanwhile ... here is a stub that does like its doing proper logging but actually just prints
"""

class FakeLog(object):
    def __init__(self, logger):
        self.logger = logger

    def info(self, text):
        print('%s: %s' % (self.logger, text))
    def error(self, text):
        print('ERROR! %s: %s' % (self.logger, text))
    def warn(self, text):
        print('Warning! %s: %s' % (self.logger, text))

def getLogger(logger):
    return FakeLog(logger)