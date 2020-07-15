import os
import sys
import ssl
import json
import inspect
import getpass
import smtplib
import pathlib
import argparse
import subprocess
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from .scripts import build_py_mail_config

#get the install directory for this package
install_dir = pathlib.Path(
    inspect.getfile(sys.modules[__name__])).parent.resolve()

class PyMail():
    """Handler class for sending mail
    """
    def __init__(self, config_path= (install_dir / 'config.json'),
                 mail_dir=None):
        self.user = getpass.getuser()
        self.config_path = config_path
        #load config
        try:
            with self.config_path.open() as temp:
                self.config = json.load(temp)
        except:
            build_py_mail_config.main(install_dir)
        finally:
            with self.config_path.open() as temp:
                self.config = json.load(temp)
        #handle alternate mail_dir paths
        if (mail_dir is not None):
            if (type(mail_dir) == str):
                self.mail_dir = pathlib.Path(mail_dir)
            if (issubclass(type(mail_dir), pathlib.Path)):
                self.mail_dir = mail_dir
        else:
            self.mail_dir = pathlib.Path(self.config[self.user]['mail_dir'])
        if (self.config[self.user]['default_profile'] is not None):
            self.setup_profile(
                self.mail_dir / 'ref' / 
                self.config[self.user]['default_profile'])
        else:
            self.profile_loaded = False

    def setup_profile(self, path):
        """Read and setup a profile"""
        profile = json.load(path.open())
        self.type = profile['type']
        self.fromaddr = profile['from']
        self.ssl = profile['ssl']
        self.port = profile['port']
        self.pw = profile['pw']
        self.profile_loaded = True

    def send_email_from_json(self, file, attach_list=None):
        """Send an email built from a json doc within the working directory"""
        if (self.profile_loaded != True):
            print('You must setup a profile to send mail')
            return 1
        mail_path = pathlib.Path(self.mail_dir / 'mail'/ file)
        attach_path = pathlib.Path(self.mail_dir / 'files' )
        mail = json.load(mail_path.open())
        msg = MIMEMultipart()
        msg['From'] = self.fromaddr
        self.to_list = ', '.join(mail['to'])
        msg['To'] = self.to_list
        msg['Subject'] = mail['subject']
        msg.attach(MIMEText(mail['body'], 'plain'))
        if (attach_list is not None):
            for attach in attach_list:
                attachment = MIMEBase('application', 'octet-stream')
                with (attach_path / attach).open('rb') as read_file:
                    attachment.set_payload(read_file.read())
                encoders.encode_base64(attachment)
                attachment.add_header(
                    'Content-Disposition',
                    f'attachment; filename={attach}')
                msg.attach(attachment)
        if (self.type == 'gmail'):
            if (self.ssl != True):
                print('Gmail profiles require ssl')
                return 1
            else:
                context = ssl.create_default_context()
                gmail_ssl = smtplib.SMTP_SSL(
                    'smtp.gmail.com', self.port, context=context)
                gmail_ssl.login(self.fromaddr, password=self.pw)
                gmail_ssl.sendmail(self.fromaddr, self.to_list, msg.as_string())
                return 0

    def send_email_from_eml(self, file, attach_list=None):
        """Send an email from .eml file within the working directory"""
        return 1

def send(file, attach_list=None, profile=None):
    """Send an email. 
    Builds a PyMail class using given profile
    Then calls the send mail function for target file's type
    File will be searched for in PyMail obj's mail_dir attribute
    """
    mailer = PyMail()
    if (file.endswith('.json') == True):
        mail_res = mailer.send_email_from_json(file, attach_list=attach_list)
    if (file.endswith('.eml') == True):
        mail_res = mailer.send_email_from_eml(file, attach_list=attach_list)
    if (mail_res != 0):
        raise Exception('Something went wrong!')
    else:
        return f'Email Sent Successfully to {mailer.to_list}'

def main():
    parser = argparse.ArgumentParser(
        prog='py_mail', description='Simple mailing tools')
    #positionals
    parser.add_argument(
        'file', metavar='file', type=str, help='the email file to be sent')
    #optionals
    parser.add_argument(
        '-a', dest='attach_list', metavar='attachment', type=str, 
        help='a file to attach. May be passed multiple times',
        action='append', default=None)
    
    args = parser.parse_args()

    send(args.file, args.attach_list)

if (__name__ == '__main__'):
    main()