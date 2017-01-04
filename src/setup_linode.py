from collections import OrderedDict
from datetime import datetime
import shutil
import os

'''
Template
Host my-linode
Hostname xxx.xxx.xxx.xxx
User <server_user>
Port <ssh_port>
IdentityFile <~/.ssh/id_rsa>
'''

ssh_config_file = os.path.join(os.environ['HOME'], '.ssh/config')
if os.path.isfile(ssh_config_file):
    with open(ssh_config_file) as fl:
        ssh_config = fl.read()
else:
    with open(ssh_config_file, 'w') as fl:
        fl.write('')
        ssh_config = ''

try:
    input = raw_input
except NameError:
    pass

if 'Host my-linode' not in ssh_config:
    ans = input('No host `my-linode` found. If you have a remote server, do you want to configure now? y/n: ')

    if ans.lower() in ('y', 'yes'):
        while True:
            config_data = {'Host': 'my-linode'}

            config_template = OrderedDict([
                ('Host', 'my-linode'),
                ('Hostname', '<xxx.xxx.xxx.xxx>'),
                ('User', '<server_username>'),
                ('Port', '<22>'),
                ('IdentityFile', '<~/.ssh/id_rsa>'),
            ])

            print('Creating config for host `{}`.'.format(config_data['Host']))

            for key, sample in config_template.iteritems():
                if key == 'Host':
                    continue

                val = input('Input {}. Example: {}: '.format(key, sample))
                config_data[key] = val

            config = ''
            for key in config_template:
                config += '{} {}\n'.format(key, config_data[key])

            print('Please review generated config...')

            print('\n' + '-' * 50 + '\n' + config + '-' * 50 + '\n')

            ans = input('Add generated config to ssh config file? (y/n): ')
            if ans.lower() in ('y', 'yes'):
                config += ssh_config

                shutil.copy(ssh_config_file, '{}-{}'.format(ssh_config_file, datetime.now()))

                with open(ssh_config_file, 'w') as fl:
                    fl.write(config)

                print('Successfully saved config!')
                break
            else:
                ans = input('(r)egenerate or (a)bort config creation?: ')
                if ans.lower() in ('r', 'regenerate'):
                    continue
                else:
                    print('Aborting config creation!')
                    break

