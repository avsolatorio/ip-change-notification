from collections import OrderedDict
import cPickle
import os

creds = {}

key_notes = OrderedDict([
    ('name', '\n\nInput gmail of sender account: '),
    ('passwd', '\n\nInput password for sender gmail account: '),
    ('recipient', '\n\nInput e-mail address of target recipient: '),
])

try:
    input = raw_input
except NameError:
    pass

for key, note in key_notes.iteritems():
    value = input(note)

    if key in ['name', 'recipient']:
        assert '@' in value, "Invalid e-mail address!"

        if key == 'name':
            value = value.split('@')[0]

    creds[key] = value

creds_file = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    '../data/personal_email_creds.dict'
)

with open(creds_file, 'w') as fl:
    cPickle.dump(creds, fl, protocol=2)

print('Credentials successfully stored in {}!'.format(creds_file))

