import subprocess as sub
import time
from personal_email_sender import email_to_me
import os


if __name__ == '__main__':
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
    init_ip = '122.2.234.158'  # Actual is '122.2.234.157'
    is_init_check = True

    print('Starting IP checker!')

    while True:
        # Check only after 5 minutes of launching the app
        if is_init_check:
            time.sleep(1 * 60)
            is_init_check = False

        print('Starting to check public IP...')
        p = sub.Popen(ip_check_command, shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
        stdout, stderr = p.communicate()

        if stdout.strip() != init_ip:
            new_ip = stdout.strip()

            text = "Hey Aivin!\n\nI detected that your public IP address changed from {} to {}!".format(init_ip, new_ip)
            html = """\
            <html>
              <head></head>
              <body>
                <p>Hey Aivin!<br><br>
                   I detected that your public IP address changed from {} to {}!
                </p>
              </body>
            </html>
            """.format(init_ip, new_ip)

            email_to_me(text, html)
            print('Email sent to Notify change in IP!')

            init_ip = new_ip

        # Sleep for 15 minutes
        print('Sleeping for 15 minutes...')
        time.sleep(15 * 60)
