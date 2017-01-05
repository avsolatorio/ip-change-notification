import os
import cPickle

'''
Follow the steps here: https://travismaynard.com/writing/dynamic-dns-using-the-linode-api

Create a new A/AAAA record and note the hostname. Get the resourceid for the hostname you created (name attribute in the json) returned by this api call: `https://api.linode.com/?api_key=<api_key>&api_action=domain.resource.list&domainid=<domain_id>`
'''

data_dir = os.path.join(
    os.path.abspath(
        os.path.dirname(__file__)
    ), '../../data'
)


linode_host_data = os.path.join(
    data_dir,
    'linode_host_data.dict'
)

with open(linode_host_data) as fl:
    linode_payload = cPickle.load(fl)

update_api = 'https://api.linode.com/?api_key={api_key}\&api_action=domain.resource.update\&domainid={domainid}\&resourceid={resourceid}\&target=[remote_addr]'.format(**linode_payload)


linode_update_cron_entry = "*/10 * * * * /bin/echo `/bin/date`: `/usr/bin/wget -qO- --no-check-certificate {}` >> /var/log/linode_dyndns.log".format(update_api)

cron_entry_file = os.path.join(
    data_dir,
    'linode_host_updata.cron'
)

with open(cron_entry_file, 'w') as fl:
    fl.write(linode_update_cron_entry)

