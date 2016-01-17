#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='tingbot-gui',
      version='0.1',
      description='Graphical User Interface for tingbot',
      url='http://github.com/furbrain/tingbot-gui',
      author='Phil Underwood',
      author_email='beardydoc@gmail.com',
      license='BSD',
      packages=['tingbot_gui'],
      package_dir={'tingbot_gui': 'tingbot_gui'},
      install_requires=['tingbot'],
      dependency_links=['https://github.com/tingbot/tingbot-python/tarball/master'],
      zip_safe=False,
      keywords='tingbot',)
