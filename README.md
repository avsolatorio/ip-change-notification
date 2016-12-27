# ip-change-notification

This module is designed to keep track of the current public ip address of a server by sending an e-mail to your designated recipient (set in the credentials file below).

If you don't have a DDNS setup, this can help you connect to, for example, a server at home via the ip address (with proper firewall/ports setup of course!).

Specifically, this can also be used in raspberry pi's if you want to access it remotely!


### Requirements
This needs a pickled file called `personal_email_creds.dict` containing your gmail credentials (name, passwd, and recipient email address). This part is not secure, so make sure that nobody gets access to this file!

Here's how you can generate the pickle credentials. This file should be in the `./data` directory of this project.

```
import cPickle

with open('./data/personal_email_creds.dict', 'w') as fl:
    creds = dict(name=<your_gmail_name>, passwd=<gmail_account_passwd>, recipient=<recipient_email_address>)
    cPickle.dump(creds, fl)
```

### Running automatically
For this to serve its purpose, this script should run automatically on startup or whenever it's not running!
This is done by installing the entry I placed in the `crontab.entry` file into your server's crontab.

An assumption here is that the project is in your home directory. You can just simply make a symbolic link from the actual project location to your home directory.
