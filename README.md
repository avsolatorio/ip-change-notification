# ip-change-notification

This module is designed to keep track of the current public ip address of a server.

If you don't have a DDNS setup, this can help you connect to, for example, a server at home via the ip address (with proper firewall/ports setup of course!).

Specifically, this can also be used in raspberry pi's if you want to access it remotely!


### Requirements
This needs a pickled file called `personal_email_creds.dict` containing your gmail credentials. This part is not secure, so make sure that nobody gets access to this file!

Here's how you can generate the pickle credentials. This file should be in the same directory as the script files.

```
import cPickle

with open('personal_email_creds.dict', 'w') as fl:
    creds = dict(name=<your_gmail_name>, passwd=<gmail_account_passwd>)
    cPickle.dump(creds, fl)
```

### Running automatically
For this to serve its purpose, this script should run automatically on startup or whenever it's not running!
This is done by installing the entry I placed in the `crontab.entry` file into your server's crontab.
