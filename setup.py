import os
import json
import pathlib
import setuptools

here = pathlib.Path(__file__).parent.resolve()

NAME = 'py_mail'
DESCRIPTION = ('Simple mail sending tool')
LONG_DESCRIPTION = (here / 'README.md').read_text(encoding='utf-8')
URL = 'https://github.com/nwalt/py_mail'
EMAIL = 'nathanhwalton@gmail.com'
AUTHOR = 'Nathan Walton'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '1.0.0'

REQUIRED = []

setuptools.setup(
    name=NAME,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    version=VERSION,
    url=URL,
    author=AUTHOR,
    author_email=EMAIL,
    packages=setuptools.find_packages(),
    classifiers=[
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires=REQUIRES_PYTHON,
    entry_points={'console_scripts':[
        'py_mail = py_mail.core:main'
    ]}
)

# set up working location for mail files/logins and config file for module
wd = pathlib.Path.home() / 'py_mail'
if (not wd.exists()):
    wd.mkdir()

with (here / 'py_mail' / 'config.json').open('w') as config_file:
    json.dump(
        {
            'wd':str(wd),
            'default_profile':None
        },
        config_file
    )
locs = [
    wd / 'mail',
    wd / 'files',
    wd / 'ref',
    wd / 'done'
]
for loc in locs:
    if (not loc.exists()):
        loc.mkdir()