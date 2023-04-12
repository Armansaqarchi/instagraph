from random import randint
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse


def digit_random6(self) -> str:
    '''Generate a random 6 digit string'''

    return ''.join(str(randint(0,9)) for _ in range (6))


def send_email(subject = None, message = None, from_email = None, to = None):
    try:
        if to is None:
            raise BadHeaderError
        send_mail()
    except BadHeaderError :
        return HttpResponse("Bad header error : make sure from, to and subject are included")
