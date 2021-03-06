# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os
import sys

from codecs import open

version_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            'pynocchio',
                            '__version__.py')

about = {}
with open(version_path, 'r') as f:
    exec(f.read(), about)

if sys.argv[-1] == 'build_deb':
    os.system('./scripts/build_deb.sh %s' % about['__version__'])
    sys.exit()

if sys.argv[-1] == 'build_pro':
    os.system('./scripts/build_pro.sh')
    sys.exit()

try:
    from pyqt_distutils.build_ui import build_ui
    cmdclass = {'build_ui': build_ui}
except ImportError:
    build_ui = None
    cmdclass = {}

setup(
    name=about['__title__'],
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    license=about['__license__'],
    description=about['__description__'],
    long_description='Pynocchio Comic Reader is a new and nice image viewer '
                     'which uses PySide API specialized in comic reading. '
                     'It is a comic reader that allow read cbr, cbz and cbt '
                     'files and have nice elementary icons theme on your '
                     'interface.',
    keywords="pynocchio comics manga viewer image",
    packages=find_packages(exclude=["*.test", "*.test.*", "test.*", "test"]),
    cmdclass=cmdclass,
    test_suite='test',
    scripts=[
        'pynocchio-client.py',
    ],
    include_package_data=True,
    install_requires=[
        'rarfile==3.0',
        'peewee==2.10.2',
        'PyQt5==5.10',
        'qdarkgraystyle>=0.0.3',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Users',
        'License :: OSI Approved :: GPLv3 License',
        'Operating System :: OS Independent',
        'Programming Language :: Python 3.5',
    ],
)
