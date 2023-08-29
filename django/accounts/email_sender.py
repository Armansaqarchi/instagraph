from django.core.mail import send_mail
from django.template.loader import render_to_string

def send_email(activation, user):
    html_message = render_to_string("email.html", context={"username" : user.username, "activation_code" : activation})
    send_mail(
        subject="Instagraph Account Activation Code",
        html_message= html_message,
        message="verify your account",
        from_email="arman.saqarchi@gmail.com",
        recipient_list=[user.email],
        fail_silently=True
    )