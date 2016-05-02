# -*- coding: utf-8 -*-
#
# Copyright (C) 2014-2016  Michell Stuttgart Faria

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.

# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import distutils.cmd
import distutils.log
from setuptools import setup
import os
import re
import sys


def get_version(package):
    """
    Based in https://github.com/tomchristie/django-rest-framework/blob/
    971578ca345c3d3bae7fd93b87c41d43483b6f05/setup.py
    :param package Package name
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_packages(package):
    """
    Based id https://github.com/tomchristie/django-rest-framework/blob/
    971578ca345c3d3bae7fd93b87c41d43483b6f05/setup.py
    :param package Package name
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_regex_files(path, extension):
    """
    :param path Path of ui files
    :param extension Extension of file. .ui, .qrc, .ts, for example.
    Return list of files with selected extension .
    """
    ret = []

    for dirpath, dirnames, filenames in os.walk(path):
        ret += [(os.path.join(dirpath, fname), os.path.splitext(fname)[0]) for
                fname in filenames if os.path.splitext(fname)[1] == extension]

    return ret


package_name = 'pynocchio'
version = get_version(package_name)


class CompileUiFileCommand(distutils.cmd.Command):
    """
    A command compile ui files.
    """

    description = "Compile PySide ui files"

    # The format is (long option, short option, description).
    user_options = [
        ('path=', None, 'The path of ui files folder'),
    ]

    def initialize_options(self):
        """
        Sets the default value for the server socket.

        The method is responsible for setting default values for
        all the options that the command supports.

        Option dependencies should not be set here.
        """
        self.path = 'data'

    def finalize_options(self):
        """
        Overriding a required abstract method.

        The method is responsible for setting and checking the
        final values and option dependencies for all the options
        just before the method run is executed.

        In practice, this is where the values are assigned and verified.
        """
        assert os.path.isdir(self.path) is True
        assert os.path.lexists(self.path) is True

    def run(self):

        print "[INFO] Compile ui files..."

        uic_folder = 'pynocchio/src/uic_files'
        files = get_regex_files(self.path, '.ui')
        for f in files:
            uic_name = os.path.join(uic_folder, 'ui_' + f[1] + '.py')
            os.system('pyside-uic %s -o %s' % (f[0], uic_name))

        sys.exit()


class CompileQrcFileCommand(distutils.cmd.Command):
    """
    A command compile qrc resource files.
    """

    description = "Compile PySide qrc files"

    # The format is (long option, short option, description).
    user_options = [
        ('path=', None, 'The path of qrc files folder'),
    ]

    def initialize_options(self):
        self.path = 'data'

    def finalize_options(self):
        assert os.path.isdir(self.path) is True
        assert os.path.lexists(self.path) is True

    def run(self):

        print "[INFO] Compile qrc files..."

        uic_folder = 'pynocchio/src/uic_files'
        files = get_regex_files(self.path, '.qrc')
        for f in files:
            uic_name = os.path.join(uic_folder, f[1] + '_rc.py')
            os.system('pyside-rcc -verbose -o %s %s' % (uic_name, f[0]))

        sys.exit()

setup(
    name=package_name,
    version=version,
    author='Michell Stuttgart Faria',
    author_email='michellstut@gmail.com',
    url='https://github.com/mstuttgart/pynocchio-comic-reader',
    license='GPL v3',
    description='Pynocchio is a image viewer specialized in comic reading.',
    long_description='Pynocchio Comic Reader is a new and nice image viewer '
                     'which uses PySide API specialized in comic reading. '
                     'It is a comic reader that allow read cbr, cbz and cbt '
                     'files and have nice elementary icons theme on your '
                     'interface.',
    packages=get_packages(package_name),
    test_suite='test',
    cmdclass={
        'compile_ui': CompileUiFileCommand,
        'compile_qrc': CompileQrcFileCommand,
    },
    scripts=[
        'pynocchio-comic-reader/pynocchio/main',
    ],
    data_files=[
        ('/usr/share/applications',
         ['linux/usr/share/applications/pynocchio.desktop']),
        ('/usr/share/pixmaps', ['linux/usr/share/pixmaps/pynocchio_icon.png']),
        ('/usr/share/pynocchio/locale/', [
            'pynocchio/locale/pynocchio_en_US.qm',
            'pynocchio/locale/pynocchio_pt_BR.qm',
        ]),
        ('/usr/share/icons/hicolor/16x16/apps',
         ['linux/usr/share/icons/hicolor/16x16/apps/pynocchio.png']),
        ('/usr/share/icons/hicolor/32x32/apps',
         ['linux/usr/share/icons/hicolor/32x32/apps/pynocchio.png']),
        ('/usr/share/icons/hicolor/48x48/apps',
         ['linux/usr/share/icons/hicolor/48x48/apps/pynocchio.png']),
        ('/usr/share/icons/hicolor/128x128/apps',
         ['linux/usr/share/icons/hicolor/128x128/apps/pynocchio.png']),
        ('/usr/share/icons/hicolor/256x256/apps',
         ['linux/usr/share/icons/hicolor/256x256/apps/pynocchio.png']),
    ],
    install_requires=[
        'rarfile',
        'peewee',
    ],
)
