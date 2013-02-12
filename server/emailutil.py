from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

FROM_EMAIL = "admin@listypedia.com"
def send_welcome_email(user):
    email_template = get_template('welcome_email.html')
    context = Context({'user': user})
    email_msg = email_template.render(context)
    subject = "Welcome to listypedia"
    from_email = FROM_EMAIL
    to = []
    to.append(user.email)
    msg = EmailMultiAlternatives(subject, email_msg, from_email, to)
    msg.content_subtype = "html"
    msg.send(fail_silently=True)
