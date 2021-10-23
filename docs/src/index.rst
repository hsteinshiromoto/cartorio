.. Cartorio documentation master file, created by
   sphinx-quickstart on Thu Oct 21 11:11:37 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Cartorio's documentation!
====================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api

Intallation
===========

``pip install cartorio``

Usage
=====

.. code-block:: python

   import sys
   from pathlib import Path

   from cartorio import fun, log

   # Test instantiation of log file
   logger = log(filename=Path(__file__).resolve().stem, logs_path=Path(__file__).resolve().parent)

   @fun
   def multiply(num1, num2):
      return num1 * num2

   # Test if entry and exit log messages are correct
   multiply(10, 1)


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
