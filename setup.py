#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='tingbot-gui',
      version='0.9',
      description='Graphical User Interface for tingbot',
      url='http://github.com/furbrain/tingbot-gui',
      author='Phil Underwood',
      author_email='beardydoc@gmail.com',
      license='BSD',
      packages=['tingbot_gui'],
      package_dir={'tingbot_gui': 'tingbot_gui'},
      include_package_data=True,
      install_requires=['tingbot-python'],
      dependency_links=['https://github.com/tingbot/tingbot-python/tarball/master'],
      download_url="https://github.com/furbrain/tingbot-gui/archive/v0.9.tar.gz"
      zip_safe=False,
      keywords='tingbot',
      classifiers=[
          "Development Status :: 4 - Beta",
          "Environment :: Other Environment",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: BSD License",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: User Interfaces"
      ])
