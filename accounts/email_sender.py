from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_email(activation, user, subject = None, template = "email_verification.html"):

    html_message = render_to_string(template, context={"username" : user.username, "activation_code" : activation})
    print(user.email)
    send_mail(
        subject=subject,
        html_message= html_message,
        message="verify your account",
        from_email="arman.saqarchi@gmail.com",
        recipient_list=[user.email],
        fail_silently=True
    )