#! /usr/bin/env python3
# Add a default config entry for the current user in installed directory
import json
import inspect
import getpass
import pathlib
import py_mail

def main(install_dir):
    install_dir = pathlib.Path(install_dir)
    user_name = getpass.getuser()
    user_home = pathlib.Path.home()
    mail_dir = user_home / 'py_mail'
    config_path = install_dir / 'config.json'
    print(
        f'\nAdding a config entry for user {user_name}\n'
        f'Your mail directory will be {mail_dir}\n')
    with config_path.open() as temp:
        config = json.load(temp)
    config[user_name] = {
            'mail_dir':str(mail_dir),
            'default_profile':None
        }
    with config_path.open('w') as temp:
        json.dump(config, config_path.open('w'))

    locs = [
        mail_dir / 'mail',
        mail_dir / 'files',
        mail_dir / 'ref',
        mail_dir / 'done'
    ]

    for loc in locs:
        if (not loc.exists()):
            loc.mkdir(parents=True)