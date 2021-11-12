import logging
import smtplib
import ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Messenger(object):

    def send_email(self, receiver_address, subject, mail_content, config):
        message = MIMEMultipart()
        message['From'] = config.sender_address
        message['To'] = receiver_address
        message['Subject'] = subject
        message.attach(MIMEText(mail_content, 'plain'))
        session = smtplib.SMTP_SSL(config.smtp_server_host,
                                   config.smtp_server_port)
        if config.smtp_tls_enabled:
            session.starttls()
        session.login(config.sender_address, config.sender_passwd)
        recipients = receiver_address.split(",")
        logging.info("sending an email to {}".format(str(recipients)))
        result = session.sendmail(config.sender_address,
                                  recipients, message.as_string())
        session.quit()
        logging.info("smtp server returns {}".format(str(result)))

    def send_heartbeat(self, mail_content, config):
        self.send_email(config.heartbeat_receiver_addresses,
                        config.heartbeat_subject,
                        mail_content,
                        config)

    def send_alert(self, mail_content, config):
        self.send_email(config.alert_receiver_addresses,
                        config.alert_subject, mail_content, config)


messenger = Messenger()
