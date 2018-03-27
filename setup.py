# -*- coding:utf-8 -*-

import codecs
import os
import re

from shutil import rmtree

import sys
from setuptools import find_packages, setup,Command

required = [
    'jenkins-api',
]

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, "auto-jenkins", "__version__.py")) as f:
    exec(f.read(), about)

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel upload")
    sys.exit()


# https://pypi.python.org/pypi/stdeb/0.8.5#quickstart-2-just-tell-me-the-fastest-way-to-make-a-deb
class DebCommand(Command):
    """Support for setup.py deb"""

    description = 'Build and publish the .deb package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'deb_dist'))

            # Remove concurrent27, at it causes issues with compilation.
            # rmtree(os.path.join(here, 'auto-jenkins', 'vendor', 'concurrent27'))
        except FileNotFoundError:
            pass
        self.status(u'Creating debian mainfest…')
        os.system('python setup.py --command-packages=stdeb.command sdist_dsc -z artful --package3=auto-jenkins')

        self.status(u'Building .deb…')
        os.chdir('deb_dist/auto-jenkins-{0}'.format(about['__version__']))
        os.system('dpkg-buildpackage -rfakeroot -uc -us')


class UploadCommand(Command):
    """Support setup.py publish."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except FileNotFoundError:
            pass

        self.status('Building Source distribution…')
        os.system('{0} setup.py sdist'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


setup(
    name="auto-jenkins",
    version=about['__version__'],
    author="bxiaopeng",
    author_email="wirelessqa@163.com",
    description="Auto Jenkins for Humans",
    url="https://github.com/bxiaopeng/auto-jenkins",
    packages=find_packages(exclude=["examples", "tests"]),
    install_requires=required,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
)
