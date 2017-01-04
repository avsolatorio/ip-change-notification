# ip-change-notification

This module is designed to keep track of the current public ip address of a server by sending an e-mail to your designated recipient (set in the credentials file below).

If you don't have a DDNS setup, this can help you connect to, for example, a server at home via the ip address (with proper firewall/ports setup of course!).

Specifically, this can also be used in raspberry pi's if you want to access it remotely!


### Requirements
- **Install the required python modules**: the `enum` module is used which is not a standard python library.
```
$ cd ./src
$ pip install -r requirements.txt
```

- **Create credential file**: this service needs a pickled file called `personal_email_creds.dict` containing your gmail credentials (name, passwd, and recipient email address). This part is not secure, so make sure that nobody gets access to this file! A utility script is available to assist you in creating this file.
```
$ cd ./src/utils
$ python generate_credentials.py
```

### Running automatically
For this to serve its purpose, this script should run automatically on startup or whenever it's not running!
This is done by installing the entry I placed in the `crontab.entry` file into your server's crontab.

An assumption here is that the project is in your home directory. You can just simply make a symbolic link from the actual project location to your home directory.

### Additional features
I added a feature that updates an html file in a remote server (with static public IP) running an http service. Having this, aside from receiving an e-mail when the IP changes, you can view the current IP by checking the updated page.  See `update_remote_server` method inside the `public_ip_checker.py` script. This requires proper ssh configuration to the remote server. You can use a utility script I wrote to create/add the ssh config file if you have a remote server.

```
$ cd ./src/utils
$ python setup_remote_server_config.py
```

### Debugging notes
In case the service is not running, make sure that the lock file (`/tmp/public_ip_checker.py.lock`) is not present. I made a mechanism that will automatically remove this lock during ungraceful shutdown of the service. I might have missed handling all scenario so this lock might persist which will result to the service to not run automatically the next it's suppose to run.
