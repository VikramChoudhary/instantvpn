# vim: tabstop=4 shiftwidth=4 softtabstop=4
# Copyright 2013 Somebody
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import itertools
import smtplib

def send_mail(subject, text):
    msg = MIMEMultipart()
    msg['From'] = "vikschw@gmail.com"
    msg['To'] = ",".join("vikram.choudhary@huawei.com")
    msg['Subject'] = subject
    msg.attach(MIMEText(text))
    mailServer = smtplib.SMTP("smtp.gmail.com", 
                              587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    
    # TODO: Enable lesssecure option @
    # https://www.google.com/settings/security/lesssecureapps
    # Otherwise you will face authentication issues    
    mailServer.login("vikschw@gmail.com",
                     "xxxxxxxx")
    mailServer.sendmail("vikschw@gmail.com",
                        "vikram.choudhary@huawei.com",
                        msg.as_string())
    mailServer.close()

def _prepare_message(data):

    def _build_line(key, value):
        return "%s: %s\n" % (key, value)

    message_lines = itertools.imap(_build_line,
                                   data.keys(),
                                   data.values())
    return "".join(message_lines)


def notify_instantvpn_create(instvpn_data):
    subject = "[INSTVPN] Create instantvpn request:%s" % instvpn_data['name']
    send_mail(subject, _prepare_message(instvpn_data))


def notify_instantvpn_delete(instvpn_data):
    subject = "[INSTVPN] Delete instantvpn request:%s" % instvpn_data['name']
    message = "Request coming from tenant:%s" % instvpn_data['tenant_id']
    send_mail(subject, message)
