from .celery import app

@app.task()
def func():
    print("hello there")
    return