# py_mail
Simple mail tools written in python. 

Currently Supports:
-Sending Mail

Profiles Supported:
-Gmail

When installed with pip, sets up a directory in installing user's home where profiles, mail files, and attachment files can be placed.

Email files can currently only be json objects. .eml file support coming soon.

Creates a command line entry point allowing for usage like:
```
py_mail an_email_file.json -a some_attachment.jpg
```
