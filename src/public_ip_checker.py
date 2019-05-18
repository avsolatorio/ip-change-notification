import subprocess as sub
import time
from datetime import datetime
from personal_email_sender import email_to_me, return_code_enum
import os
import cPickle
from signal import (
    signal, SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM
)
import atexit
import sys


lock_file = '/tmp/{}.lock'.format(__file__)
signal_set = (SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM)


def log_print(x):
    print('{}: {}'.format(datetime.now(), x))


def remove_lock(*args):
    try:
        os.remove(lock_file)
        log_print('Terminating service!')
    except OSError:
        # The lock is already not present.
        pass

    sys.exit(0)


def make_lock():
    with file(lock_file, 'w'):
        pass

    for sig in signal_set:
        signal(sig, remove_lock)


def update_remote_server(ip, now):
    remote_status_text = '''
    <h1>Current public ip: {}</h1>
    <br>
    <h3>Updated at: {}</h3>
    '''.format(ip, now)

    remote_status_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/home-public-ip.html')
    with open(remote_status_path, 'w') as fl:
        fl.write(remote_status_text)

    try:
        sub.check_call(
            [
                'scp',
                remote_status_path,
                'my-linode:~/home-public-ip/home-public-ip.html'
            ]
        )
    except Exception as e:
        log_print('Something went wrong in syncing with the remove server...')
        log_print('Error {} message {}'.format(type(e), e.message))


def get_ip():
    ip_check_command = 'wget http://ipinfo.io/ip -qO -'
    log_print('Starting to check public IP...')
    p = sub.Popen(ip_check_command, shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
    stdout, stderr = p.communicate()

    new_ip = stdout.strip()

    return new_ip


atexit.register(remove_lock)

if __name__ == '__main__':
    NAME = 'Aivin'
    INIT_SLEEP_TIME = 0.1  # minutes
    CHECK_FREQUENCY = 15  # minutes

    pid = os.getpid()
    make_lock()

    log_print('Script pid is: {}'.format(pid))

    curr_ip = get_ip()

    pid_text = "IP checker script launched with pid: {}".format(pid)
    pid_html = """\
            <html>
              <head></head>
              <body>
                <p>IP checker script launched with pid: {}</p>
                <p>Current IP: {}</p>
              </body>
            </html>
            """.format(pid, curr_ip)

    email_to_me(pid_text, pid_html, subject='Public IP checker started with pid: {}'.format(pid))

    ip_archive_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/ip_archive.dict')
    
    ips = {}
    if os.path.isfile(ip_archive_file):        
        with open(ip_archive_file) as fl:
            ips = cPickle.load(fl)
            init_ip = ips[max(ips)]
    else:
        init_ip = ''

    is_init_check = True

    log_print('Starting IP checker!')

    while True:
        # Check only after INIT_SLEEP_TIME minute of launching the app
        if is_init_check:
            time.sleep(INIT_SLEEP_TIME * 60)
            is_init_check = False

        new_ip = get_ip()
        now = datetime.now()
        if new_ip != init_ip:

            ips[now] = new_ip
            with open(ip_archive_file, 'w') as fl:
                cPickle.dump(ips, fl)
            html = """\
            <html>
              <head></head>
              <body>
                <p>Hey {}!<br><br>
                   I detected that your public IP address changed from {} to {}!
                </p>
              </body>
            </html>
            """.format(NAME, init_ip, new_ip)

            return_code = return_code_enum.failed
            while return_code != return_code_enum.success:
                return_code = email_to_me(text, html)

            log_print('Email sent to Notify change in IP!')

            init_ip = new_ip

        update_remote_server(init_ip, now)
        # Sleep for CHECK_FREQUENCY minutes
        log_print('Sleeping for {} minutes...'.format(CHECK_FREQUENCY))
        time.sleep(CHECK_FREQUENCY * 60)

