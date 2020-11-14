#!/usr/bin/env python
import os, sys

sys.path.append(os.getcwd())

from mypackage import mymodule
import logging, os

def main():
    logger.debug('This is a debug message.')
    logger.info('This is an info message.')
    mymodule.test()

if __name__=='__main__':
    logger = logging.getLogger(__name__)
    main()
