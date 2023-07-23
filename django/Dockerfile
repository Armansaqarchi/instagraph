FROM python:3.12.0b4-alpine3.18

COPY . ./django-instagraph


RUN pip install --upgrade pip


ENV PYTHONUNBUFFERED=1


RUN apk update

RUN apk update \
    && apk add gcc \
    && apk add python3-dev musl-dev \
    && apk add jpeg-dev zlib-dev libjpeg
    

RUN pip install -U setuptools

RUN pip install -r /django-instagraph/requirements.txt


EXPOSE 8000

RUN python ./django-instagraph/manage.py migrate

CMD ["python", "./django-instagraph/manage.py", "runserver", "0.0.0.0:8000"]


