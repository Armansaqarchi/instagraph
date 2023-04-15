from random import randint
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse




def digit_random6() -> str:
    '''Generate a random 6 digit string'''

    return ''.join(str(randint(0,9)) for _ in range (6))


def send_email(subject = None, message = None, from_email = None, to = None):
    try:
        if subject and from_email and to:
            send_mail(subject=subject, message=message, from_email=from_email, recipient_list=[to])
        else:
            raise BadHeaderError
    except BadHeaderError :
        return HttpResponse("Bad header error : make sure from, to and subject are included")
    

    return HttpResponse("email has been sent")



def signup_verification(subject, message, email):
    send_email(subject=subject, message=message, to = email, from_email="arman.saghari81@gmail.com")
