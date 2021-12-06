from simple_mail.mailer import BaseSimpleMail, simple_mailer

class WelcomeMail(BaseSimpleMail):
    email_key = 'welcome'

    def set_context(self, subject, title, content, button_label, button_link):
        self.context = {
            'subject' : subject,
            'title': title,
            'body': content,
            'button_label': button_label,
            'button_link': button_link,
        }


simple_mailer.register(WelcomeMail)