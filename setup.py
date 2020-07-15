import os
import sys
import json
import atexit
import getpass
import pathlib
import setuptools
import subprocess
from setuptools.command.install import install
from py_mail.scripts import build_py_mail_config


#override the built in install method to allow for post-install work
class custom_install(install):
    def run(self):
        # atexit method runs after binary wheel creation.
        # def _post_install():
            # build_py_mail_config.main(
                # os.path.join(self.install_purelib, 'py_mail'))
        #atexit.register(_post_install)
        install.run(self)
        build_py_mail_config.main(os.path.join(self.install_purelib, 'py_mail'))

here = pathlib.Path(__file__).parent.resolve()

NAME = 'py_mail'
DESCRIPTION = ('Simple mail sending tool')
LONG_DESCRIPTION = (here / 'README.md').read_text(encoding='utf-8')
URL = 'https://github.com/nwalt/py_mail'
EMAIL = 'nathanhwalton@gmail.com'
AUTHOR = 'Nathan Walton'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '1.0.1'

REQUIRED = []

setuptools.setup(
    name=NAME,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    version=VERSION,
    url=URL,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    cmdclass={'install':custom_install},
    packages=setuptools.find_packages(),
    entry_points={'console_scripts':[
        'py_mail = py_mail.core:main'
    ]},
    classifiers=[
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_data={
        "":["config.json"]
    }
    
)
