from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context


FROM_EMAIL = "support@listypedia.com"


def send_welcome_email(user):
    email_template = get_template('email/welcome.html')
    context = Context({'user': user})
    email_msg = email_template.render(context)
    subject = "Welcome to Listypedia!"
    from_email = FROM_EMAIL
    to = []
    to.append(user.email)
    msg = EmailMultiAlternatives(subject, email_msg, from_email, to)
    msg.content_subtype = "html"
    msg.send(fail_silently=True)


def send_follow_confirmation_email(user, list):
    email_template = get_template('email/follow_confirmation.html')
    context = Context({'user': user, 'list': list})
    email_msg = email_template.render(context)
    subject = "You are now following list - %s" % list.name
    from_email = FROM_EMAIL
    to = []
    to.append(user.email)
    msg = EmailMultiAlternatives(subject, email_msg, from_email, to)
    msg.content_subtype = "html"
    msg.send(fail_silently=True)


def send_collabaration_invitation_email(user, list, collabaration_invitation):
    email_template = get_template('email/collaboration_invitation.html')
    context = Context({'user': user, 'list': list, 'collabaration_invitation': collabaration_invitation})
    email_msg = email_template.render(context)
    subject = "You are invited to collaborate on - %s" % list.name
    from_email = FROM_EMAIL
    to = []
    to.append(collabaration_invitation.email)
    msg = EmailMultiAlternatives(subject, email_msg, from_email, to)
    msg.content_subtype = "html"
    msg.send(fail_silently=True)


def send_item_add_notification_email(user, list, item, followers):
    email_template = get_template('email/item_add_notification.html')
    context = Context({'user': user, 'list': list, 'item': item})
    email_msg = email_template.render(context)
    subject = "listypedia notification"
    from_email = FROM_EMAIL
    to = []
    for follower in followers:
        to.append(follower.user.email)
    msg = EmailMultiAlternatives(subject, email_msg, from_email, to)
    msg.content_subtype = "html"
    msg.send(fail_silently=True)
