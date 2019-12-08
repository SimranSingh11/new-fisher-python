import threading
from django.core.mail import EmailMessage
from django.conf import settings


class EmailThread(threading.Thread):

    subject = None
    message = None
    to_email_list = []
    bcc = []
    attachment = None
    attachment_name = None
    attachment_type = None

    def set_email(self, subject=None, message=None, to_email_list=[], bcc=[], attachment=None, attachment_name=None, attachment_type=None):
        self.subject = subject
        self.message = message
        self.to_email_list = to_email_list
        self.bcc = bcc
        self.attachment = attachment
        self.attachment_name = attachment_name
        self.attachment_type = attachment_type
        self.from_email = 'no-reply@fisherapp.com'

    def send_email(self):
        if settings.DEBUG:
            print("===> To Email: ", self.to_email_list)
        try:
            email = EmailMessage(self.subject, self.message, from_email=self.from_email, to=self.to_email_list, bcc=self.bcc)
            if self.attachment:
                email.attach('{}'.format(self.attachment_name), self.attachment, '{}'.format(self.attachment_type))
            email.content_subtype = 'html'
            email.send()
        except Exception as error:
            if settings.DEBUG:
                print("error:", error)

    def run(self):

        if settings.DEBUG:
            print("===> Email-Thread (START)")

        self.send_email()

        if settings.DEBUG:
            print("===> Email-Thread (END)")


def email_send(subject, message, to_email_list, attachment=None, attachment_name="", attachment_type=""):
        email = EmailThread()
        email.set_email(subject=subject, message=message, to_email_list=to_email_list, attachment=attachment,
                        attachment_name=attachment_name, attachment_type=attachment_type)
        email.start()
