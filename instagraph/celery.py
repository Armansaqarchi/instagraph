from celery import Celery
from celery.schedules import crontab
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "instagraph.settings")
app = Celery("instagraph")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_url = "redis://localhost:6379"
app.conf.result_backend = "redis://localhost:6379"
app.conf.task_default_exchange = "tasks"
app.conf.task_default_exchange_type = "topic"


app.conf.task_routes = [
    ("queue1", "queue1.*"),
    ("queue2", "queue2.*"),
]

app.conf.task_routes = (
    {"instagraph.celery_test.func" : {
        "queue" : "queue1",
        }
    }
)


#settings crontab
app.conf.beat_schedule = {
    "send_mail_if_birthday" : {
        "task" : "accounts.models.account.congrats",
        "crontab" : crontab(hour = 5)
    }
}

app.autodiscover_tasks()
