import subprocess as sub
import time
from datetime import datetime
from personal_email_sender import email_to_me, return_code_enum
import os
import cPickle


if __name__ == '__main__':
    NAME = 'Aivin'
    pid = os.getpid()

    print('Script pid is: {}'.format(pid))

    pid_text = "IP checker script launched with pid: {}".format(pid)
    pid_html = """\
            <html>
              <head></head>
              <body>
                <p>IP checker script launched with pid: {}</p>
              </body>
            </html>
            """.format(pid)

    email_to_me(pid_text, pid_html, subject='Public IP checker started with pid: {}'.format(pid))

    ip_check_command = 'wget http://ipinfo.io/ip -qO -'
    ip_archive_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ip_archive.dict')
    
    ips = {}
    if os.path.isfile(ip_archive_file):        
        with open(ip_archive_file) as fl:
            ips = cPickle.load(fl)
            init_ip = ips[max(ips)]
    else:
        init_ip = ''

    is_init_check = True

    print('Starting IP checker!')

    while True:
        # Check only after 1 minute of launching the app
        if is_init_check:
            time.sleep(1 * 60)
            is_init_check = False

        print('Starting to check public IP...')
        p = sub.Popen(ip_check_command, shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
        stdout, stderr = p.communicate()

        if stdout.strip() != init_ip:
            new_ip = stdout.strip()

            now = datetime.now()
            ips[now] = new_ip
            with open(ip_archive_file, 'w') as fl:
                cPickle.dump(ips, fl)

            text = "Hey {}!\n\nI detected that your public IP address changed from {} to {}!".format(NAME, init_ip, new_ip)
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

            print('Email sent to Notify change in IP!')

            init_ip = new_ip

        # Sleep for 15 minutes
        print('Sleeping for 15 minutes...')
        time.sleep(15 * 60)

