# instagraph

You guessed it right. instagram like application using Django DRF



## About the project
<div align="left">
This project aims to give an intuition of how the database schemas and apis might look for designing a social media application.
though for the sake of simplicity, its based on DRF architecture which is more supported and easier to develop.
<br>
<br>
as you might know, popular social medias like instagram and facebook are now using an architecture called graphql.
the problem with this architecture is having complexity of query.
parsing the query and extracting the semantics might be time consuming,
while its wide types of queries could lead to making complex queries much easier than DRF
</div>


### Built With
<div>
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/daphne-092E20?style=for-the-badge&logo=django&logoColor=green"/>
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green"/>
  <br>
  <img src="https://img.shields.io/badge/redis-%23DD0031.svg?&style=for-the-badge&logo=redis&logoColor=white">
  <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white">
  <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white">
  <img src="https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white">
</div>


### Installation

> Manually

you will need to have the python installed, and then run the following command in the **root directory** of the project:

```md
python -m pip install -r requirements.txt
```
> Using Docker

use the docker-compose.yaml in the root project.
```shell
docker-compose up
```
You can also **customize** the docker file.
by default, the docker file is configured to create a container compatible with sqlite.
the reason behind this is that postgres and its dependencies require a hige space compared to the container space.
but if you want to make it compatible with postgres, you can add these commands before installation for psycopg:
```shell
apk add postgresql-dev gcc python3-dev musl-dev && pip3 install psycopg2
```

### Usages
> Secret key


```python
SECRET_KEY = YOUR_SECRET 
```
you may want to generate your own secret key, if using built in django classes, you might want to create a **random secret** key using the following command:
```python
from django.core.management.utils import get_random_secret_key
generate_random_secret_key()
```

> google authentication

to add features like authentication using third party services like google, you must get a cloud google account in <a href="https://console.developers.google.com">Google developers console</a>

```md
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': YOUR_CLIENT_ID,
            'secret': YOUR_GOOGLE_CLOUD_SECRET,
        }
    }
}
```

> Channels

```python
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": YOUR_BACKEND, //e.g : "channels_redis.core.RedisChannelLayer"
        "CONFIG": {
            "hosts": [(YOUR_LAYER_IP, YOUR_LAYER_PORT)],
        },
        "TEST_CONFIG": {
            "hosts": [(YOUR_LAYER_IP, YOUR_LAYER_PORT)],
        }
    },
}
```

> Databases
```python
DATABASES = {
    'default': {
        'ENGINE': YOUR_ENGINE //e.g : 'django.db.backends.postgresql',
        'USER' : YOUR_USER,
        'PASSWORD' : YOUR_PASSWORD,,
        "HOST" : YOUR_HOST,,
        "PORT" : YOUR_PORT,,
        "NAME" : YOUR_NAME,
    }
}
```

> Cache pages

default cache backend to store cache pages response
```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "example"
    }
}
DEFAULT_CACHE_TIMEOUT = 240
```


> smtp email backend

configure this fields in settings.py to set up smtp server for your email.
note that you should first create an app password for your application, see <a href="https://support.google.com/mail/answer/185833?hl=en">here</a>
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = YOUR_EMAIL
EMAIL_HOST_PASSWORD = YOUR_EMAIL_PASSWORD_APP
ACTIVATION_TIMEOUT = 1200 # defualt time out to verify email account
EMAIL_ACTIVATION = False # whether enable activation with email otp
```

> Celery

to instantiate a celery for you application, you can simply run the ./run_celery.sh file.
**note that you must run the file inside the root directory to work**:
```md
instagraph/run_celery.sh
```



