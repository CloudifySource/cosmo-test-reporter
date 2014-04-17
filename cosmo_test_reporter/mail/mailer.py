__author__ = 'nirb'

import smtplib
from email.mime.text import MIMEText
from cosmo_test_reporter import params

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
# fp = open(textfile, 'rb')
# # Create a text/plain message
# msg = MIMEText(fp.read())
# fp.close()


def send_unit_tests_mail():
    msg = MIMEText('there are failed unit tests')
    me = 'tgrid@gigaspaces.com'
    you = 'nirb@gigaspaces.com'

    msg['Subject'] = 'cosmo unit tests report'
    msg['From'] = me
    msg['To'] = you

    s = smtplib.SMTP(host=params.MAIL_HOST)
    s.ehlo()
    s.starttls()
    s.login(params.MAIL_USER, params.MAIL_PASS)
    s.sendmail(me, [you], msg.as_string())
    s.quit()