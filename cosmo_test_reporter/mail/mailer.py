__author__ = 'nirb'

import smtplib
from email.mime.text import MIMEText
from cosmo_test_reporter import params

def send_unit_tests_mail():
    message_text = """
        <html>
            <h1>Cosmo Unit Test Result: </h1>
            <h2 style="color:red">There are unit test failures</h2>
        </html>
        """

    msg = MIMEText(message_text, 'html')
    me = 'tgrid@gigaspaces.com'
    you = ['nirb@gigaspaces.com']

    msg['Subject'] = 'cosmo unit tests report'
    msg['From'] = me
    msg['To'] = ', '.join(you)

    s = smtplib.SMTP(host=params.MAIL_HOST)
    s.ehlo()
    s.starttls()
    s.login(params.MAIL_USER, params.MAIL_PASS)
    s.sendmail(me, you, msg.as_string())
    s.quit()


send_unit_tests_mail()