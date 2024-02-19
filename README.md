# py_mail

Practice Project.

Simple mail tools written in python. 

Currently Supports:
-Sending Mail

Authorization Profiles Supported:
-Gmail

Install with:
```
$pip3 install git+https://github.com/nwalt/py_mail
```

Creates a command line entry point allowing for usage like:
```
py_mail an_email_file.json -a some_attachment.jpg
```

Each user configured to user the tool will have a directory specified for managing their emails - py_mail looks here for mail to be sent, for attachments to attach, and for authorization profiles to use .

Email files can currently only be json objects. .eml file support coming soon.

