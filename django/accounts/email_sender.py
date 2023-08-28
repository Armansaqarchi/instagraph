from django.core.mail import send_mail


def send_email(activation, user):
    send_mail(
        subject="Instagraph Account Activation Code",
        message=f"Dear {user.username}, here is your activation code : {activation}\n\
            ti activate your account, fill the activation field with the activation code",
        from_email="arman.saqarchi@gmail.com",
        recipient_list=[user.email],
        fail_silently=True
    )